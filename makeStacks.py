from os import path, makedirs
from ROOT import *
from pyrootTools import getSortedDictKeys, drawInNewCanvas
from testpy import getRangesDict, getHiggsRangesDict, getSidebandRangesDict, makeAllHists
from HgParameters import getSamplesDirs, getVariableDict
from getMCbgWeights import getWeightsDict, getMCbgWeightsDict, getMCbgColors, getMCbgOrderedList, getMCbgLabels
from tcanvasTDR import TDRify
from copy import deepcopy

# new script to make all stackplots.
# John Hakala 7/14/16

#for withBtag in [True, False]:
for withBtag in [False]:
  printNonempties = False
  printFileNames  = False
  showSigs        = False
  blindData       = False

  sampleDirs = getSamplesDirs()

  rangesDict = getRangesDict()
  print ""
  print "getRangesDict:"
  print rangesDict

  higgsRangesDict = getHiggsRangesDict()
  print ""
  print "getHiggsRangesDict:"
  print higgsRangesDict

  #for sideband in ['100110','5070']:
  #  SidebandRangesDict = getSidebandRangesDict(sideband)
  #  print ""
  #  print "getSidebandRangesDict('%s')" % sideband
  #  print SidebandRangesDict


  print ""
  print ""
  print "getMCbgWeights(): "
  mcBgWeights = getMCbgWeightsDict(sampleDirs["small3sDir"])
  print mcBgWeights
  treekey="higgs"
  #for cutName in ["antibtag"]:
  #for cutName in ["btag"]:
  #for cutName in [ "nobtag"]:
  #for cutName in [ "nMinus1"]:
  #for cutName in [ "btag", "antibtag", "nobtag", "preselection", "nMinus1"]:
  for cutName in [ "antibtag"]:
    if cutName in [ "nMinus1" ]:
      if withBtag:
        histsDir = "~/WZgammaMacros/weightedMCbgHists_%s_withBtag/"%cutName 
      if not withBtag:
        histsDir = "~/WZgammaMacros/weightedMCbgHists_%s_noBtag/"%cutName 
      nonEmptyFilesDict = makeAllHists(cutName, withBtag)
    else:
      histsDir = "~/WZgammaMacros/weightedMCbgHists_%s/"%cutName
      nonEmptyFilesDict = makeAllHists(cutName)
    print "done making all histograms."
    thstacks=[]
    thstackCopies=[]
    cans=[]
    pads=[]
    hists=[]
    tfiles=[]
    datahists=[]
    datahistsCopies=[]
    datafiles=[]
    sighists=[]
    sigfiles=[]
    legendLabels = getMCbgLabels()
    varDict = getVariableDict()

    #for varkey in [higgsRangesDict.keys()[0]]:
    for varkey in higgsRangesDict.keys():
      cans.append(TCanvas())
      pads.append(TPad("stack_%s_%s"%(cutName, varkey), "stack_%s_%s"%(cutName, varkey), 0, 0.3, 1, 1.0))
      cans[-1].cd()
      pads[-1].Draw()
      pads[-1].cd()

      #### Build the stackplot
      thstacks.append(THStack("thstack_%s_%s"%(cutName, varkey),""))
      thstackCopies.append(THStack("thstackCopy_%s_%s"%(cutName, varkey),""))
      integralsDict={}
      namesDict={}
      for filekey in mcBgWeights.keys():
        filename = varkey+"_"+treekey+"_"+filekey
        if printNonempties:
          print "The nonempty files dict is:"
          print nonEmptyFilesDict
        if cutName in "nMinus1":
          if withBtag:
            thisFileName = "weightedMCbgHists_%s_withBtag/%s" % (cutName, filename)
          else:
            thisFileName = "weightedMCbgHists_%s_noBtag/%s" % (cutName, filename)
        else:
          thisFileName = "weightedMCbgHists_%s/%s" % (cutName, filename)
        if nonEmptyFilesDict[thisFileName] == "nonempty":
          if printFileNames:
            print thisFileName
          tfiles.append(TFile(histsDir + filename))
          hists.append(tfiles[-1].Get("hist_%s" % filename))
          hists[-1].SetFillColor(getMCbgColors()[filekey])
          drawInNewCanvas(hists[-1])
          integralsDict[hists[-1].Integral()] = hists[-1] 
          namesDict[hists[-1].GetName()] = hists[-1]
      for mcBG in getMCbgOrderedList():
        for key in namesDict:
          if mcBG in key:
            #print "adding %s to stackplot; it has integral %f" % (integralsDict[key], key)
            thstacks[-1].Add(namesDict[key])
            thstackCopies[-1].Add(namesDict[key])

      #### Get the signal histograms
      

      if cutName in "nMinus1":
        if withBtag:
          outDirName = "stackplots_%s_withBtag" % cutName
        else:
          outDirName = "stackplots_%s_noBtag" % cutName
      else:
        outDirName = "stackplots_%s" % cutName
      if not path.exists(outDirName):
        makedirs(outDirName)
      outfileName = "%s/%s_stack_%s.root"%(outDirName, cutName, varkey)
      outfile=TFile(outfileName, "RECREATE")
      cans[-1].cd()
      pads[-1].Draw()
      pads[-1].cd()
      thstacks[-1].Draw()
      thstacks[-1].SetMinimum(0.08)
      thstacks[-1].SetMaximum(thstacks[-1].GetMaximum()*45)
      if varkey in varDict.keys():
        thstacks[-1].GetXaxis().SetTitle(varDict[varkey])
      thstacks[-1].GetYaxis().SetTitle("Events/%g"%thstacks[-1].GetXaxis().GetBinWidth(1))
      thstacks[-1].GetYaxis().SetLabelSize(0.04)
      thstacks[-1].GetYaxis().SetTitleSize(0.04)
      thstacks[-1].GetYaxis().SetTitleOffset(1.2)

      dataFileName = varkey+"_"+treekey+"_SilverJson.root"
      datafiles.append(TFile("weightedMCbgHists_%s/%s"%(cutName, dataFileName)))
      print datafiles[-1]
      datahists.append(datafiles[-1].Get("hist_%s"%dataFileName))
      print datahists[-1]
      if not blindData:
        datahists[-1].Draw("PE SAME")
      datahists[-1].SetMarkerStyle(20)
      datahistsCopies.append(datahists[-1].Clone())
      #for sigMass in [650, 750, 1000, 1250, 1500, 1750, 2000, 2500, 3000, 3500, 4000]:
      if showSigs:
        colors={}
        colors[750]=kCyan-6
        colors[1000]=kOrange
        colors[2000]=kMagenta
        colors[3000]=kRed
        for sigMass in [750, 1000, 2000, 3000]:
          sigFileName = varkey+"_"+treekey+"_Hgamma_m%i.root"%sigMass
          if cutName in "nMinus1":
            if withBtag:
              sigfiles.append(TFile("weightedMCbgHists_%s_withBtag/%s"%(cutName, sigFileName)))
            else:
              sigfiles.append(TFile("weightedMCbgHists_%s_noBtag/%s"%(cutName, sigFileName)))
          else:
            outDirName = "stackplots_%s" % cutName
            sigfiles.append(TFile("weightedMCbgHists_%s/%s"%(cutName, sigFileName)))
          sighists.append(sigfiles[-1].Get("hist_%s"%sigFileName))
          sighists[-1].SetLineStyle(3)
          sighists[-1].SetLineWidth(2)
          sighists[-1].SetLineColor(colors[sigMass])
          sighists[-1].SetTitle("H#gamma(%r TeV)"%(sigMass/float(1000)))
          sighists[-1].SetMarkerSize(0)
          sighists[-1].Draw("SAME")

      pads[-1].SetBottomMargin(0)
      pads[-1].SetLogy()
      pads[-1].BuildLegend()
      cans[-1].cd()
      pads[-1].Draw()

      TDRify(pads[-1])
      for prim in pads[-1].GetListOfPrimitives():
        if "TLegend" in prim.IsA().GetName():
          prim.SetX1NDC(0.753)
          prim.SetY1NDC(0.703)
          prim.SetX2NDC(0.946)
          prim.SetY2NDC(0.911)
          for subprim in prim.GetListOfPrimitives():
            for key in legendLabels:
              if key in subprim.GetLabel():
                subprim.SetLabel(legendLabels[key])
                subprim.SetOption("lf")
              elif "SilverJson" in subprim.GetLabel():
                subprim.SetLabel("data")
                subprim.SetOption("pe")

      pads.append(TPad("ratio_%s_%s"%(cutName, varkey), "ratio_%s_%s"%(cutName, varkey), 0, 0.05, 1, 0.3))
      pads[-1].SetTopMargin(0)
      pads[-1].SetBottomMargin(0.15)
      pads[-1].cd()

      fullStack = thstackCopies[-1].GetStack().Last()
      fullStack.Sumw2()
      if varkey in varDict.keys():
        fullStack.GetXaxis().SetTitle(varDict[varkey])
      fullStack.GetXaxis().SetLabelSize(0.10)
      fullStack.GetXaxis().SetTitleSize(0.13)
      fullStack.GetXaxis().SetTitleOffset(2)
      gStyle.SetOptStat(0)
      datahistsCopies[-1].Sumw2()
      datahistsCopies[-1].Divide(fullStack)
      datahistsCopies[-1].Draw("PE")
      datahistsCopies[-1].SetTitle("")
      datahistsCopies[-1].GetYaxis().SetRangeUser(0,2)
      datahistsCopies[-1].SetLineColor(kBlack)
      datahistsCopies[-1].SetStats(kFALSE)
      datahistsCopies[-1].GetXaxis().SetLabelSize(0.10)
      datahistsCopies[-1].GetXaxis().SetTitleSize(0.13)
      datahistsCopies[-1].GetXaxis().SetTitleOffset(2)

      pads[-1].cd()
      gStyle.SetOptStat(0)
      cans[-1].cd()
      if not blindData:
        pads[-1].Draw()
      #for prim in pads[-1].GetListOfPrimitives():
      #  if "Text" in prim.IsA().GetName():
      #    prim.Delete()
      #  if "Stats" in prim.IsA().GetName():
      #    prim.Delete()
      datahistsCopies[-1].GetYaxis().SetTitle("data/MC")
      datahistsCopies[-1].GetYaxis().SetTitleSize(0.13)
      datahistsCopies[-1].GetYaxis().SetTitleOffset(0.24)
      datahistsCopies[-1].GetYaxis().SetLabelSize(0.08)
      TDRify(pads[-1], True)
      outfile.cd()
      cans[-1].Write()
      outfile.Close()

