#!/bin/bash
sigs=( flatTuple_m1000 flatTuple_m1300 flatTuple_m1600 flatTuple_m1900 flatTuple_m2450 flatTuple_m3250 flatTuple_m750 flatTuple_m1150 flatTuple_m1450 flatTuple_m1750 flatTuple_m2050 flatTuple_m2850 flatTuple_m650  flatTuple_m850 )
for sig in "${sigs[@]}"; do NEWNAME=`echo $sig | sed 's/flatTuple/signal/g'`; python runHbbGammaSelector.py ~/physics/80Xsignals/${sig}.root 80XDDs_sigs/ddTree_${NEWNAME}.root load & done
