from ROOT import *
from os import path, makedirs
import makeHiggsOptimization as opt
from sys import argv

# John Hakala, March 10 2016


#masses = ["2000"]
category = argv[1]
masses = ["750", "1000", "2000", "3000"]
sidebands = ["100to110", "50to70"]

pages=[]
for iPage in range(0, 4):
    pages.append(TCanvas("optimization for M=%s"%masses[iPage], "optimization for M=%s"%masses[iPage], 2480*2, 3508*2))
    pages[iPage].cd()
    pages[iPage].Divide(2, 4)
    pages[iPage].ls()

graphs=[]
iMass = 0
for sideband in sidebands:
    iMass=0
    for mass in masses:
        iCanvas = 0
        if mass == "750" or mass == "1000":
            cosThetaMin = 30
        else:
            if category == "EB":
                cosThetaMin = 55
            elif category == "EE":
                if mass == "2000":
                    cosThetaMin = 70
                elif mass == "3000":
                    cosThetaMin=95
            else:
                exit("Forgot to pick EE or EB category")
        if mass == "750" or mass == "1000":
            jetEtaMin = 100
        elif mass == "2000":
            if category == "EB":
                jetEtaMin = 100
            elif category == "EE":
                jetEtaMin = 125
            else:
                exit("Forgot to pick EE or EB category")
        if sideband == "50to70":
            iCanvas = 1
        outputDir = "optimization_%s_m%s_sb%s"%(category, mass, sideband)
        if not path.exists(outputDir):
            makedirs(outputDir)
        graphs.append( opt.optimize(mass, sideband, "jet eta", str(jetEtaMin), "240", "%s/opt_jetEta_m%s_sb%s"%(outputDir, mass, sideband), category) )
        pages[iMass].cd(iCanvas+1)
        graphs[-1].Draw()
        graphs.append(   opt.optimize(mass, sideband, "photon eta", "100", "250", "%s/opt_phoEta_m%s_sb%s"%(outputDir, mass, sideband), category) )
        pages[iMass].cd(iCanvas+3)
        graphs[-1].Draw()
        graphs.append( opt.optimize(mass, sideband, "delta R", "0", "320", "%s/opt_deltaR_m%s_sb%s"%(outputDir, mass, sideband), category))
        pages[iMass].cd(iCanvas+5)
        graphs[-1].Draw()
        graphs.append( opt.optimize(mass, sideband, "cos theta", str(cosThetaMin), "100", "%s/opt_cosTheta_m%s_sb%s"%(outputDir, mass, sideband), category))
        pages[iMass].cd(iCanvas+7)
        graphs[-1].Draw()
        iMass+=1

for iPage in range(0, len(pages)):
    pages[iPage].cd()
    pages[iPage].Print("%soptimization_page%i.pdf"%(category, iPage))
