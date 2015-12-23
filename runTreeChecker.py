from ROOT import *
import os, subprocess
def compileMacro(macroName):
	if os.path.exists(macroName+"_C_ACLiC_dict_rdict.pcm"):
    		os.remove(macroName+"_C_ACLiC_dict_rdict.pcm")
	if os.path.exists(macroName+"_C.d"):
    		os.remove(macroName+"_C.d")
	if os.path.exists(macroName+"_C.so"):
    		os.remove(macroName+"_C.so")
	macro = macroName + ".C++g"
	subprocess.call(["root", "-l", "-q", macro])
compileMacro("treeChecker")
gSystem.Load('treeChecker_C')
checker = treeChecker()
checker.Loop()
