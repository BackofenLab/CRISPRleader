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

# $Id: Conservation.pm,v 1.1 2015/06/14 17:09:04 npb Exp $

###########################################################################
package Bio::MView::Align::Conservation;

use Bio::MView::Align;
use Bio::MView::Display;
use Bio::MView::Align::Row;

use strict;
use vars qw(@ISA $Debug);

@ISA = qw(Bio::MView::Align::Sequence);

$Debug = 0;

sub new {
    my $type = shift;
    warn "${type}::new() (@_)\n"    if $Debug;
    if (@_ < 1) {
	die "${type}::new() missing arguments\n";
    }
    my ($from, $to, $string) = @_;

    my $self = { %Bio::MView::Align::Sequence::Template };

    $self->{'id'}   = "clustal";
    $self->{'type'} = 'conservation';
    $self->{'from'} = $from;
    $self->{'to'}   = $to;
   
    #encode the new "sequence"
    $self->{'string'} = new Bio::MView::Sequence;
    $self->{'string'}->set_find_pad(' ');
    $self->{'string'}->set_find_pad(' ');
    $self->{'string'}->set_pad(' ');
    $self->{'string'}->set_gap(' ');
    $self->{'string'}->insert([$string, $from, $to]);

    bless $self, $type;

    $self->reset_display;

    $self;
}


###########################################################################
1;
