import os
import sys
import csv
from Date import Date
from operator import itemgetter

def main():
    inputFile = argv[1]
    outputFile = argv[2]

    importantValues = []
    startCol = 3
    with open(inputFile) as file:
        reader = csv.reader(file, delimiter=",")
        lineCount = 0
        for row in list(reader):
            importantValues.append(row[startCol:])
            lineCount+= 1

    outputDict = {}
    endList = []
    dataTypes = importantValues[0]
    depth = len(row) - startCol - 1

    for bigList in importantValues[1:]:
        dataDict = listToDict(bigList)
        currentDict = dataDict
        updateDict(outputDict, dataDict, depth)
        #print("result is:",outputDict,"\n")
    dictToLists(outputDict, startCol, [], endList)
    endList.sort(key = itemgetter(1,3,2,0))
    for row in endList:
        border = row[0]
        date = row[1]
        measure = row[2]
        prevDate = getPrevMonthDate(date)
        endIndex = endList.index(row)
        testList = [border, prevDate, measure]
        runningSum = 0
        numPrevMonths = 0
        foundPrev = False
        for prevRow in endList[:endIndex]:
            if(all(item in prevRow for item in testList)):
                foundPrev = True
                oldValue = prevRow[-3]
                numPrevMonths = prevRow[-1]
                runningSum = prevRow[-2]*numPrevMonths
                row.append(round((oldValue + runningSum)/(numPrevMonths + 1)+0.5))
                #print("RUNNING AVG:", round((oldValue + runningSum)/(numPrevMonths+1) + 0.5))
                row.append(numPrevMonths + 1)
                break
        if(not foundPrev):
            row.append(0)
            row.append(0)


    for line in reversed(endList):
        line.pop()

    endList.append(dataTypes)
    with open(outputFile,"w") as outFile:
        writer = csv.writer(outFile)
        writer.writerows(reversed(endList))


if __name__ == '__main__':
    main()
