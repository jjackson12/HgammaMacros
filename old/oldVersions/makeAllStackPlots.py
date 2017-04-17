from sys import argv
import subprocess
from  dictmaker import makeStackplotsDict

print "inputs list file is: %s"%argv[1]
print "stackplots list file is: %s"%argv[2]

stackplotsDict = makeStackplotsDict(argv[2])
print stackplotsDict

for key in stackplotsDict.keys():
    subprocess.call(["python", "makeStackPlot.py", argv[1], "requireTrigger", key, stackplotsDict[key][0], str(stackplotsDict[key][1]), stackplotsDict[key][2], "-b"])
