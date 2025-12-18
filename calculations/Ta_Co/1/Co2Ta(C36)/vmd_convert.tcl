#!/usr/bin/vmd
mol new "calculations/Ta_Co/1/Co2Ta(C36)/Co2Ta(C36).xyz" type xyz
cd "calculations/Ta_Co/1/Co2Ta(C36)"

molinfo top set a 19.1
molinfo top set b 19.1
molinfo top set c 62.0
molinfo top set alpha 90.0
molinfo top set beta 90.0
molinfo top set gamma 90.0

topo writelammpsdata "Co2Ta(C36).data" full
quit
