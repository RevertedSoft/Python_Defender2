# this module holds the player class
import pygame, copy
from . import equipment, aiship, ship
from .globals import *

class Player(ship.Ship):
    
    

    def __init__(self, position):
        print("Building player object.")
        self.positionX = position[0]# tracking the position, and moving the ship in accordance to the position is much smoother than moving the rect every tick
        self.positionY = position[1]

        self.facing = 'up'
        ship.Ship.__init__(self)


    def addEquipment(self, equipmentX):
        #self.currentID += 1
        if equipmentX.equipType == 'weapon' and self.nodesUsed < self.hullNodes:
            self.weaponList.append(equipment.Weapon(equipmentX.name, equipmentX.weaponType, equipmentX.damage, equipmentX.fireRate, equipmentX.projSpeed, equipmentX.reactorUse, equipmentX.acceleration, equipmentX.missileType))##################################I AM APPENDING A COPY OF THE OBJECT FROM THE MENU :@
            self.nodesUsed += 1
 
            print("Adding weapon.")
        elif equipmentX.equipType == 'reactor' and self.nodesUsed < self.hullNodes:
            self.reactorList.append(equipment.Reactor(equipmentX.name, equipmentX.capacity, equipmentX.recharge))
            self.nodesUsed += 1

            print("Adding reactor.")
        elif equipmentX.equipType == 'shield' and self.nodesUsed < self.hullNodes:
            self.shieldList.append(equipment.Shield(equipmentX.name, equipmentX.strength, equipmentX.recharge, equipmentX.reactorUse))
            self.nodesUsed += 1

            print("Adding shield.")
        elif equipmentX.equipType == 'engine' and self.nodesUsed < self.hullNodes:
            self.engineList.append(equipment.Engine(equipmentX.name, equipmentX.maxSpeed, equipmentX.acceleration, equipmentX.reactorUse))
            self.nodesUsed += 1

            print("Adding engine.")
        elif self.nodesUsed >= self.hullNodes:
            print("The nodes on your ship are full.")
        else:
            print("There is no equipment of specified type.")

    def addDrone(self, droneX):
        #this method adds a drone to the players drone list

        if self.currentDrones < self.droneBay:
            if droneX.hullType == 'cannon drone':
                newDrone = (aiship.AiShip((self.positionX, self.positionY), ship.findShip(droneX.name, DRONES), [copy.deepcopy(WEAPONS[0])], [copy.deepcopy(REACTORS[0])], [copy.deepcopy(SHIELDS[1])], [copy.deepcopy(ENGINES[2])], 'basic', 'player'))
            elif droneX.hullType == 'laser drone':
                newDrone = (aiship.AiShip((self.positionX, self.positionY), ship.findShip(droneX.name, DRONES), [copy.deepcopy(WEAPONS[1])], [copy.deepcopy(REACTORS[1])], [copy.deepcopy(SHIELDS[0])], [copy.deepcopy(ENGINES[1])], 'basic', 'player'))
            elif droneX.hullType == 'missile drone':
                newDrone = (aiship.AiShip((self.positionX, self.positionY), ship.findShip(droneX.name, DRONES), [copy.deepcopy(WEAPONS[6])], [copy.deepcopy(REACTORS[2])], [copy.deepcopy(SHIELDS[1])], [copy.deepcopy(ENGINES[0])], 'basic', 'player'))             
            self.droneList.append(copy.deepcopy(newDrone))
            self.currentDrones += 1
        


    

    def getShipSpeed(self):
        print("Calculating speed and acceleration.")
        self.maxSpeed = 0.0
        self.currentSpeed = float(0.0)
        self.currentVerticleSpeed = 0
        self.acceleration = float(0.0)

        for engines in self.engineList[:]:
            self.maxSpeed += engines.maxSpeed
            self.acceleration += engines.acceleration

    def getShipReactorPower(self):
        print("Calculating the power of the reactors.")
        self.currentCapacitor = 0
        self.maxCapacitor = 0
        self.capacitorRecharge = 0

        for reactors in self.reactorList[:]:
            self.currentCapacitor += reactors.capacity
            self.maxCapacitor += reactors.capacity
            self.capacitorRecharge += reactors.recharge

    def getShipShieldPower(self):
        print("Calculating ships shield power.")
        self.currentShield = 0
        self.maxShield = 0
        self.shieldRecharge = 0
        self.shieldCapUse = 0
        self.shieldResetCount = 0

        for shields in self.shieldList[:]:
            self.currentShield += shields.strength
            self.maxShield += shields.strength
            self.shieldRecharge += float(shields.recharge)
            self.shieldCapUse += shields.reactorUse
            
