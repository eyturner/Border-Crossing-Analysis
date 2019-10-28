import os
import sys
import csv
from Date import Date
from operator import itemgetter

def main():
    csvFile = sys.argv[1]
    importantValues = []
    depth = 3
    with open(csvFile) as file:
        reader = csv.reader(file, delimiter=",")
        lineCount = 0
        for row in list(reader):
            importantValues.append(row[depth:])
            lineCount+= 1

    outputDict = {}
    endList = []

    for bigList in importantValues[1:]:
        dataDict = listToDict(bigList)
        currentDict = dataDict
        updateDict(outputDict, dataDict, 3)
        #print("result is:",outputDict,"\n")
    dictToLists(outputDict, depth, [], endList)
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
        print(line)

if __name__ == '__main__':
    main()
