from ROOT import *
inFile = TFile("all2015.root")
leadingPhHist  = inFile.Get("leadingPhPtHist")
leadingJetHist = inFile.Get("leadingJetPtHist")
HThist         = inFile.Get("HThist")

canvas1 = TCanvas("canvas1", "canvas1", 800, 800)
canvas2 = TCanvas("canvas2", "canvas2", 800, 800)
canvas3 = TCanvas("canvas3", "canvas3", 800, 800)

canvas1.SetLogy()
canvas2.SetLogy()
canvas3.SetLogy()

leadingPhHist  .GetXaxis().SetTitle("Leading photon P_{T} [GeV]")
leadingJetHist .GetXaxis().SetTitle("Leading jet P_{T} [GeV]")
HThist         .GetXaxis().SetTitle("HT [GeV]")
leadingPhHist  .GetYaxis().SetTitle("Events")
leadingJetHist .GetYaxis().SetTitle("Events")
HThist         .GetYaxis().SetTitle("Events")

canvas1.cd()
leadingPhHist  .Draw()
canvas2.cd()
leadingJetHist .Draw()
canvas3.cd()
HThist         .Draw()

canvas1.Print("leadingPhPt.pdf")
canvas2.Print("leadingJetPt.pdf")
canvas3.Print("HT.pdf")
