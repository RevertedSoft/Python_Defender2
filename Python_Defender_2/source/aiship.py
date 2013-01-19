# this module is used to create AI ships, be it enemies, or drones

import pygame
from pygame.locals import *

from . import ship

from .globals import *

class AiShip(ship.Ship):

    def __init__(self, position, shipHull, weaponList, reactorList, shieldList, engineList, behaviour, team):
        '''This class takes arguments to initialize the enemy ship. Pass [] if you wish to pass nothing'''
        ship.Ship.__init__(self, shipHull.name, shipHull.hullType, shipHull.hullPoints, shipHull.hullNodes, shipHull.hullAgility, shipHull.hullWidth, shipHull.hullHeight, shipHull.droneBay)
        self.positionX = position[0]
        self.positionY = position[1]
        self.weaponList = weaponList
        self.reactorList = reactorList
        self.shieldList = shieldList
        self.engineList = engineList
        self.behaviour = behaviour

        self.targetY = self.positionY #this is used in the ai scripts, if the ai is more aggresive, it will attempt to get closer to the player
        self.team = team # the ship can belong to the enemies, or be a drone from the player

        self.target = ''

        # now initialize any variables that derive from the arguments passed via the class call
        self.rect = pygame.Rect(self.positionX,self.positionY, self.hullWidth, self.hullHeight)
        self.shieldRadius = int(self.hullWidth * 1.5)
        self.shieldPosition = self.rect.center
        self.shieldRect = pygame.Rect(0,0,self.shieldRadius * 2,self.shieldRadius * 2)

        #is the ship facing up or down?
        if self.team == 'player':
            self.facing = 'up'
        else:
            self.facing = 'down'

        # init reactors
        self.currentCapacitor = 0
        self.maxCapacitor = 0
        self.capacitorRecharge = 0
        for reactors in self.reactorList[:]:
            
            self.currentCapacitor += reactors.capacity
            self.maxCapacitor += reactors.capacity
            self.capacitorRecharge += reactors.recharge

        # init shields
        self.currentShield = 0
        self.maxShield = 0
        self.shieldRecharge = 0
        self.shieldCapUse = 0
        for shields in self.shieldList[:]:
            self.currentShield += shields.strength
            self.maxShield += shields.strength
            self.shieldRecharge += float(shields.recharge)
            self.shieldCapUse += shields.reactorUse

        # init engines
        self.maxSpeed = 0
        self.currentSpeed = 0
        self.currentVerticleSpeed = 0#this is how fast the enemy is moving up or down, used along with the ai scripting
        self.acceleration = 0
        self.engineCapUse = 0
        for engines in self.engineList[:]:
            self.maxSpeed += engines.maxSpeed
            self.acceleration += engines.acceleration
            self.engineCapUse += engines.reactorUse


    def getTarget(self, targetList):
        #This method will choose a target depending on its behaviour (currently only neccesary for drones)
        for targets in targetList[:]:
            if self.hullType == 'cannon drone' or self.hullType == 'laser drone':
                if targets.hullType == 'heavy frigate':
                    self.target = targets
                    break
                elif targets.hullType == 'frigate':
                    self.target = targets
                elif targets.hullType == 'corvette':
                    self.target = targets
                elif targets.hullType == 'heavy fighter':
                    self.target = targets
                elif targets.hullType == 'fighter':
                    self.target = targets
            elif self.hullType == 'missile drone':
                if targets.hullType == 'fighter':
                    self.target = targets
                    break
                elif targets.hullType == 'heavy fighter':
                    self.target = targets
                elif targets.hullType == 'corvette':
                    self.target = targets
                elif targets.hullType == 'frigate':
                    self.target = targets
                elif targets.hullType == 'heavy frigate':
                    self.target = targets

            else:
                if targets.hullType == 'heavy frigate':
                    self.target = targets
                    break
                elif targets.hullType == 'frigate':
                    self.target = targets
                elif targets.hullType == 'corvette':
                    self.target = targets
                elif targets.hullType == 'heavy fighter':
                    self.target = targets
                elif targets.hullType == 'fighter':
                    self.target = targets
    
