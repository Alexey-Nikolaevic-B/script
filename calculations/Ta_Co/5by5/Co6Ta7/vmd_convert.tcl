#!/usr/bin/vmd
mol new "calculations/Ta_Co/5by5/Co6Ta7/Co6Ta7.xyz" type xyz
cd "calculations/Ta_Co/5by5/Co6Ta7"

molinfo top set a 19.8
molinfo top set b 19.8
molinfo top set c 105.8
molinfo top set alpha 90.0
molinfo top set beta 90.0
molinfo top set gamma 90.0

topo writelammpsdata "Co6Ta7.data" full
quit
