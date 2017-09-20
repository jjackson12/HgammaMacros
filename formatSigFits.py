from os import path, makedirs
from optparse import OptionParser
from pprint import pprint
import copy

#fitParams = {    '650_antibtag' :[707.012, 14.4759, 1.3, 5, 707.012, 102.161, 0.401398],
#                 '750_antibtag' :[750.247, 24.3098, 1.28213, 1.05337, 750.247, 152.79, 0.95748],
#                 '2050_antibtag' :[2037.03, 56.1349, 0.996959, 13.8877, 2037.03, 215.071, 0.991319],
#                 '2450_antibtag' :[2435.02, 63.3563, 0.961534, 11.0749, 2435.02, 152.976, 0.989579],
#                 '2850_antibtag' :[2838.58, 61.1034, 0.70446, 18.303, 2838.58, 89.81, 0.739841],
#                 '3250_antibtag' :[3229.71, 83.488, 0.993156, 17.474, 3229.71, 308.516, 0.992014],
#                 '850_antibtag' :[848.704, 27.9359, 1.24925, 144.848, 848.704, 124.851, 0.979694],
#                 '1000_antibtag' :[999.801, 29.8081, 1.01506, 132.45, 999.801, 109.576, 0.976133],
#                 '1150_antibtag' :[1146.5, 34.5643, 0.968532, 140.407, 1146.5, 151.335, 0.982746],
#                 '1300_antibtag' :[1292.85, 39.8239, 0.981872, 32.9175, 1292.85, 159.078, 0.987803],
#                 '1450_antibtag' :[1444.26, 40.9502, 0.890855, 44.9158, 1444.26, 193.554, 0.98623],
#                 '1600_antibtag' :[1591.27, 46.4988, 0.921928, 113.92, 1591.27, 318.954, 0.990417],
#                 '1750_antibtag' :[1742.01, 47.5577, 0.926966, 15.4472, 1742.01, 347.2, 0.99272],
#                 '1900_antibtag' :[1887.1, 54.1408, 0.944332, 138.304, 1887.1, 234.969, 0.991259],
#                 '650_btag' :[712.15, 5.00003, 1.3, 148.055, 712.15, 156.714, 1],
#                 '750_btag' :[747.205, 23.5298, 0.967991, 25.151, 747.205, 150, 1],
#                 '2050_btag' :[2026.55, 57.556, 0.911508, 137.018, 2026.55, 150, 1],
#                 '2450_btag' :[2423.36, 67.4885, 0.910848, 127.446, 2423.36, 150, 1],
#                 '2850_btag' :[2820.56, 74.1179, 0.952412, 30.5146, 2820.56, 150, 1],
#                 '3250_btag' :[3220.77, 83.0422, 0.866869, 138.154, 3220.77, 150, 1],
#                 '850_btag' :[844.947, 26.288, 1.27328, 134.689, 844.947, 199.02, 1],
#                 '1000_btag' :[992.924, 32.1325, 1.10991, 143.968, 992.924, 150, 1],
#                 '1150_btag' :[1140.51, 35.0192, 1.00252, 139.973, 1140.51, 150, 1],
#                 '1300_btag' :[1284.81, 41.8153, 1.06789, 138.204, 1284.81, 150, 1],
#                 '1450_btag' :[1432.16, 44.238, 1.09711, 128.841, 1432.16, 150, 1],
#                 '1600_btag' :[1584.5, 44.3586, 0.885069, 138.453, 1584.5, 150, 1],
#                 '1750_btag' :[1726.96, 52.5625, 1.0501, 134.05, 1726.96, 150, 1],
#                 '1900_btag' :[1876.51, 55.8298, 0.9715, 132.231, 1876.51, 150, 1]}




parser = OptionParser()
parser.add_option("-c", dest="category",
                  help = "the category: either btag or antibtag")
parser.add_option("-r", dest="binWidth", type=int, default=10,
                  help = "the bin width for output plot")
parser.add_option("-g", action="store_true", dest="graphics",
                  help = "turn off batch mode")
(options, args) = parser.parse_args()
if not options.category in ["btag", "antibtag"]:
  print "you must pick either 'btag' or 'antibtag' as the -c option"
  exit(1)
from ROOT import *
print "options.graphics is:", options.graphics
if not options.graphics:
  print "setting batch mode"
  gROOT.SetBatch()

#hakala@brux6 ~/cmssw/CMSSW_7_4_7/src/HgammaDebug/HgammaMacros # pyroot /home/hakala/cmssw/CMSSW_7_4_7/src/HgammaDebug/Vg/signalFits_antibtag_fullsim/w_signal_1750.root
#Opened /home/hakala/cmssw/CMSSW_7_4_7/src/HgammaDebug/Vg/signalFits_antibtag_fullsim/w_signal_1750.root as 'tfile'
#TFile**    /home/hakala/cmssw/CMSSW_7_4_7/src/HgammaDebug/Vg/signalFits_antibtag_fullsim/w_signal_1750.root
# TFile*    /home/hakala/cmssw/CMSSW_7_4_7/src/HgammaDebug/Vg/signalFits_antibtag_fullsim/w_signal_1750.root
#  KEY: RooWorkspace  Vg;1  Vg
#  KEY: TProcessID  ProcessID0;1  dc714cb8-98b2-11e7-9717-f13fa8c0beef
#>>> vg = tfile.Get("Vg")
#>>> vg.Print()
#
#RooWorkspace(Vg) Vg contents
#
#variables
#---------
#(signal_p0_antibtag,signal_p1_antibtag,signal_p2_antibtag,signal_p3_antibtag,x)
#
#p.d.f.s
#-------
#RooCBShape::signal_fixed_antibtag[ m=x m0=signal_p0_antibtag sigma=signal_p1_antibtag alpha=signal_p2_antibtag n=signal_p3_antibtag ] = 4.47238e-74
#
#>>> vg.var("signal_p0_antibtag")
#<ROOT.RooRealVar object ("signal_p0_antibtag") at 0x4810530>
#>>> vg.var("signal_p0_antibtag").GetValV()
#Traceback (most recent call last):
#  File "<stdin>", line 1, in <module>
#AttributeError: 'RooRealVar' object has no attribute 'GetValV'
#>>> vg.var("signal_p0_antibtag").getValV()
#1738.1156693379787
def makeCrystalBall(mass, category):
  fileName = "../Vg/signalFits_{}_fullsim/w_signal_{}.root".format(category, mass)
  fitFile = TFile(fileName)
  mu    = fitFile.Get("Vg").var("signal_p0_{}".format(category)).getValV()
  sigma = fitFile.Get("Vg").var("signal_p1_{}".format(category)).getValV()
  alpha = fitFile.Get("Vg").var("signal_p2_{}".format(category)).getValV()
  n     = fitFile.Get("Vg").var("signal_p3_{}".format(category)).getValV()
  formula = 'ROOT::Math::crystalball_function(x, %f, %f, %f, %f)' % (alpha, n, sigma, mu)
  #formula = "ROOT::Math::crystalball_function(x, 2, 1, 1, 0)"
  #print formula
  return formula
#def makeGauss(mass, category):
#  key="%i_%s"%(mass, category)
#  mu    = fitParams[key][4]
#  sigma = fitParams[key][5]
#  relN  = (1-fitParams[key][6])
#  formula = "%f*ROOT::Math::gaussian_pdf(x, %f, %f)" % (relN, sigma, mu)
#  #formula = "ROOT::Math::crystalball_function(x, 2, 1, 1, 0)"
#  #print formula
#  return formula

gStyle.SetOptStat(0)
if not path.exists("outSigFits"):
  makedirs("outSigFits")
outFile = TFile("outSigFits/prettyFits_%s.root" % options.category, "RECREATE")
#def getIntegral(curve, xLow, xHi, crystalBall=TF1(), gauss=TF1()):
def getIntegral(curve, xLow, xHi, crystalBall=TF1()):
  #integral = Double(0)
  #yLow  = Double(curve.Eval(xLow))
  #yHi   = Double(curve.Eval(xHi) )
  ##print "curve at x=%f has value y=%f" % (xLow, yLow)
  ##print "curve at x=%f has value y=%f" % (xHi, yHi)
  #xLast = Double(xLow            )
  #yLast = Double(yLow            )
  #xx = Double(xLow               )
  #yy = Double(yLow               )
  #for iPoint in range(0, curve.GetN()):
  #  #curve.GetPoint(iPoint-1, xLast, yLast)
  #  curve.GetPoint(iPoint, xx, yy)
  #  if xx>=xLow and xx<=xHi :
  #    #print "python evaluates %f <= %f to %r" % (xx, xHi, xx<=xHi)
  #    #print "found a point between %f and %f: it has (x,y) value (%f, %f)"%(xLow, xHi, xx,yy)
  #    #print "will add (%f=%f) * (%f+%f)/2" % (xx, xLast, yy, yLast)
  #    integral +=  (xx-xLast) *(yy+yLast)/2
  #    #print "   == %f" % ((xx-xLast) *(yy+yLast)/2)
  #    #print " total   == %f" % integral
  #    xLast = Double(float(xx))
  #    yLast = Double(float(yy))
  ##print "  adding the last piece"
  ##print "(%f-%f) * (%f+%f)/2" % (xHi, xLast, yHi, yLast) 
  #integral +=  (xHi-xLast) *(yHi+yLast)/2 
  ##print "   == %f" % ((xHi-xLast) *(yHi+yLast)/2)
  ##print "total = %f" % integral
  #integral = crystalBall.Integral(xLow, xHi)+gauss.Integral(xLow, xHi)
  integral = crystalBall.Integral(xLow, xHi)
  return integral

from ROOT import *
fullsimMCs      = [750, 850, 1000, 1150, 1300, 1450, 1600, 1750, 1900, 2050, 2450, 2850, 3250]
#fullsimMCs      = [1000]
ksTestResults = {}
ksTestResults["category"] = options.category
stdDevs = {}
stdDevs["category"] = options.category
for fullsimMC in fullsimMCs:
  outCan = TCanvas("c_%i"% fullsimMC, "c_%i"% fullsimMC, 600, 800)
  fullsimHist     = None
  fullsimCurve     = None
  topPad       = TPad("rebinned_sigfit_%i" % fullsimMC, "Signal fit, m_{X}=%i GeV" % fullsimMC, 0, 0.3, 1, 1.0)
  bottomPad       = TPad("rebinned_sigpull_%i" % fullsimMC, "Fit Pull, m_{X}=%i GeV"  % fullsimMC, 0, 0.05, 1, 0.29)
  topPad.SetName("rebinned_%i" % fullsimMC)
  fullsimFileName = "../Vg/signalFits_%s_fullsim/c_mX_SR_%i.root" % (options.category, fullsimMC)
  fullsimFile = TFile(fullsimFileName)
  fullsimCanvas = fullsimFile.Get("c_mX_SR_%i" % fullsimMC)
  fullsimPad = fullsimCanvas.GetPrimitive("p_1")
  for primitive in fullsimPad.GetListOfPrimitives():
    #print "fullsimPad has primitive:", primitive
    if "RooHist" in primitive.IsA().GetName():
      fullsimHist = primitive
      fullsimHist.SetName("hist_%i" % fullsimMC)
    elif "RooCurve" in primitive.IsA().GetName():
      fullsimCurve = primitive
      fullsimCurve.SetName("curve_%i" % fullsimMC)
  hist = TH1F("rebinned_hist", "Signal fit, m_{X}=%i GeV" % fullsimMC, 100000, 0, 10000)
  hist.Sumw2()
  x = Double()
  xLast = Double()
  y = Double()
  sumY = 0
  for iPoint in range(0, fullsimHist.GetN()+5):
    fullsimHist.GetPoint(iPoint, x, y)
    sumY += y
    e= fullsimHist.GetErrorYhigh(iPoint)
    #if (y >= 0):
    #  print "checking point %i: (%f, %f)" % (iPoint, x, y)
    histBin = hist.GetXaxis().FindBin(x)
    #print "histBin is:", histBin
    hist.SetBinContent(histBin, y)
    hist.SetBinError(histBin, e)

  #print "fullsimHist has number of entries:", sumY
  #print "hist has number of entries:", hist.GetSumOfWeights()
  hist.Rebin(options.binWidth*10)
  #print "after rebin, hist has number of entries:", hist.GetEntries()
  hist.SetMarkerStyle(20)

  topPad.cd()
  hist.Draw("PE1")
  hist.GetYaxis().SetTitle("Events (A.U.)")
  hist.GetXaxis().SetTitle("M_{X} (GeV)")
  hist.GetYaxis().SetTitleOffset(1.2)
  hist.GetYaxis().SetRangeUser(float(0), hist.GetMaximum()*1.45)
  hist.GetXaxis().SetRangeUser(float(fullsimMC)*0.75, float(fullsimMC)*1.25)

  for iPoint in range(0, fullsimCurve.GetN()+5):
    fullsimCurve.GetPoint(iPoint, x, y)
    #fullsimCurve.SetPoint(iPoint, x, options.binWidth*y/1.5)
    fullsimCurve.SetPoint(iPoint, x, options.binWidth*y)
    #print "fullSimCurve has (x,y) values: (%f,%f)" % (x,y)
  fullsimCurve.SetLineColor(kRed)
  fullsimCurve.Draw("SAME")
  #norm = hist.GetSumOfWeights()
  norm = fullsimCurve.Integral() / float(options.binWidth)
  crystalBall =TF1("cb_%i_%s" % (fullsimMC, options.category), "%s"%(  makeCrystalBall(fullsimMC, options.category)), float(fullsimMC)*0.75, float(fullsimMC)*1.2)
  #gaussian =TF1("gauss_%i_%s" % (fullsimMC, options.category), "%f*%s"%(norm*options.binWidth, makeGauss(fullsimMC, options.category)), float(fullsimMC)*0.75, float(fullsimMC)*1.2)

  # Check the normalization:
  x = Double(0)
  y = Double(0)
  yMax = Double(0)
  xMax = Double(0)
  for point in range(5, fullsimCurve.GetN()-5):
    fullsimCurve.GetPoint(point, x, y)
    if yMax < y:
      yMax = float(y)
      xMax = float(x)
  print "(xMax, yMax)=(%f, %f)"%(xMax, yMax)
  crystalBallYmax = crystalBall.Eval(xMax)
  fracHeight = crystalBallYmax/ yMax
  #print "the fractional height of the peak is:", fracHeight
  if fracHeight < 0.995 or fracHeight > 1.005:
    crystalBall.SetParameter(0, 1/float(fracHeight))
    #gaussian.SetParameter(0, 1/float(fracHeight))
    crystalBall =TF1("cb_%i_%s" % (fullsimMC, options.category), "%f*%s"%(1/float(fracHeight), makeCrystalBall(fullsimMC, options.category)), float(fullsimMC)*0.75, float(fullsimMC)*1.2)
    #gaussian =TF1("gauss_%i_%s" % (fullsimMC, options.category), "%f*%s"%(1/float(fracHeight)*norm*options.binWidth, makeGauss(fullsimMC, options.category)), float(fullsimMC)*0.75, float(fullsimMC)*1.2)

  #crystalBall.Draw("SAME")
  #crystalBall.SetLineColor(kBlue)
  #gaussian.Draw("SAME")
  #gaussian.SetLineColor(kGreen)
  outCan.cd()
  topPad.Draw()
  outCan.Draw()
  cloneHist = hist.Clone()
  ksHist = hist.Clone() 
  pullHist = hist.Clone() 
  pullHist.SetName("ratio_%i" % fullsimMC)
  for iBin in range(1,hist.GetXaxis().GetNbins()):
    #integral = getIntegral(fullsimCurve, hist.GetXaxis().GetBinLowEdge(iBin), hist.GetXaxis().GetBinUpEdge(iBin), crystalBall, gaussian)
    integral = getIntegral(fullsimCurve, hist.GetXaxis().GetBinLowEdge(iBin), hist.GetXaxis().GetBinUpEdge(iBin), crystalBall)
    #print "bin content from %f to %f is: %f" % (hist.GetXaxis().GetBinLowEdge(iBin), hist.GetXaxis().GetBinUpEdge(iBin), hist.GetBinContent(iBin))
    #print "adjusted from x=%f to %f is: %f" % (hist.GetXaxis().GetBinLowEdge(iBin), hist.GetXaxis().GetBinUpEdge(iBin), integral/hist.GetXaxis().GetBinWidth(iBin))
    if not hist.GetBinError(iBin) == 0 :
      binnedCurveVal = integral/hist.GetXaxis().GetBinWidth(iBin) 
      if hist.GetXaxis().GetBinUpEdge(iBin) > 700 and hist.GetXaxis().GetBinLowEdge(iBin) > float(fullsimMC)*0.75 and hist.GetXaxis().GetBinUpEdge(iBin) < float(fullsimMC)*1.2:
        cloneHist.SetBinContent(iBin, hist.GetBinContent(iBin))
        ksHist.SetBinContent(iBin, binnedCurveVal)
        if binnedCurveVal < 0:
          print "Got a weird binned curve val!: ", binnedCurveVal
          print "integral:", integral
          print "bin width:", hist.GetXaxis().GetBinWidth(iBin)
       
      else: 
        cloneHist.SetBinContent(iBin, 0)
        ksHist.SetBinContent(iBin, 0)
      if not hist.GetBinContent(iBin) <=0.1 :
        pullHist.SetBinContent(iBin, (binnedCurveVal - hist.GetBinContent(iBin))/hist.GetBinError(iBin))
        pullHist.SetBinError(iBin, 0)
      else:
        pullHist.SetBinContent(iBin, -999)
    else:
      ksHist.SetBinContent(iBin, 0)
      cloneHist.SetBinContent(iBin, 0)
      pullHist.SetBinContent(iBin, -999)
  cloneHist = hist.Clone()
  #cloneHist.Divide(pullHist)
  bottomPad.cd()
  #cloneHist.GetXaxis().SetRangeUser(float(fullsimMC)*0.75, float(fullsimMC)*1.2)
  #cloneHist.Draw()
  #cloneHist.GetXaxis().SetLabelSize(.1)
  #cloneHist.GetYaxis().SetLabelSize(.1)
  #cloneHist.GetYaxis().SetRangeUser(0, 2)
  pullHist.GetXaxis().SetRangeUser(float(fullsimMC)*0.75, float(fullsimMC)*1.2)
  pullHist.Draw("P")
  pullHist.SetMarkerStyle(2)
  pullHist.SetTitle("")
  pullHist.GetXaxis().SetLabelSize(0)
  pullHist.GetXaxis().SetTitle("")
  pullHist.GetYaxis().SetTitle("Pull")
  pullHist.GetYaxis().SetTitleSize(0.1)
  pullHist.GetYaxis().SetTitleOffset(0.3)
  pullHist.GetYaxis().SetLabelSize(.13)
  pullHist.GetYaxis().SetRangeUser(-5, 5)
  pullHist.GetYaxis().SetNdivisions(405)
  outCan.cd()
  bottomPad.Draw()
#  newCan = TCanvas()
#  newCan.SetName("k_%s" % fullsimMC)
#  newCan.cd()
#  hist.Draw()
#  hist.SetLineColor(kGreen)
#  hist.SetMarkerColor(kGreen)
#  ksHist.Draw("SAME")
#  ksHist.SetLineColor(kRed)
#  ksHist.SetMarkerColor(kRed)
#  ksHist.SetName("ksHist")
  cloneHist.Draw("SAME")
  cloneHist.SetMarkerColor(kBlue)
  cloneHist.SetLineColor(kBlue)
  cloneHist.SetName("cloneHist")
  for iBin in range(0, cloneHist.GetNbinsX()):
    if cloneHist.GetXaxis().GetBinUpEdge(iBin) < 700 or cloneHist.GetXaxis().GetBinUpEdge(iBin) < float(fullsimMC)*0.75 or cloneHist.GetXaxis().GetBinLowEdge(iBin) > float(fullsimMC)*1.2:
      cloneHist.SetBinContent(iBin, 0)
#  fullsimCurve.Draw("SAME")
#  fullsimCurve.SetLineColor(kBlack)
#  newCan.Write()
  ksTestResults[fullsimMC] = cloneHist.KolmogorovTest(ksHist)
  stdDevs[fullsimMC] = cloneHist.GetStdDev()
  topPad.cd()
  fullsimPad.GetPrimitive("TPave").AddEntry(0, "RMS_{signal}=%3d GeV"%stdDevs[fullsimMC], "")
  fullsimPad.GetPrimitive("TPave").Draw("SAME")
  topPad.GetPrimitive("TPave").SetY1NDC(topPad.GetPrimitive("TPave").GetY1NDC() * .6)
  outFile.cd()
  outCan.Write()
  outCan.SaveAs("outSigFits/%s_%i.pdf" % (options.category, fullsimMC))
#outFile.Close()
pprint(ksTestResults)
pprint(stdDevs)
  
