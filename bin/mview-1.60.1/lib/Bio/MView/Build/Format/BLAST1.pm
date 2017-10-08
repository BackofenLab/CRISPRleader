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

# $Id: BLAST1.pm,v 1.22 2015/06/14 17:09:04 npb Exp $

###########################################################################
#
# NCBI BLAST 1.4, WashU BLAST 2.0
#
#   blastp, blastn, blastx, tblastn, tblastx
#
###########################################################################
package Bio::MView::Build::Format::BLAST1;

use Bio::MView::Build::Format::BLAST0;

use strict;
use vars qw(@ISA);

@ISA = qw(Bio::MView::Build::Format::BLAST0);

sub begin_parse {
    my $self = shift;
    my $s = $self->{'entry'};
    my $r = $self->{'entry'}->parse(qw(RANK));
    return ()  unless defined $r;
    my $h  = $self->{'entry'}->parse(qw(HEADER));
    ($s, $h, $r);
}

sub end_parse { $_[0]->{'entry'}->free(qw(HEADER RANK MATCH)) }

#sub str { join ", ", map { defined $_ ? $_ : 'undef' } @_ }

sub parse_record {
    my ($self, $k, $hdr, $sum, $aln) = @_;
    #warn "[@{[str($k, $hdr, $sum, $aln)]}]\n";
    my ($id, $desc, $score, $p, $n) = ('','','','','');
    $k = ''  unless defined $k;  #row number = rank

    if (defined $hdr) {
        ($id, $desc) = ($hdr->{'query'}, $hdr->{'summary'});
    } elsif (defined $sum) {
        ($id, $desc) = ($sum->{'id'},    $sum->{'desc'});
    } elsif (defined $aln) {
        ($id, $desc) = ($aln->{'id'},    $aln->{'summary'});
    }
    if (defined $aln) {
        ($score, $p, $n) = ($aln->{'score'}, $aln->{'p'}, $aln->{'n'});
    }
    #warn "[$k, $id, $desc, $score, $p, $n]\n";
    ($k, $id, $desc, $score, $p, $n);
}

sub get_scores {
    my ($self, $list) = @_;
    my @tmp = $self->SUPER::get_scores($list);
    return ()  unless @tmp;

    my $sig = \$tmp[2];

    #try to preserve original precision/format as far as possible
    if ($$sig !~ /e/i) {
        $$sig = sprintf("%.5f", $$sig);
        $$sig =~ s/\.(\d{2}\d*?)0+$/.$1/;  #drop trailing zeros after 2dp
        $$sig = "0.0"  if $$sig == 0;
        $$sig = "1.0"  if $$sig == 1;
    }

    @tmp;
}

#score/significance filter
sub skip_hsp {
    my ($self, $hsp) = @_;
    return 1  if
        defined $self->{'minscore'} and $hsp->{'score'} < $self->{'minscore'};
    return 1  if
        defined $self->{'maxpval'}  and $hsp->{'p'} > $self->{'maxpval'};
    return 0;
}

sub attr_score { 'score' }
sub attr_sig   { 'p' }


###########################################################################
package Bio::MView::Build::Row::BLAST1;

use vars qw(@ISA);

@ISA = qw(Bio::MView::Build::Row::BLAST);

sub schema {[
    # use? rdb?  key              label         format   default
    [ 1,   1,    'score',         'score',      '5N',      ''  ],
    [ 2,   2,    'p',             'P(N)',       '9S',      ''  ],
    [ 3,   3,    'n',             'N',          '2N',      ''  ],
    [ 4,   4,    'query_orient',  'qy',         '2S',      '?' ],
    [ 5,   5,    'sbjct_orient',  'ht',         '2S',      '?' ],
    ]
}


###########################################################################
package Bio::MView::Build::Row::BLAST1::blastp;

use vars qw(@ISA);

@ISA = qw(Bio::MView::Build::Row::BLAST1);

#suppress query and sbjct orientations for blastp
sub schema {[
    # use? rdb?  key              label         format   default
    [ 1,   1,    'score',         'score',      '5N',      ''  ],
    [ 2,   2,    'p',             'P(N)',       '9S',      ''  ],
    [ 3,   3,    'n',             'N',          '2N',      ''  ],
    [ 0,   0,    'query_orient',  'qy',         '2S',      '?' ],
    [ 0,   0,    'sbjct_orient',  'ht',         '2S',      '?' ],
    ]
}


###########################################################################
package Bio::MView::Build::Row::BLAST1::blastn;

use vars qw(@ISA);

@ISA = qw(Bio::MView::Build::Row::BLAST1);


###########################################################################
package Bio::MView::Build::Row::BLAST1::blastx;

use vars qw(@ISA);

@ISA = qw(Bio::MView::Build::Row::BLASTX);

sub schema { Bio::MView::Build::Row::BLAST1::schema }


###########################################################################
package Bio::MView::Build::Row::BLAST1::tblastn;

use vars qw(@ISA);

@ISA = qw(Bio::MView::Build::Row::BLAST1);


###########################################################################
package Bio::MView::Build::Row::BLAST1::tblastx;

use vars qw(@ISA);

@ISA = qw(Bio::MView::Build::Row::BLASTX);

sub schema { Bio::MView::Build::Row::BLAST1::schema }


###########################################################################
###########################################################################
package Bio::MView::Build::Format::BLAST1::blastp;

use vars qw(@ISA);

@ISA = qw(Bio::MView::Build::Format::BLAST1
          Bio::MView::Build::Format::BLAST0::blastp
);

sub scheduler { 'none' }

sub record_type { 'Bio::MView::Build::Row::BLAST1::blastp' }


###########################################################################
package Bio::MView::Build::Format::BLAST1::blastn;

use vars qw(@ISA);

@ISA = qw(Bio::MView::Build::Format::BLAST1
          Bio::MView::Build::Format::BLAST0::blastn
);

sub scheduler { 'strand' }

sub record_type { 'Bio::MView::Build::Row::BLAST1::blastn' }

sub subheader {
    my ($self, $quiet) = (@_, 0);
    my $s = '';
    return $s  if $quiet;
    $s  = $self->SUPER::subheader($quiet);
    $s .= "Query orientation: " . $self->strand . "\n";
    $s;
}


###########################################################################
package Bio::MView::Build::Format::BLAST1::blastx;

use vars qw(@ISA);

@ISA = qw(Bio::MView::Build::Format::BLAST1
          Bio::MView::Build::Format::BLAST0::blastx
);

sub scheduler { 'strand' }

sub record_type { 'Bio::MView::Build::Row::BLAST1::blastx' }

sub subheader {
    my ($self, $quiet) = (@_, 0);
    my $s = '';
    return $s  if $quiet;
    $s  = $self->SUPER::subheader($quiet);
    $s .= "Query orientation: " . $self->strand . "\n";
    $s;
}


###########################################################################
package Bio::MView::Build::Format::BLAST1::tblastn;

use vars qw(@ISA);

@ISA = qw(Bio::MView::Build::Format::BLAST1
          Bio::MView::Build::Format::BLAST0::tblastn
);

sub scheduler { 'none' }

sub record_type { 'Bio::MView::Build::Row::BLAST1::tblastn' }


###########################################################################
package Bio::MView::Build::Format::BLAST1::tblastx;

use vars qw(@ISA);

@ISA = qw(Bio::MView::Build::Format::BLAST1
          Bio::MView::Build::Format::BLAST0::tblastx
);

sub scheduler { 'strand' }

sub record_type { 'Bio::MView::Build::Row::BLAST1::tblastx' }

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
