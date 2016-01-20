from os import path
def makeInputsDict(inputsListFile):
	inputsList = open(inputsListFile)
	inputsDict = dict()
	for line in inputsList:
		lineParts = line.split()
		if not path.exists(lineParts[1]):
			exit("\nError: file %s not found.\n"%lineParts[1])
		inputsDict[lineParts[0]] = lineParts[1]
	return inputsDict
