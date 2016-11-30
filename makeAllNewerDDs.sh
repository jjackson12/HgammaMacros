#!/bin/bash

#python runHbbGammaSelector.py ~/hbbgamma80X/small3s/HgammaSlimmedData_Oct5.root newerDDs/ddTree_Hgamma_data27fb-1.root compile

#backgroundsAndData=( DYJetsToQQ_HT180 GJets_HT-100To200 GJets_HT-200To400 GJets_HT-400To600 GJets_HT-600ToInf QCD_HT100to200 QCD_HT200to300 QCD_HT300to500 QCD_HT500to700 QCD_HT700to1000 QCD_HT1000to1500 QCD_HT1500to2000 QCD_HT2000toInf RunC  WJetsToQQ_HT-600ToInf )
backgrounds=( 2016DYJetsToQQ180 2016GJets100-200 2016GJets200-400 2016GJets400-600 2016GJets600-Inf 2016QCD1000-1500 2016QCD1500-2000 2016QCD200-300 2016QCD2000-Inf 2016QCD300-500 2016QCD500-700 2016QCD700-1000 2016WJetsToQQ180 )
data=( 2016B-0 2016B-1 2016C 2016D 2016E 2016F 2016G-0 2016G-1 2016Hv2-0 2016Hv2-1 2016Hv3 )
#
#for file in "${backgroundsAndData[@]}"
#do
#  python runHbbGammaSelector.py ~/physics/nTuplizerStep/small3s/small3_${file}.root newerDDs/ddTree_${file}.root load
#done
#
for file in "${data[@]}"; do python runHbbGammaSelector.py ~/physics/nov21_ntuples/fragments/dataFrags/${file}.root 80XDDs_Nov21/dataFrags/ddTree_${file}.root load & done
#
for file in "${backgrounds[@]}"; do python runHbbGammaSelector.py ~/physics/nov21_ntuples/${file}.root 80XDDs_Nov21/ddTree_${file}.root load & done
#
##initialMass=650
##python runHbbGammaSelector.py ~/WZgammaMacros/HgSig_flatTuples_July19/flatTuple_Hgamma_m${initialMass}.root newerDDs/ddTree_Hgamma_m${initialMass}.root compile

#masses=( 650 750 1000 1250 1500 1750 2000 2500 3000 3500 4000 )
#masses=( 750 1000 1250 1500 1750 2000 2500 3000 3500 4000 )

#masses=(650 750 850 1000 1150 1300 1450 1600 1750 1900 2050 2450 2850 3250)
#for mass in "${masses[@]}"
#do
#  python runHbbGammaSelector.py ~/hbbgamma80X/small3s/flatTuple_m${mass}.root 80XDDs/ddTree_Hgamma_m${mass}.root load
#done
