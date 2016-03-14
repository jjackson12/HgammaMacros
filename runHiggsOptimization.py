from ROOT import *
from os import path, makedirs
import makeHiggsOptimization as opt

# John Hakala, March 10 2016


#masses = ["2000"]
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
            cosThetaMin = 55
        if sideband == "50to70":
            iCanvas = 1
        outputDir = "optimization_m%s_sb%s"%(mass, sideband)
        if not path.exists(outputDir):
            makedirs(outputDir)
        graphs.append( opt.optimize(mass, sideband, "jet eta", "100", "240", "%s/opt_jetEta_m%s_sb%s"%(outputDir, mass, sideband)) )
        pages[iMass].cd(iCanvas+1)
        graphs[-1].Draw()
        graphs.append(   opt.optimize(mass, sideband, "photon eta", "100", "240", "%s/opt_phoEta_m%s_sb%s"%(outputDir, mass, sideband)) )
        pages[iMass].cd(iCanvas+3)
        graphs[-1].Draw()
        graphs.append( opt.optimize(mass, sideband, "delta R", "0", "320", "%s/opt_deltaR_m%s_sb%s"%(outputDir, mass, sideband)))
        pages[iMass].cd(iCanvas+5)
        graphs[-1].Draw()
        graphs.append( opt.optimize(mass, sideband, "cos theta", str(cosThetaMin), "100", "%s/opt_cosTheta_m%s_sb%s"%(outputDir, mass, sideband)))
        pages[iMass].cd(iCanvas+7)
        graphs[-1].Draw()
        iMass+=1

for iPage in range(0, len(pages)):
    pages[iPage].cd()
    pages[iPage].Print("page%i.pdf"%iPage)
