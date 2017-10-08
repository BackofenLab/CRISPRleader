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

# $Id: Align.pm,v 1.12 2015/06/14 17:09:04 npb Exp $

###########################################################################
package Bio::MView::Build::Align;

use Bio::MView::Build;

use strict;
use vars qw(@ISA);

@ISA = qw(Bio::MView::Build);

sub use_row {
    my ($self, $num, $nid, $sid) = @_;
    my $pat;

    #warn "use_row($num, $nid, $sid)\n";

    #first, check explicit keeplist and reference row
    foreach $pat (@{$self->{'keeplist'}}, $self->{'ref_id'}) {

	#Align subclass only
	return 1  if $pat eq '0'     and $num == 1;
	return 1  if $pat eq 'query' and $num == 1;

	#look at row number
	return 1  if $nid eq $pat;      #major
	
	#look at identifier
	return 1  if $sid eq $pat;      #exact match
	if ($pat =~ /^\/(.*)\/$/) {     #regex match (case insensitive)
	    return 1  if $sid =~ /$1/i;
	}
    }

    #second, check skiplist and reference row
    foreach $pat (@{$self->{'skiplist'}}, $self->{'ref_id'}) {

	#Align subclass only
	return 0  if $pat eq '0'     and $num == 1;
	return 0  if $pat eq 'query' and $num == 1;

	#look at row number
	return 0  if $nid eq $pat;      #major
	
	#look at identifier
	return 0  if $sid eq $pat;      #exact match
	if ($pat =~ /^\/(.*)\/$/) {     #regex match (case insensitive)
	    return 0  if $sid =~ /$1/i;
	}
    }

    #assume implicit membership of keeplist
    return 1;    #default
}

sub map_id {
    my ($self, $ref) = @_;
    $ref = 1  if $ref eq '0' or $ref =~ /query/i;
    $self->SUPER::map_id($ref);
}


###########################################################################
1;
