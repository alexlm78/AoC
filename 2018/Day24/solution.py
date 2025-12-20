import re
import copy

class Group:
    def __init__(self, id, army_type, units, hp, weaknesses, immunities, attack_damage, attack_type, initiative):
        self.id = id
        self.army_type = army_type
        self.units = units
        self.hp = hp
        self.weaknesses = weaknesses
        self.immunities = immunities
        self.attack_damage = attack_damage
        self.attack_type = attack_type
        self.initiative = initiative
        self.boost = 0
        
    @property
    def effective_power(self):
        return self.units * (self.attack_damage + self.boost)
        
    def calculate_damage(self, target):
        if self.attack_type in target.immunities:
            return 0
        damage = self.effective_power
        if self.attack_type in target.weaknesses:
            damage *= 2
        return damage
        
    def __repr__(self):
        return f"{self.army_type} {self.id}: {self.units} units, {self.hp} HP, {self.effective_power} EP"

def parse_input(filename):
    groups = []
    current_army = ""
    group_id_counter = 1
    
    with open(filename, "r") as f:
        lines = f.readlines()
        
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line == "Immune System:":
            current_army = "Immune System"
            group_id_counter = 1
            continue
        if line == "Infection:":
            current_army = "Infection"
            group_id_counter = 1
            continue
            
        # Parse group
        # 933 units each with 3691 hit points with an attack that does 37 cold damage at initiative 15
        # 3108 units each with 2902 hit points (weak to bludgeoning; immune to slashing, fire) with an attack that does 7 cold damage at initiative 13
        
        pattern = r"(\d+) units each with (\d+) hit points (\((.*?)\) )?with an attack that does (\d+) (\w+) damage at initiative (\d+)"
        match = re.match(pattern, line)
        
        if match:
            units = int(match.group(1))
            hp = int(match.group(2))
            attributes = match.group(4)
            attack_damage = int(match.group(5))
            attack_type = match.group(6)
            initiative = int(match.group(7))
            
            weaknesses = []
            immunities = []
            
            if attributes:
                parts = attributes.split(';')
                for part in parts:
                    part = part.strip()
                    if part.startswith("weak to"):
                        weaknesses = [x.strip() for x in part[8:].split(',')]
                    elif part.startswith("immune to"):
                        immunities = [x.strip() for x in part[10:].split(',')]
            
            groups.append(Group(group_id_counter, current_army, units, hp, weaknesses, immunities, attack_damage, attack_type, initiative))
            group_id_counter += 1
            
    return groups

def fight(groups):
    # Target Selection Phase
    groups.sort(key=lambda g: (-g.effective_power, -g.initiative))
    
    targets = {} # attacker -> target
    targeted = set()
    
    for attacker in groups:
        possible_targets = [g for g in groups if g.army_type != attacker.army_type and g not in targeted]
        if not possible_targets:
            continue
            
        # Select target that takes most damage, then largest EP, then highest initiative
        possible_targets.sort(key=lambda t: (-attacker.calculate_damage(t), -t.effective_power, -t.initiative))
        
        best_target = possible_targets[0]
        if attacker.calculate_damage(best_target) > 0:
            targets[attacker] = best_target
            targeted.add(best_target)
            
    # Attacking Phase
    groups.sort(key=lambda g: -g.initiative)
    
    total_units_killed = 0
    
    for attacker in groups:
        if attacker.units <= 0:
            continue
            
        target = targets.get(attacker)
        if target and target.units > 0:
            damage = attacker.calculate_damage(target)
            units_killed = damage // target.hp
            units_killed = min(units_killed, target.units)
            target.units -= units_killed
            total_units_killed += units_killed
            
    # Remove dead groups
    return [g for g in groups if g.units > 0], total_units_killed

def solve():
    initial_groups = parse_input("input.txt")
    
    # Part 1
    groups = copy.deepcopy(initial_groups)
    while True:
        immune_count = sum(1 for g in groups if g.army_type == "Immune System")
        infection_count = sum(1 for g in groups if g.army_type == "Infection")
        
        if immune_count == 0 or infection_count == 0:
            break
            
        groups, killed = fight(groups)
        if killed == 0: # Stalemate detection
            break
            
    remaining_units = sum(g.units for g in groups)
    print(f"Part 1 Result: {remaining_units}")
    
    # Part 2
    # Binary search or linear search for boost?
    # Linear search is safer for small values, but let's see.
    boost = 1
    while True:
        groups = copy.deepcopy(initial_groups)
        for g in groups:
            if g.army_type == "Immune System":
                g.boost = boost
                
        while True:
            immune_count = sum(1 for g in groups if g.army_type == "Immune System")
            infection_count = sum(1 for g in groups if g.army_type == "Infection")
            
            if immune_count == 0 or infection_count == 0:
                break
                
            groups, killed = fight(groups)
            if killed == 0: # Stalemate
                break
        
        immune_alive = sum(g.units for g in groups if g.army_type == "Immune System")
        infection_alive = sum(g.units for g in groups if g.army_type == "Infection")
        
        if infection_alive == 0 and immune_alive > 0:
            print(f"Part 2 Result: {immune_alive}")
            break
        
        boost += 1

if __name__ == "__main__":
    solve()
