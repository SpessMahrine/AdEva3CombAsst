import json
import random
import re

with open('config/weaponProperties.json') as data_file:
    GlobalWeaponPropertyList = json.loads(data_file.read())

class Weapon:
    def __init__(self, name, weaponType, weaponRange, hands, attackMode, damage, ammo,
                 reload, addStrFlag, damageType, properties, cost):
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
        return ('The weapon deals ' + self.damage + strAdd + ' '
                + self.damageType + '-type damage.')
    def rollDamage(self):
        damage = 0
        try:
            damStr = self.damage.split('+')
            damage = 0 + int(damStr[1])
        except IndexError:
            damStr = [self.damage]
        diceToRoll = int(damStr[0].split('d')[0])
        while diceToRoll > 0:
            damage = damage + random.randint(1,int(damStr[0].split('d')[1]))
            diceToRoll = diceToRoll - 1
        return [damage, self.addStrFlag, self.damageType]
