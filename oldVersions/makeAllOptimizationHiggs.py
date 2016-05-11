import subprocess
from ROOT import *
from sys import argv
argsList =  [
              ["leadingPhPt"               , "leadingPhPt"                     ]  ,
              ["leadingPhAbsEta"           , "leadingPhAbsEta"                 ]  ,
              ["cosThetaStar"              , "cosThetaStar"                    ]  ,
              ["phPtOverMgammaj"           , "phPtOverMgammaj"                 ]
            ]
if argv[1]=="50to70":
    argsList.append(["phJetDeltaR_sig"           , "phJetDeltaR_sideLowThree"          ]  )
    argsList.append(["phJetInvMass_pruned_sig"   , "phJetInvMass_pruned_sideLowThree"  ]  )
    argsList.append(["matchedJet_pruned_abseta"  , "sideLowThreeJet_pruned_abseta"     ]  )
    argsList.append(["matchedJett2t1"            , "sideLowThreeJett2t1"               ]  )
    argsList.append(["matchedJet_pruned_abseta"  , "sideLowThreeJet_pruned_abseta"     ]  )
elif argv[1]=="100to110":
    argsList.append(["phJetDeltaR_sig"           , "phJetDeltaR_sideLowFour"           ]  )
    argsList.append(["phJetInvMass_pruned_sig"   , "phJetInvMass_pruned_sideLowFour"   ]  )
    argsList.append(["matchedJet_pruned_abseta"  , "sideLowFourJet_pruned_abseta"      ]  )
    argsList.append(["matchedJett2t1"            , "sideLowFourJett2t1"                ]  )
    argsList.append(["matchedJet_pruned_abseta"  , "sideLowFourJet_pruned_abseta"      ]  )
else:
    exit("please pick sideband, 50to70 or 100to110")

for args in argsList:
    subprocess.call(["python", "makeOptimizationHiggs.py", args[0], args[1], argv[1], "-b"])
exit()
