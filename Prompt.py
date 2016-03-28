import random
import re

class Prompt:
    #Required: command, prompt, typing, manualFlag, owner.
    #warnValue, prompt, and typing should all have the same size.
    def __init__(self, command, prompt, typing, warnValue, manualFlag, owner):
        self.command = command #the command that will be returned that should
            #be fed into an EXEC statement. 
        self.prompt = prompt #the human prompts as an array that will be returned as a reqest.
        self.results = [] #the results that will be combined with the command as
            #final output.
        self.typing = typing #types of variable expected. s(tring), i(nt), d(ie)N.
        self.warnValue = warnValue #Must be same size as prompt array.
            #Any value other than '' for s type will ask for confirmation
            #Any value larger than * for i type will ask for confirmation
            #Any value for d will override the inherent d limit.
        self.manualFlag = manualFlag #should dice be rolled manually?
        self.confirmAwait = False #is the prompt waiting for a confirmation?
        self.confirmMessage = '' #the confirmation the prompt is waiting for
        self.confirmValue = 0 #the value to be confirmed
        self.owner = owner #the user who needs to respond to the prompt

    # Returns tompost prompt or the value to be fed to an ExecStatement if isComplete is True.
    def givePrompt(self):
        if not self.isComplete():
            promptPosn = len(self.results)
            if not self.confirmAwait:
                if self.typing[promptPosn].startswith('d'):
                    if self.manualFlag:
                        return 'Enter the result of a ' + self.typing[promptPosn]
                    else:
                        rollResult = self.rollDie(int(self.typing[promptPosn][1:]))
                        self.addResult(rollResult)
                        return 'Rolled ' + str(rollResult) + ' on a ' + self.typing[promptPosn]
                return self.prompt[promptPosn]
            else:
                return 'You must first confirm. ' + self.confirmMessage
        else:
            retVal = self.command
            for a in range(len(self.results)):
                if self.typing[a] == 's':
                    retVal = re.sub('qqq',"'" + self.results[a] + "'",retVal, count=1)
                else:
                    retVal = re.sub('qqq',self.results[a],retVal, count=1)
            return retVal
            
    # Adds the result of the most recent prompt to the list if it is correct
    def addResult(self, result):
        promptPosn = len(self.results)
        correct = False
        if self.confirmAwait:
            if result == self.confirmValue:
                self.unsetConfirm()
                correct = True
            else:
                self.unsetConfirm()
                return 'Confirmation failed.'
        elif self.typing[promptPosn] == 's':
            if self.warnValue[promptPosn] == '': correct = True
            else: correct = False
        elif self.typing[promptPosn] == 'i':
            if self.isInt(result):
                if int(result) <= self.warnValue[promptPosn]: correct = True
                else: correct = False
            else: return 'This value is invalid. Expecting integer.'
        elif self.typing[promptPosn].startsWith('d'):
            if self.isValidRoll(int(result), self.typing[promptPosn][1:]):
                correct = True
            elif self.warnValue[promptPosn] != '': correct = True
            elif self.isInt(result): correct = False
            else: return 'This value is invalid.'
        if correct:
            self.results.append(result)
            return 'Queued ' + str(result)
        else: return self.setConfirm(result)

    # Sets the confirmation value and returns a string asking for confirmation
    def setConfirm(self, value):
        self.confirmAwait = True
        self.confirmMessage = 'Enter ' + value + ' again to confirm.'
        self.confirmValue = value
        return self.confirmMessage

    # Resets the confirmation value to nothing. Returns a string saying it did so.
    def unsetConfirm(self):
        self.confirmAwait = False
        self.confirmMessage = ''
        self.confirmValue = 0
        return 'Confirmation failed.'
    
    # Returns True if the value can be cast as an int, False otherwise
    def isInt(self, a):
        try:
            int(a)
            return True
        except ValueError: return False
        
    # Check to see if the input value of a die is valid
    def isValidRoll(self, a, dieSize):
        if a > 0 and a <= dieSize: return True
        else: return False

    # Rolls a die of size n. is always valid but it uses random so...
    def rollDie(self, n):
        return random.randint(1,n)

    # Returns True if the prompt is complete. False otherwise.
    def isComplete(self):
        if len(self.results) == len(self.prompt): return True
        else: return False
