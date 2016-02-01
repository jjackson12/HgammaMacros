from ROOT import *
lowerFitLim=600
upperFitLim=2000
rebin=10
c2 = TCanvas("c2", "c2", 800, 800)
c2.cd()
gJetsFile = TFile("inputs/allgJets_Jan29.root")
sideBandHisto = gJetsFile.Get("Resonance/phJetInvMassHist_pruned_sideLow")
sideBandHisto.Rebin(rebin)
sigRegHisto = gJetsFile.Get("Resonance/phJetInvMassHist_pruned_sig")
sigRegHisto.Rebin(rebin)
func = TF1("func", "[0]*pow([1]-x,[2])/pow(x,[3])", lowerFitLim, upperFitLim)
for i in range(1,20):
    sideBandHisto.Fit("func","R")
c2.SetLogy()
sideBandHisto.GetXaxis().SetRangeUser(lowerFitLim,upperFitLim)
sideBandHisto.GetXaxis().SetTitle("m_{#gammaj} (GeV)")
sideBandHisto.GetYaxis().SetTitle("Events / %i GeV" % int(sideBandHisto.GetXaxis().GetBinWidth(10)))
sideBandHisto.Draw()
gStyle.SetOptFit(1111)
c2.Update()
c2.Print("fitInGjetsSideband.pdf")

c3 = TCanvas("c3","c3",800,800)
c3.cd()
dataFile = TFile("inputs/all2015data_Jan29.root")
dataSigHisto = dataFile.Get("Resonance/phJetInvMassHist_pruned_sig")
dataSigHisto.Rebin(rebin)
#dataSigHisto.GetXaxis().SetRangeUser(500,1000)
dataSigHisto.Draw("pE")
dataSigHisto.GetXaxis().SetRangeUser(200, 3000)
dataSigHisto.GetXaxis().SetTitle("m_{#gammaj} (GeV)")
dataSigHisto.GetYaxis().SetTitle("Events/5 GeV")
dataSigHisto.SetMarkerStyle(20)
dataSigHisto.SetLineColor(kBlack)
c3.SetLogy()
fitFunc = TF1("fitFunc","[0]*pow([1]-x,[2])/pow(x,[3])", 0, 7000)
fitFunc.SetParameters( func.GetParameter(0), func.GetParameter(1), func.GetParameter(2), func.GetParameter(3))
lowerNormBin = dataSigHisto.GetXaxis().FindBin(float(lowerFitLim))
upperNormBin = dataSigHisto.GetXaxis().FindBin(float(upperFitLim))
totalInNormRange = 0
for normbin in range(lowerNormBin, upperNormBin):
    totalInNormRange += dataSigHisto.GetBinContent(normbin)
print "total in norm range is %i"%totalInNormRange
fitFuncNormRangeIntegral = fitFunc.Integral(dataSigHisto.GetXaxis().GetBinLowEdge(lowerNormBin),dataSigHisto.GetXaxis().GetBinLowEdge(upperNormBin))
print "fitFunctionNormRangeIntegral is %f"%fitFuncNormRangeIntegral
normfactor = dataSigHisto.GetXaxis().GetBinWidth(lowerNormBin) * float(totalInNormRange) / fitFuncNormRangeIntegral
print "normfactor is %f" % normfactor
fitFunc.SetParameter(0, fitFunc.GetParameter(0)*normfactor)
fitFunc.Draw("SAME")
c3.Print("fitOverlaidOnData.pdf")
