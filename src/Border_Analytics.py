import os
import sys
import csv
from Date import Date
from operator import itemgetter
import DictList_Functions

def listToDict(list):
    newDict = {}
    lastDict = {}
    for item in reversed(list):
        if(item != list[-1]):
            tempDict = {item:lastDict}
            lastDict = tempDict
            newDict = tempDict
        else:
            lastDict = item
    return newDict

def updateDict(dict, newDict, depth):
    # print('depth is now:', depth)
    # print('dict is:',dict,'newDict is:', newDict)
    if(depth == 0):
        ints = int(dict) + int(newDict)
        return ints
    else:
        for key in newDict:
            if key in dict:
                dict[key] = (updateDict(dict[key], newDict[key], depth - 1))
                #print('after update with key, dict is:', dict)
                return dict
            else:
                dict.update(newDict)
                #print('after update w/out key, dict is:', dict)
                return dict


def main():
    inputFile = sys.argv[1]
    outputFile = sys.argv[2]

    importantValues = []
    with open(inputFile) as file:
        reader = csv.reader(file, delimiter=",")
        lineCount = 0
        for row in list(reader):
            if(lineCount == 0):
                borderIndex = row.index('Border')
                valueIndex = row.index('Value')
            importantValues.append(row[borderIndex:valueIndex + 1])
            lineCount+= 1

    depth = valueIndex - borderIndex
    outputDict = {}
    endList = []
    dataTypes = importantValues[0]

    for bigList in importantValues[1:]:
        dataDict = listToDict(bigList)
        currentDict = dataDict
        updateDict(outputDict, dataDict, depth)
        #print("result is:",outputDict,"\n")
    dictToLists(outputDict, borderIndex, [], endList)
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
