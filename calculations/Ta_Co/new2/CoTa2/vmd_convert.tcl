#!/usr/bin/vmd
mol new "calculations/Ta_Co/new2/CoTa2/CoTa2.xyz" type xyz
cd "calculations/Ta_Co/new2/CoTa2"

molinfo top set a 24.5
molinfo top set b 24.5
molinfo top set c 19.9
molinfo top set alpha 90.0
molinfo top set beta 90.0
molinfo top set gamma 90.0

topo writelammpsdata "CoTa2.data" full
quit
