from optparse import OptionParser

fitParams = {'850_btag' :[846.528, 26.8804, 1.92619, 2.58327, 846.528, 199.939, 1],
 '650_btag' :[705.199, 5, 1.3, 78.7663, 705.199, 152.568, 1],
 '1000_btag' :[998.219, 30.0323, 1.2553, 14.5686, 998.219, 150, 1],
 '750_btag' :[747.715, 24.668, 2.00076, 4.36479, 747.715, 150, 1],
 '1300_btag' :[1295.78, 36.1013, 1.29065, 8.6706, 1295.78, 150, 1],
 '1150_btag' :[1145.53, 33.9461, 1.50535, 5.63408, 1145.53, 150, 1],
 '1450_btag' :[1444.81, 39.2996, 1.20681, 20.692, 1444.81, 150, 1],
 '1600_btag' :[1592.86, 41.842, 1.25069, 13.525, 1592.86, 150, 1],
 '1750_btag' :[1738.83, 47.7861, 1.51134, 7.20404, 1738.83, 150, 1],
 '1900_btag' :[1888.55, 49.5046, 1.4133, 6.38389, 1888.55, 150, 1],
 '2050_btag' :[2037.72, 50.923, 1.2687, 9.29857, 2037.72, 150, 1],
 '2450_btag' :[2433.19, 62.2407, 1.26703, 9.14573, 2433.19, 150, 1],
 '2850_btag' :[2830.31, 66.6616, 1.08743, 26.7857, 2830.31, 207.864, 1],
 '3250_btag' :[3224.36, 75.4772, 0.961861, 129.036, 3224.36, 150, 1],
 '650_antibtag' :[703.629, 12.5929, 1.3, 5, 703.629, 82.9436, 0.443267],
 '750_antibtag' :[750.966, 22.8891, 1.21791, 123.133, 750.966, 109.897, 0.951299],
 '850_antibtag' :[851.01, 25.9014, 1.24099, 132.715, 851.01, 98.6574, 0.967787],
 '1000_antibtag' :[1003.69, 27.6435, 1.09741, 143.658, 1003.69, 115.707, 0.966824],
 '1150_antibtag' :[1151.42, 32.6319, 1.21667, 19.7317, 1151.42, 191.108, 0.973386],
 '1300_antibtag' :[1299.08, 37.0637, 1.44266, 5.28244, 1299.08, 217.066, 0.98536],
 '1450_antibtag' :[1449.8, 37.3017, 1.43623, 4.29502, 1449.8, 143.919, 0.971258],
 '1750_antibtag' :[1746.46, 44.4236, 1.61348, 2.82067, 1746.46, 197.523, 0.985869],
 '1600_antibtag' :[1597.55, 42.239, 1.40307, 4.97437, 1597.55, 184.385, 0.980136],
 '1900_antibtag' :[1895.26, 47.2437, 1.33438, 5.22512, 1895.26, 174.547, 0.983629],
 '2050_antibtag' :[2043.4, 51.4661, 1.60823, 3.25372, 2043.4, 185.97, 0.983146],
 '2450_antibtag' :[2439.88, 54.5334, 1.43573, 3.08462, 2439.88, 109.638, 0.908153],
 '2850_antibtag' :[2838.68, 56.8804, 1.13643, 4.5485, 2838.68, 108.544, 0.856111],
 '3250_antibtag' :[3231.7, 73.4536, 1.16618, 6.36565, 3231.7, 191.195, 0.970774]}




parser = OptionParser()
parser.add_option("-c", dest="category",
                  help = "the category: either btag or antibtag")
parser.add_option("-r", dest="binWidth", type=int, default=10,
                  help = "the bin width for output plot")
parser.add_option("-b", action="store_true", dest="batch",
                  help = "turn on batch mode")
(options, args) = parser.parse_args()
if not options.category in ["btag", "antibtag"]:
  #print "you must pick either 'btag' or 'antibtag' as the -c option"
  exit(1)
from ROOT import *
if options.batch:
  gROOT.SetBatch()

def makeCrystalBall(mass, category):
  key="%i_%s"%(mass, category)
  mu    = fitParams[key][0]
  sigma = fitParams[key][1]
  alpha = fitParams[key][2]
  n     = fitParams[key][3]
  relN  = fitParams[key][6]
  formula = "%f*ROOT::Math::crystalball_pdf(x, %f, %f, %f, %f)" % (relN, alpha, n, sigma, mu)
  #formula = "ROOT::Math::crystalball_function(x, 2, 1, 1, 0)"
  print formula
  return formula
def makeGauss(mass, category):
  key="%i_%s"%(mass, category)
  mu    = fitParams[key][4]
  sigma = fitParams[key][5]
  relN  = (1-fitParams[key][6])
  formula = "%f*ROOT::Math::gaussian_pdf(x, %f, %f)" % (relN, sigma, mu)
  #formula = "ROOT::Math::crystalball_function(x, 2, 1, 1, 0)"
  print formula
  return formula

gStyle.SetOptStat(0)
outFile = TFile("prettyFits_%s.root" % options.category, "RECREATE")
def getIntegral(curve, xLow, xHi):
  integral = Double(0)
  yLow  = Double(curve.Eval(xLow))
  yHi   = Double(curve.Eval(xHi) )
  #print "curve at x=%f has value y=%f" % (xLow, yLow)
  #print "curve at x=%f has value y=%f" % (xHi, yHi)
  xLast = Double(xLow            )
  yLast = Double(yLow            )
  xx = Double(xLow               )
  yy = Double(yLow               )
  for iPoint in range(0, curve.GetN()):
    #curve.GetPoint(iPoint-1, xLast, yLast)
    curve.GetPoint(iPoint, xx, yy)
    if xx>=xLow and xx<=xHi :
      #print "python evaluates %f <= %f to %r" % (xx, xHi, xx<=xHi)
      #print "found a point between %f and %f: it has (x,y) value (%f, %f)"%(xLow, xHi, xx,yy)
      #print "will add (%f=%f) * (%f+%f)/2" % (xx, xLast, yy, yLast)
      integral +=  (xx-xLast) *(yy+yLast)/2
      #print "   == %f" % ((xx-xLast) *(yy+yLast)/2)
      #print " total   == %f" % integral
      xLast = Double(float(xx))
      yLast = Double(float(yy))
  #print "  adding the last piece"
  #print "(%f-%f) * (%f+%f)/2" % (xHi, xLast, yHi, yLast) 
  integral +=  (xHi-xLast) *(yHi+yLast)/2 
  #print "   == %f" % ((xHi-xLast) *(yHi+yLast)/2)
  #print "total = %f" % integral
  return integral

from ROOT import *
fullsimMCs      = [750, 850, 1000, 1150, 1300, 1450, 1600, 1750, 1900, 2050, 2450, 2850, 3250]
#fullsimMCs      = [1000]
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
    print "fullsimPad has primitive:", primitive
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
    if (y >= 0):
      print "checking point %i: (%f, %f)" % (iPoint, x, y)
    histBin = hist.GetXaxis().FindBin(x)
    print "histBin is:", histBin
    hist.SetBinContent(histBin, y)
    hist.SetBinError(histBin, e)

  print "fullsimHist has number of entries:", sumY
  print "hist has number of entries:", hist.GetSumOfWeights()
  hist.Rebin(options.binWidth*10)
  print "after rebin, hist has number of entries:", hist.GetEntries()
  hist.SetMarkerStyle(20)

  topPad.cd()
  hist.Draw("PE1")
  hist.GetYaxis().SetTitle("Events (A.U.)")
  hist.GetXaxis().SetTitle("M_{X} (GeV)")
  hist.GetYaxis().SetTitleOffset(1.2)
  hist.GetXaxis().SetRangeUser(float(fullsimMC)*0.75, float(fullsimMC)*1.2)

  for iPoint in range(0, fullsimCurve.GetN()+5):
    fullsimCurve.GetPoint(iPoint, x, y)
    fullsimCurve.SetPoint(iPoint, x, options.binWidth*y/1.5)
    #print "fullSimCurve has (x,y) values: (%f,%f)" % (x,y)
  fullsimCurve.SetLineColor(kRed)
  fullsimCurve.Draw("SAME")
  norm = hist.GetSumOfWeights()
  crystalBall =TF1("cb_%i_%s" % (fullsimMC, options.category), "%f*%s"%(norm*options.binWidth, makeCrystalBall(fullsimMC, options.category)), float(fullsimMC)*0.75, float(fullsimMC)*1.2)
  crystalBall.Draw("SAME")
  crystalBall.SetLineColor(kBlue)
  gaussian =TF1("gauss_%i_%s" % (fullsimMC, options.category), "%f*%s"%(norm*options.binWidth, makeGauss(fullsimMC, options.category)), float(fullsimMC)*0.75, float(fullsimMC)*1.2)
  gaussian.Draw("SAME")
  gaussian.SetLineColor(kGreen)
  outCan.cd()
  topPad.Draw()
  outCan.Draw()
  pullHist = hist.Clone() 
  pullHist.SetName("ratio_%i" % fullsimMC)
  for iBin in range(1,hist.GetXaxis().GetNbins()):
    integral = getIntegral(fullsimCurve, hist.GetXaxis().GetBinLowEdge(iBin), hist.GetXaxis().GetBinUpEdge(iBin))
    #print "bin content from %f to %f is: %f" % (hist.GetXaxis().GetBinLowEdge(iBin), hist.GetXaxis().GetBinUpEdge(iBin), hist.GetBinContent(iBin))
    #print "adjusted from x=%f to %f is: %f" % (hist.GetXaxis().GetBinLowEdge(iBin), hist.GetXaxis().GetBinUpEdge(iBin), integral/hist.GetXaxis().GetBinWidth(iBin))
    if not hist.GetBinError(iBin) == 0 and not hist.GetBinContent(iBin) <=0.1 :
      pullHist.SetBinContent(iBin, (hist.GetBinContent(iBin) - integral/hist.GetXaxis().GetBinWidth(iBin) )/hist.GetBinError(iBin))
      pullHist.SetBinError(iBin, 0)
    else:
      pullHist.SetBinContent(iBin, -999)
  #cloneHist = hist.Clone()
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
  outFile.cd()
  outCan.Write()
  outCan.SaveAs("%s_%i.pdf" % (options.category, fullsimMC))
outFile.Close()
  
