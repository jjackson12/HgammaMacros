from ROOT import *
from math import sqrt

dataFile = TFile("optimizationTreeSmall3data.root")
sigFile = TFile("optimizationTreeM750.root")

sig          = sigFile.Get("sig"     )
data          = dataFile.Get("sig"     )
sideLowOne   = dataFile.Get("side5060")
sideLowTwo   = dataFile.Get("side6070")
sideLowThree = dataFile.Get("side5070")
g = TGraph()
for i in range(1, 240):
    masscutSideband = TCut("(phJetInvMass_pruned_sideLowTwo>700)&&(phJetInvMass_pruned_sideLowTwo<800)&&(phJetDeltaR_sideLowTwo>0.8)&&(leadingPhAbsEta<1.4442)&&(cosThetaStar<0.7)")
    masscutData = TCut("(phJetInvMass_pruned_sig>700)&&(phJetInvMass_pruned_sig<800)&&(phJetDeltaR_sig>0.8)&&(leadingPhAbsEta<1.4442)&&(cosThetaStar<0.7)")
    cutValue = float(i)/float(100)
    thisSidebandCut = TCut("sideLowTwoJet_pruned_abseta<%s"%str(cutValue))
    thisSigRegionCut = TCut("matchedJet_pruned_abseta<%s"%str(cutValue))
    print "the cut value is %f" % cutValue
    print "the cut string for the signal region is %s" % thisSigRegionCut
    print "the cut string for the sideband region is %s" % thisSidebandCut
    masscutSideband+=thisSidebandCut
    masscutData+=thisSigRegionCut
    c = TCanvas()
    t = TGraph()
    data.Draw("matchedJet_pruned_abseta", masscutData)
    for primitive in c.GetListOfPrimitives():
        primitive.SetName("data")
        primitive.SetLineColor(kBlack)
    dataEntries = c.GetPrimitive("data").GetEntries()
    print "data has %i entries" % dataEntries
    sideLowTwo.Draw("sideLowTwoJet_pruned_abseta", masscutSideband, "SAME")
    for primitive in c.GetListOfPrimitives():
        if not primitive.GetName()=="data":
            primitive.SetName("sideband")
    sidebandEntries = c.GetPrimitive("sideband").GetEntries()
    print "sideband has %i entries" % sidebandEntries
    sidebandNormalization = dataEntries/sidebandEntries
    print "sideband normalization factor is %f" % sidebandNormalization
    for sidebandBin in range (0, c.GetPrimitive("sideband").GetNbinsX()):
        c.GetPrimitive("sideband").SetBinContent(sidebandBin, c.GetPrimitive("sideband").GetBinContent(sidebandBin)*sidebandNormalization)
    c.GetPrimitive("sideband").SetLineColor(kGreen)
    c.Update()
    c.Draw()
    primitives = []
    for primitive in c.GetListOfPrimitives():
        print "adding primitive with name %s" % primitive.GetName()
        primitives.append(primitive.GetName())
    print primitives
    sig.Draw("matchedJet_pruned_abseta", masscutData, "SAME")
    for primitive in c.GetListOfPrimitives():
        print primitive
        if not primitive.GetName() in primitives:
            print "found new primitive with name %s" % primitive.GetName()
            primitive.SetName("signal")
            print "found updated primitive with name %s" % primitive.GetName()

    ss = c.GetPrimitive("signal").GetEntries()
    print "number of signal events is %i" % ss
    bb = c.GetPrimitive("sideband").GetEntries()
    print "number of background events is %i" % bb
    sOverRootB=ss/sqrt(bb)
    print "s over root b is %f" % sOverRootB
    g.SetPoint(g.GetN(), cutValue, sOverRootB)
    c.Clear()
c2 = TCanvas()
c2.cd()
g.SetTitle("S/#sqrt{B} for jet #||{#eta} cuts")
g.GetXaxis().SetTitle("max #||{#eta_j}")
g.GetYaxis().SetTitle("S/#sqrt{B}")
g.Draw()

c2.Print("jetEtaOptimization_60-70sideband.pdf")

#matchedJett2t1_sig             = sig.Get("matchedJett2t1")
#cosThetaStar_sig               = sig.Get("cosThetaStar")
#leadingPhEta_sig               = sig.Get("leadingPhEta")
#leadingPhAbsEta_sig            = sig.Get("leadingPhAbsEta")
#phJetInvMass_pruned_sig        = sig.Get("phJetInvMass_pruned_sig")
#phJetDeltaR_sig                = sig.Get("phJetDeltaR_sig")
#matchedJet_pruned_abseta_sig   = sig.Get("matchedJet_pruned_abseta")
#
#matchedJett2t1_data             = data.Get("matchedJett2t1")
#cosThetaStar_data               = data.Get("cosThetaStar")
#leadingPhEta_data               = data.Get("leadingPhEta")
#leadingPhAbsEta_data            = data.Get("leadingPhAbsEta")
#phJetInvMass_pruned_data        = data.Get("phJetInvMass_pruned_sig")
#phJetDeltaR_data                = data.Get("phJetDeltaR_sig")
#matchedJet_pruned_abseta_data   = data.Get("matchedJet_pruned_abseta")
#
#sideLowOneJett2t1               = sideLowOne.Get("sideLowOneJett2t1")
#cosThetaStar_sideLowOne         = sideLowOne.Get("cosThetaStar")
#leadingPhEta_sideLowOne         = sideLowOne.Get("leadingPhEta")
#phJetInvMass_pruned_sideLowOne  = sideLowOne.Get("phJetInvMass_pruned_sideLowOne")
#phJetDeltaR_sideLowOne          = sideLowOne.Get("phJetDeltaR_sideLowOne")
#leadingPhAbsEta_sideLowOne      = sideLowOne.Get("leadingPhAbsEta")
#sideLowOneJet_pruned_abseta     = sideLowOne.Get("sideLowOneJet_pruned_abseta")
#
#
#sideLowTwoJett2t1               = sideLowTwo.Get("sideLowTwoJett2t1")
#cosThetaStar_sideLowTwo         = sideLowTwo.Get("cosThetaStar")
#leadingPhEta_sideLowTwo         = sideLowTwo.Get("leadingPhEta")
#phJetInvMass_pruned_sideLowTwo  = sideLowTwo.Get("phJetInvMass_pruned_sideLowTwo")
#phJetDeltaR_sideLowTwo          = sideLowTwo.Get("phJetDeltaR_sideLowTwo")
#leadingPhAbsEta_sideLowTwo      = sideLowTwo.Get("leadingPhAbsEta")
#sideLowTwoJet_pruned_abseta     = sideLowTwo.Get("sideLowTwoJet_pruned_abseta")
#
#
#sideLowThreeJett2t1               = sideLowThree.Get("sideLowThreeJett2t1")
#cosThetaStar_sideLowThree         = sideLowThree.Get("cosThetaStar")
#leadingPhEta_sideLowThree         = sideLowThree.Get("leadingPhEta")
#phJetInvMass_pruned_sideLowThree  = sideLowThree.Get("phJetInvMass_pruned_sideLowThree")
#phJetDeltaR_sideLowThree          = sideLowThree.Get("phJetDeltaR_sideLowThree")
#leadingPhAbsEta_sideLowThree      = sideLowThree.Get("leadingPhAbsEta")
#sideLowThreeJet_pruned_abseta     = sideLowThree.Get("sideLowThreeJet_pruned_abseta")
