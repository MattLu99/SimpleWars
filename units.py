import os
import pygame as pg
from random import randint

class __UnitImages:
    """Class for statically storing the location of unit images."""
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
    """Class for representing a unit and handling any actions taken on it."""
    moved = 0
    attacked = True
    health = 100

    def __init__(self, type: str, team: str, movement: str, speed: int, capture: bool, 
                 defense: float, armor: float, ammunition: str, attack: float, maxrange: int = 1, minrange: int = 1):
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

    def attack_value(self, range: float = 5) -> float:
        """Returns the amount of damage the unit deals, with small randomness."""
        return (self.health / 100) * (self.attack * range + randint(0, range))

    def defense_value(self, terrain: object) -> float:
        """Returns with the defense of the unit based on terrain."""
        defense = ((100 - (self.health / 10 * terrain.defense + self.defense)) / 50)
        if defense <= 0:
            return 0
        return defense

    def getting_attacked(self, attacking: object, terrain: object) -> None:
        """Takes the attacking unit and terrain as parameters and handles how much damage the unit takes."""
        damage = attacking.attack_value() *  self.defense_value(terrain)
        if attacking.ammunition == "Bullets":
            self.health -= damage / self.armor
        elif attacking.ammunition == "Piercing":
            self.health -= damage / (1 + self.armor / 10)
        elif attacking.ammunition == "Explosives":
            self.health -= damage / (self.armor / 2)
        else:
            self.health -= damage
    
    def can_attack(self, turn_team: str, target: object, terrain: object) -> bool:
        """Checks if a unit can attack in the current turn and returns it in a boolean."""
        return target is not None and not self.attacked and self.team == turn_team and (self.team != target.team or self.team != terrain.team)

    def can_capture(self, terrain: object) -> bool:
        """Checks if a unit can capture the terrain it is standing and returns it in a boolean."""
        return self.capture and not self.attacked and terrain.capturable and terrain.team != self.team

    def in_attack_range(self, distance: int) -> bool:
        """Checks if the selection is in attack range and returns it in a boolean."""
        return distance >= self.minrange and distance <= self.maxrange

    def enough_moves_left(self, terrain: object) -> bool:
        """Checks if the unit would make a valid move and has enough moves left, then returns this in a boolean."""
        return terrain.can_move_on(self.movement) and terrain.transports[self.movement] + self.moved <= self.speed

    def has_moved(self, terrain: object) -> None:
        """Adds how much a unit has moved and removes its attack if its an indirect attacking unit."""
        if self.minrange != 1:
            self.attacked = True
        self.moved += terrain.transports[self.movement]

    def has_attacked(self) -> None:
        """Locks all further actions after a unit has attacked."""
        self.moved = self.speed
        self.attacked = True

    def heal_up(self) -> None:
        """Restores 10 points of health to a unit and ensures there is no overflow."""
        self.health += 10
        if self.health > 100:
            self.health = 100

    def reset_actions(self) -> None:
        """Resets the actions of a unit, in preparation for a new turn."""
        self.moved = 0
        self.attacked = False

def get_units() -> list:
    """Function for statically storing the names of all of the units."""
    return ["Gunner", "Sniper", "Bazooka", "Mortar", "Biker", "Jeep", "Light tank", "Tank", "Heavy tank", "Flamethrower", "Artilery", "Rocket"]

def get_prices() -> list:
    """Function for statically storing the prices of all of the units."""
    return {0: 10, 1: 40, 2: 30, 3: 70, 4: 50, 5: 80, 6: 80, 7: 100, 8: 160, 9: 120, 10: 130, 11: 180, 12: 0, 13: 0, 14: 0, 15: 0}

def spawn_unit(team: str, type: str = "Gunner") -> Unit:
    """Gets the requested unit and returns with it for the given team."""
    unit_types = get_units()
    if type == unit_types[0]:
        # UNIT 1 - GUNNER
        return Unit(type, team, "Foot", 3, True, 7, 0.9, "Bullets", 5)
    elif type == unit_types[1]:
        # UNIT 2 - SNIPER
        return Unit(type, team, "Foot", 2, True, 8, 0.8, "Bullets", 7, 2)
    elif type == unit_types[2]:
        # UNIT 3 - BAZOOKA
        return Unit(type, team, "Foot", 3, True, 7, 1, "Piercing", 6)
    elif type == unit_types[3]:
        # UNIT 4 - MORTAR
        return Unit(type, team, "Foot", 2, False, 7, 0.8, "Explosives", 5, 3, 2)
    elif type == unit_types[4]:
        # UNIT 5 - BIKER
        return Unit(type, team, "Wheels", 5, True, 6, 1, "Bullets", 5)
    elif type == unit_types[5]:
        # UNIT 6 - JEEP
        return Unit(type, team, "Wheels", 7, False, 4, 1.4, "Explosives", 4)
    elif type == unit_types[6]:
        # UNIT 7 - LIGHT TANK
        return Unit(type, team, "Wheels", 6, False, 4, 1.8, "Bullets", 7)
    elif type == unit_types[7]:
        # UNIT 8 - TANK
        return Unit(type, team, "Tracks", 5, True, 4, 2.4, "Piercing", 7)
    elif type == unit_types[8]:
        # UNIT 9 - HEAVY TANK
        return Unit(type, team, "Tracks", 4, True, 4, 2.8, "Piercing", 9)
    elif type == unit_types[9]:
        # UNIT 10 - FLAMETHROWER
        return Unit(type, team, "Tracks", 5, True, 2, 2.4, "Explosives", 6)
    elif type == unit_types[10]:
        # UNIT 11 - ARTILERY
        return Unit(type, team, "Tracks", 5, True, 5, 2.2, "Piercing", 8, 4, 2)
    elif type == unit_types[11]:
        # UNIT 12 - ROCKET LAUNCHER
        return Unit(type, team, "Wheels", 5, True, 6, 1.6, "Explosives", 7, 5, 2)

def __block_translator(onblock: object, window: object, onwindow: tuple) -> Unit:
    """Private Terrain handler function that automatically places Gunner units on both HQs."""
    images = __UnitImages()
    if onblock.identifier == 'H':
        if onblock.team == 'Red':
            window.blit(images.INF_1, onwindow)
            return spawn_unit('Red')
        elif onblock.team == 'Blue':
            window.blit(images.INF_2, onwindow)
            return spawn_unit('Blue')
    return None

def block_draw(onblock: Unit, window: object, onwindow: tuple) -> None:
    """Function that takes in placement data and draws the unit on the game window."""
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

def drawadd(window: object, BLOCK: int, terrainmap: list[list], xrn: int, yrn: int) -> list[list]:
    """Function that initializes the basic unit map and adds the default units to it."""
    unitmap = [[None  for i in range(yrn)] for j in range(xrn)]
    row = 0
    for xon in range(0, xrn * BLOCK, BLOCK):
        column = 0
        for yon in range(0, yrn * BLOCK, BLOCK):
            unitmap[row][column] = __block_translator(terrainmap[row][column], window, (xon, yon))
            column += 1
        row += 1
    return unitmap