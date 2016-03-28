import sys
import re
import json
import random
import Actor
import HitLocation
import Weapon
import Prompt

################ COMBAT STUFF



def importWeapon(name):
    for w in GlobalWeaponsList['data']:
        if w['name'] == name:
            return Weapon.Weapon(w['name'],w['weaponType'],w['weaponRange'],w['hands'],w['attackMode'],
                          w['damage'],w['ammo'],w['reload'],w['addStrFlag'],w['damageType'],
                          w['properties'],w['cost'])
    return Weapon.Weapon('!ERROR! ' + name,'N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A',
                  'N/A',['N/A'],'N/A')

# Returns True of obj.owner is owner, or if owner is a GM. False otherwise
# obj must have an owner value!
def canCommand(obj, owner):
    global combatOwner
    if owner in combatOwner or obj.owner == owner: return True
    else: return False

# Adds a prompt to the global prompt list that builds an arbitrary Evangelion
def buildArbitraryEva(owner):
    global currentPrompt
    currentPrompt = Prompt.Prompt("addActor(Actor.Actor(qqq, '"+owner+"','Evangelion Unit',qqq,qqq,\
                                  qqq,qqq,qqq,qqq,qqq,qqq,qqq,qqq,0,0,\
                                  [HitLocation.HitLocation(1,10,'head'),\
                                  HitLocation.HitLocation(11,20,'r arm'),\
                                  HitLocation.HitLocation(21,30,'l arm'),\
                                  HitLocation.HitLocation(31,70,'body'),\
                                  HitLocation.HitLocation(71,100,'legs')], 15))",
                                  ['Name', 'Strength', 'Toughness', 'Armor',
                                   'Reflexes', 'Eva Martial', 'Eva Firearms',
                                   'Physique', 'Intelligence', 'Empathy',
                                   'Synch Ratio'],
                                  ['s','i','i','i','i','i','i','i','i','i','i'],
                                  ['',10,10,5,50,80,80,40,40,40,50],
                                  False,owner)
    return 'Entering eva construction mode.'

def promptRespond(owner, response):
    global currentPrompt
    if currentPrompt != 0:
        if canCommand(currentPrompt, owner):
            if not currentPrompt.isComplete(): return currentPrompt.addResult(response)
            else: return 'Cannot respond, prompt is complete.'
        else: return 'You cannot respond to the prompt.'
    else: return 'Cannot respond, no prompt is active.'

def promptGive():
    global currentPrompt
    if currentPrompt != 0:
        if not currentPrompt.isComplete(): return currentPrompt.givePrompt()
        else:
            toExec = currentPrompt.givePrompt()
            response = str(exec(toExec))
            currentPrompt = 0
            return response + '\nPrompt reset.'
    else: return 'No prompt is active.'

def buildEva(name, owner):
    return Actor.Actor(name, owner, 'Production Eva', 3, 5, 3, 40, 68, 63, 24, 27, 27, 49, 2, 4,
                       [HitLocation.HitLocation(1,10,'head'),
                        HitLocation.HitLocation(11,20,'r arm'),
                        HitLocation.HitLocation(21,30,'l arm'),
                        HitLocation.HitLocation(31,70,'body'),
                        HitLocation.HitLocation(71,100,'legs')], 15)

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
            return ['Ending combat module. Combat channel has been deactivated. '+
                    'Combat owner has been reset.',originOfAction]
        else:
            return ['Combat is not running.',originOfAction]
    elif cmd[0] == 'start' and cmd[1] == 'combat':
        if combatMode:
            ownerStr = ''
            for o in combatOwner: ownerStr = ownerStr + o + ' or '
            return ['A combat is already running. ' + ownerStr.rstrip(' or ') +
                    ' must end it before a new combat can start.',
                    originOfAction]
        else:
            combatMode = True
            combatOutput = originOfAction
            combatOwner = [player]
            return ['Starting combat module. All combat output will be written to this channel. ' +
                    player +
                    ' is the GM of combat. Combat mode is set to automatic because manual mode ' +
                    'has not yet been implemented.', originOfAction]
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
            return ['Unrecognized condition (' + cmd[1] + ') or unhandled error (likely parsing).'
                    , originOfAction]
    elif cmd[0] == 'defwep':
        w = importWeapon(cmd[1])
        return [w.whoAmI() +'\n', originOfAction]
    elif request == 'help':
        return ['Adeptus Evangelion CombAsst module.\n' +
                'Current functions are:\n' +
                '?defcon [condition] (case sensitive) to define Eva conditions\n' +
                '?defwep [weapon] (case sensitive) to give information about weapons\n' +
                'Combat mode is currently ' + str(combatMode) +'\n' +
                'To start combat type ?start combat\n' +
                'To spawn an Eva for testing type ?spawn UnitName\n' +
                'To give an Eva a weapon, type ?givewep UnitName;WeaponName\n' +
                'To see who is where and what, type ?listactors\n' +
                'To test damage, type ?weapontest UnitName;WeaponName;target\n' +
                'To add a condition, type ?addcondition UnitName;hitLocation;condition;duration\n' +
                'To end an interval and clean up conditions, type ?endinterval'
                , originOfAction]
                #these all have ? in front since this is meant to be
                #plugged into a chatbot that feeds substr[1:] to this parser
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
        return [addCondition(args[0],player,args[1],args[2],int(args[3])),combatOutput]
    elif cmd[0] == 'endinterval':
        return [endInterval(),combatOutput]
    elif cmd[0] == 'buildEva':
        return [buildArbitraryEva(player),originOfAction]
    elif cmd[0] == 'p':
        if cmd[1] == 'give': return [promptGive(), originOfAction]
        else: return [promptRespond(player, cmd[1]), originOfAction]
    else:
        return ['Unrecognized command: ' + request + '. Type ?help for help.', originOfAction]

combatMode = False
combatOutput = -1
combatOwner = []
GlobalCriticalMomentumTicker = 15
actors = []
currentPrompt = 0

with open('config/conditions.json','r') as data_file:
    GloablConditionDefinitions = json.loads(data_file.read())
with open('config/weapons.json') as data_file:
    GlobalWeaponsList = json.loads(data_file.read())
with open('config/hit_effects.json') as data_file:
    GlobalHitEffects = json.loads(data_file.read())

errorSuppress = False #doesn't crash the module if something goes wrong.
#set to False to lose data and get tracebacks

print(parseInput('start combat', 'TESTPLAYER', 'TESTORIGIN')[0])

while combatMode:
    if errorSuppress:
        try: print(parseInput(input('INPUT COMMAND: '),'TESTPLAYER','TESTORIGIN')[0])
        except: print(sys.exc_info())
    else: print(parseInput(input('INPUT COMMAND: '),'TESTPLAYER','TESTORIGIN')[0])
