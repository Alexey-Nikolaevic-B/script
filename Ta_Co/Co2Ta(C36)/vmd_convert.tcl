#!/usr/bin/vmd
mol new "Ta_Co/Co2Ta(C36)/Co2Ta(C36).xyz" type xyz
cd "Ta_Co/Co2Ta(C36)"

molinfo top set a 14.3
molinfo top set b 14.3
molinfo top set c 46.5
molinfo top set alpha 90.0
molinfo top set beta 90.0
molinfo top set gamma 90.0

topo writelammpsdata "Co2Ta(C36).data" full
quit
