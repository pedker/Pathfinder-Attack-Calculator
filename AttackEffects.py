import random


'''

LIST OF IMPLEMENTED EFFECTS:

Flame -> Flaming Burst
Frost -> Icy Burst
Shock -> Shocking Burst

'''


class _Magic_Damage:
    def __init__(self):
        self.name = "ERROR"

    def calculateDamage(self, multiplier: int, threatened: bool, auto: bool) -> (int, int):
        while True:
            if auto:
                damage = random.randrange(1, 7)
                print(f"{self.name} Damage (1d6): {damage}")
            else:
                damage = _getIntegerInput(f"{self.name} Damage (1d6): ")
            if damage <= 0 or damage > 6:
                print("Invalid.")
                continue
            else:
                return (damage, damage)


class _Magic_Burst:
    def __init__(self):
        self.name = "ERROR"
        self.child = "ERROR"

    def calculateDamage(self, multiplier: int, threatened: bool, auto: bool) -> (int, int):
        damage = ( (eval(self.child))() ).calculateDamage(multiplier, threatened, auto)
        if not threatened:
            return damage
        elif threatened:
            while True:
                dice = multiplier - 1
                if dice > 3:
                    dice = 3
                if auto:
                    burstDamage = 0
                    for i in range(dice):
                        burstDamage += random.randrange(1, 11)
                    print(f"{self.name} Damage ({dice}d10): {burstDamage}")
                else:
                    burstDamage = _getIntegerInput(f"{self.name} Damage ({dice}d10): ")
                if burstDamage < dice or burstDamage > (dice*10):
                    print("Invalid.")
                    continue
                else: 
                    return (damage[0], burstDamage+damage[0])

                

class Flame(_Magic_Damage):
    def __init__(self):
        self.name = "Flame"

class Shock(_Magic_Damage):
    def __init__(self):
        self.name = "Shock"

class Frost(_Magic_Damage):
    def __init__(self):
        self.name = "Frost"

class ShockingBurst(_Magic_Burst):
    def __init__(self):
        self.name = "Shocking Burst"
        self.child = "Shock"

class FlamingBurst(_Magic_Burst):
    def __init__(self):
        self.name = "Flaming Burst"
        self.child = "Flame"

class IcyBurst(_Magic_Burst):
    def __init__(self):
        self.name = "Icy Burst"
        self.child = "Frost"



'''
--------------------------------------------------------------------------------------------
'''

def _getIntegerInput(text: str) -> int:
    while True:
        try:
            return int(input(text))
        except:
            print("Invalid.")
            continue
