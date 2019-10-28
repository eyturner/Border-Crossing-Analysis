# Date class for the Insight Challenge. DateStr are of the form 'mm/dd/yyyy hh:mm:ss XM'
# For now, I'm just going to worry about month/day/year. If later we need to worry about the time,
# just update the methods.
class Date:
    def __init__(self, dateStr):
        self.month = int(dateStr[0:2])
        self.day = int(dateStr[3:5])
        self.year = int(dateStr[6:10])
        self.time = dateStr[11:]

    def getMonth(self):
        return self.month

    def getDay(self):
        return self.day

    def getYear(self):
        return self.year

    def __str__(self):
        if(self.month < 10):
            monthStr = '0'+str(self.month)
        else:
            monthStr = str(self.month)
        if(self.day < 10):
            dayStr = '0'+str(self.day)
        else:
            dayStr = str(self.day)
        return(monthStr+'/'+dayStr+'/'+str(self.year)+' '+self.time)

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if(self.month == other.getMonth()):
            if(self.day == other.getDay()):
                if(self.year == other.getYear()):
                    return True
        return False

    #By less than, I mean earlier in time (older)
    def __lt__(self, other):
        if(self == other):
            return False
        if(self.year < other.getYear()):
            return True
        elif(self.year > other.getYear()):
            return False
        else:
            if(self.month < other.getMonth()):
                return True
            elif(self.month > other.getMonth()):
                return False
            else:
                if(self.day < other.getDay()):
                    return True
                else:
                    return False

    def __gt__(self, other):
        if(self == other):
            return False
        return not(self < other)

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


def dateTest():
    newDate = Date('10/10/2019 12:00:00 AM')
    secondDate = Date('10/10/2019 12:00:00 AM')
    print(newDate > secondDate)
