class HitLocation:
    def __init__(self, lowerBound, upperBound, name):
        self.lowerBound = lowerBound
        self.upperBound = upperBound
        self.name = name
        self.conditions = []
    def addCondition(self, condition, duration):
        self.conditions.append([condition, duration])
    def decrementConditions(self):
        outStr = ''
        for a in self.conditions:
            if a[1] > 0:
                a[1] = a[1] - 1
                outStr = outStr + self.name + ' is now ' + a[0] + ' for ' + str(a[1]) + ' intervals.\n'
        return outStr.rstrip('\n')
    def cleanupConditions(self):
        tempList = self.conditions.copy()
        self.conditions.clear()
        condLength = len(tempList)
        cleanedConditions = []
        while condLength > 0:
            c = tempList.pop(0)
            if c[1] != 0:
                self.conditions.append(c)
            else:
                cleanedConditions.append(c[0])
            condLength = condLength - 1
        return cleanedConditions
    def endCondition(self, condName):
        tempList = self.conditions.copy()
        self.conditions.clear()
        condLength = len(tempList)
        cleanedConditions = []
        while condLength > 0:
            c = tempList.pop(0)
            if c[0] != condName:
                self.conditions.append(c)
            else:
                cleanedConditions.append(c[0])
            condLength = condLength - 1
        return cleanedConditions
    def replaceCondition(self, conditionToRemove, conditionToAdd, duration):
        outStr = ''
        tempList = self.conditions.copy()
        self.conditions.clear()
        condLength = len(tempList)
        while condLength > 0:
            c = tempList.pop(0)
            if c[0] != conditionToRemove:
                self.conditions.append(c)
            else:
                outStr = outStr + self.name + ' is no longer ' + c[0]
                self.conditions.append([conditionToAdd, duration])
            condLength = condLength - 1
        if outStr != '':
            return outStr + ' but is now ' + conditionToAdd + ' for ' + str(duration)
        else: return 'Replacement failed, could not find ' + conditionToRemove
    def readConditions(self):
        outStr = ''
        for c in self.conditions:
            if c[1] < 0:
                outStr = outStr + self.name + ' is ' + c[0] + ' until further notice.\n' 
            else:
                outStr = outStr + self.name + ' is ' + c[0] + ' for ' + str(c[1]) + ' intervals.\n'
        if outStr == '':
            return self.name + ' has no conditions.\n'
        else:
            return outStr
