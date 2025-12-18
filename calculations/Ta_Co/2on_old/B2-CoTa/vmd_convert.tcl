#!/usr/bin/vmd
mol new "calculations/Ta_Co/2on_old/B2-CoTa/B2-CoTa.xyz" type xyz
cd "calculations/Ta_Co/2on_old/B2-CoTa"

molinfo top set a 12.3
molinfo top set b 12.3
molinfo top set c 12.3
molinfo top set alpha 90.0
molinfo top set beta 90.0
molinfo top set gamma 90.0

topo writelammpsdata "B2-CoTa.data" full
quit
