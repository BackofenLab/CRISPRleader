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

# $Id: Stream.pm,v 1.9 2005/12/12 20:42:48 brown Exp $

###########################################################################
package NPB::Parse::Stream;

use vars qw(@ISA);
use NPB::Parse::Message;
use NPB::Parse::Record;
use NPB::Parse::Substring;
use strict;

@ISA = qw(NPB::Parse::Message);

#assumes a stream doesn't mix formats
sub new {
    my $type = shift;
    my ($file, $format) = @_;
    my $self = {};
    bless $self, $type;

    $self->{'file'}   = $file;
    $self->{'format'} = $format;
    $self->{'text'}   = new NPB::Parse::Substring($file);
    $self->{'offset'} = 0;  #where to start parsing

    ($file = "NPB::Parse::Format::$format") =~ s/::/\//g;
    require "$file.pm";

    $self;
}

sub get_file   { $_[0]->{'file'} }
sub get_format { $_[0]->{'format'} }
sub get_length { $_[0]->{'text'}->get_length }

sub get_entry {
    my $self = shift;
    #warn "Stream::get_entry: offset= $self->{'offset'}\n";

    $self->{'text'}->reset($self->{'offset'});  #start parsing here

    no strict 'refs';

    my $pv = &{"NPB::Parse::Format::$self->{'format'}::get_entry"}($self);
    return undef  unless $pv;

    $self->{'offset'} += $pv->{'bytes'};  #parsed this many bytes

    $pv;
}

sub print {
    my $self = shift;
    $self->examine(qw(file format));
} 

sub close { $_[0]->{'text'}->close }

sub DESTROY { $_[0]->close }


###########################################################################
1;
