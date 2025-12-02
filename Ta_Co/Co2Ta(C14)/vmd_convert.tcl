#!/usr/bin/vmd
mol new "Ta_Co/Co2Ta(C14)/Co2Ta(C14).xyz" type xyz
cd "Ta_Co/Co2Ta(C14)"

molinfo top set a 14.6
molinfo top set b 14.6
molinfo top set c 23.6
molinfo top set alpha 90.0
molinfo top set beta 90.0
molinfo top set gamma 90.0

topo writelammpsdata "Co2Ta(C14).data" full
quit
