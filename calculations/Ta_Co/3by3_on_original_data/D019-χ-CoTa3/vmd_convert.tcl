#!/usr/bin/vmd
mol new "calculations/Ta_Co/3by3/D019-χ-CoTa3/D019-χ-CoTa3.xyz" type xyz
cd "calculations/Ta_Co/3by3/D019-χ-CoTa3"

molinfo top set a 16.2
molinfo top set b 16.2
molinfo top set c 16.2
molinfo top set alpha 90.0
molinfo top set beta 90.0
molinfo top set gamma 90.0

topo writelammpsdata "D019-χ-CoTa3.data" full
quit
