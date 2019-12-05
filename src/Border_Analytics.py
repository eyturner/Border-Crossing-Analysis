import os
import sys
import csv
from Date import Date
from operator import itemgetter

# Takes a dictionary, the "depth" of the dictionary: the number of dictionaries/
# subdictionaries in the dictionary, a localList which is the list that we will
# populate and manipulate within this local function, And an endList which is
# what will be modified back in the main function. dictToLists results in a list
# that contains every possible path of the original dictionary.
def dictToLists(dict, depth, localList, endList):
    if(depth == 0):
        integer = [int(dict)]
        localList.extend(integer)
        endList.append(localList[:])
        localList.pop()
        return localList
    else:
        for key in dict:
            if(depth == 2):
                localList.append(Date(key))
            else:
                localList.append(key)
            localList = dictToLists(dict[key], depth - 1, localList, endList)
            localList.pop()
    return localList


# returns a Date object of the previous month of the date given.
# Ex: date = 02/01/2000, getPrevMonthDate(date) = 01/01/2000
def getPrevMonthDate(date):
    if(date.getMonth() == 1):
        prevMonth = 12
        prevYear = date.getYear() - 1
    else:
        prevMonth = date.getMonth() - 1
        prevYear = date.getYear()
    if(prevMonth < 10):
        monthStr = '0'+str(prevMonth)
    else:
        monthStr = str(prevMonth)
    yearStr = str(prevYear)
    dayStr = '0'+str(date.getDay())
    timeStr = date.getTime()
    return Date(monthStr + '/' + dayStr + '/'+ yearStr + ' '+ timeStr)

# Takes the list of data that we care about, and makes each index a dictionary
# containing the subsequent indicies as more dictionaries.
# Ex: list = [key1,key2,key3,key], listToDict(list) = {key1:{key2:{key3:{key4}}}
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

# Given out dictionary created from the list of data, updateDict adds values for
# any dictionary entries with same Border, Date, and Measure and updates value to
# reflect the sum for each Border,Date,Measure
# Ex: {Border:{Date:{Measure:value1, Measure: value2}}}
# -->{Border:{Date:{Measure:value1 + value2}}}
def updateDict(dict, newDict, depth):
    if(depth == 0):
        ints = int(dict) + int(newDict)
        return ints
    else:
        for key in newDict:
            if key in dict:
                dict[key] = (updateDict(dict[key], newDict[key], depth - 1))
                return dict
            else:
                dict.update(newDict)
                return dict


def main():
    inputFile = sys.argv[1]
    outputFile = sys.argv[2]

    #importantValues will contain the data subset that we are interested in.
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

    # Now creating the dictionary that will contain all our data combined and the
    # "endList" whcih will contain all forms of border crossing for the entire data set
    for bigList in importantValues[1:]:
        dataDict = listToDict(bigList)
        updateDict(outputDict, dataDict, depth)
    dictToLists(outputDict, borderIndex, [], endList)

    # After sorting the "endList" in the manner requested, we will then add two
    # values to each row. The running average and the previous number of months
    # where the same method of crossing at the same border has occurred.
    endList.sort(key = itemgetter(1,3,2,0))
    for row in endList:
        testList = row[0:depth]
        prevDate = getPrevMonthDate(testList[-2])
        testList[-2] = prevDate
        endIndex = endList.index(row)
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
                row.append(numPrevMonths + 1)
                break
        if(not foundPrev):
            row.append(0)
            row.append(0)

    # Now getting ready to print to CSV. First we get rid of the count of months
    # from the endList. Then we add the data types back in, adding a column to include
    # "Average". And finally writing the whole thing to the output file.
    for line in reversed(endList):
        line.pop()
    dataTypes.append("Average")
    endList.append(dataTypes)
    with open(outputFile,"w") as outFile:
        writer = csv.writer(outFile)
        writer.writerows(reversed(endList))


if __name__ == '__main__':
    main()
