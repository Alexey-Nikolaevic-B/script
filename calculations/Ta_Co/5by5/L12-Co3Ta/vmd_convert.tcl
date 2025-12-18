#!/usr/bin/vmd
mol new "calculations/Ta_Co/5by5/L12-Co3Ta/L12-Co3Ta.xyz" type xyz
cd "calculations/Ta_Co/5by5/L12-Co3Ta"

molinfo top set a 14.6
molinfo top set b 14.6
molinfo top set c 14.6
molinfo top set alpha 90.0
molinfo top set beta 90.0
molinfo top set gamma 90.0

topo writelammpsdata "L12-Co3Ta.data" full
quit
