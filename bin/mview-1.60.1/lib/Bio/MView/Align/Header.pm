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
package Bio::MView::Align::Header;

use Bio::MView::Align;
use Bio::MView::Display;
use Bio::MView::Align::Row;

use vars qw(@ISA);

@ISA = qw(Bio::MView::Align::Row);

sub new {
    my $type = shift;
    my ($length, $refobj) = @_;
    my $self = {};
    bless $self, $type;

    $self->{'type'}   = 'header';
    $self->{'length'} = $length;

    $self->reset_display($refobj);

    $self;
}

sub id     { $_[0] }
sub string { '' }
sub length { $_[0]->{'length'} }

sub reset_display {
    my ($self, $refobj) = @_;
    my ($data, $pcid) = ('', '');
    if (defined $refobj) {
	$data = $refobj->head;
	$pcid = $refobj->pcid;
    }
    $self->{'display'} =
	{
	 'type'     => $self->{type},
	 'label0'   => '',
	 'label1'   => '',
	 'label2'   => '',
	 'label3'   => $data,
	 'label4'   => $pcid,
	 'label5'   => '',
	 'label6'   => '',
	 'range'    => [],
	 'number'   => 0,
	};
    $self;
}


###########################################################################
1;
