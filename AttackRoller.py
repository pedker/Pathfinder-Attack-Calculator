from AttackEffects import *
from CyrusConstants import *
import random




def _startRolling() -> None:
    
    universalMod = _getIntegerInput("Universal Attack Roll Modifier: ")
    universalDamage = _getIntegerInput("Universal Damage Modifier: ")
    criticalRange = _getIntegerInput("Minimum Critical Threat: ")
    criticalMultiplier = _getIntegerInput("Critical Multiplier: x")
    attackLimit = _getIntegerInput("Number of Attacks: ")
    auto = bool(_getIntegerInput("Automated? (0 = NO): "))
    

    attackNumber = 0
    
    while attackNumber < attackLimit:
        attackNumber += 1
        threatened = False
        finalAttackRoll = 0
        finalConfirmRoll = 0
        effectDamage = 0
        criticalEffectDamage = 0

        print(f"\n********** ATTACK {attackNumber} **********")

        if auto:
            newRoll = random.randrange(1, 21)
            print(f"Attack Roll (1d20): {newRoll}")
        else:
            newRoll = _getIntegerInput("Attack Roll (1d20): ")
        if newRoll > 20 or newRoll <= 0:
            print("Invalid Roll.")
            continue

        elif newRoll == 20:
            finalAttackRoll = 30 + ATTACK_BONUS \
                              + universalMod
            finalConfirmRoll = _rollToConfirm(universalMod, criticalRange, auto)
            threatened = True

        elif newRoll == 1:
            finalAttackRoll = -9 + ATTACK_BONUS \
                              - NONCRITICAL_PENALTY \
                              + universalMod
        
        elif newRoll < criticalRange:
            finalAttackRoll = newRoll + ATTACK_BONUS \
                              - NONCRITICAL_PENALTY \
                              + universalMod
            
        elif newRoll < 20 and newRoll > 1:
            finalAttackRoll = newRoll + ATTACK_BONUS \
                              + universalMod
            finalConfirmRoll = _rollToConfirm(universalMod, criticalRange, auto)
            threatened = True

        else:
            continue

        
        if threatened:
            print(f"(Final Values: {finalAttackRoll} to hit, {finalConfirmRoll} to confirm)")
        else:
            print(f"(Final Value: {finalAttackRoll} to hit)")

        damage = _rollDamage(criticalMultiplier, threatened, universalDamage, auto)

        for effect in EFFECTS:
            effectDamageTuple = effect.calculateDamage(criticalMultiplier, threatened, auto)
            effectDamage += effectDamageTuple[0]
            criticalEffectDamage += effectDamageTuple[1]

        print("\n--- RESULTS ---")
        
        print(f"ATTACK ROLL: {finalAttackRoll}")
        if threatened:
            print(f"CONFIRMATION ROLL: {finalConfirmRoll}")
        print(f"WEAPON DAMAGE: {damage[0]}")
        if threatened:
            print(f"WEAPON CRITICAL DAMAGE: {damage[1]}")
        print(f"FULL DAMAGE: {damage[0] + effectDamage}")
        if threatened:
            print(f"FULL CRITICAL DAMAGE: {damage[1] + criticalEffectDamage}")

    print("\n------------------------------------------\n")
    _startRolling()

def _rollToConfirm(universalMod: int, criticalRange: int, auto: bool) -> int:
    while True:
        if auto:
            confirmRoll = random.randrange(1, 21)
            print(f"Roll to Confirm: {confirmRoll}")
        else:
            confirmRoll = _getIntegerInput("Roll to Confirm: ")
        
        if confirmRoll > 20 or confirmRoll <= 0:
            print("Invalid Roll.")
            continue
        
        elif confirmRoll == 20:
            return 30 + ATTACK_BONUS \
                   + universalMod + CONFIRM_BONUS

        elif confirmRoll == 1:
            return -9 + ATTACK_BONUS \
                   - NONCRITICAL_PENALTY \
                   + universalMod + CONFIRM_BONUS
            
        elif confirmRoll < 20 and confirmRoll > 1:
            return confirmRoll + ATTACK_BONUS \
                               + universalMod + CONFIRM_BONUS
        
        else:
            continue


def _rollDamage(multiplier: int, threatened: bool, universalDamage: int, auto: bool) -> (int, int):
    while True:
        if auto:
            damageRolls = random.randrange(1, int(WEAPON_DAMAGE[1])+1)
            print(f"Weapon Damage (1{WEAPON_DAMAGE}): {damageRolls}")
        else:
            damageRolls = _getIntegerInput(f"Weapon Damage (1{WEAPON_DAMAGE}): ")
        if damageRolls > int(WEAPON_DAMAGE[1]) or damageRolls <= 0:
            print("Invalid")
            continue
        if threatened:
            while True:
                if auto:
                    criticalDamageRolls = 0
                    for i in range(multiplier-1):
                        criticalDamageRolls += random.randrange(1, int(WEAPON_DAMAGE[1])+1) 
                    print(f"Critical Weapon Damage ({multiplier-1}{WEAPON_DAMAGE}): {criticalDamageRolls}")
                else:
                    criticalDamageRolls = _getIntegerInput(f"Critical Weapon Damage ({multiplier-1}{WEAPON_DAMAGE}): ")
                if criticalDamageRolls > ((multiplier-1)*int(WEAPON_DAMAGE[1])) or criticalDamageRolls < (multiplier-1):
                    print("Invalid.")
                    continue
                return ( (damageRolls + DAMAGE_BONUS + universalDamage + PRECISION_BONUS), \
                         criticalDamageRolls + damageRolls + (multiplier*DAMAGE_BONUS) + (multiplier*universalDamage) + PRECISION_BONUS )
        
        elif not threatened:
            return ( (damageRolls + DAMAGE_BONUS + universalDamage + PRECISION_BONUS), 0 )
                      


def _getIntegerInput(text: str) -> int:
    while True:
        try:
            return int(input(text))
        except:
            print("Invalid.")
            continue
        

if __name__ == '__main__':
    _startRolling()
