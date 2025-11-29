#!/usr/bin/vmd
mol new "./Ta_Co/vesta/CoTa2.xyz" type xyz

cd "./Ta_Co/vmd"

topo retypebonds
topo guessangles  
topo guessdihedrals

topo writelammpsdata "CoTa2.data" full

quit