# This macro makes the trigger turn-on plot
# it takes one argument: the input filename
# Example: python makeTriggerTurnOnPlot.py myFlatTuple.root
# John Hakala 1/15/2016

from sys import argv
from os import path, makedirs
import copy
from ROOT import *
from HgParameters import getSamplesDirs
from pyrootTools import drawInNewCanvas
from array import array

#if not len(argv)>1 :
# print "Please supply one argument to this macro: the name of the input root file."
# exit(1)
masses = [650, 750, 1000, 1250, 1500, 1750, 2000, 2500, 3000, 3500, 4000]
#masses = [650]
for mass in masses:
  samplesDirs = getSamplesDirs()
  outputDir = "output_July18"

  if not path.exists(outputDir):
    makedirs(outputDir)
  outFile=TFile("%s/trigTurnOn_m%r.root"%(outputDir, mass), "RECREATE")

  #noTrigFile = TFile("%s/ddTree_Hgamma_noTrigger_m%i.root"%(samplesDirs["ddDir"], mass),"r")
  #print noTrigFile
  trigFile = TFile("%s/ddTree_Hgamma_triggerFired_m%i.root"%(samplesDirs["dataDDdir"], mass),"r")
  noTrigFile = TFile("%s/ddTree_Hgamma_triggerFired_m%i.root"%(samplesDirs["dataDDdir"], mass),"r")
  print trigFile

  #noTrigTree = noTrigFile.Get("higgs")
  #print noTrigTree
  trigTree = trigFile.Get("higgs")
  noTrigTree = noTrigFile.Get("higgs")
  print trigTree

  #inputHistNames  = [ ["leadingPhPtHist_trig", "leadingPhPtHist_noTrig"], ["leadingPhPt_noIDHist_trig","leadingPhPt_noIDHist"] ] 
  outputPlotNames = [ "triggerTurnOn_IDapplied_m%r.pdf"%mass, "triggerTurnOn_noID.pdf" ]
  xbins = []
  for i in range(9, 45):
    xbins.append(i*4)
  xbinshigh = [200, 225, 250, 300, 600]
  for bn in xbinshigh:
    xbins.append(bn)
  print "length of xbins is %r" % len(xbins)

  noTrigHist = TH1D("nt", "nt", 1000, 0, 1000)
  noTrigHist.SetName("nt")
  noTrigHist.Draw()

  can1=TCanvas()
  can1.cd()
  noTrigTree.Draw("leadingPhPt>> nt", TCut())
  newNT = noTrigHist.Rebin(len(xbins)-1, "newnt",  array('d', xbins))
  print "newNT: ",
  print newNT
  newNT.Draw()

  ## Trick to keep plot open
  #if __name__ == '__main__':
  #   rep = ''
  #   while not rep in [ 'q', 'Q' ]:
  #      rep = raw_input( 'enter "q" to quit: ' )
  #      if 1 < len(rep):
  #         rep = rep[0]

  outFile.cd()
  newNT.Write()

  trigHist = TH1D("t", "t", 1000, 0, 1000)
  trigHist.SetName("t")
  trigHist.Draw()

  can2=TCanvas()
  can2.cd()
  trigTree.Draw("leadingPhPt>> t", TCut("triggerFired>0"))
  newT = trigHist.Rebin(len(xbins)-1, "newt",  array('d', xbins))
  print "newT: ",
  print newT
  newT.Draw()

  #if __name__ == '__main__':
  #   rep = ''
  #   while not rep in [ 'q', 'Q' ]:
  #      rep = raw_input( 'enter "q" to quit: ' )
  #      if 1 < len(rep):
  #         rep = rep[0]

  outFile.cd()
  newT.Write()

  #for prim in can1.GetListOfPrimitives():
  #  print "can1 primitive: %r" % prim.GetName()
  #  print "prim.IsA().GetName(): %s" % prim.IsA().GetName()
  #for prim in can2.GetListOfPrimitives():
  #  print "can2 primitive: %r" % prim.GetName()
  #  print "prim.IsA().GetName(): %s" % prim.IsA().GetName()
  ratio=TGraphAsymmErrors()
  print "newNT has nbins %r" % newNT.GetXaxis().GetNbins()
  print "newT has nbins %r" % newT.GetXaxis().GetNbins()
  ratio.Divide(newT, newNT)
  #ratio.Divide(can2.GetPrimitive("t"), can1.GetPrimitive("nt"))
  #print "nt has nBins %r" % can1.GetPrimitive("nt").GetXaxis().GetNbins()
  #print "t has nBins %r" % can2.GetPrimitive("t").GetXaxis().GetNbins()
  canvas=TCanvas()
  canvas.cd()
  ratio.GetXaxis().SetTitle("Leading #gamma p_{T} (GeV)")
  ratio.GetYaxis().SetTitle("Efficiency")
  ratio.SetTitle("HLT_Photon_175_v1 Trigger Efficiency")
  ratio.Draw("ap")
  canvas.Print("%s/%s"%(outputDir, outputPlotNames[0]))
  outFile.Close()


