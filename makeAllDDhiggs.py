from ROOT import *
from sys import argv
from os import path, makedirs
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
    else:
        exit("please pick sideband, 50to70 or 100to110 here")

    for args in argsList:
        if sideband=="50to70":
            canvases1.append(dd.makeDDhiggs(args[0], args[1], sideband, argv[1], argv[2], argv[3], argv[4]))

        if sideband=="100to110":
            print "dd.makeDDhiggs(" + args[0] + ", " + args[1] + ", " + sideband + ", " + argv[1] + ", " + argv[2] + ")"
            canvases2.append(dd.makeDDhiggs(args[0], args[1], sideband, argv[1], argv[2], argv[3], argv[4]))

outputDir = "validationPlots_%s_%s"%(argv[1], argv[2])
if not path.exists(outputDir):
   makedirs(outputDir)

page1 = TCanvas("page1", "page1", 3508*4, 2480*4)
page1.Draw()
page1.Divide(2,2)

realCanvases1=[]
realCanvases2=[]
tfiles1 = []
tfiles2 = []
for i in range (0,2):
    tfiles1.append(TFile(canvases1[i], "r"))
    realCanvases1.append(tfiles1[-1].Get("ddPlot"))
    tfiles2.append(TFile(canvases2[i], "r"))
    realCanvases2.append(tfiles2[-1].Get("ddPlot"))

    page1.cd(2*i+1)
    realCanvases1[-1].DrawClonePad()
    page1.cd()
    page1.cd(2*i+2)
    realCanvases2[-1].DrawClonePad()
    page1.cd()
page1.Print("%s/page1_MassWindow%s_%s.pdf"%(outputDir, argv[1], argv[2]))

page2 = TCanvas("page2", "page2",  3508*4, 2480*4)
page2.Draw()
page2.Divide(2,2)
for i in range (0,2):
    tfiles1.append(TFile(canvases1[i+2], "r"))
    realCanvases1.append(tfiles1[-1].Get("ddPlot"))
    tfiles2.append(TFile(canvases2[i+2], "r"))
    realCanvases2.append(tfiles2[-1].Get("ddPlot"))

    page2.cd(2*i+1)
    realCanvases1[-1].DrawClonePad()
    page2.cd()
    page2.cd(2*i+2)
    realCanvases2[-1].DrawClonePad()
    page2.cd()
page2.Print("%s/page2_MassWindow%s_%s.pdf"%(outputDir, argv[1], argv[2]))

page3 = TCanvas("page3", "page3",  3508*4, 2480*4)
page3.Draw()
page3.Divide(2,2)
for i in range (0,2):
    tfiles1.append(TFile(canvases1[i+4], "r"))
    realCanvases1.append(tfiles1[-1].Get("ddPlot"))
    tfiles2.append(TFile(canvases2[i+4], "r"))
    realCanvases2.append(tfiles2[-1].Get("ddPlot"))

    page3.cd(2*i+1)
    realCanvases1[-1].DrawClonePad()
    page3.cd()
    page3.cd(2*i+2)
    realCanvases2[-1].DrawClonePad()
    page3.cd()
page3.Print("%s/page3_MassWindow%s_%s.pdf"%(outputDir, argv[1], argv[2]))
page4 = TCanvas("page4", "page4",  3508*4, 2480*4)
page4.Draw()
page4.Divide(2,2)
for i in range (0,2):
    tfiles1.append(TFile(canvases1[i+6], "r"))
    realCanvases1.append(tfiles1[-1].Get("ddPlot"))
    tfiles2.append(TFile(canvases2[i+6], "r"))
    realCanvases2.append(tfiles2[-1].Get("ddPlot"))

    page4.cd(2*i+1)
    realCanvases1[-1].DrawClonePad()
    page4.cd()
    page4.cd(2*i+2)
    realCanvases2[-1].DrawClonePad()
    page4.cd()
page4.Print("%s/page4_MassWindow%s_%s.pdf"%(outputDir, argv[1], argv[2]))
page5 = TCanvas("page5", "page5",  3508*4, 2480*4)
page5.Draw()
