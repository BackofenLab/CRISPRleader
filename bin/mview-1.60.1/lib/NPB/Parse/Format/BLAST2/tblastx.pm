# -*- perl -*-
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

# $Id: tblastx.pm,v 1.10 2015/06/14 17:09:04 npb Exp $

###########################################################################
package NPB::Parse::Format::BLAST2::tblastx;

use NPB::Parse::Format::BLAST2::blastx;
use strict;

use vars qw(@ISA);

@ISA = qw(NPB::Parse::Format::BLAST2::blastx);


###########################################################################
package NPB::Parse::Format::BLAST2::tblastx::HEADER;

use vars qw(@ISA);

@ISA = qw(NPB::Parse::Format::BLAST2::blastx::HEADER);


###########################################################################
package NPB::Parse::Format::BLAST2::tblastx::SEARCH;

use vars qw(@ISA);

@ISA = qw(NPB::Parse::Format::BLAST2::blastx::SEARCH);


###########################################################################
package NPB::Parse::Format::BLAST2::tblastx::SEARCH::RANK;

use vars qw(@ISA);

@ISA = qw(NPB::Parse::Format::BLAST2::blastx::SEARCH::RANK);


###########################################################################
package NPB::Parse::Format::BLAST2::tblastx::SEARCH::MATCH;

use vars qw(@ISA);

@ISA = qw(NPB::Parse::Format::BLAST2::blastx::SEARCH::MATCH);


###########################################################################
package NPB::Parse::Format::BLAST2::tblastx::SEARCH::MATCH::SUM;

use vars qw(@ISA);

@ISA = qw(NPB::Parse::Format::BLAST2::blastx::SEARCH::MATCH::SUM);


###########################################################################
package NPB::Parse::Format::BLAST2::tblastx::SEARCH::MATCH::ALN;

use vars qw(@ISA);

@ISA = qw(NPB::Parse::Format::BLAST2::SEARCH::MATCH::ALN);

sub new {
    my $type = shift;
    my $self = new NPB::Parse::Format::BLAST2::SEARCH::MATCH::ALN(@_);
    my $text = new NPB::Parse::Record_Stream($self);

    my $line;

    $line = $text->next_line(1);
    $line = $text->next_line(1);
    $line = $text->next_line(1);

    #warn "[$line]\n";

    #tblastx 2.0.5 has no Frame line, so set a useful default
    $self->{'query_frame'} = $self->{'query_orient'};
    $self->{'sbjct_frame'} = $self->{'sbjct_orient'};

    #query and sbjct frames
    if ($line =~ /^\s*Frame\s*=\s+(\S+)\s*\/\s*(\S+)/) {
        $self->{'query_frame'} = $1;
        $self->{'sbjct_frame'} = $2;
    }

    #record paired orientations in MATCH list
    push @{$self->get_parent(1)->{'orient'}->{
				 $self->{'query_orient'} .
                                 $self->{'sbjct_orient'}
				}}, $self;
    bless $self, $type;
}

sub print_data {
    my ($self, $indent) = (@_, 0);
    my $x = ' ' x $indent;
    $self->SUPER::print_data($indent);
    printf "$x%20s -> %s\n",  'query_frame',  $self->{'query_frame'};
    printf "$x%20s -> %s\n",  'sbjct_frame',  $self->{'sbjct_frame'};
}

###########################################################################
package NPB::Parse::Format::BLAST2::tblastx::WARNING;

use vars qw(@ISA);

@ISA = qw(NPB::Parse::Format::BLAST::WARNING);


###########################################################################
package NPB::Parse::Format::BLAST2::tblastx::PARAMETERS;

use vars qw(@ISA);

@ISA = qw(NPB::Parse::Format::BLAST::PARAMETERS);


###########################################################################
1;
