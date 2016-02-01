from dictmaker import makeCanvasDict
from sys import argv
from ROOT import *

canvasDict = makeCanvasDict(argv[1])
#for key in canvasDict.keys():
#    print "key is %s" % key
#    print "x-axis lower bound is %s" % canvasDict[key][0]
#    print "x-axis upper bound is %s" % canvasDict[key][1]
#    print "x-axis title is %s"       % canvasDict[key][2]
#    print "y-axis lower bound is %s" % canvasDict[key][3]
#    print "y-axis upper bound is %s" % canvasDict[key][4]
#    print "y-axis title is %s"       % canvasDict[key][5]
#    print "plot title is %s"         % canvasDict[key][6]
#    print "legend title is %s"       % canvasDict[key][7]
for key in canvasDict.keys():
    canvasFile = TFile("output/%s.root"%key)
    canvas = canvasFile.Get("canvas")
    canvas.Draw()
    stackPlot=canvas.GetPrimitive("stackPlot")
    stackPlot.GetXaxis().SetRangeUser(float(canvasDict[key][0]), float(canvasDict[key][1]))
    stackPlot.GetXaxis().SetTitle(canvasDict[key][2])
    stackPlot.GetYaxis().SetRangeUser(float(canvasDict[key][3]), float(canvasDict[key][4]))
    stackPlot.GetYaxis().SetTitle(canvasDict[key][5])
    stackPlot.SetTitle(canvasDict[key][6])
    canvas.Print("output/%s.pdf"%key)
