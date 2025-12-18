#!/usr/bin/vmd
mol new "calculations/Ta_Co/5by5/Co2Ta(C14)/Co2Ta(C14).xyz" type xyz
cd "calculations/Ta_Co/5by5/Co2Ta(C14)"

molinfo top set a 19.4
molinfo top set b 19.4
molinfo top set c 31.5
molinfo top set alpha 90.0
molinfo top set beta 90.0
molinfo top set gamma 90.0

topo writelammpsdata "Co2Ta(C14).data" full
quit
