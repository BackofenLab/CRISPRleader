###########################################################################
#
# Copyright (C) 1997-2015 Nigel P. Brown
# 
# (i) License
# 
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
# 
# (ii) Contacts
# 
#  Project Admin:      Nigel P. Brown
#  Email:              biomview@gmail.com
#  Project URL:        http://bio-mview.sourceforge.net
# 
# (iii) Citation
# 
#  Please acknowledge use of this Program by citing the following reference in
#  any published work including web-sites:
#  
#   Brown, N.P., Leroy C., Sander C. (1998) MView: A Web compatible database
#   search or multiple alignment viewer. Bioinformatics. 14(4):380-381.
#  
#  and provide a link to the MView project URL given above under 'Contacts'.
#
###########################################################################

# $Id: MAF.pm,v 1.2 2015/06/14 17:09:04 npb Exp $

###########################################################################
package Bio::MView::Build::Row::MAF;

use Bio::MView::Build::Row;

use strict;
use vars qw(@ISA);

@ISA = qw(Bio::MView::Build::Row);

sub schema {[
    # use? rdb?  key              label         format   default
    [ 1,   1,    'start',         'start',      '8N',       '' ],
    [ 2,   2,    'size',          'size',       '8N',       '' ],
    [ 3,   3,    'strand',        'strand',     '6S',       '' ],
    [ 4,   4,    'srcsize',       'srcsize',    '10S',      '' ],
    ]
}

sub pcid { $_[0]->SUPER::pcid_std }

sub head {
    my $self = shift;
    my $tmp = $self->{'num'};
    $self->{'num'} = '';
    my $s = $self->data;
    $self->{'num'} = $tmp;
    $s;
}


###########################################################################
package Bio::MView::Build::Format::MAF;

use Bio::MView::Build::Align;

use strict;
use vars qw(@ISA);

@ISA = qw(Bio::MView::Build::Align);

#the name of the underlying NPB::Parse::Format parser
sub parser { 'MAF' }

my %Known_Parameters =
    (
     #name        => [ format  default ]
     'block'      => [ [],     undef   ],
    );

#tell the parent
sub known_parameters { \%Known_Parameters }

#called by the constructor
sub initialise_child {
    my $self = shift;

    #MAF ordinal block number: counted 1..N whereas the actual
    #block has its own 'number' field which is reported by subheader().
    my $last = $self->{'entry'}->count(qw(BLOCK));

    #free object
    $self->{'entry'}->free(qw(BLOCK));

    $self->{scheduler} = new Bio::MView::Build::Scheduler([1..$last]);

    $self->{'parsed'} = undef;  #ref to parsed block

    $self;
}

#called on each iteration
sub reset_child {
    my $self = shift;
    #warn "reset_child [@{$self->{'block'}}]\n";
    $self->{scheduler}->filter($self->{'block'});
    $self;
}

#current block being processed
sub block { $_[0]->{scheduler}->item }

sub subheader {
    my ($self, $quiet) = (@_, 0);
    my $s = '';
    return $s  if $quiet;
    $s .= "Block: " . $self->block;
    $s .= "  score: $self->{'parsed'}->{'score'}"
	if $self->{'parsed'}->{'score'} ne '';
    $s .= "  pass: $self->{'parsed'}->{'pass'}"
	if $self->{'parsed'}->{'pass'} ne '';
    $s .= "\n";
}

sub parse {
    my $self = shift;
    my ($rank, $use, $desc, $seq, @hit) = (0);

    return  unless defined $self->{scheduler}->next;

    $self->{'parsed'} = $self->{'entry'}->parse("BLOCK[@{[$self->block]}]");

    #block doesn't exist?
    return  unless defined $self->{'parsed'};

    foreach my $row (@{$self->{'parsed'}->{'row'}}) {

	$rank++;

        last  if $self->topn_done($rank);
        next  if $self->skip_row($rank, $rank, $row->{'id'});

	#warn "KEEP: ($rank,$row->{'id'})\n";

	push @hit, new Bio::MView::Build::Row::MAF($rank,
						   $row->{'id'},
						   '',
						   $row->{'start'},
						   $row->{'size'},
						   $row->{'strand'},
						   $row->{'srcsize'});
        $hit[$#hit]->add_frag($row->{'seq'});
    }
    #map { $_->print } @hit;

    #free objects
    $self->{'entry'}->free(qw(BLOCK));

    return \@hit;
}


###########################################################################
1;
