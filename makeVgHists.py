from os import makedirs, path
from shutil import rmtree
from glob import glob
from ROOT import *
from HgCuts import getAntiBtagComboCut, getBtagComboCut
from HgParameters import getSigNevents

debug = True

def makeHist(inFileName, category, sampleType, sigNevents, windowEdges=[0.,0.]):
  gROOT.SetBatch()
  inFile = TFile(inFileName)
  tree = inFile.Get("higgs")
  hist = TH1D("distribs_X", "distribs_X", 4000, 700, 4700)

  region = "higgs"

  if sampleType == "signals":
    sideband = False
    useTrigger = False
    scaleFactors = True
    normalization = 1/float(sigNevents)
    if category == "antibtag":
      cut = "%f*(antibtagSF*(%s))" % (normalization, getAntiBtagComboCut(region, useTrigger, sideband, scaleFactors, windowEdges))
    elif category == "btag":
      cut = "%f*(btagSF*(%s))" % (normalization, getBtagComboCut(region, useTrigger, sideband, scaleFactors, windowEdges))

  elif sampleType == "data":
    sideband   = True
    useTrigger = True
    scaleFactors = False
    if category == "antibtag":
      cut = "weightFactor*(%s)" % getAntiBtagComboCut(region, useTrigger, sideband, scaleFactors, windowEdges)
    elif category == "btag":
      cut = "weightFactor*(%s)" % getBtagComboCut(region, useTrigger, sideband, scaleFactors, windowEdges)
  else:
    print "invalid sample type!"
    exit(1)
  

  if debug:
    print "working on file %s" % inFile.GetName()
    print "sample", inFileName, "category", category
    print "weights/cuts:", cut
  tree.Draw("phJetInvMass_puppi_softdrop_higgs>> distribs_X", cut)

  outputDir = "vgHists/%s"%category
  if not path.exists(outputDir):
    makedirs(outputDir)

  outFileName = inFileName.replace("organize_DDs/%s/ddTree"%sampleType, "%s/histos" % outputDir)
  if sampleType == "data" and windowEdges is not [0.,0.]:
    outFileName = outFileName.replace("data2016SinglePhoton.root", "sideband%i%i.root"%(int(windowEdges[0]), int(windowEdges[1])))
    
  outFile = TFile(outFileName, "CREATE")
  outFile.cd()
  hist.Write()
  outFile.Close()

if __name__=="__main__":
  from sys import argv
  if len(argv) > 0 and argv[1] == "vgMC":
    inDirs = ["stackplots_puppiSoftdrop_antibtag_SF_vgMC","stackplots_puppiSoftdrop_btag_SF_vgMC"]
    inFiles = {}
    for inDir in inDirs:
      fileNames = glob("%s/*.root" % inDir)
      for fileName in fileNames:
        if "stack_phJetInvMass_puppi_softdrop_higgs" in fileName:
          kind = "antibtag" if "antibtag" in fileName else "btag"
          inFiles[kind] = TFile(fileName)
    inHists = {}
    for cat in inFiles.keys():
      for key in inFiles[cat].GetListOfKeys():
        if "TCanvas" in inFiles[cat].Get(key.GetName()).IsA().GetName():
          for primitive in inFiles[cat].Get(key.GetName()).GetListOfPrimitives():
            if "TPad" in primitive.IsA().GetName():
              for subprim in primitive.GetListOfPrimitives():
                if "THStack" in subprim.IsA().GetName():
                  inHists[cat] = subprim.GetStack().Last()
    for cat in inHists.keys():
      outputDir = path.join("vgHists", cat)
      outFileName = path.join(outputDir, "histos_mcBG.root")
      outFile = TFile(outFileName, "RECREATE")
      inHists[cat].SetName("distribs_X")
      inHists[cat].Write()
      outFile.Close()
    
      
    
  else:
    if path.exists("vgHists"):
      rmtree ("vgHists")
    inSigFileNames = glob("organize_DDs/signals/*.root")
    sigNevents = getSigNevents()
    print "sigNevents:", sigNevents
    for inSigFileName in inSigFileNames:
      if "650" in inSigFileName:
        continue;
      mass = inSigFileName.split("sig_m")[-1].split(".root")[0]
      makeHist(inSigFileName, "btag", "signals", sigNevents[mass])
      makeHist(inSigFileName, "antibtag", "signals", sigNevents[mass])
    inDataName = "organize_DDs/data/ddTree_data2016SinglePhoton.root"
    for windowEdges in [[100., 110.], [50., 70.]]:
      makeHist(inDataName, "antibtag", "data", -999, windowEdges)
      makeHist(inDataName, "btag", "data", -999, windowEdges)
