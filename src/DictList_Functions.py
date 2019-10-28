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
