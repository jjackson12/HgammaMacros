from ROOT import *
from math import sqrt
from sys import argv

# John Hakala, March 10 2016

def optimize(sigMass, sideband, whichCut, lowerLimit, upperLimit, outputFilename, category):
    dataFile = TFile("../HgammaSamples/ddTrees/ddNew_silver.root")
    sigFile = TFile("../HgammaSamples/ddTrees/ddNew_Hgamma_m%s.root"%sigMass)
    print "Signal mass is %s" % sigMass

    sig          = sigFile.Get("higgs"     )
    data          = dataFile.Get("higgs"     )
    if sideband == "100to110":
        sideLow   = dataFile.Get("side100110")
        sidebandIndex = "Four"
    elif sideband == "50to70":
        sideLow   = dataFile.Get("side5070")
        sidebandIndex = "Three"
    g = TGraph()

    if sigMass=="750":
        massWindowLo = 700
        massWindowHi = 800

    elif sigMass=="1000":
        massWindowLo = 900
        massWindowHi = 1100

    elif sigMass=="2000":
        massWindowLo = 1800
        massWindowHi = 2200

    elif sigMass=="3000":
        massWindowLo = 2200
        massWindowHi = 4000

    else:
        exit("pick the signal mass")

    phoEtaMaxEB   = 1.4442
    phoEtaMaxEE   = 2.5
    phoEtaMinEE   = 1.566
    jetEtaMax   = 2.2
    deltaRmin   = 1.1

    dataCuts     = []
    sidebandCuts = []
    if category=="EB":
        phoEtaCut       = TCut("leadingPhAbsEta<%s"               % str(phoEtaMaxEB  ) )
    if category=="EE":
        phoEtaCut       = TCut("%s<leadingPhAbsEta&&leadingPhAbsEta<%s"               % ( str(phoEtaMinEE),str(phoEtaMaxEE) ) )
    if category=="EBEE":
        phoEtaCut       = TCut("leadingPhAbsEta<%s"               %  str(phoEtaMaxEE) )
    deltaRdataCut       = TCut("phJetDeltaR_higgs>%s"             % str(deltaRmin  ) )
    deltaRsidebandCut   = TCut("phJetDeltaR_sideLow%s>%s"         % ( sidebandIndex, str(deltaRmin)) )
    jetEtaDataCut       = TCut("higgsJet_pruned_abseta<%s"        % str(jetEtaMax  ) )
    jetEtaSidebandCut   = TCut("sideLow%sJet_pruned_abseta<%s"% (sidebandIndex, str(jetEtaMax)) )
    cosThetadataCut     = TCut("cosThetaStar<0.5+0.25*(phJetInvMass_pruned_higgs-750)/250"                                          )
    cosThetasidebandCut = TCut("cosThetaStar<0.5+0.25*(phJetInvMass_pruned_sideLow%s-750)/250"  % sidebandIndex                   )

    dataMassCuts         = TCut("(phJetInvMass_pruned_higgs>%s)&&(phJetInvMass_pruned_higgs<%s)"               % ( str(massWindowLo), str(massWindowHi) )    )
    sidebandMassCuts     = TCut("(phJetInvMass_pruned_sideLow%s>%s)&&(phJetInvMass_pruned_sideLow%s<%s)" % ( sidebandIndex, str(massWindowLo), sidebandIndex, str(massWindowHi) )    )

    if not whichCut == "photon eta":
        dataCuts.append(      phoEtaCut   )
        sidebandCuts.append(  phoEtaCut   )

    if not whichCut == "delta R":
        dataCuts.append(      deltaRdataCut   )
        sidebandCuts.append(  deltaRsidebandCut   )

    if not whichCut == "jet eta":
        dataCuts.append(      jetEtaDataCut   )
        sidebandCuts.append(  jetEtaSidebandCut   )

    if not whichCut == "cos theta":
        dataCuts.append(      cosThetadataCut   )
        sidebandCuts.append(  cosThetasidebandCut   )

    dataCuts.append(      dataMassCuts   )
    sidebandCuts.append(  sidebandMassCuts   )

    for i in range(int(lowerLimit),int(upperLimit)):
        cutValue = float(i)/float(100)
        masscutSideband = TCut()
        masscutData = TCut()
        for cut in sidebandCuts:
            masscutSideband += cut
        #masscutSideband += sidebandMassCuts + deltaRsidebandCut + phoEtaCut + cosThetasidebandCut
        for cut in dataCuts:
            masscutData += cut
        #masscutData += dataMassCuts + deltaRdataCut + phoEtaCut + cosThetadataCut
        if whichCut == "jet eta":
            thisSidebandCut = TCut("sideLow%sJet_pruned_abseta<%s"%(sidebandIndex, str(cutValue)))
            thisSigRegionCut = TCut("higgsJet_pruned_abseta<%s"%str(cutValue))
        if whichCut == "photon eta":
            thisSidebandCut = TCut("leadingPhAbsEta<%s"%str(cutValue))
            thisSigRegionCut = TCut("leadingPhAbsEta<%s"%str(cutValue))
        if whichCut == "delta R":
            thisSidebandCut    = TCut("phJetDeltaR_sideLow%s>%s"         % ( sidebandIndex, str(cutValue)) )
            thisSigRegionCut   = TCut("phJetDeltaR_higgs>%s"             % str(cutValue  ) )
        if whichCut == "cos theta":
            thisSidebandCut    = TCut("cosThetaStar<%s" % str(cutValue) )
            thisSigRegionCut   = TCut("cosThetaStar<%s"             % str(cutValue  ) )
        #print "the cut value on %s is %f" % (whichCut, cutValue)
        masscutSideband+=thisSidebandCut
        masscutData+=thisSigRegionCut
        #print "the cut string for the signal region is %s" % thisSigRegionCut
        #print "the cut string for the sideband region is %s" % thisSidebandCut
        c = TCanvas()
        t = TGraph()
        data.Draw("higgsJet_pruned_abseta", masscutData)
        for primitive in c.GetListOfPrimitives():
            primitive.SetName("data")
            primitive.SetLineColor(kBlack)
        dataEntries = c.GetPrimitive("data").GetEntries()
        #print "data has %i entries" % dataEntries
        sideLow.Draw("sideLow%sJet_pruned_abseta"%sidebandIndex, masscutSideband, "SAME")
        for primitive in c.GetListOfPrimitives():
            if not primitive.GetName()=="data":
                primitive.SetName("sideband")
        sidebandEntries = c.GetPrimitive("sideband").GetEntries()
        #print "sideband has %i entries" % sidebandEntries
        sidebandNormalization = dataEntries/sidebandEntries
        #print "sideband normalization factor is %f" % sidebandNormalization
        for sidebandBin in range (0, c.GetPrimitive("sideband").GetNbinsX()):
            c.GetPrimitive("sideband").SetBinContent(sidebandBin, c.GetPrimitive("sideband").GetBinContent(sidebandBin)*sidebandNormalization)
        c.GetPrimitive("sideband").SetLineColor(kGreen)
        c.Update()
        c.Draw()
        primitives = []
        for primitive in c.GetListOfPrimitives():
            #print "adding primitive with name %s" % primitive.GetName()
            primitives.append(primitive.GetName())
        #print primitives
        sig.Draw("higgsJet_pruned_abseta", masscutData, "SAME")
        for primitive in c.GetListOfPrimitives():
            #print primitive
            if not primitive.GetName() in primitives:
                #print "found new primitive with name %s" % primitive.GetName()
                primitive.SetName("signal")
                #print "found updated primitive with name %s" % primitive.GetName()

        ss = c.GetPrimitive("signal").GetEntries()
        #print "number of signal events is %i" % ss
        bb = c.GetPrimitive("sideband").GetEntries()
        #print "number of background events is %i" % bb
        sOverRootB=ss/sqrt(bb)
        #print "s over root b is %f" % sOverRootB
        g.SetPoint(g.GetN(), cutValue, sOverRootB)
        c.Clear()
    c2 = TCanvas()
    c2.cd()
    if whichCut == "jet eta":
        g.SetTitle("S/#sqrt{B} for jet #||{#eta} cuts")
        g.GetXaxis().SetTitle("max #||{#eta_{j}}")
    if whichCut == "photon eta":
        g.SetTitle("S/#sqrt{B} for photon #||{#eta} cuts")
        g.GetXaxis().SetTitle("max #||{#eta_{#gamma}}")
    if whichCut == "delta R":
        g.SetTitle("S/#sqrt{B} for #DeltaR(j, #gamma) cuts")
        g.GetXaxis().SetTitle("min #DeltaR")
    if whichCut == "cos theta":
        g.SetTitle("S/#sqrt{B} for #||{cos(#theta*)} cuts")
        g.GetXaxis().SetTitle("max #||{cos(#theta*)}")
    g.GetYaxis().SetTitle("S/#sqrt{B} (a.u.)")
    g.Draw()

    outfile = TFile("%s.root"%outputFilename, "RECREATE")
    outfile.cd()
    g.Write()

    c2.Print("%s.pdf"%outputFilename)
    print "Done with optimization step for %s\n\n"%outputFilename
    return g
