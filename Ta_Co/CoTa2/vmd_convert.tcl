#!/usr/bin/vmd
mol new "Ta_Co/CoTa2/CoTa2.xyz" type xyz
cd "Ta_Co/CoTa2"

molinfo top set a 18.4
molinfo top set b 18.4
molinfo top set c 15.0
molinfo top set alpha 90.0
molinfo top set beta 90.0
molinfo top set gamma 90.0

topo writelammpsdata "CoTa2.data" full
quit
