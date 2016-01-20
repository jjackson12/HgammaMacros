def makeInputsDict(inputsListFile):
	inputsList = open(inputsListFile)
	inputsDict = dict()
	for line in inputsList:
		lineParts = line.split()
		inputsDict[lineParts[0]] = lineParts[1]
	return inputsDict
