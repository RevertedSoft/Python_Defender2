# this module will contain the different types of equipment that the player can use
import pygame
from pygame.locals import *

#from .globals import *

class Weapon:
    equipType = 'weapon'
    currentReload = 0
    hullRect = 0

    def __init__(self, name, weaponType, damage, fireRate, projSpeed, reactorUse, acceleration, missileType):
        self.name = name
        self.damage = int(damage)
        self.fireRate = int(fireRate)
        self.projSpeed = int(projSpeed)
        self.reactorUse = int(reactorUse)
        self.weaponType = weaponType
        self.acceleration = float(acceleration)
        self.missileType = missileType

    def getWeaponPosition(self, hull, spacer):
        #print("Attaching weapons to hull...")
        
        self.hullRect = pygame.Rect(hull.rect.left + (spacer) - 2, hull.rect.top, 1, 1)#+ (spacer/2)
        if self.hullRect.right > hull.rect.right:
            self.hullRect.right = hull.rect.right
        if self.hullRect. left < hull.rect.left:
            self.hullRect. left = hull.rect.left
        #self.hullPosition += spacer


class Shield:
    equipType = 'shield'

    def __init__(self, name, strength, recharge, reactorUse):
        self.name = name
        self.strength = int(strength)
        self.recharge = float(recharge)
        self.reactorUse = int(reactorUse)


class Reactor:
    equipType = 'reactor'

    def __init__(self, name, capacity, recharge):
        self.name = name
        self.capacity = int(capacity)
        self.recharge = int(recharge)


class Engine:
    equipType = 'engine'

    def __init__(self, name, maxSpeed, acceleration, reactorUse):
        self.name = name
        self.maxSpeed = float(maxSpeed)
        self.acceleration = float(acceleration)
        self.reactorUse = int(reactorUse)
