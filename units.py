import os
import pygame as pg
from random import randint

class __UnitImages:
    location = os.path.join("Images", "Units")
    INF_1 = pg.image.load(os.path.join(location, "infantry1.png"))
    INF_2 = pg.image.load(os.path.join(location, "infantry2.png"))
    SNP_1 = pg.image.load(os.path.join(location, "sniper1.png"))
    SNP_2 = pg.image.load(os.path.join(location, "sniper2.png"))
    BZK_1 = pg.image.load(os.path.join(location, "bazooka1.png"))
    BZK_2 = pg.image.load(os.path.join(location, "bazooka2.png"))
    MRT_1 = pg.image.load(os.path.join(location, "mortar1.png"))
    MRT_2 = pg.image.load(os.path.join(location, "mortar2.png"))
    BKR_1 = pg.image.load(os.path.join(location, "biker1.png"))
    BKR_2 = pg.image.load(os.path.join(location, "biker2.png"))
    JEP_1 = pg.image.load(os.path.join(location, "jeep1.png"))
    JEP_2 = pg.image.load(os.path.join(location, "jeep2.png"))
    LTK_1 = pg.image.load(os.path.join(location, "lighttank1.png"))
    LTK_2 = pg.image.load(os.path.join(location, "lighttank2.png"))
    TNK_1 = pg.image.load(os.path.join(location, "tank1.png"))
    TNK_2 = pg.image.load(os.path.join(location, "tank2.png"))
    HVT_1 = pg.image.load(os.path.join(location, "heavytank1.png"))
    HVT_2 = pg.image.load(os.path.join(location, "heavytank2.png"))
    FMT_1 = pg.image.load(os.path.join(location, "flamethrower1.png"))
    FMT_2 = pg.image.load(os.path.join(location, "flamethrower2.png"))
    ATY_1 = pg.image.load(os.path.join(location, "artillery1.png"))
    ATY_2 = pg.image.load(os.path.join(location, "artillery2.png"))
    RKL_1 = pg.image.load(os.path.join(location, "rocketlauncher1.png"))
    RKL_2 = pg.image.load(os.path.join(location, "rocketlauncher2.png"))

class Unit:
    moved = 0
    attacked = True
    health = 100

    def __init__(self, type, team, movement, speed, capture, defense, armor, ammunition, attack, maxrange=1, minrange=1):
        #IDENTIFIER
        self.type = type
        self.team = team
        #MOVEMENT PROPETIES
        self.moved = speed
        self.movement = movement
        self.speed = speed
        #COMBAT PROPETIES
        self.capture = capture
        self.defense = defense
        self.armor = armor
        self.ammunition = ammunition
        self.attack = attack
        self.maxrange = maxrange
        self.minrange = minrange

    def attack_value(self, range=5):
        return (self.health / 100) * (self.attack * range + randint(0, range))

    def defense_value(self, terrain):
        defense = ((100 - (self.health / 10 * terrain.defense + self.defense)) / 50)
        if defense <= 0:
            return 0
        return defense

    def getting_attacked(self, attacking, terrain):
        damage = attacking.attack_value() *  self.defense_value(terrain)
        if attacking.ammunition == "Bullets":
            self.health -= damage / self.armor
        elif attacking.ammunition == "Piercing":
            self.health -= damage / (1 + self.armor / 10)
        elif attacking.ammunition == "Explosives":
            self.health -= damage / (self.armor / 2)
        else:
            self.health -= damage
    
    def can_attack(self, turn_team, target, terrain):
        return target is not None and not self.attacked and self.team == turn_team and (self.team != target.team or self.team != terrain.team)

    def can_capture(self, terrain):
        return self.capture and not self.attacked and terrain.capturable and terrain.team != self.team

    def in_attack_range(self, distance):
        return distance >= self.minrange and distance <= self.maxrange

    def enough_move_left(self, terrain):
        return terrain.can_move_on(self.movement) and terrain.transports[self.movement] + self.moved <= self.speed

    def has_moved(self, terrain):
        if self.minrange != 1:
            self.attacked = True
        self.moved += terrain.transports[self.movement]

    def has_attacked(self):
        self.moved = self.speed
        self.attacked = True

    def heal_up(self):
        self.health += 10
        if self.health > 100:
            self.health = 100

    def reset_actions(self):
        self.moved = 0
        self.attacked = False

def get_units():
    return ["Infantry", "Sniper", "Bazooka", "Mortar", "Biker", "Jeep", "Light tank", "Tank", "Heavy tank", "Flamethrower", "Artilery", "Rocket"]

def get_prices():
    return {0: 10, 1: 40, 2: 30, 3: 60, 4: 50, 5: 80, 6: 80, 7: 100, 8: 150, 9: 110, 10: 90, 11: 130, 12: 0, 13: 0, 14: 0, 15: 0}

def spawn_infantry(team):
    unit_types = get_units()
    return Unit(unit_types[0], team, "Foot", 3, True, 7, 0.9, "Bullets", 5)

def spawn_sniper(team):
    unit_types = get_units()
    return Unit(unit_types[1], team, "Foot", 2, True, 8, 0.8, "Bullets", 7, 2)

def spawn_bazooka(team):
    unit_types = get_units()
    return Unit(unit_types[2], team, "Foot", 3, True, 6, 0.9, "Piercing", 6)

def spawn_mortar(team):
    unit_types = get_units()
    return Unit(unit_types[3], team, "Foot", 2, False, 6, 0.9, "Explosives", 5, 3, 2)

def spawn_biker(team):
    unit_types = get_units()
    return Unit(unit_types[4], team, "Wheels", 5, True, 6, 1, "Bullets", 6)

def spawn_jeep(team):
    unit_types = get_units()
    return Unit(unit_types[5], team, "Wheels", 7, False, 4, 1.4, "Explosives", 4)
    
def spawn_lighttank(team):
    unit_types = get_units()
    return Unit(unit_types[6], team, "Wheels", 6, False, 4, 1.8, "Bullets", 7)

def spawn_tank(team):
    unit_types = get_units()
    return Unit(unit_types[7], team, "Tracks", 5, True, 4, 2.4, "Piercing", 7)

def spawn_heavytank(team):
    unit_types = get_units()
    return Unit(unit_types[8], team, "Tracks", 4, True, 4, 2.8, "Piercing", 9)

def spawn_flamethrower(team):
    unit_types = get_units()
    return Unit(unit_types[9], team, "Tracks", 5, True, 2, 2.6, "Explosives", 6)

def spawn_artillery(team):
    unit_types = get_units()
    return Unit(unit_types[10], team, "Tracks", 5, True, 5, 2.2, "Piercing", 8, 4, 2)

def spawn_rocketlauncher(team):
    unit_types = get_units()
    return Unit(unit_types[11], team, "Wheels", 5, True, 6, 1.6, "Explosives", 7, 5, 2)

def spawn_unit(team, type):
    unit_types = get_units()
    if type == unit_types[0]:
        return spawn_infantry(team)
    elif type == unit_types[1]:
        return spawn_sniper(team)
    elif type == unit_types[2]:
        return spawn_bazooka(team)
    elif type == unit_types[3]:
        return spawn_mortar(team)
    elif type == unit_types[4]:
        return spawn_biker(team)
    elif type == unit_types[5]:
        return spawn_jeep(team)
    elif type == unit_types[6]:
        return spawn_lighttank(team)
    elif type == unit_types[7]:
        return spawn_tank(team)
    elif type == unit_types[8]:
        return spawn_heavytank(team)
    elif type == unit_types[9]:
        return spawn_flamethrower(team)
    elif type == unit_types[10]:
        return spawn_artillery(team)
    elif type == unit_types[11]:
        return spawn_rocketlauncher(team)

def __block_translator(onblock, window, onwindow):
    images = __UnitImages()
    if onblock.identifier == 'H':
        if onblock.team == 'Red':
            window.blit(images.INF_1, onwindow)
            return spawn_infantry('Red')
        elif onblock.team == 'Blue':
            window.blit(images.INF_2, onwindow)
            return spawn_infantry('Blue')
    return None

def block_draw(onblock, window, onwindow):
    images = __UnitImages()
    unit_types = get_units()
    if onblock.team == "Red":
        if onblock.type == unit_types[0]:
            window.blit(images.INF_1, onwindow)
        elif onblock.type == unit_types[1]:
            window.blit(images.SNP_1, onwindow)
        elif onblock.type == unit_types[2]:
            window.blit(images.BZK_1, onwindow)
        elif onblock.type == unit_types[3]:
            window.blit(images.MRT_1, onwindow)
        elif onblock.type == unit_types[4]:
            window.blit(images.BKR_1, onwindow)
        elif onblock.type == unit_types[5]:
            window.blit(images.JEP_1, onwindow)
        elif onblock.type == unit_types[6]:
            window.blit(images.LTK_1, onwindow)
        elif onblock.type == unit_types[7]:
            window.blit(images.TNK_1, onwindow)
        elif onblock.type == unit_types[8]:
            window.blit(images.HVT_1, onwindow)
        elif onblock.type == unit_types[9]:
            window.blit(images.FMT_1, onwindow)
        elif onblock.type == unit_types[10]:
            window.blit(images.ATY_1, onwindow)
        elif onblock.type == unit_types[11]:
            window.blit(images.RKL_1, onwindow)
    elif onblock.team == "Blue":
        if onblock.type == unit_types[0]:
            window.blit(images.INF_2, onwindow)
        elif onblock.type == unit_types[1]:
            window.blit(images.SNP_2, onwindow)
        elif onblock.type == unit_types[2]:
            window.blit(images.BZK_2, onwindow)
        elif onblock.type == unit_types[3]:
            window.blit(images.MRT_2, onwindow)
        elif onblock.type == unit_types[4]:
            window.blit(images.BKR_2, onwindow)
        elif onblock.type == unit_types[5]:
            window.blit(images.JEP_2, onwindow)
        elif onblock.type == unit_types[6]:
            window.blit(images.LTK_2, onwindow)
        elif onblock.type == unit_types[7]:
            window.blit(images.TNK_2, onwindow)
        elif onblock.type == unit_types[8]:
            window.blit(images.HVT_2, onwindow)
        elif onblock.type == unit_types[9]:
            window.blit(images.FMT_2, onwindow)
        elif onblock.type == unit_types[10]:
            window.blit(images.ATY_2, onwindow)
        elif onblock.type == unit_types[11]:
            window.blit(images.RKL_2, onwindow)

def drawadd(window, BLOCK, terrainmap, xrn, yrn):
    unitmap = [[None  for i in range(yrn)] for j in range(xrn)]
    row = 0
    for xon in range(0, xrn * BLOCK, BLOCK):
        column = 0
        for yon in range(0, yrn * BLOCK, BLOCK):
            unitmap[row][column] = __block_translator(terrainmap[row][column], window, (xon, yon))
            column += 1
        row += 1
    return unitmap