import json

with open('config/sr.json') as data_file:
    GlobalSyncDefinition = json.loads(data_file.read())
    
class Actor:
    def __init__(self, name, owner, actorType, strength, toughness, armor, reflexes, em, ef, physique, intelligence, empathy, sr, ats, atp, hitProfile, cmTicker):
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
        self.criticalMomentumTicker = cmTicker
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
