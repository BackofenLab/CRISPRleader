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

# $Id: fasta.pm,v 1.21 2015/06/14 17:09:04 npb Exp $

###########################################################################
package NPB::Parse::Format::FASTA3::fasta;

use NPB::Parse::Format::FASTA3;
use strict;

use vars qw(@ISA);

@ISA = qw(NPB::Parse::Format::FASTA3);

sub new { my $self=shift; $self->SUPER::new(@_) }


###########################################################################
package NPB::Parse::Format::FASTA3::fasta::HEADER;

use vars qw(@ISA);

@ISA   = qw(NPB::Parse::Format::FASTA3::HEADER);


###########################################################################
package NPB::Parse::Format::FASTA3::fasta::RANK;

use vars qw(@ISA);

@ISA   = qw(NPB::Parse::Format::FASTA::RANK);

sub new {
    my $type = shift;
    if (@_ < 2) {
	#at least two args, ($offset, $bytes are optional).
	NPB::Message::die($type, "new() invalid arguments (@_)");
    }
    my ($parent, $text, $offset, $bytes) = (@_, -1, -1);
    my ($self, $line, $record);
    
    $self = new NPB::Parse::Record($type, $parent, $text, $offset, $bytes);
    $text = new NPB::Parse::Record_Stream($self);

    #ranked search hits
    while (defined ($line = $text->next_line)) {
	
	next    if $line =~ /$NPB::Parse::Format::FASTA3::RANK_START/o;

	#pre-fasta3.3 behaviour
	if ($line =~ /^
	    \s*
	    (\S+)                #id
	    \s+
	    (.*)                 #description (may be empty)
	    \s+
	    (?:\[[^]]+\])?       #don't know - reported by rls@ebi.ac.uk
	    \s*
	    \(\s*(\d+)\)         #aa
	    \s+
	    (?:\[(\S)\])?        #orientation
	    \s*
	    (\d+)                #initn
	    \s+
	    (\d+)                #init1
	    \s+
	    (\d+)                #opt
	    \s+
	    (\S+)                #z-score
	    \s+
	    (\S+)                #E(205044)
	    \s*
	    $/xo) {
	    
	    $self->test_args($line, $1, $3, $5,$6, $7,$8,$9); #not $2,$4
	    
	    push(@{$self->{'hit'}},
		 { 
		  'id'     => NPB::Parse::Record::clean_identifier($1),
		  'desc'   => $2,
		  'length' => $3,
		  'frame'  => NPB::Parse::Format::FASTA::parse_frame($4),
		  'orient' => NPB::Parse::Format::FASTA::parse_orient($4),
		  'initn'  => $5,
		  'init1'  => $6,
		  'opt'    => $7,
		  'zscore' => $8,
		  'bits'   => 0,
		  'expect' => $9,
		 });
	    next;
	}

	#fasta3.3 behaviour
	if ($line =~ /^
	    \s*
	    (\S+)                #id
	    \s+
	    (.*)                 #description (may be empty)
	    \s+
	    (?:\[[^]]+\])?       #don't know - reported by rls@ebi.ac.uk
	    \s*
	    \(\s*(\d+)\)         #aa
	    \s+
	    (?:\[(\S)\])?        #orientation
	    \s*
	    (\d+)                #opt
	    \s+
	    (\S+)                #bits
	    \s+
	    (\S+)                #E(205044)
	    \s*
	    $/xo) {

	    $self->test_args($line, $1, $3, $5,$6,$7); #not $2,$4
	    
	    push(@{$self->{'hit'}},
		 { 
		  'id'     => NPB::Parse::Record::clean_identifier($1),
		  'desc'   => $2,
		  'length' => $3,
		  'frame'  => NPB::Parse::Format::FASTA::parse_frame($4),
		  'orient' => NPB::Parse::Format::FASTA::parse_orient($4),
		  'initn'  => 0,
		  'init1'  => 0,
		  'opt'    => $5,
		  'zscore' => 0,
		  'bits'   => $6,
		  'expect' => $7,
		 });
	    next;
	}
     
   	#blank line or empty record: ignore
	next    if $line =~ /$NPB::Parse::Format::FASTA3::NULL/o;
	 
	#default
	$self->warn("unknown field: $line");
    }
    $self;
}


###########################################################################
package NPB::Parse::Format::FASTA3::fasta::TRAILER;

use vars qw(@ISA);

@ISA   = qw(NPB::Parse::Format::FASTA::TRAILER);


###########################################################################
package NPB::Parse::Format::FASTA3::fasta::MATCH;

use vars qw(@ISA);

@ISA = qw(NPB::Parse::Format::FASTA::MATCH);


###########################################################################
package NPB::Parse::Format::FASTA3::fasta::MATCH::SUM;

use vars qw(@ISA);
use NPB::Parse::Regexps;

@ISA   = qw(NPB::Parse::Format::FASTA::MATCH::SUM);

sub new {
    my $type = shift;
    if (@_ < 2) {
	#at least two args, ($offset, $bytes are optional).
	NPB::Message::die($type, "new() invalid arguments (@_)");
    }
    my ($parent, $text, $offset, $bytes) = (@_, -1, -1);
    my ($self, $line, $record);
    
    $self = new NPB::Parse::Record($type, $parent, $text, $offset, $bytes);
    $text = new NPB::Parse::Record_Stream($self);

    while (defined ($line = $text->next_line(1))) {

	if ($line =~ /^>+/) {
	    $record = $line;       #process this later
	    next;
	}

	#pre-fasta3.3 behaviour
	if ($line =~ /^
	    (rev-comp)?            #frame
	    \s*
	    initn\:\s*(\S+)        #initn
	    \s*
	    init1\:\s*(\S+)        #init1
	    \s*
	    opt\:\s*(\S+)          #opt
	    \s*
            Z-score\:\s*(\S+)      #z
	    \s*
	    expect\(\)\s*(\S+)     #E
	    \s*
	    $/xo) {
	    
	    $self->test_args($line,$2,$3,$4,$5,$6); #not $1

	    (
	     $self->{'frame'},
	     $self->{'orient'},
	     $self->{'initn'},
	     $self->{'init1'},
	     $self->{'opt'},
	     $self->{'zscore'},
	     $self->{'expect'},
	    ) = (
		NPB::Parse::Format::FASTA::parse_frame($1),
		NPB::Parse::Format::FASTA::parse_orient($1),
		$2, $3, $4, $5, $6,
	    );
	    next;
	}
	
	#fasta3.3 behaviour
	if ($line =~ /^
	    (rev-comp)?            #frame
	    \s*
	    initn\:\s*(\S+)        #initn
	    \s*
	    init1\:\s*(\S+)        #init1
	    \s*
	    opt\:\s*(\S+)          #opt
	    \s*
            Z-score\:\s*(\S+)      #z
	    \s*
	    bits\:\s*(\S+)         #bits
	    \s*
	    E\((?:\d+)?\):\s*(\S+) #E; fasta36 adds parenthesized integer
	    \s*
	    /xo) {

	    $self->test_args($line,$2,$3,$4,$5,$6,$7); #not $1

	    (
	     $self->{'frame'},
	     $self->{'orient'},
	     $self->{'initn'},
	     $self->{'init1'},
	     $self->{'opt'},
	     $self->{'zscore'},
	     $self->{'bits'},
	     $self->{'expect'},
	    ) = (
		NPB::Parse::Format::FASTA::parse_frame($1),
		NPB::Parse::Format::FASTA::parse_orient($1),
		$2, $3, $4, $5, $6, $7,
	    );
	    next;
	}
	
	if ($line =~ /^
	    (?:(?:banded\s+)?Smith-Waterman\s+score:\s*(\d+);)?  #sw score
	    \s*($RX_Ureal)%\s*identity               #percent identity
	    (?:\s+\(($RX_Ureal)%\s+(?:ungapped|similar)\))?  #percent similar
	    \s+in\s+(\d+)                            #overlap length
	    \s+(?:aa|nt)\s+overlap
	    (?:\s+\((\S+)\))?                        #sequence ranges
	    /xo) {
	    
	    $self->test_args($line,$2,$4);

	    (
	     $self->{'score'},
	     $self->{'id_percent'},
	     $self->{'id_percent_similar'},
	     $self->{'overlap'},
	     $self->{'ranges'},
	    ) = (defined $1?$1:0,$2,defined $3?$3:'',$4,defined $5?$5:'');
	    next;
	}

   	#blank line or empty record: ignore
	next    if $line =~ /$NPB::Parse::Format::FASTA3::NULL/o;
 	
	#should only get here for multiline descriptions
	if (defined $self->{'initn'}) {
	    $self->warn("unknown field: $line");
	    next;
	}

	#accumulate multiline descriptions (fasta... -L)
	$record .= ' ' . $line;
    }

    #now split out the description
    if ($record =~ /^
	>*
	(\S+)                       #id
	\s+
	(.*)                        #description (may be empty)
	\s+
	\(\s*(\d+)\s*(?:aa|nt)\)    #length
	/xo) {
	
	$self->test_args($record, $1, $3); #not $2

	(
	 $self->{'id'},
	 $self->{'desc'},
	 $self->{'length'},
	 ) = (NPB::Parse::Record::clean_identifier($1),
	      NPB::Parse::Record::strip_english_newlines($2),
	      $3);

    } else {
	$self->warn("unknown field: $record");
    }
    $self;
}


###########################################################################
package NPB::Parse::Format::FASTA3::fasta::MATCH::ALN;

use vars qw(@ISA);

@ISA   = qw(NPB::Parse::Format::FASTA3::MATCH::ALN);

sub query_orient { $_[0]->get_summary->{'orient'} }
sub sbjct_orient { '+' }


###########################################################################
1;
