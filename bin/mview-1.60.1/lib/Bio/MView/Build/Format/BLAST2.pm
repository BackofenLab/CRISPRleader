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

# $Id: BLAST2.pm,v 1.17 2015/06/14 17:09:04 npb Exp $

###########################################################################
#
# NCBI BLAST 2.0, PSI-BLAST 2.0, BLAST+
#
#   blastp, blastn, blastx, tblastn, tblastx
#
###########################################################################
package Bio::MView::Build::Format::BLAST2;

use Bio::MView::Build::Format::BLAST0;

use strict;
use vars qw(@ISA);

@ISA = qw(Bio::MView::Build::Format::BLAST0);

sub begin_parse {
    my $self = shift;
    my $s = $self->{'entry'}->parse("SEARCH[@{[ $self->cycle ]}]");
    return ()  unless defined $s;
    my $r = $s->parse(qw(RANK));
    return ()  unless defined $r;
    my $h  = $self->{'entry'}->parse(qw(HEADER));
    ($s, $h, $r);
}

sub end_parse { $_[0]->{'entry'}->free(qw(SEARCH)) }

#sub str { join ", ", map { defined $_ ? $_ : 'undef' } @_ }

sub parse_record {
    my ($self, $k, $hdr, $sum, $aln) = @_;
    #warn "[@{[str($k, $hdr, $sum, $aln)]}]\n";

    my ($id, $desc, $bits, $expect, $n) = ('','','','','');

    $k = ''  unless defined $k;  #row number = rank

    if (defined $hdr) {
        ($id, $desc) = ($hdr->{'query'}, $hdr->{'summary'});
    } elsif (defined $sum) {
        ($id, $desc) = ($sum->{'id'},    $sum->{'desc'});
    } elsif (defined $aln) {
        ($id, $desc) = ($aln->{'id'},    $aln->{'summary'});
    }
    if (defined $aln) {
        ($bits, $expect, $n) = ($aln->{'bits'}, $aln->{'expect'}, $aln->{'n'});
    }

    #warn "[$k, $id, $desc, $self->cycle, $bits, $expect, $n]\n";
    ($k, $id, $desc, $self->cycle, $bits, $expect, $n);
}

sub get_scores {
    my ($self, $list) = @_;
    my @tmp = $self->SUPER::get_scores($list);
    return ()  unless @tmp;

    my $bits = \$tmp[1];

    #try to preserve original precision/format as far as possible
    my $val = sprintf("%.0f", $$bits);     #bits as integer
    if ($val != $$bits) {                  #num. different? put 1dp back
        $$bits = sprintf("%.1f", $$bits);  #bit score to 1 dp
    }

    @tmp;
}

#score/significance filter
sub skip_hsp {
    my ($self, $hsp) = @_;
    return 1  if
        defined $self->{'minbits'} and $hsp->{'bits'} < $self->{'minbits'};
    return 1  if
        defined $self->{'maxeval'} and $hsp->{'expect'} > $self->{'maxeval'};
    return 0;
}

#standard attribute names
sub attr_score { 'bits' }
sub attr_sig   { 'expect' }


###########################################################################
package Bio::MView::Build::Row::BLAST2;

use vars qw(@ISA);

@ISA = qw(Bio::MView::Build::Row::BLAST);

#suppress cycle in all output; it's only for blastp/psi-blastp
sub schema {[
    # use? rdb?  key              label         format   default
    [ 0,   0,    'cycle',         'cycle',      '2N',      ''  ],
    [ 2,   2,    'bits',          'bits',       '5N',      ''  ],
    [ 3,   3,    'expect',        'E-value',    '9S',      ''  ],
    [ 4,   4,    'n',             'N',          '2N',      ''  ],
    [ 5,   5,    'query_orient',  'qy',         '2S',      '?' ],
    [ 6,   6,    'sbjct_orient',  'ht',         '2S',      '?' ],
    ]
}


###########################################################################
package Bio::MView::Build::Row::BLAST2::blastp;

use vars qw(@ISA);

@ISA = qw(Bio::MView::Build::Row::BLAST2);

#enable cycle in rdb tabulated output
#suppress query and sbjct orientations for blastp data
sub schema {[
    # use? rdb?  key              label         format   default
    [ 0,   1,    'cycle',         'cycle',      '2N',      ''  ],
    [ 2,   2,    'bits',          'bits',       '5N',      ''  ],
    [ 3,   3,    'expect',        'E-value',    '9S',      ''  ],
    [ 4,   4,    'n',             'N',          '2N',      ''  ],
    [ 0,   0,    'query_orient',  'qy',         '2S',      '?' ],
    [ 0,   0,    'sbjct_orient',  'ht',         '2S',      '?' ],
    ]
}


###########################################################################
package Bio::MView::Build::Row::BLAST2::blastn;

use vars qw(@ISA);

@ISA = qw(Bio::MView::Build::Row::BLAST2);


###########################################################################
package Bio::MView::Build::Row::BLAST2::blastx;

use vars qw(@ISA);

@ISA = qw(Bio::MView::Build::Row::BLASTX);

sub schema { Bio::MView::Build::Row::BLAST2::schema }


###########################################################################
package Bio::MView::Build::Row::BLAST2::tblastn;

use vars qw(@ISA);

@ISA = qw(Bio::MView::Build::Row::BLAST2);


###########################################################################
package Bio::MView::Build::Row::BLAST2::tblastx;

use vars qw(@ISA);

@ISA = qw(Bio::MView::Build::Row::BLASTX);

sub schema { Bio::MView::Build::Row::BLAST2::schema }


###########################################################################
###########################################################################
package Bio::MView::Build::Format::BLAST2::blastp;

use vars qw(@ISA);

@ISA = qw(Bio::MView::Build::Format::BLAST2
          Bio::MView::Build::Format::BLAST0::blastp
);

sub scheduler { 'cycle' }

sub record_type { 'Bio::MView::Build::Row::BLAST2::blastp' }

sub subheader {
    my ($self, $quiet) = (@_, 0);
    my $s = '';
    return $s  if $quiet;
    $s  = $self->SUPER::subheader($quiet);
    $s .= "Search cycle: " . $self->cycle . "\n";
    $s;
}


###########################################################################
package Bio::MView::Build::Format::BLAST2::blastn;

use vars qw(@ISA);

@ISA = qw(Bio::MView::Build::Format::BLAST2
          Bio::MView::Build::Format::BLAST0::blastn
);

sub scheduler { 'strand' }

sub record_type { 'Bio::MView::Build::Row::BLAST2::blastn' }

sub subheader {
    my ($self, $quiet) = (@_, 0);
    my $s = '';
    return $s  if $quiet;
    $s  = $self->SUPER::subheader($quiet);
    $s .= "Query orientation: " . $self->strand . "\n";
    $s;
}


###########################################################################
package Bio::MView::Build::Format::BLAST2::blastx;

use vars qw(@ISA);

@ISA = qw(Bio::MView::Build::Format::BLAST2
          Bio::MView::Build::Format::BLAST0::blastx
);

sub scheduler { 'strand' }

sub record_type { 'Bio::MView::Build::Row::BLAST2::blastx' }

sub subheader {
    my ($self, $quiet) = (@_, 0);
    my $s = '';
    return $s    if $quiet;
    $s  = $self->SUPER::subheader($quiet);
    $s .= "Query orientation: " . $self->strand . "\n";
    $s;
}


###########################################################################
package Bio::MView::Build::Format::BLAST2::tblastn;

use vars qw(@ISA);

@ISA = qw(Bio::MView::Build::Format::BLAST2
          Bio::MView::Build::Format::BLAST0::tblastn
);

sub scheduler { 'none' }

sub record_type { 'Bio::MView::Build::Row::BLAST2::tblastn' }


###########################################################################
package Bio::MView::Build::Format::BLAST2::tblastx;

use vars qw(@ISA);

@ISA = qw(Bio::MView::Build::Format::BLAST2
          Bio::MView::Build::Format::BLAST0::tblastx
);

sub scheduler { 'strand' }

sub record_type { 'Bio::MView::Build::Row::BLAST2::tblastx' }

sub subheader {
    my ($self, $quiet) = (@_, 0);
    my $s = '';
    return $s  if $quiet;
    $s  = $self->SUPER::subheader($quiet);
    $s .= "Query orientation: " . $self->strand . "\n";
    $s;
}


###########################################################################
1;
