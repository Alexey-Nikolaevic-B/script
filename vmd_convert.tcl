#!/usr/bin/vmd
mol new "./Ta_Co/vesta/CoTa2.xyz" type xyz

cd "./Ta_Co/vmd"

topo retypebonds
topo guessangles  
topo guessdihedrals

topo writelammpsdata "CoTa2.data" full

molinfo top set a 30.0
molinfo top set b 30.0
molinfo top set c 30.0
molinfo top set alpha 90.0
molinfo top set beta 90.0
molinfo top set gamma 90.0

quit