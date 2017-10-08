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

# $Id: Header.pm,v 1.1 2015/06/14 17:09:04 npb Exp $

###########################################################################
package Bio::MView::Display::Header;

use Bio::MView::Display::Any;

use strict;
use vars qw(@ISA);

@ISA = qw(Bio::MView::Display::Any);

sub new {
    my $type = shift;
    my $self = new Bio::MView::Display::Any(@_);
    bless $self, $type;
}

sub next {
    my $self = shift;
    my ($html, $bold, $col, $gap, $pad, $lap, $ruler) = @_;
    my ($string, $length, $i, $start, $pos) = ([]);
	 					  
    return 0    if $self->{'cursor'} > $self->{'length'};

    $length = $self->{'length'} - $self->{'cursor'} +1; #length remaining
    $col = $length    if $col > $length;                #consume smaller amount
    $start = $self->{'start'} + $self->{'cursor'} -1;   #current real position

    #warn "($self->{'cursor'}, $col, $length, ($self->{'start'},$self->{'stop'}))\n";

    for ($i = 0; $i < $col; $i++) {
	$pos = $start + $i;     #real data position
	push @$string, ' ';
    }

    $string= $self->strip_html_repeats($string)    if $html;

    if ($html) {
	unshift @$string, '<STRONG>'           if $bold;
	unshift @$string, $self->{'prefix'}    if $self->{'prefix'};
	push    @$string, $self->{'suffix'}    if $self->{'suffix'};
	push    @$string, '</STRONG>'          if $bold;
    }

    $self->{'cursor'} += $col;

    return [ $start, $pos, join('', @$string) ];
}


###########################################################################
1;
