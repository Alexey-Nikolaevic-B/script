#!/usr/bin/vmd
mol new "calculations/Ta_Co/Co2Ta(C15)/Co2Ta(C15).xyz" type xyz
cd "calculations/Ta_Co/Co2Ta(C15)"

topo retypebonds
topo guessangles  
topo guessdihedrals

molinfo top set a 27.2
molinfo top set b 27.2
molinfo top set c 27.2
molinfo top set alpha 90.0
molinfo top set beta 90.0
molinfo top set gamma 90.0

topo writelammpsdata "Co2Ta(C15).data" full
quit
