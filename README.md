flash-archive
=============

SD card with wifi + paper archival source +flash-archive = efficiently dealing with archival materials

This is useful if you do a lot of work with paper-based archival sources, and need to keep track of the images and the bibliographic information.
It calls up a graphical interface and prompts you for  bibliographic information. once entered, it creates a unique subdirectory with the biblio info (presently in BibTeX format), into which photographs taken are automatically transferred.


At present, this script is known to work:
from the linux command line (tested on ubuntu)
using	Python 3.4
using a Toshiba FlashAir SD card with WIFI in a Sony Alpha 35 camera (should work with most cameras that take full-size SD cards)

Needs to be done:
cleaning up and standardizing the code - re-writing with objects to facilitate multi-platform and multi-hardware configurations - it is pure functions at present
standardizing window tool kits
setting up good command line options
making code ready to take options for different OS, cards, etc.
have a image-name only (no transfer) option, to deal with high battery usage if transferring lots of photographs - a script to copy them over later would also be generated. (by putting the SD card into a local reader, rather than using the wifi transfer)
allow a session to be re-started, jumping straight into the transfer stage
support for other SD card/WIFI combos.  If you have one, let me know, and we can try to add that in.
Windows and OSX support. The latter should be easy enough, and for the former, I've no idea. Might be easy too. I don't use either, so your help testing would be useful.
longterm - use some sort of network library to negotiate the WIFI connection with the flashair, and if really ambitions (perhaps command line option), drop the network connection and re-connect to your regular one when the session is done. Clearly, this would be OS dependent, and perhaps more involved than that.

Issues:
if you are not connected to the 'flashair' network that the Toshiba flashair uses as its default, then the programme will crash


Collaboration: 
if you would like to help with the project in any way, email me at daniel.simeone@gmail.com, and I'll add you as a collaborator. If there are several people who do so, I'll make a mailing list.




Licence
===========

    flash-archive -- tool for using SD/WIFI combo cards to simplify
    use of paper archival sources.
    Copyright (C) 2014  Daniel Simeone

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

