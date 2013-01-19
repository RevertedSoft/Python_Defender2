import pygame
from pygame.locals import *

#from .globals import *


class Ship():
    #constructs a ship object, based on the arguments passed
    #i am making individual ships into objects, because I wish to have the player able to upgrade the ship at a later point

    def __init__(self, name=None, hullType=None, hullPoints=None, hullNodes=0, hullAgility=None, hullWidth=None, hullHeight=None, droneBay=0):
        #set up the ship
        self.name = name
        self.hullType = hullType
        if hullPoints:
            self.hullPoints = int(hullPoints)
        #if hullNodes:
        self.hullNodes = int(hullNodes)
        if hullAgility:
            self.hullAgility = float(hullAgility)
        if hullWidth:
            self.hullWidth = int(hullWidth)
        if hullHeight:
            self.hullHeight = int(hullHeight)
        #if droneBay:
        self.droneBay = int(droneBay)
        #initialize the attributes to a starting state

        self.weaponList = [] # the list of weapons equiped on the ship
        self.reactorList = [] # the list of reactors equiped on the ship
        self.shieldList = [] # the list of shields equiped on the ship
        self.engineList = [] # the list of engines equiped on the ship
        self.nodesUsed = 0 # the number of nodes used by equipment on the players ship
        self.currentDrones = 0 # the number of drones the player ship is fielding

        self.movingLeft = False # is the player moving left?
        self.movingRight = False # is the player moving right?
        self.movingUp = False
        self.movingDown = False
        self.isFiring = False # is the player firing their weapons?

        self.bulletList = [] # the list of bullets belonging to the player
        self.missileList = [] # the list of smart missiles belonging to the player
        self.droneList = []

        self.shieldPosition = 0
        self.shieldResetCount = 0

    def rechargeShields(self):
        if self.shieldResetCount > 0:# if the computers shield is resetting, iterate the counter down
            self.shieldResetCount -= 1

        if self.shieldResetCount == 0:
            # recharge the self's shields
            if self.currentShield < self.maxShield and self.shieldCapUse <= self.currentCapacitor:
                self.currentShield += self.shieldRecharge
                self.currentCapacitor -= self.shieldCapUse# drain the players cap over time while the shield is recharging
            if self.currentShield > self.maxShield:
                self.currentShield = self.maxShield

        self.currentCapacitor -= int(self.shieldCapUse / 2)# drain the players cap over time for having an active shield

    def rechargeCapacitor(self):
        # recharge the self's capacitor
        if self.currentCapacitor < self.maxCapacitor:
            self.currentCapacitor += self.capacitorRecharge
        if self.currentCapacitor > self.maxCapacitor:
            self.currentCapacitor = self.maxCapacitor
        if self.currentCapacitor < 0:
            self.currentCapacitor = 0

    def changeSpeed(self):
        # apply force depending on which direction the self is trying to move
        if self.movingRight and self.currentSpeed < self.maxSpeed:
            self.currentSpeed += (self.acceleration * self.hullAgility)

        elif self.movingLeft and self.currentSpeed > -(self.maxSpeed):
            self.currentSpeed -= (self.acceleration * self.hullAgility)

        if self.movingUp and self.currentVerticleSpeed > -(self.maxSpeed):
            self.currentVerticleSpeed -= (self.acceleration * self.hullAgility)

        elif self.movingDown and self.currentVerticleSpeed < (self.maxSpeed):
            self.currentVerticleSpeed += (self.acceleration * self.hullAgility)

        if self.movingRight or self.movingLeft:
            for engines in self.engineList[:]:
                self.currentCapacitor -= engines.reactorUse

        if self.movingUp or self.movingDown:
            for engines in self.engineList[:]:
                self.currentCapacitor -= engines.reactorUse

        # decrease the self's speed over time while the engines are not active, speed decreases faster depending on the ships agility
        elif not self.movingRight and not self.movingLeft:
            if self.currentSpeed > 0:
                self.currentSpeed -= (0.2 * self.hullAgility)
            elif self.currentSpeed < 0:
                self.currentSpeed += (0.2 * self.hullAgility)

            if self.currentSpeed <  1:
                if self.currentSpeed > 0:
                    self.currentSpeed = 0

            elif self.currentSpeed >  1:
                if self.currentSpeed < 0:
                    self.currentSpeed = 0

    def move(self, windowWidth, windowHeight):
        #move the self according to their speed
        if self.facing == 'down':
            if self.rect.top > 0 and self.rect.bottom < (windowHeight - (windowHeight /2)):
                self.positionY += self.currentVerticleSpeed
                self.rect.top = self.positionY
            else:
                if self.rect.bottom > (windowHeight - (windowHeight /2)):
                    self.positionY = ((windowHeight - (windowHeight /2)) - self.hullHeight) - 1
                elif self.rect.top < 10:
                    self.positionY = 11
                self.currentVerticleSpeed = 0
            
        if self.rect.right < windowWidth and self.rect.left > 0:
            self.positionX += self.currentSpeed#
            self.rect.left = self.positionX#
            self.shieldPosition = self.rect.center
            self.shieldRect.center = self.shieldPosition

        # bounce the self off the walls
        if self.rect.right >= windowWidth:
            self.rect.right = windowWidth - 1
            self.positionX = self.rect.left
            if self.currentSpeed <= 2:
                self.currentSpeed = 0
            self.currentSpeed = (self.currentSpeed * 0.3) * -1
        elif self.rect.left <= 0:
            self.rect.left = 1
            self.positionX = self.rect.left
            if self.currentSpeed >= 2:
                self.currentSpeed = 0
            self.currentSpeed = abs(self.currentSpeed) * 0.3

        

        # move the self's gun points before firing bullets so they fire from the right position
        if len(self.weaponList) > 0:
            i = 0
            for weapons in self.weaponList[:]:
                if len(self.weaponList) == 1:
                    spacer = self.hullWidth / 2
                    
                elif len(self.weaponList) == 2:
                    spacer = self.hullWidth * i
                    
                else:
                    spacer = (self.hullWidth / len(self.weaponList)) * i
                    spacer += spacer / 2
                    
                weapons.getWeaponPosition(self, spacer)
                i += 1

    def setupShip(self, ship):#this method sets up the players ship after selected from menu
        print("Finding ship.")
        #self.ship = ship
        self.hullType = ship.hullType
        self.hullPoints = ship.hullPoints
        self.hullNodes = int(ship.hullNodes)
        self.hullAgility = float(ship.hullAgility)
        self.hullWidth = int(ship.hullWidth)
        self.hullHeight = int(ship.hullHeight)
        self.droneBay = int(ship.droneBay)
        self.rect = pygame.Rect(self.positionX,self.positionY, ship.hullWidth, ship.hullHeight)
        self.shieldRadius = int(ship.hullWidth * 1.5)
        self.shieldRect = pygame.Rect(0,0,self.shieldRadius * 2,self.shieldRadius * 2)


def findShip(ship, shipList):
    # gets the requested ship from the given list of ships
    for ships in shipList[:]:
        if ships.name == ship:
            selectedShip = Ship(ships.name, ships.hullType, ships.hullPoints, ships.hullNodes, ships.hullAgility, ships.hullWidth, ships.hullHeight, ships.droneBay)
            return selectedShip

    print('Ship not found.')
