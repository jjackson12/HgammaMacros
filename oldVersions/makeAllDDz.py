from ROOT import *
from sys import argv
from os import path, makedirs
import makeDDz as dd

sideband="50to70"
canvases=[]
tfiles = []
argsList =  [
              ["leadingPhPt"               , "leadingPhPt"                     ]  ,
              ["leadingPhAbsEta"           , "leadingPhAbsEta"                 ]  ,
              ["cosThetaStar"              , "cosThetaStar"                    ]  ,
              ["phPtOverMgammaj"           , "phPtOverMgammaj"                 ]
            ]
if sideband=="50to70":
    argsList.append(["phJetDeltaR_sig"           , "phJetDeltaR_sideLowThree"          ]  )
    argsList.append(["phJetInvMass_pruned_sig"   , "phJetInvMass_pruned_sideLowThree"  ]  )
    argsList.append(["matchedJet_pruned_abseta"  , "sideLowThreeJet_pruned_abseta"     ]  )
    argsList.append(["matchedJett2t1"            , "sideLowThreeJett2t1"               ]  )
    argsList.append(["matchedJet_pruned_abseta"  , "sideLowThreeJet_pruned_abseta"     ]  )
elif sideband=="100to110":
    argsList.append(["phJetDeltaR_sig"           , "phJetDeltaR_sideLowFour"           ]  )
    argsList.append(["phJetInvMass_pruned_sig"   , "phJetInvMass_pruned_sideLowFour"   ]  )
    argsList.append(["matchedJet_pruned_abseta"  , "sideLowFourJet_pruned_abseta"      ]  )
    argsList.append(["matchedJett2t1"            , "sideLowFourJett2t1"                ]  )
    argsList.append(["matchedJet_pruned_abseta"  , "sideLowFourJet_pruned_abseta"      ]  )
else:
    exit("please pick sideband, 50to70 or 100to110")

for args in argsList:
    if sideband=="50to70":
        canvases.append(dd.makeDDz(args[0], args[1], sideband, argv[1], argv[2], argv[3], argv[4]))
        tfiles.append(TFile(canvases[-1], "r"))
        canvas = tfiles[-1].Get("ddPlot")
        outputDir = "zValidationPlots_%s_%s"%(argv[1], argv[2])
        if not path.exists(outputDir):
            makedirs(outputDir)
        canvas.Print("%s/%s_%s_%s-%s_%s_%s"%(outputDir, args[0], sideband, argv[1], argv[2], argv[3], argv[4]))
