def getVarsAndCorrMatrix(inFileName):
  from ROOT import TFile, RooWorkspace, RooRealVar
  response = {}
  inFile = TFile(inFileName)
  ws = inFile.Get("Vg")

  par1 = {"name":"bkg_dijetsimple2_lin2", "val":ws.var("bkg_dijetsimple2_lin2").getValV(), "errHi":ws.var("bkg_dijetsimple2_lin2").getAsymErrorHi(), "errLo":ws.var("bkg_dijetsimple2_lin2").getAsymErrorLo()} 
  print par1

  par2 = {"name":"bkg_dijetsimple2_log2", "val":ws.var("bkg_dijetsimple2_log2").getValV(), "errHi":ws.var("bkg_dijetsimple2_log2").getAsymErrorHi(), "errLo":ws.var("bkg_dijetsimple2_log2").getAsymErrorLo()} 
  print par2

  inFile.ls()
  fitResult = inFile.Get("fitTest")
  corrMatrix = fitResult.correlationMatrix()
  covMatrix = fitResult.covarianceMatrix()
  covarianceMatrix = [[covMatrix[0][0], covMatrix[0][1]], [covMatrix[1][0], covMatrix[1][1]]]
  correlationMatrix = [[corrMatrix[0][0], corrMatrix[0][1]], [corrMatrix[1][0], corrMatrix[1][1]]]
  print covarianceMatrix
  print correlationMatrix

  return (par1, par2, correlationMatrix, covarianceMatrix)

def generateToyFunctions(normNom, normErr, p1, p1err, p2, p2err, corrMatrix, covMatrix, nToys):
  from ROOT import TF1, TRandom
  from math import sqrt
  functions = []
  formula = "[0]*TMath::Power(x, [1]+[2]*TMath::Log(x))"
  gaussDist = TRandom()
  x1Nom = (-0.997412*p1-0.0719019*p2)
  x2Nom = (0.0719019*p1-0.997412*p2)
  print "p1 is ", p1
  print "p1err is ", p1err
  print "x1Nom is ", x1Nom
  print "p2 is ", p2
  print "p2err is ", p2err
  print "x2Nom is ", x2Nom
  x1err = -0.997412*p1err-0.0719019*p2err
  x2err = 0.0719019*p1err-0.997412*p2err
  print "x1err is ",  -0.997412*p1err-0.0719019*p2err
  print "x2err is ",  (0.0719019*p1err-0.997412*p2err)
  for i in range (0, nToys):
    print "--------"
    print "toy %i:" % i
    x1 = gaussDist.Gaus(x1Nom,x1err)
    x2 = gaussDist.Gaus(x2Nom, x2err)
    varp1 = (-0.997412*x1+0.0719019*x2)
    varp2 = (-0.0719019*x1-0.997412*x2) 
    print "original p1, p2:        %f, %f" % (p1, p2)
    print "original p1err, p2err:  %f, %f" % (p1err, p2err)
    print "translates to x1, x2:   %f, %f" % (x1Nom, x2Nom)
    print "x1err, x2err:           %f, %f" % (x1err, x2err)
    print "picked x1, x2:          %f, %f" % (x1, x2)
    print "translates to  p1, p2:  %f, %f" % (varp1, varp2)
    functions.append(TF1("f_%i" % i, formula, 700, 4700))
    functions[-1].SetParameters(1, varp1, varp2)
    if functions[-1].Integral(700, 4700)  == 0:
      del(functions[-1])
    else:
      prenorm = functions[-1].Integral(700, 4700)
      norm = gaussDist.Gaus(normNom, normErr)/prenorm
      print "norm is: ", norm
      functions[-1].SetParameter(0, norm)

  return functions
