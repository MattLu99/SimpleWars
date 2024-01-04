import os
import pygame as pg

class __TerrainImages:
    """Class for statically storing the location of terrain images."""
    location = os.path.join("Images", "Terrains")
    PLAINS = pg.image.load(os.path.join(location, "plains.png"))
    SWAMP = pg.image.load(os.path.join(location, "swamp.png"))
    FOREST = pg.image.load(os.path.join(location, "forest.png"))
    MOUNTAIN = pg.image.load(os.path.join(location, "mountain.png"))
    FRESHWATER = pg.image.load(os.path.join(location, "freshwater.png"))
    SALTWATER = pg.image.load(os.path.join(location, "saltwater.png"))
    ROAD_NORTHSOUTH = pg.image.load(os.path.join(location, "roadns.png"))
    ROAD_WESTEAST = pg.image.load(os.path.join(location, "roadwe.png"))
    ROAD_NORTHEAST = pg.image.load(os.path.join(location, "roadne.png"))
    ROAD_NORTHWEST = pg.image.load(os.path.join(location, "roadnw.png"))
    ROAD_SOUTHEAST = pg.image.load(os.path.join(location, "roadse.png"))
    ROAD_SOUTHWEST = pg.image.load(os.path.join(location, "roadsw.png"))
    ROAD_NORTHINTERSECTION = pg.image.load(os.path.join(location, "roadni.png"))
    ROAD_EASTINTERSECTION = pg.image.load(os.path.join(location, "roadei.png"))
    ROAD_SOUTHINTERSECTION = pg.image.load(os.path.join(location, "roadsi.png"))
    ROAD_WESTINTERSECTION = pg.image.load(os.path.join(location, "roadwi.png"))
    ROAD_FULLINTERSECTION = pg.image.load(os.path.join(location, "roadci.png"))
    BRIDGE_FRESH_NORTHSOUTH = pg.image.load(os.path.join(location, "bridgefns.png"))
    BRIDGE_FRESH_WESTEAST = pg.image.load(os.path.join(location, "bridgefwe.png"))
    BRIDGE_SALT_NORTHSOUTH = pg.image.load(os.path.join(location, "bridgesns.png"))
    BRIDGE_SALT_WESTEAST = pg.image.load(os.path.join(location, "bridgeswe.png"))
    CITY_NEUTRAL = pg.image.load(os.path.join(location, "cityneutral.png"))
    CITY_1 = pg.image.load(os.path.join(location, "city1.png"))
    CITY_2 = pg.image.load(os.path.join(location, "city2.png"))
    WORKSHOP_NEUTRAL = pg.image.load(os.path.join(location, "workshopneutral.png"))
    WORKSHOP_1 = pg.image.load(os.path.join(location, "workshop1.png"))
    WORKSHOP_2 = pg.image.load(os.path.join(location, "workshop2.png"))
    HQ_1 = pg.image.load(os.path.join(location, "hq1.png"))
    HQ_2 = pg.image.load(os.path.join(location, "hq2.png"))
    DEBRIS = pg.image.load(os.path.join(location, "debris.png"))
    ABANDONED_CITY = pg.image.load(os.path.join(location, "abandonedcity.png"))

class Terrain:
    """Class for representing all terrain and handling any actions taken on them."""
    def __init__(self, identifier: str, type: str, defense: float, transports: dict, capturable: bool, team: str, health: float = 200):
        self.identifier = identifier
        self.type = type
        self.defense = defense
        self.transports = transports
        self.capturable = capturable
        self.default_health = health
        self.health = health
        self.team = team

    def can_move_on(self, movement: str) -> bool:
        """Function that checks if a certain movment type can move on the given terrain."""
        return self.transports[movement] > 0

    def remaining_health(self) -> float:
        """Calculates remaining terrain capture health."""
        return round(((self.default_health - self.health) / 2), 2)

    def getting_captured(self, unit: object) -> bool:
        """Advances capture of terrain depending on capturing unit's remaining health. 
        Returns true if capture is completed, returns false otherwise."""
        self.health -= unit.health
        if self.health <= 0:
            self.health = self.default_health
            self.team = unit.team
            return True
        return False

    def all_one_movement(self) -> bool:
        """Returns true if all movement types cost 1 on itself."""
        return all(value == 1 for value in self.transports.values())

    def is_team_workshop(self, team: str) -> bool:
        """Returns true if it is a workshop and the correct team is using it."""
        return self.identifier == 'W' and self.team == team

    def is_a_hq(self) -> bool:
        """Returns true if it's a HQ."""
        return self.identifier == 'H'

def __complete_intersection(rawmap: list[list], row: int, column: int, connectors: list) -> bool:
    """Checks to see if the current tile is completely surrounded by road connecting terrain."""
    return rawmap[column - 1][row].upper() in connectors and rawmap[column][row - 1].upper() in connectors and rawmap[column + 1][row].upper() in connectors and rawmap[column][row + 1].upper() in connectors

def __north_intersection(rawmap: list[list], row: int, column: int, connectors: list) -> bool:
    """Checks to see if the current tile is surrounded by road connecting terrain, except on its south side."""
    return rawmap[column - 1][row].upper() in connectors and rawmap[column][row + 1].upper() in connectors and rawmap[column][row - 1].upper() in connectors

def __east_intersection(rawmap: list[list], row: int, column: int, connectors: list) -> bool:
    """Checks to see if the current tile is surrounded by road connecting terrain, except on its west side."""
    return rawmap[column][row - 1].upper() in connectors and rawmap[column + 1][row].upper() in connectors and rawmap[column - 1][row].upper() in connectors

def __south_intersection(rawmap: list[list], row: int, column: int, connectors: list) -> bool:
    """Checks to see if the current tile is surrounded by road connecting terrain, except on its north side."""
    return rawmap[column + 1][row].upper() in connectors and rawmap[column][row + 1].upper() in connectors and rawmap[column][row - 1].upper() in connectors

def __west_intersection(rawmap: list[list], row: int, column: int, connectors: list) -> bool:
    """Checks to see if the current tile is surrounded by road connecting terrain, except on its east side."""
    return rawmap[column][row + 1].upper() in connectors and rawmap[column + 1][row].upper() in connectors and rawmap[column - 1][row].upper() in connectors

def __north_east_turn(rawmap: list[list], row: int, column: int, connectors: list) -> bool:
    """Checks to see if the current tile has road connecting terrain on its north and east sides."""
    return rawmap[column - 1][row].upper() in connectors and rawmap[column][row + 1].upper() in connectors

def __north_west_turn(rawmap: list[list], row: int, column: int, connectors: list) -> bool:
    """Checks to see if the current tile has road connecting terrain on its north and west sides."""
    return rawmap[column - 1][row].upper() in connectors and rawmap[column][row - 1].upper() in connectors

def __south_east_turn(rawmap: list[list], row: int, column: int, connectors: list) -> bool:
    """Checks to see if the current tile has road connecting terrain on its south and east sides."""
    return rawmap[column + 1][row].upper() in connectors and rawmap[column][row + 1].upper() in connectors

def __south_west_turn(rawmap: list[list], row: int, column: int, connectors: list) -> bool:
    """Checks to see if the current tile has road connecting terrain on its south and west sides."""
    return rawmap[column + 1][row].upper() in connectors and rawmap[column][row - 1].upper() in connectors

def __bridge_salt_ns(rawmap: list[list], row: int, column: int) -> bool:
    """Checks to see if the current tile has salt water on its east and west sides."""
    return rawmap[column][row - 1].upper() == 'O' and rawmap[column][row + 1].upper() == 'O'

def __bridge_salt_we(rawmap: list[list], row: int, column: int) -> bool:
    """Checks to see if the current tile has salt water on its south and north sides."""
    return rawmap[column - 1][row].upper() == 'O' and rawmap[column + 1][row].upper() == 'O'

def __bridge_fresh_ns(rawmap: list[list], row: int, column: int) -> bool:
    """Checks to see if the current tile has fresh water on its east and west sides."""
    return rawmap[column][row - 1].upper() == 'L' and rawmap[column][row + 1].upper() == 'L'

def __bridge_fresh_we(rawmap: list[list], row: int, column: int) -> bool:
    """Checks to see if the current tile has fresh water on its south and north sides."""
    return rawmap[column - 1][row].upper() == 'L' and rawmap[column + 1][row].upper() == 'L'

def __horizontal_line(rawmap: list[list], row: int, column: int, connectors: list) -> bool:
    """Checks to see if the current tile has road connecting terrain on its east and west sides."""
    return rawmap[column - 1][row].upper() in connectors or rawmap[column + 1][row].upper() in connectors

def __vertical_line(rawmap: list[list], row: int, column: int, connectors: list) -> bool:
    """Checks to see if the current tile has road connecting terrain on its north and south sides."""
    return rawmap[column][row - 1].upper() in connectors or rawmap[column][row + 1].upper() in connectors

def __top_left_corner(rawmap: list[list], row: int, column: int, roadconnectors: list) -> str:
    """Returns appropriate road type, without looking into non-existing locations compared to the top left corner of the map."""
    if __south_east_turn(rawmap, row, column, roadconnectors):
        return 'RSE'
    elif rawmap[column][row + 1].upper() in roadconnectors:
        return 'RWE'
    return 'RNS'

def __bottom_left_corner(rawmap: list[list], row: int, column: int, roadconnectors: list) -> str:
    """Returns appropriate road type, without looking into non-existing locations compared to the bottom left corner of the map."""
    if __north_east_turn(rawmap, row, column, roadconnectors):
        return 'RNE'
    elif rawmap[column][row + 1].upper() in roadconnectors:
        return 'RWE'
    return 'RNS'

def __left_column(rawmap: list[list], row: int, column: int, roadconnectors: list) -> str:
    """Returns appropriate road type, based on what can be found on the left-most column of the map."""
    if __west_intersection(rawmap, row, column, roadconnectors):
        return 'RWI'
    elif __north_east_turn(rawmap, row, column, roadconnectors):
        return 'RNE'
    elif __south_east_turn(rawmap, row, column, roadconnectors):
        return 'RSE'
    elif __bridge_salt_we(rawmap, row, column):
        return 'BSWE'
    elif __bridge_fresh_we(rawmap, row, column):
        return 'BFWE'
    elif __horizontal_line(rawmap, row, column, roadconnectors):
        return 'RNS'
    return 'RWE'

def __top_right_corner(rawmap: list[list], row: int, column: int, roadconnectors: list) -> str:
    """Returns appropriate road type, without looking into non-existing locations compared to the top right corner of the map."""
    if __south_west_turn(rawmap, row, column, roadconnectors):
        return 'RSW'
    elif rawmap[column][row - 1].upper() in roadconnectors:
        return 'RWE'
    return 'RNS'

def __bottom_right_corner(rawmap: list[list], row: int, column: int, roadconnectors: list) -> str:
    """Returns appropriate road type, without looking into non-existing locations compared to the bottom right corner of the map."""
    if __north_west_turn(rawmap, row, column, roadconnectors):
        return 'RNW'
    elif rawmap[column][row - 1].upper() in roadconnectors:
        return 'RWE'
    return 'RNS'

def __right_column(rawmap: list[list], row: int, column: int, roadconnectors: list) -> str:
    """Returns appropriate road type, based on what can be found on the right-most column of the map."""
    if __east_intersection(rawmap, row, column, roadconnectors):
        return 'REI'
    elif __north_west_turn(rawmap, row, column, roadconnectors):
        return 'RNW'
    elif __south_west_turn(rawmap, row, column, roadconnectors):
        return 'RSW'
    elif __bridge_salt_we(rawmap, row, column):
        return 'BSWE'
    elif __bridge_fresh_we(rawmap, row, column):
        return 'BFWE'
    elif __horizontal_line(rawmap, row, column, roadconnectors):
        return 'RNS'
    return 'RWE'

def __top_row(rawmap: list[list], row: int, column: int, roadconnectors: list) -> str:
    """Returns appropriate road type, based on what can be found on the top-most column of the map."""
    if __south_intersection(rawmap, row, column, roadconnectors):
        return 'RSI'
    elif __south_east_turn(rawmap, row, column, roadconnectors):
        return 'RSE'
    elif __south_west_turn(rawmap, row, column, roadconnectors):
        return 'RSW'
    elif __bridge_salt_ns(rawmap, row, column):
        return 'BSNS'
    elif __bridge_fresh_ns(rawmap, row, column):
        return 'BFNS'
    elif __vertical_line(rawmap, row, column, roadconnectors):
        return 'RWE'
    return 'RNS'

def __bottom_row(rawmap: list[list], row: int, column: int, roadconnectors: list) -> str:
    """Returns appropriate road type, based on what can be found on the bottom-most column of the map."""
    if __north_intersection(rawmap, row, column, roadconnectors):
        return 'RNI'
    elif __north_east_turn(rawmap, row, column, roadconnectors):
        return 'RNE'
    elif __north_west_turn(rawmap, row, column, roadconnectors):
        return 'RNW'
    elif __bridge_salt_ns(rawmap, row, column):
        return 'BSNS'
    elif __bridge_fresh_ns(rawmap, row, column):
        return 'BFNS'
    elif __vertical_line(rawmap, row, column, roadconnectors):
        return 'RWE'
    return 'RNS'

def __center_roads(rawmap: list[list], row: int, column: int, roadconnectors: list) -> str:
    """Returns appropriate road type, without any precautions for overflow or out of bounds issues."""
    if __complete_intersection(rawmap, row, column, roadconnectors):
        return 'RCI'
    elif __north_intersection(rawmap, row, column, roadconnectors):
        return 'RNI'
    elif __east_intersection(rawmap, row, column, roadconnectors):
        return 'REI'
    elif __south_intersection(rawmap, row, column, roadconnectors):
        return 'RSI'
    elif __west_intersection(rawmap, row, column, roadconnectors):
        return 'RWI'
    elif __north_east_turn(rawmap, row, column, roadconnectors):
        return 'RNE'
    elif __north_west_turn(rawmap, row, column, roadconnectors):
        return 'RNW'
    elif __south_east_turn(rawmap, row, column, roadconnectors):
        return 'RSE'
    elif __south_west_turn(rawmap, row, column, roadconnectors):
        return 'RSW'
    elif __bridge_salt_ns(rawmap, row, column):
        return 'BSNS'
    elif __bridge_salt_we(rawmap, row, column):
        return 'BSWE'
    elif __bridge_fresh_ns(rawmap, row, column):
        return 'BFNS'
    elif __bridge_fresh_we(rawmap, row, column):
        return 'BFWE'
    elif __horizontal_line(rawmap, row, column, roadconnectors):
        return 'RNS'
    elif __vertical_line(rawmap, row, column, roadconnectors):
        return 'RWE'
    return 'RCI'

def __road_connections(rawmap: list[list], row: int, column: int, x: int, y: int) -> str:
    """Returns appropriate road type, based on row and column numbers and exact positions of the current road."""
    roadconnectors = ['R', '1', '2', 'C', 'A', 'W', 'H'] #VALID ROAD CONNECTING TERRAIN TYPES
    if row == 0:
        if column == 0:
            return __top_left_corner(rawmap, row, column, roadconnectors)
        elif column == y - 1:
            return __bottom_left_corner(rawmap, row, column, roadconnectors)
        else:
            return __left_column(rawmap, row, column, roadconnectors)
    elif row == x - 1:
        if column == 0:
            return __top_right_corner(rawmap, row, column, roadconnectors)
        elif column == y - 1:
            return __bottom_right_corner(rawmap, row, column, roadconnectors)
        else:
            return __right_column(rawmap, row, column, roadconnectors)
    else:
        if column == 0:
            return __top_row(rawmap, row, column, roadconnectors)
        elif column == y - 1:
            return __bottom_row(rawmap, row, column, roadconnectors)
        else:
            return __center_roads(rawmap, row, column, roadconnectors)

def __block_translator(onblock: str, window: object, onwindow: tuple) -> Terrain:
    """Function that takes processed terrain map data and returns with its appropriate version after drawing it on the displayed map.
        Safely retuns with salt water terrain type, if it couldn't detect any type of valid terrain data."""
    images = __TerrainImages()
    if onblock == "O":
        window.blit(images.SALTWATER, onwindow)
        return Terrain(onblock, "Saltwater", 0, {"Foot": 0, "Wheels": 0, "Tracks": 0}, False, None)
    elif onblock == "L":
        window.blit(images.FRESHWATER, onwindow)
        return Terrain(onblock, "Freshwater", 0, {"Foot": 2, "Wheels": 0, "Tracks": 0}, False, None)
    elif onblock == "P":
        window.blit(images.PLAINS, onwindow)
        return Terrain(onblock, "Plains", 1, {"Foot": 1, "Wheels": 2, "Tracks": 1}, False, None)
    elif onblock == "S":
        window.blit(images.SWAMP, onwindow)
        return Terrain(onblock, "Swamp", 1, {"Foot": 2, "Wheels": 3, "Tracks": 1}, False, None)
    elif onblock == "F":
        window.blit(images.FOREST, onwindow)
        return Terrain(onblock, "Forest", 2, {"Foot": 1, "Wheels": 3, "Tracks": 2}, False, None)
    elif onblock == "M":
        window.blit(images.MOUNTAIN, onwindow)
        return Terrain(onblock, "Mountain", 4, {"Foot": 2, "Wheels": 0, "Tracks": 0}, False, None)
    elif onblock == "D":
        window.blit(images.DEBRIS, onwindow)
        return Terrain(onblock, "Wreckage", 2, {"Foot": 2, "Wheels": 2, "Tracks": 1}, False, None)
    elif onblock == "A":
        window.blit(images.ABANDONED_CITY, onwindow)
        return Terrain(onblock, "Ghost Town", 3, {"Foot": 1, "Wheels": 2, "Tracks": 1}, False, None)
    elif onblock == "C":
        window.blit(images.CITY_NEUTRAL, onwindow)
        return Terrain(onblock, "City", 3, {"Foot": 1, "Wheels": 1, "Tracks": 1}, True, None)
    elif onblock == "1":
        window.blit(images.CITY_1, onwindow)
        return Terrain('C', "City", 3, {"Foot": 1, "Wheels": 1, "Tracks": 1}, True, "Red")
    elif onblock == "2":
        window.blit(images.CITY_2, onwindow)
        return Terrain('C', "City", 3, {"Foot": 1, "Wheels": 1, "Tracks": 1}, True, "Blue")
    elif onblock == "W":
        window.blit(images.WORKSHOP_NEUTRAL, onwindow)
        return Terrain(onblock, "Factory", 3, {"Foot": 1, "Wheels": 1, "Tracks": 1}, True, None)
    elif onblock == "HQ1":
        window.blit(images.HQ_1, onwindow)
        return Terrain('H', "Headquarters", 3,{"Foot": 1, "Wheels": 1, "Tracks": 1}, True, "Red")
    elif onblock == "HQ2":
        window.blit(images.HQ_2, onwindow)
        return Terrain('H', "Headquarters", 3, {"Foot": 1, "Wheels": 1, "Tracks": 1}, True, "Blue")
    elif onblock == "RNS":
        window.blit(images.ROAD_NORTHSOUTH, onwindow)
        return Terrain(onblock, "Road", 0, {"Foot": 1, "Wheels": 1, "Tracks": 1}, False, None)
    elif onblock == "RWE":
        window.blit(images.ROAD_WESTEAST, onwindow)
        return Terrain(onblock, "Road", 0, {"Foot": 1, "Wheels": 1, "Tracks": 1}, False, None)
    elif onblock == "RNE":
        window.blit(images.ROAD_NORTHEAST, onwindow)
        return Terrain(onblock, "Road", 0, {"Foot": 1, "Wheels": 1, "Tracks": 1}, False, None)
    elif onblock == "RNW":
        window.blit(images.ROAD_NORTHWEST, onwindow)
        return Terrain(onblock, "Road", 0, {"Foot": 1, "Wheels": 1, "Tracks": 1}, False, None)
    elif onblock == "RSE":
        window.blit(images.ROAD_SOUTHEAST, onwindow)
        return Terrain(onblock, "Road", 0, {"Foot": 1, "Wheels": 1, "Tracks": 1}, False, None)
    elif onblock == "RSW":
        window.blit(images.ROAD_SOUTHWEST, onwindow)
        return Terrain(onblock, "Road", 0, {"Foot": 1, "Wheels": 1, "Tracks": 1}, False, None)
    elif onblock == "RNI":
        window.blit(images.ROAD_NORTHINTERSECTION, onwindow)
        return Terrain(onblock, "Road", 0, {"Foot": 1, "Wheels": 1, "Tracks": 1}, False, None)
    elif onblock == "REI":
        window.blit(images.ROAD_EASTINTERSECTION, onwindow)
        return Terrain(onblock, "Road", 0, {"Foot": 1, "Wheels": 1, "Tracks": 1}, False, None)
    elif onblock == "RSI":
        window.blit(images.ROAD_SOUTHINTERSECTION, onwindow)
        return Terrain(onblock, "Road", 0, {"Foot": 1, "Wheels": 1, "Tracks": 1}, False, None)
    elif onblock == "RWI":
        window.blit(images.ROAD_WESTINTERSECTION, onwindow)
        return Terrain(onblock, "Road", 0, {"Foot": 1, "Wheels": 1, "Tracks": 1}, False, None)
    elif onblock == "RCI":
        window.blit(images.ROAD_FULLINTERSECTION, onwindow)
        return Terrain(onblock, "Road", 0, {"Foot": 1, "Wheels": 1, "Tracks": 1}, False, None)
    elif onblock == "BSNS":
        window.blit(images.BRIDGE_SALT_NORTHSOUTH, onwindow)
        return Terrain(onblock, "Bridge", 0, {"Foot": 1, "Wheels": 1, "Tracks": 1}, False, None)
    elif onblock == "BSWE":
        window.blit(images.BRIDGE_SALT_WESTEAST, onwindow)
        return Terrain(onblock, "Bridge", 0, {"Foot": 1, "Wheels": 1, "Tracks": 1}, False, None)
    elif onblock == "BFNS":
        window.blit(images.BRIDGE_FRESH_NORTHSOUTH, onwindow)
        return Terrain(onblock, "Bridge", 0, {"Foot": 1, "Wheels": 1, "Tracks": 1}, False, None)
    elif onblock == "BFWE":
        window.blit(images.BRIDGE_FRESH_WESTEAST, onwindow)
        return Terrain(onblock, "Bridge", 0, {"Foot": 1, "Wheels": 1, "Tracks": 1}, False, None)
    window.blit(images.SALTWATER, onwindow)
    return Terrain('O', "Saltwater", 0, {"Foot": 0, "Wheels": 0, "Tracks": 0}, False, None)

def block_draw(onblock: str, window: object, onwindow: tuple) -> None:
    """Function that takes processed terrain map data, and draws it on the displayed windows."""
    images = __TerrainImages()
    if onblock.team == None:
        if onblock.identifier == "O":
            window.blit(images.SALTWATER, onwindow)
        elif onblock.identifier == "L":
            window.blit(images.FRESHWATER, onwindow)
        elif onblock.identifier == "P":
            window.blit(images.PLAINS, onwindow)
        elif onblock.identifier == "S":
            window.blit(images.SWAMP, onwindow)
        elif onblock.identifier == "F":
            window.blit(images.FOREST, onwindow)
        elif onblock.identifier == "M":
            window.blit(images.MOUNTAIN, onwindow)
        elif onblock.identifier == "D":
            window.blit(images.DEBRIS, onwindow)
        elif onblock.identifier == "A":
            window.blit(images.ABANDONED_CITY, onwindow)
        elif onblock.identifier == "C":
            window.blit(images.CITY_NEUTRAL, onwindow)
        elif onblock.identifier == "W":
            window.blit(images.WORKSHOP_NEUTRAL, onwindow)
        elif onblock.identifier == "RNS":
            window.blit(images.ROAD_NORTHSOUTH, onwindow)
        elif onblock.identifier == "RWE":
            window.blit(images.ROAD_WESTEAST, onwindow)
        elif onblock.identifier == "RNE":
            window.blit(images.ROAD_NORTHEAST, onwindow)
        elif onblock.identifier == "RNW":
            window.blit(images.ROAD_NORTHWEST, onwindow)
        elif onblock.identifier == "RSE":
            window.blit(images.ROAD_SOUTHEAST, onwindow)
        elif onblock.identifier == "RSW":
            window.blit(images.ROAD_SOUTHWEST, onwindow)
        elif onblock.identifier == "RNI":
            window.blit(images.ROAD_NORTHINTERSECTION, onwindow)
        elif onblock.identifier == "REI":
            window.blit(images.ROAD_EASTINTERSECTION, onwindow)
        elif onblock.identifier == "RSI":
            window.blit(images.ROAD_SOUTHINTERSECTION, onwindow)
        elif onblock.identifier == "RWI":
            window.blit(images.ROAD_WESTINTERSECTION, onwindow)
        elif onblock.identifier == "RCI":
            window.blit(images.ROAD_FULLINTERSECTION, onwindow)
        elif onblock.identifier == "BSNS":
            window.blit(images.BRIDGE_SALT_NORTHSOUTH, onwindow)
        elif onblock.identifier == "BSWE":
            window.blit(images.BRIDGE_SALT_WESTEAST, onwindow)
        elif onblock.identifier == "BFNS":
            window.blit(images.BRIDGE_FRESH_NORTHSOUTH, onwindow)
        elif onblock.identifier == "BFWE":
            window.blit(images.BRIDGE_FRESH_WESTEAST, onwindow)
    elif onblock.team == "Red":
        if onblock.identifier == "H":
            window.blit(images.HQ_1, onwindow)
        elif onblock.identifier == "W":
            window.blit(images.WORKSHOP_1, onwindow)
        elif onblock.identifier == "C":
            window.blit(images.CITY_1, onwindow)
    elif onblock.team == "Blue":
        if onblock.identifier == "H":
            window.blit(images.HQ_2, onwindow)
        elif onblock.identifier == "W":
            window.blit(images.WORKSHOP_2, onwindow)
        elif onblock.identifier == "C":
            window.blit(images.CITY_2, onwindow)

def __map_processor(rawmap: list[list], xrn: int, yrn: int) -> tuple:
    """Function that takes in the raw terrain map data, then returns with the number of allied buildings a team has and with the processed map datas."""
    procmap = [['O' for i in range(yrn)] for j in range(xrn)]
    team_buildings = [1, 1]
    hqnum = 0
    for row in range(xrn):
        for column in range(yrn):
            tile = rawmap[column][row].upper()
            if tile == 'H':
                procmap[row][column] = 'HQ{}'.format(hqnum + 1)
                hqnum += 1
            elif tile == '1':
                team_buildings[0] += 1
                procmap[row][column] = '1'
            elif tile == '2':
                team_buildings[1] += 1
                procmap[row][column] = '2'
            elif tile == 'R':
                procmap[row][column] = __road_connections(rawmap, row, column, xrn, yrn)
            else:
                procmap[row][column] = tile
    return team_buildings, procmap

def drawadd(window: object, BLOCK: int, rawmap: list[list], xrn: int, yrn: int) -> tuple:
    """Function that takes in all the raw terrain data and returns with the number of allied buildings a team has and with the processed map datas."""
    team_buildings, procmap = __map_processor(rawmap, xrn, yrn)
    return team_buildings, [[__block_translator(procmap[xon][yon], window, (xon * BLOCK, yon * BLOCK)) for yon in range(yrn)] for xon in range(xrn)]