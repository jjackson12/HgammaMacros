from ROOT import *
from sys import argv
import makeDDhiggs as dd

canvases1=[]
canvases2=[]
sidebands = ["50to70","100to110"]
for sideband in sidebands:
    print sideband
    argsList =  [
                  ["leadingPhPt"               , "leadingPhPt"                     ]  ,
                  ["leadingPhAbsEta"           , "leadingPhAbsEta"                 ]  ,
                  ["cosThetaStar"              , "cosThetaStar"                    ]  ,
                  ["phPtOverMgammaj"           , "phPtOverMgammaj"                 ]
                ]
    if sideband=="50to70":
        argsList.append(["phJetDeltaR_higgs"           , "phJetDeltaR_sideLowThree"          ]  )
        argsList.append(["phJetInvMass_pruned_higgs"   , "phJetInvMass_pruned_sideLowThree"  ]  )
        argsList.append(["higgsJet_pruned_abseta"      , "sideLowThreeJet_pruned_abseta"     ]  )
        argsList.append(["higgsJett2t1"                , "sideLowThreeJett2t1"               ]  )
        argsList.append(["higgsJet_pruned_abseta"      , "sideLowThreeJet_pruned_abseta"     ]  )
    elif sideband=="100to110":
        argsList.append(["phJetDeltaR_higgs"           , "phJetDeltaR_sideLowFour"           ]  )
        argsList.append(["phJetInvMass_pruned_higgs"   , "phJetInvMass_pruned_sideLowFour"   ]  )
        argsList.append(["higgsJet_pruned_abseta"      , "sideLowFourJet_pruned_abseta"      ]  )
        argsList.append(["higgsJett2t1"                , "sideLowFourJett2t1"                ]  )
        argsList.append(["higgsJet_pruned_abseta"      , "sideLowFourJet_pruned_abseta"      ]  )
    else:
        exit("please pick sideband, 50to70 or 100to110 here")

    for args in argsList:
        if sideband=="50to70":
            dd.makeDDhiggs(args[0], args[1], sideband, argv[1], argv[2])
        if sideband=="100to110":
            dd.makeDDhiggs(args[0], args[1], sideband, argv[1], argv[2])

