import os, sys, pygame

from . import equipment,ship
from pygame.locals import *
pygame.init()
# set up global variables
print('Setting up global values.')
# center the pygame window
os.environ['SDL_VIDEO_CENTERED'] = '1'

# set up the clock speed and window surface
print('Setting up clock.')
fpsClock = pygame.time.Clock()
FPS = 60
print('Setting up pygame window.')
windowWidth = 1024
windowHeight = 600
windowSurface = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption('Python Defender 2')
pygame.display.set_icon(pygame.image.load('graphics' + os.sep + 'PythonDefenderTwoIcon.png'))

# set up the background
backgroundImage = pygame.image.load('graphics' + os.sep + 'Starfield.png')
backgroundRect = pygame.transform.scale(backgroundImage, (windowWidth, windowHeight))

#setup the combat surface, everything will be drawn to this first, then blitted to winowsurface
combatSurf = pygame.Surface((windowWidth, windowHeight))
combatSurfRect = (0,0, windowWidth, windowHeight)

# set up the colors
BLACK = (0,0,0)
WHITE = (255,255,255)
GREY = (128,128,128)
DARKGREY = (52,52,52)
RED = (255,0,0)
GREEN = (0,255,0)
LIGHTBLUE = (0,255,255)
TURQUOISE = (0,255,126)
BLUE = (0,0,255)
YELLOW = (255,255,0)
ORANGE = (255,126,0)
PURPLE = (255,0,255)
DEEPPURPLE = (128,0,128)

# set up the font
font = pygame.font.SysFont(None, 18)
#smallFont = pygame.font.SysFont(None, 14)


def drawText(text, font, surface, x, y, color):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def terminate():
    # call this to close the game
    pygame.quit()
    sys.exit()

def getWeapons(directory):
    weaponList = []
    #weapon = {}
    i = 0
    # read the weapon text file in the equipment directory
    print('Reading weapon files.')
    readFile = open(os.path.join(directory,"weapons.txt"), "rt")
    while True:
        readLine = readFile.readline()
        if not readLine:
            break
        if '//' in readLine:
            continue
        readLine = readLine[:-1]
        name, weaponType, damage, fireRate, projSpeed, reactorUse, acceleration, missileType  = readLine.split(",")
        newWeapon = equipment.Weapon(name, weaponType, damage, fireRate, projSpeed, reactorUse, acceleration, missileType)

        weaponList.append(newWeapon)

        i += 1

    readFile.close
        

    return weaponList

def getShields(directory):

    shieldList = []
    #shield = {}
    i = 0
    # read the shield text file in the equipment directory
    print('Reading shield files.')
    readFile = open(os.path.join(directory,"shields.txt"), "rt")
    while True:
        readLine = readFile.readline()
        if not readLine:
            break
        if '//' in readLine:
            continue
        readLine = readLine[:-1]
        name, strength, recharge, reactorUse = readLine.split(",")
        newShield = equipment.Shield(name, strength, recharge, reactorUse)

        shieldList.append(newShield)

        i += 1

    readFile.close
        

    return shieldList

def getReactors(directory):

    reactorList = []
    #rector = {}
    i = 0
    # read the reactor text file in the equipment directory
    print('Reading reactor files.')
    readFile = open(os.path.join(directory,"reactors.txt"), "rt")
    while True:
        readLine = readFile.readline()
        if not readLine:
            break
        if '//' in readLine:
            continue
        readLine = readLine[:-1]
        name, capacity, recharge = readLine.split(",")
        newReactor = equipment.Reactor(name, capacity, recharge)

        reactorList.append(newReactor)

        i += 1

    readFile.close
        

    return reactorList

def getEngines(directory):

    engineList = []
    #engine = {}
    i = 0
    # read the engine text file in the equipment directory
    print('Reading engine files.')
    readFile = open(os.path.join(directory,"engines.txt"), "rt")
    while True:
        readLine = readFile.readline()
        if not readLine:
            break
        if '//' in readLine:
            continue
        readLine = readLine[:-1]
        name, maxSpeed, acceleration, reactorUse = readLine.split(",")
        newEngine = equipment.Engine(name, maxSpeed, acceleration, reactorUse)

        engineList.append(newEngine)

        i += 1

    readFile.close
        

    return engineList

def getShips(directory, file):

    shipList = []
    #ship = {}
    i = 0
    # read the ship text file in the equipment directory
    print('Reading ship files.')
    readFile = open(os.path.join(directory,file), "rt")
    while True:
        readLine = readFile.readline()
        if not readLine:
            break
        if '//' in readLine:
            continue
        readLine = readLine[:-1]
        name, hullType, hullPoints, hullNodes, hullAgility, hullWidth, hullHeight, droneBay = readLine.split(",")
        newShip = ship.Ship(name, hullType, hullPoints, hullNodes, hullAgility, hullWidth, hullHeight, droneBay)
        shipList.append(newShip)

        i += 1

    readFile.close
        

    return shipList


WEAPONS = getWeapons("equipment")
SHIELDS = getShields("equipment")
REACTORS = getReactors("equipment")
ENGINES = getEngines("equipment")
SHIPS = getShips("ships", "ships.txt")
DRONES = getShips("ships", "drones.txt")
    
