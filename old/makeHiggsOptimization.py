from ROOT import *
from math import sqrt
from sys import argv

# John Hakala, March 10 2016

def optimize(sigMass, sideband, whichCut, lowerLimit, upperLimit, outputFilename, category):
    compareCosAndPtOverM = True

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
    if compareCosAndPtOverM and whichCut == "cos theta":
        comparison = TGraph()

    if sigMass=="750":
        massWindowLo = 700
        massWindowHi = 800

    elif sigMass=="1000":
        massWindowLo = 950
        massWindowHi = 1050

    elif sigMass=="2000":
        massWindowLo = 1900
        massWindowHi = 2100

    elif sigMass=="3000":
        massWindowLo = 2200
        massWindowHi = 3800

    else:
        exit("pick the signal mass")

    phoEtaMaxEB   = 1.4442
    phoEtaMaxEE   = 2.2
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
    #cosThetadataCut     = TCut("cosThetaStar<0.5+0.25*(phJetInvMass_pruned_higgs-750)/250"                                       )
    #cosThetasidebandCut = TCut("cosThetaStar<0.5+0.25*(phJetInvMass_pruned_sideLow%s-750)/250"  % sidebandIndex                  )
    cosThetadataCut     = TCut("cosThetaStar<-0.627*TMath::ATan((-0.005938*phJetInvMass_pruned_higgs)+3.427)"                      )
    cosThetasidebandCut = TCut("cosThetaStar<-0.627*TMath::ATan((-0.005938*phJetInvMass_pruned_sideLow%s)+3.427)"%sidebandIndex    )

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
        if compareCosAndPtOverM and whichCut == "cos theta":
            print "the cut value for cosThetaStar is %f" % cutValue
            comparisonCutValue = float(i)/float(180)
            print "the cut value for pT/Mgj is %f" % comparisonCutValue
        masscutSideband = TCut()
        masscutData = TCut()
        if compareCosAndPtOverM and whichCut == "cos theta":
            comparisoncutSideband = TCut()
            comparisoncutData = TCut()
        for cut in sidebandCuts:
            masscutSideband += cut
            if compareCosAndPtOverM and whichCut == "cos theta":
                comparisoncutSideband += cut
        #masscutSideband += sidebandMassCuts + deltaRsidebandCut + phoEtaCut + cosThetasidebandCut
        for cut in dataCuts:
            masscutData += cut
            if compareCosAndPtOverM and whichCut == "cos theta":
                comparisoncutData += cut
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
            if compareCosAndPtOverM and whichCut == "cos theta":
                comparisonSidebandCut    = TCut("phPtOverMgammaj>%s" % str(comparisonCutValue) )
                comparisonSigRegionCut   = TCut("phPtOverMgammaj>%s"             % str(comparisonCutValue  ) )
        masscutSideband+=thisSidebandCut
        masscutData+=thisSigRegionCut
        if compareCosAndPtOverM and whichCut == "cos theta":
            comparisoncutSideband+=comparisonSidebandCut
            comparisoncutData+=comparisonSigRegionCut
            #print "the comparison cuts are:"
            #comparisoncutSideband.Print()
            #comparisoncutData.Print()
        #print "the cut string for the signal region is %s" % thisSigRegionCut
        #print "the cut string for the sideband region is %s" % thisSidebandCut
        c = TCanvas()
        #t = TGraph()
        data.Draw("higgsJet_pruned_abseta", masscutData)
        for primitive in c.GetListOfPrimitives():
            primitive.SetName("data")
            primitive.SetLineColor(kBlack)
        if compareCosAndPtOverM and whichCut == "cos theta" and cutValue>0.2:
            dataEntries = c.GetPrimitive("data").GetEntries()
        #print "data has %i entries" % dataEntries
        sideLow.Draw("sideLow%sJet_pruned_abseta"%sidebandIndex, masscutSideband, "SAME")
        for primitive in c.GetListOfPrimitives():
            if not primitive.GetName()=="data":
                primitive.SetName("sideband")
        if compareCosAndPtOverM and whichCut == "cos theta" and cutValue>0.2:
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


        if compareCosAndPtOverM and whichCut == "cos theta" and comparisonCutValue<0.6:
            data.Draw("higgsJet_pruned_abseta", comparisoncutData, "SAME")
            #print "comparisoncutSideband is ",
            #print comparisoncutSideband
            for primitive in c.GetListOfPrimitives():
                if not primitive.GetName() in primitives:
                    primitive.SetName("data2")
            data2Entries = c.GetPrimitive("data2").GetEntries()
            #print "data2Entries is %i " % data2Entries
            sideLow.Draw("sideLow%sJet_pruned_abseta"%sidebandIndex, comparisoncutSideband, "SAME")
            for primitive in c.GetListOfPrimitives():
                if not primitive.GetName() in primitives :
                    primitive.SetName("sideband2")
            sideband2Entries = c.GetPrimitive("sideband2").GetEntries()
            #print "sideband2Entries is %i" % sideband2Entries
            #print "sideband has %i entries" % sidebandEntries
            sidebandNormalization2 = data2Entries/sideband2Entries
            #print "sideband normalization factor is %f" % sidebandNormalization
            for sidebandBin in range (0, c.GetPrimitive("sideband2").GetNbinsX()):
                c.GetPrimitive("sideband2").SetBinContent(sidebandBin, c.GetPrimitive("sideband2").GetBinContent(sidebandBin)*sidebandNormalization2)
            c.GetPrimitive("sideband2").SetLineColor(kRed)
            c.Update()
            c.Draw()
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
        for primitive in c.GetListOfPrimitives():
            #print "adding primitive with name %s" % primitive.GetName()
            primitives.append(primitive.GetName())

        if compareCosAndPtOverM and whichCut == "cos theta" and comparisonCutValue<0.9:
            sig.Draw("higgsJet_pruned_abseta", comparisoncutData, "SAME")
            for primitive in c.GetListOfPrimitives():
                #print primitive
                if not primitive.GetName() in primitives:
                    #print "found new primitive with name %s" % primitive.GetName()
                    primitive.SetName("signal2")
                    #print "found updated primitive with name %s" % primitive.GetName()
            for primitive in c.GetListOfPrimitives():
                #print "adding primitive with name %s" % primitive.GetName()
                primitives.append(primitive.GetName())
            #print "signal2 has number of entries %i" % c.GetPrimitive("signal2").GetEntries()

        if compareCosAndPtOverM and whichCut == "cos theta" and cutValue>0.1:
            ss = c.GetPrimitive("signal").GetEntries()
            #print "number of signal events is %i" % ss
            bb = c.GetPrimitive("sideband").GetEntries()
        if compareCosAndPtOverM and whichCut == "cos theta" and comparisonCutValue<0.9:
            ss2 = c.GetPrimitive("signal2").GetEntries()
            bb2 = c.GetPrimitive("sideband2").GetEntries()
        elif not whichCut == "cos theta":
            ss = c.GetPrimitive("signal").GetEntries()
            #print "number of signal events is %i" % ss
            bb = c.GetPrimitive("sideband").GetEntries()
        #print "number of background events is %i" % bb
        if compareCosAndPtOverM and whichCut == "cos theta" and cutValue>0.1:
            sOverRootB=ss/sqrt(bb)
        if compareCosAndPtOverM and whichCut == "cos theta" and comparisonCutValue<0.9:
            sOverRootB2=ss2/sqrt(bb2)
            #print "for comparisonCutValue %f, s is %f, b is %f, and s/root(b) is %f" % (comparisonCutValue, ss2, bb2, sOverRootB2)
        elif not whichCut == "cos theta":
            sOverRootB=ss/sqrt(bb)
        #print "s over root b is %f" % sOverRootB
        if compareCosAndPtOverM and whichCut == "cos theta" and cutValue>0.1:
            g.SetPoint(g.GetN(), cutValue, sOverRootB)
            g.GetXaxis().SetRangeUser(0,1.2)
        if compareCosAndPtOverM and whichCut == "cos theta" and comparisonCutValue<0.9:
            comparison.SetPoint(comparison.GetN(), comparisonCutValue, sOverRootB2)
            #print "Set a point comparisonCutValue, sqrt(b) for the comparison plot: %f, %f" % (comparisonCutValue, sOverRootB2)
        elif not whichCut == "cos theta":
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
        if compareCosAndPtOverM and whichCut == "cos theta":
            g.SetTitle("S/#sqrt{B} for #||{cos(#theta*)} and p_{T}/M_{#gammaj} cuts")
            g.GetXaxis().SetTitle("cut value")
        else:
            g.SetTitle("S/#sqrt{B} for #||{cos(#theta*)} cuts")
            g.GetXaxis().SetTitle("max #||{cos(#theta*)}")
    g.GetYaxis().SetTitle("S/#sqrt{B} (a.u.)")
    g.Draw()
    if whichCut == "cos theta":
        g.GetXaxis().SetRangeUser(0, 1.1)
    c2.Update()

    if compareCosAndPtOverM and whichCut == "cos theta":
        comparison.SetLineColor(kRed)
        comparison.Draw("SAME")
        c2.Update()

    outfile = TFile("%s.root"%outputFilename, "RECREATE")
    outfile.cd()
    g.Write()

    c2.Print("%s.pdf"%outputFilename)
    print "Done with optimization step for %s\n\n"%outputFilename
    return g
