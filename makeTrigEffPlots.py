from ROOT import *
import array
from HgCuts import getNoBtagComboCut


useEtaCut = True
gROOT.SetBatch()

if useEtaCut:
  suffix = "_etaCut"
else:
  suffix = "_noEtaCut"
fileNames = [
              "organize_DDs/data_frags/singleMuonFrags/ddTree_singleMuon2016B.root", 
              "organize_DDs/data_frags/singleMuonFrags/ddTree_singleMuon2016C.root", 
              "organize_DDs/data_frags/singleMuonFrags/ddTree_singleMuon2016D.root", 
              "organize_DDs/data_frags/singleMuonFrags/ddTree_singleMuon2016E.root", 
              "organize_DDs/data_frags/singleMuonFrags/ddTree_singleMuon2016F.root", 
              "organize_DDs/data_frags/singleMuonFrags/ddTree_singleMuon2016G.root", 
              "organize_DDs/data_frags/singleMuonFrags/ddTree_singleMuon2016Hv2.root", 
              "organize_DDs/data_frags/singleMuonFrags/ddTree_singleMuon2016Hv3.root",
              "organize_DDs/data_frags/singleMuonFrags/ddTree_singleMuon2016all.root",
              "organize_DDs/data_frags/singleMuonFrags/ddTree_singleMuon2016allButB.root"
            ] 

for fileName in fileNames:
  era = fileName.replace("organize_DDs/data_frags/singleMuonFrags/ddTree_singleMuon", "").replace(".root", "")
  print "era is:", era
  tfile = TFile(fileName)
  print tfile.GetName(), tfile
  ttree = tfile.Get("higgs")
  
  binEdges = []
  for i in range(0, 15):
    binEdges.append(20*i)
  for i in range(0, 10 ):
    binEdges.append(50*i + 300)
  for i in range(0, 4):
    binEdges.append(100*i + 800)
  print binEdges
  print "len(binEdges) =", len(binEdges)
  nBins = len(binEdges)-1
  print "nBins:", nBins
  print array.array('d', sorted(binEdges))
  
  ptHistNoTrig  = TH1D("ptNoTrig" , "p_{T}^{#gamma} efficiency", nBins, array.array('d', binEdges))
  ptHist165Trig = TH1D("pt165Trig", "p_{T}^{#gamma} efficiency", nBins, array.array('d', binEdges))
  ptHist175Trig = TH1D("pt175Trig", "p_{T}^{#gamma} efficiency", nBins, array.array('d', binEdges))
  ptHistOrTrig  = TH1D("ptOrTrig" , "p_{T}^{#gamma} efficiency", nBins, array.array('d', binEdges))
  
  cutEta = TCut("leadingPhAbsEta<1.4442")
  cutNoTrig = TCut()
  cut165 = TCut("triggerFired_165HE10>0.5")
  cut175 = TCut("triggerFired_175>0.5")
  cutOr  = TCut("triggerFired_175>0.5||triggerFired_165HE10>0.5")
  if useEtaCut:
    cutNoTrig+=cutEta
    cut165+=cutEta
    cut175+=cutEta
    cutOr+=cutEta
  ttree.Draw("leadingPhPt >> ptNoTrig", cutNoTrig) 
  ttree.Draw("leadingPhPt >> pt165Trig", cut165) 
  ttree.Draw("leadingPhPt >> pt175Trig", cut175) 
  ttree.Draw("leadingPhPt >> ptOrTrig",  cutOr) 
  
  trigEffVsPt175 = TGraphAsymmErrors(100)
  trigEffVsPt175.SetNameTitle("trigEff_175_%s" % era, "HLT_Photon175")
  trigEffVsPt165 = TGraphAsymmErrors(100)
  trigEffVsPt165.SetNameTitle("trigEff_165_%s" % era, "HLT_Photon165_HE10" )
  trigEffVsPtOr  = TGraphAsymmErrors(100)
  trigEffVsPtOr.SetNameTitle("trigEff_Or_%s" % era, "HLT_Photon175 OR HLT_Photon165_HE10")
  
  trigEffVsPt175.Divide(ptHist165Trig, ptHistNoTrig)
  trigEffVsPt165.Divide(ptHist175Trig, ptHistNoTrig)
  trigEffVsPtOr.Divide(ptHistOrTrig , ptHistNoTrig)
  trigEffGraphs=[trigEffVsPt175, trigEffVsPt165, trigEffVsPtOr]
  for trigEffGraph in trigEffGraphs:
    canPt = TCanvas()
  
  tcans=[]
  for i in range(0,3):
    print "trigEffGraphs[%i].GetName() is" % i, trigEffGraphs[i].GetName()
    tcans.append(TCanvas(trigEffGraphs[i].GetName(), trigEffGraphs[i].GetTitle()))
    tcans[-1].cd()
    trigEffGraphs[i].Draw()
    trigEffGraphs[i].GetYaxis().SetTitle("#varepsilon")
    trigEffGraphs[i].GetXaxis().SetTitle("p_{T}^{#gamma} (GeV)")
  ptCanvas = TCanvas()
  ptCanvas.cd()
  trigEffGraphs[0].Draw()
  trigEffGraphs[0].SetFillColor(kWhite)
  trigEffGraphs[0].SetLineColor(kRed)
  trigEffGraphs[0].Draw()
  trigEffGraphs[1].SetLineColor(kBlue)
  trigEffGraphs[1].SetFillColor(kWhite)
  trigEffGraphs[1].Draw("SAME")
  trigEffGraphs[2].SetLineColor(kBlack)
  trigEffGraphs[2].SetFillColor(kWhite)
  trigEffGraphs[2].Draw("SAME")
  ptCanvas.BuildLegend(0.55, 0.2, 0.85, 0.4)
  for primitive in ptCanvas.GetListOfPrimitives():
    if "TLegend" in primitive.IsA().GetName():
      print "tlegend getY1 is:", primitive.GetY1()
      print "tlegend getY2 is:", primitive.GetY2()
  trigEffVsPt175.SetTitle("Trigger efficiency: %s" % era.replace("all", ": all").replace("ButB"," but B"))
  ptCanvas.Print("trigEffVsPt_%s%s.pdf" % (era, suffix))
  ptFile = TFile("triggerEffVsPt_%s%s.root" % (era, suffix), "RECREATE")
  ptCanvas.Write()
  ptFile.Close()
  
  noTrigCuts = getNoBtagComboCut("higgs", True)
  hlt165Cuts = getNoBtagComboCut("higgs", True)
  hlt165Cuts += TCut("triggerFired_165HE10>0.5")
  hlt175Cuts = getNoBtagComboCut("higgs", True)
  hlt175Cuts += TCut("triggerFired_175>0.5")
  hltOrCuts = getNoBtagComboCut("higgs", True)
  hltOrCuts += TCut("triggerFired_175>0.5 || triggerFired_165HE10>0.5")
  
  xBinEdges = []
  for i in range(0, 5):
    xBinEdges.append(60*i+550)
  for i in range(0, 3 ):
    xBinEdges.append(150*i + 850)
  for i in range(0, 4):
    xBinEdges.append(200*i + 1300)
  print xBinEdges
  print "len(xBinEdges) =", len(xBinEdges)
  xBins = len(xBinEdges)-1
  print "xBins:", xBins
  print array.array('d', sorted(xBinEdges))
  
  invMassHistNoTrig  =  TH1D("invMassNoTrig"  , "m_{#gammaj} efficiency", xBins, array.array('d', xBinEdges))
  invMassHist165Trig =  TH1D("invMass165Trig" , "m_{#gammaj} efficiency", xBins, array.array('d', xBinEdges))
  invMassHist175Trig =  TH1D("invMass175Trig" , "m_{#gammaj} efficiency", xBins, array.array('d', xBinEdges))
  invMassHistOrTrig  =  TH1D("invMassOrTrig"  , "m_{#gammaj} efficiency", xBins, array.array('d', xBinEdges))
  
  ttree.Draw("phJetInvMass_puppi_softdrop_higgs >> invMassNoTrig", noTrigCuts) 
  ttree.Draw("phJetInvMass_puppi_softdrop_higgs >> invMass165Trig", hlt165Cuts)
  ttree.Draw("phJetInvMass_puppi_softdrop_higgs >> invMass175Trig", hlt175Cuts)
  ttree.Draw("phJetInvMass_puppi_softdrop_higgs >> invMassOrTrig",  hltOrCuts)
  
  trigEffVsInvMass175 = TGraphAsymmErrors(100)
  trigEffVsInvMass175.SetNameTitle("ttrigEff_175_%s" % era, "HLT_Photon175, %s" % era)
  trigEffVsInvMass165 = TGraphAsymmErrors(100)
  trigEffVsInvMass165.SetNameTitle("ttrigEff_165_%s" % era, "HLT_Photon165_HE10, %s" % era )
  trigEffVsInvMassOr  = TGraphAsymmErrors(100)
  trigEffVsInvMassOr.SetNameTitle("ttrigEff_Or_%s" % era,   "HLT_Photon175 OR HLT_Photon165_HE10, %s" % era)
  
  
  trigEffVsInvMass175.Divide(invMassHist165Trig, invMassHistNoTrig)
  trigEffVsInvMass165.Divide(invMassHist175Trig, invMassHistNoTrig)
  trigEffVsInvMassOr.Divide(invMassHistOrTrig , invMassHistNoTrig)
  ttrigEffGraphs=[trigEffVsInvMass175, trigEffVsInvMass165, trigEffVsInvMassOr]
  
  ttcans=[]
  for i in range(0,3):
    #HACK HACK
    print "trigEffGraphs[%i].GetName() is" % i, ttrigEffGraphs[i].GetName()
    ttcans.append(TCanvas(ttrigEffGraphs[i].GetName(), ttrigEffGraphs[i].GetTitle()))
    ttcans[-1].cd()
    ttrigEffGraphs[i].Draw()
    ttrigEffGraphs[i].GetYaxis().SetTitle("#varepsilon")
    ttrigEffGraphs[i].GetXaxis().SetTitle("m_{#gammaj} (GeV)")
    #END HACK
  allCanvas = TCanvas()
  allCanvas.cd()
  ttrigEffGraphs[0].Draw()
  ttrigEffGraphs[0].SetFillColor(kWhite)
  ttrigEffGraphs[0].SetLineColor(kRed)
  ttrigEffGraphs[0].Draw()
  ttrigEffGraphs[1].SetLineColor(kBlue)
  ttrigEffGraphs[1].SetFillColor(kWhite)
  ttrigEffGraphs[1].Draw("SAME")
  ttrigEffGraphs[2].SetLineColor(kBlack)
  ttrigEffGraphs[2].SetFillColor(kWhite)
  ttrigEffGraphs[2].Draw("SAME")
  allCanvas.BuildLegend()
  trigEffVsInvMass175.SetTitle("Trigger efficiency: %s" % era)
  allCanvas.Print("trigEffVsInvMass_%s.pdf" % era)



  outFile = TFile("triggerEffVsInvMass_%s.root" % era, "RECREATE")
  allCanvas.Write()
  outFile.Close()
