from os import path

# Methods to make dictionries to sort out stackplots, canvases, and inputs
# John Hakala, 5/11/2016

def makeInputsDict(inputsListFile):
	inputsList = open(inputsListFile)
	inputsDict = dict()
	for line in inputsList:
		lineParts = line.split()
		if not path.exists(lineParts[1]):
			exit("\nError: file %s not found.\n"%lineParts[1])
		inputsDict[lineParts[0]] = lineParts[1]
	return inputsDict

def makeStackplotsDict(stackplotsListFile):
	stackplotsList = open(stackplotsListFile)
	stackplotsDict = dict()
	for line in stackplotsList:
		lineParts = line.strip().split()
		stackplotsDict[lineParts[0]] = [lineParts[1], int(lineParts[2]), lineParts[3]]
	return stackplotsDict

def makeCanvasDict(canvasListFile):
	canvasList = open(canvasListFile)
	canvasDict = dict()
	for line in canvasList:
		lineparts = line.strip().split(',')
		for i in range(0,len(lineparts)):
			lineparts[i] = lineparts[i].strip()
		print lineparts
		canvasDict[lineparts[0]] = [lineparts[1], lineparts[2], lineparts[3], lineparts[4], lineparts[5], lineparts[6], lineparts[7], lineparts[8]]
	print canvasDict
	return canvasDict
