import re
import json
import random

################ COMBAT STUFF

class Actor:
    def __init__(self, name, owner, actorType, strength, toughness, armor, reflexes, em, ef, physique, intelligence, empathy, sr, ats, atp, hitProfile, cmModifier):
        global GlobalCriticalMomentumTicker
        self.name = name
        self.owner = owner
        self.actorType = actorType
        self.strength = strength
        self.toughness = toughness
        self.armor = armor
        self.reflexes = reflexes
        self.em = em
        self.ef = ef
        self.physique = physique
        self.intelligence = intelligence
        self.empathy = empathy
        self.sr = sr
        self.ats = ats
        self.atp = atp
        self.damage = 0
        self.criticalMomentum = 0
        self.criticalMomentumTicker = GlobalCriticalMomentumTicker + cmModifier
        self.hitProfile = hitProfile
        self.weapons = []
        self.maxATP = 0
        self.strain = 0
        self.recalculateSR()
    def defineSelf(self):
        return (self.name + ' is a ' + self.actorType
                +' owned by ' + self.owner
                +'. S: '+str(self.strength)
                +' T: '+str(self.toughness)
                +' Armor: '+str(self.armor)
                +' Ref: '+str(self.reflexes)
                +' Eva Martial: '+str(self.em)
                +' Eva Firearms: '+str(self.ef)
                +' Phys: '+str(self.physique)
                +' Int: '+str(self.intelligence)
                +' Emp: '+str(self.empathy)
                +' SR: '+str(self.sr)
                +' ATS: '+str(self.ats)
                +' ATP: '+str(self.atp)+'/'+str(self.maxATP)
                +' Damage: '+str(self.damage)
                +' CM: '+str(self.criticalMomentum)
                +'\nCurrently wielding: ' + self.readWeapons()
                +'\nCurrently suffering from:\n'+self.readConditions())
    def recalculateCM(self):
        self.criticalMomentum = int(self.damage/self.criticalMomentumTicker)
        return 'Critical momentum is now ' + str(self.criticalMomentum) +'.'
    def recalculateSR(self):
        for a in GlobalSyncDefinition['sync']:
            if self.sr >= a['min'] and self.sr <= a['max']:
                self.ats = a['ATS']
                self.maxATP = a['MaxATP']
                return 'Due to SR, set ATS/MaxATP to '+ str(self.ats) + '/' + str(self.maxATP)
    def addCondition(self, hitLocation, condition, duration):
        for l in self.hitProfile:
            if l.name == hitLocation:
                l.addCondition(condition, duration)
                return self.name + "'s " + hitLocation + ' is now ' + condition + ' for ' + str(duration) + ' intervals.'
        return 'Could not find hit location to add ' + condition + ' to.'
    def decrementConditions(self):
        outStr = 'Decrementing conditions for ' + self.name + '...\n'
        for l in self.hitProfile:
            status = l.decrementConditions()
            if status != '':
                outStr = outStr + status
        return outStr
    def readConditions(self):
        outStr = ''
        for l in self.hitProfile:
            if l.readConditions() != '':
                outStr = outStr + l.readConditions()
        return outStr
    def cleanupConditions(self):
        outStr = 'Cleaned conditions: '
        for l in self.hitProfile:
            outStr = outStr + str(l.cleanupConditions())
        return outStr
    def addWeapon(self, weapon):
        if weapon.weaponType != 'N/A':
            self.weapons.append(weapon)
            return 'Added ' + weapon.name + ' to ' + self.name
        else: return 'Cannot add: ' + weapon.name
    def readWeapons(self):
        outStr = ''
        for w in self.weapons:
            outStr = outStr + w.name + ', '
        if outStr != '':
            return outStr.rstrip(', ')
        else: return 'Nothing.'
    def attack(self, weaponName):
        for w in self.weapons:
            if w.name == weaponName:
                d = w.rollDamage()
                dam = d[0]
                if d[1]:
                    dam = dam + self.strength
                return [dam,d[2]]
        raise NameError(weaponName + ' could not be found.')
    def hit(self, damage):
        effectiveDamage = damage[0] - self.armor
        if effectiveDamage >= self.toughness:
            self.damage = self.damage + effectiveDamage
            return str(damage[0]) + ' of type ' + damage[1] + ' was rolled. ' + self.name + ' now has ' + str(self.damage) + ' damage. ' + self.recalculateCM() + ' This was a Critical Hit!'
        elif effectiveDamage <= 0:
            return str(damage[0]) + ' of type ' + damage[1] + ' was rolled. ' + self.name + ' is rocked by the hit, but it did nothing!'
        else:
            self.damage = self.damage + effectiveDamage
            return str(damage[0]) + ' of type ' + damage[1] + ' was rolled. ' + self.name + ' now has ' + str(self.damage) + ' damage. ' + self.recalculateCM() + ' This was a Glancing Hit!'

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
        

class Weapon:
    def __init__(self, name, weaponType, weaponRange, hands, attackMode, damage, ammo, reload, addStrFlag, damageType, properties, cost):
        self.name = name
        self.weaponType = weaponType #Pistol, Basic, Heavy, or Melee
        self.weaponRange = weaponRange #range in sectors. 0 for sector, E for engagement.
        self.hands = hands #1 or 2
        self.attackMode = attackMode #Single and/or Burst(X/Y)
        self.damage = damage #damage in form of XdY+Z
        self.ammo = ammo #amount of ammo carried
        self.reload = reload #cost to reload
        self.addStrFlag = addStrFlag #True or False
        self.damageType = damageType #K, E, or S
        self.properties = properties #comma list of properties
        self.cost = cost #integer of Req required
        self.currentAmmo = ammo
    def whoAmI(self):
        return ('This is a '+self.name
                +' of type '+self.weaponType
                +'. Range: '+str(self.weaponRange)
                +' hands: '+str(self.hands)
                +'. It can be fired as '+str(self.attackMode)
                +'. It has '+str(self.ammo)+' ammmunition'
                +'. It takes '+str(self.reload)+' stamina to reload'
                +'. '+self.fireWeapon()
                +'\n'+self.readProperties())
    def readProperties(self):
        retStr = ''
        for p in self.properties:
            try:
                pDef = GlobalWeaponPropertyList[p.split('(')[0]]
                if 'XXX' in pDef:
                    pDef = re.sub('XXX', p.split('(')[1].rstrip(')'), pDef)
            except KeyError:
                pDef = 'malformed/undefined property name!'
            retStr = retStr + p + ': ' + pDef + '\n'
        if retStr == '':
            return 'This weapon has no properties.'
        else:
            return retStr.rstrip('\n')
    def fireWeapon(self):
        strAdd = ''
        if self.addStrFlag:
            strAdd = '+S '
        return 'The weapon deals ' + self.damage + strAdd + ' ' + self.damageType + '-type damage.'
    def rollDamage(self):
        damage = 0
        try:
            damStr = self.damage.split('+')
            damage = 0 + int(damStr[1])
        except IndexError:
            damStr = self.damage
        diceToRoll = int(damStr[0].split('d')[0])
        while diceToRoll > 0:
            damage = damage + random.randint(1,int(damStr[0].split('d')[1]))
            diceToRoll = diceToRoll - 1
        return [damage, self.addStrFlag, self.damageType]

def importWeapon(name):
    for w in GlobalWeaponsList['data']:
        if w['name'] == name:
            return Weapon(w['name'],w['weaponType'],w['weaponRange'],w['hands'],w['attackMode'],w['damage'],w['ammo'],w['reload'],w['addStrFlag'],w['damageType'],w['properties'],w['cost'])
    return Weapon('!ERROR! ' + name,'N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A',['N/A'],'N/A')

def buildEva(name, owner):
    return Actor(name, owner, 'Production Eva', 3, 5, 3, 40, 68, 63, 24, 27, 27, 49, 2, 4, [HitLocation(1,10,'head'),HitLocation(11,20,'r arm'),HitLocation(21,30,'l arm'),HitLocation(31,70,'body'),HitLocation(71,100,'legs')], 0)

def addActor(actor):
    global actors
    actors.append(actor)
    return 'Added ' + actor.name + ' to the battlefield.'

def addCondition(actorName, requestGiver, bodyPart, condition, duration):
    global actors
    for a in actors:
        if a.name == actorName:
            if a.owner != requestGiver:
                return 'You do not own ' + actorName + ' and therefore cannot add a condition.'
            return a.addCondition(bodyPart, condition, duration)
    return 'Could not find ' + actorName

def addWeapon(actorName, requestGiver, weapon):
    global actors
    for a in actors:
        if a.name == actorName:
            if a.owner != requestGiver:
                return 'You do not own ' + actorName + ' and therefore cannot add a weapon to it.'
            w = importWeapon(weapon)
            a.addWeapon(w)
            return 'Added ' + w.name + ' to ' + a.name
    return 'Could not find ' + actorName

def fireWeapon(actorName, requestGiver, weapon, target):
    global actors
    damage = ''
    for a in actors:
        if a.name == actorName:
            if a.owner != requestGiver:
                return 'You do not own ' + actorName + ' and therefore cannot attack with it.'
            #try:
            damage = a.attack(weapon)
            #except NameError:
            #    return 'NameError. Check to make sure you spelled the weapon name right and that the actor has the weapon.'
    for a in actors:
        if a.name == target:
            return a.hit(damage)
    return 'Something went wrong and nothing was done.'

def listActors():
    outStr = ''
    global actors
    for a in actors:
        outStr = outStr + a.defineSelf() + '\n'
    return outStr.rstrip('\n')

def endInterval():
    outStr = ''
    global actors
    for a in actors:
        outStr = outStr + a.decrementConditions()
        outStr = outStr + a.cleanupConditions()
    return outStr

def parseInput(request, player, originOfAction):
    global combatMode
    global combatOutput
    global combatOwner
    global actors

    cmd = request.split(' ',1)
    
    if len(cmd) == 1:
        cmd.append('')

    if cmd[0] == 'end' and cmd[1] == 'combat':
        if combatMode:
            combatMode = False
            combatOutput  = -1
            combatOwner = []
            actors = []
            return ['Ending combat module. Combat channel has been deactivated. Combat owner has been reset.',originOfAction]
        else:
            return ['Combat is not running.',originOfAction]
    elif cmd[0] == 'start' and cmd[1] == 'combat':
        if combatMode:
            return ['A combat is already running. ' + combatOwner + ' is the owner of combat and must end it before a new combat can start.',originOfAction]
        else:
            combatMode = True
            combatOutput = originOfAction
            combatOwner = player
            return ['Starting combat module. All combat output will be written to this channel.\
' + player + ' is the GM of combat. Combat mode is set to automatic because manual mode has not yet been implemented.', originOfAction]
    elif cmd[0] == 'testCombatResponse':
        if combatMode:
            return ['Testing fixed output channel.',combatOutput]
        else:
            return ['Combat is not running.',originOfAction]
    elif cmd[0] == 'defcon':
        try:
            retStr = ''
            retStr = retStr + (cmd[1] + ': ' + GloablConditionDefinitions[cmd[1]][0])
            gainedAgain = GloablConditionDefinitions[cmd[1]][1]
            if gainedAgain != '':
                retStr = retStr + '\nWhen gained again: ' + gainedAgain
            return [retStr, originOfAction]
        except:
            return ['Unrecognized condition (' + cmd[1] + ') or unhandled error (likely parsing).', originOfAction]
    elif cmd[0] == 'defwep':
        w = importWeapon(cmd[1])
        return [w.whoAmI() +'\n', originOfAction]
    elif request == 'help':
        return ['Adeptus Evangelion CombAsst module.\n\
Current functions are:\n\
?defcon [condition] (case sensitive) to define Eva conditions\n\
?defwep [weapon] (case sensitive) to give information about weapons\n\
Combat mode is currently ' + str(combatMode) +'\n\
To start combat type ?start combat\n\
To spawn an Eva for testing type ?spawn UnitName\n\
To give an Eva a weapon, type ?givewep UnitName;WeaponName\n\
To see who is where and what, type ?listactors\n\
To test damage, type ?weapontest UnitName;WeaponName;target\n\
To add a condition, type ?addcondition UnitName;hitLocation;condition;duration\n\
To end an interval and clean up conditions, type ?endinterval'
                , originOfAction] #these all have ? in front since this is meant to be plugged into a chatbot that feeds substr[1:] to this parser
    elif cmd[0] == 'spawn':
        return [addActor(buildEva(cmd[1],player)),combatOutput]
    elif cmd[0] == 'givewep':
        args = cmd[1].split(';')
        return [addWeapon(args[0],player,args[1]),combatOutput]
    elif cmd[0] == 'listactors':
        return [listActors(),combatOutput]
    elif cmd[0] == 'weapontest':
        args = cmd[1].split(';')
        return [fireWeapon(args[0],player,args[1],args[2]),combatOutput]
    elif cmd[0] == 'addcondition':
        args = cmd[1].split(';')
        return[addCondition(args[0],player,args[1],args[2],int(args[3])),combatOutput]
    elif cmd[0] == 'endinterval':
        return[endInterval(),combatOutput]
    else:
        return ['Unrecognized command: ' + request + '. Type ?help for help.', originOfAction]

combatMode = False
combatOutput = -1
combatOwner = []
GlobalCriticalMomentumTicker = 15
actors = []

with open('conditions.json','r') as data_file:
    GloablConditionDefinitions = json.loads(data_file.read())
with open('weapons.json') as data_file:
    GlobalWeaponsList = json.loads(data_file.read())
with open('weaponProperties.json') as data_file:
    GlobalWeaponPropertyList = json.loads(data_file.read())
with open('sr.json') as data_file:
    GlobalSyncDefinition = json.loads(data_file.read())
with open('hit_effects.json') as data_file:
    GlobalHitEffects = json.loads(data_file.read())

print(parseInput('start combat', 'TESTPLAYER', 'TESTORIGIN')[0])

while combatMode:
    print(parseInput(input('INPUT COMMAND: '),'Player','Origin')[0])
