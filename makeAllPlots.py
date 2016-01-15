# This script runs all the other scripts for making all the plots.
# It needs one argument: the input filename
# Example:
# python makeAllPlots.py myInputFile.root
# John Hakala, 1/15/2016

from sys import argv
import subprocess

scripts = [
	"formatPreSelectionPlots.py" , 
	"formatSubjetVarsPlots.py"   , 
	"formatMVAvsEprofiles.py"    ,
	"makeTriggerTurnOnPlot.py"   ,
]


for script in scripts:
	subprocess.call(["python" ,  script ,  argv[1] ,  "-b"])
