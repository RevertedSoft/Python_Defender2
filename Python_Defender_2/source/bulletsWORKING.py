import pygame, random
from pygame.locals import *

from . import player
from .globals import *

class Bullet():
    self.positionX = ''
    self.positionY = ''
    self.speedX = ''
    self.speedY = ''
    self.rect = ''

    def __init__(self, source, weapon, size, direction):
        #the bullet aquires its location from the weapon, passing the source may become unneccesary once i implement hardpoints for the weapons
        self.positionX = weapon.hullRect.centerx
        self.positionY = weapon.hullRect.centery
        self.speedX = 0
        self.speedY = (weapon.projSpeed)
        self.damage = weapon.damage
        self.size = size
        self.type = weapon.weaponType
        self.weaponSource = weapon
        self.lifeTime = self.weaponSource.fireRate
        self.direction = direction

        self.rect = pygame.Rect(self.positionX, self.positionY, self.size, self.size)
        
    def move(self):
        self.positionX += self.speedX
        if self.direction == 'up':
            self.positionY -= self.speedY
        elif self.direction == 'down':
            self.positionY += self.speedY

        self.rect = pygame.Rect(self.positionX, self.positionY, self.size, self.size)

    def drawBullet(self, surface):
        pygame.draw.rect(surface, RED, self.rect)

    def didBulletHit(self, rect):
        if self.rect.colliderect(rect):
            return True
        else:
            return False

    def remove(self):
        del(self)

class Laser(Bullet):#build a subclass for lasers

    def __init__(self, source, weapon, size, direction):
        Bullet.__init__(self, source, weapon, size, direction)
        self.rect = pygame.Rect(self.positionX, 0, self.size, windowHeight)
        if self.direction == 'up':
            self.rect.bottom = source.rect.top
        elif self.direction == 'down':
            self.rect.bottom = source.rect.bottom

    def didBulletHit(self, rect):
        if self.rect.centerx >= rect.left and self.rect.centerx <= rect.right:
            if self.direction == 'up':
                self.rect = pygame.Rect(self.weaponSource.hullRect.centerx, self.positionY, self.size, -(abs(self.weaponSource.hullRect.top) - (rect.bottom)))
            elif self.direction == 'down':
                self.rect = pygame.Rect(self.weaponSource.hullRect.centerx, self.positionY, self.size, -(abs(self.weaponSource.hullRect.bottom) - (rect.top)))
            return True
        else:
            return False
    

class Missile():# missiles are created as a seperate class, they act very differently from bullets and lasers
    self.xSpeed = 0
    self.ySpeed = 0

    def __init__(self, source, weapon, size, direction):
        self.positionX = weapon.hullRect.centerx
        self.positionY = weapon.hullRect.centery
        self.source = source
        self.weapon = weapon
        self.size = size
        self.direction = direction
        self.acceleration = weapon.acceleration
        self.missileType = weapon.missileType
        self.maxSpeed = weapon.projSpeed
        self.damage = weapon.damage

        self.rect = pygame.Rect(self.positionX, self.positionY, self.size, self.size)

    def move(self):

        if self.direction == 'up':
            self.rect = pygame.Rect(self.weaponSource.hullRect.centerx, self.positionY, self.size, -windowHeight)
        elif self.direction == 'down':
            self.rect = pygame.Rect(self.weaponSource.hullRect.centerx, self.positionY, self.size, windowHeight)
        self.lifeTime -= 1

    def moveMissile(self):
        if self.direction == 'up':
            self.positionY -= self.ySpeed
            self.rect.top = self.positionY
        elif self.direction == 'down':
            self.positionY += self.ySpeed
            self.rect.bottom = self.positionY
        self.positionX += self.xSpeed
        self.rect.centerx = self.positionX

    def drawMissile(self, surface):
        pygame.draw.rect(surface, RED, self.rect)

    def didMissileHit(self, rect):
        if self.rect.colliderect(rect):
            return True
        else:
            return False

def LightMissile(Missile):

    def __init__(self, source, weapon, size, direction):

        Missile.__init__(self, source, weapon, size, direction)
        
    
    def applyForce(self):
        if abs(self.ySpeed) < self.maxSpeed:
            self.ySpeed += self.acceleration

        if self.targetFlag != -1:
            if self.direction == 'up':
                if abs(self.positionY - self.target.positionY) < windowHeight / 4:
                #if self.positionY < windowHeight / 4:
                    if self.target.rect.centerx > self.rect.centerx and abs(self.xSpeed) < self.maxSpeed:
                        self.xSpeed += (self.acceleration*2)
                    elif self.target.rect.centerx < self.rect.centerx and abs(self.xSpeed) < self.maxSpeed:
                        self.xSpeed -= (self.acceleration*2)
            elif self.direction == 'down':
                if abs(self.positionY - self.target.positionY) < windowHeight / 4:
                #if self.positionY > (windowHeight - (windowHeight / 4)):
                    if self.target.rect.centerx > self.rect.centerx and abs(self.xSpeed) < self.maxSpeed:
                        self.xSpeed += (self.acceleration)
                    elif self.target.rect.centerx < self.rect.centerx and abs(self.xSpeed) < self.maxSpeed:
                        self.xSpeed -= (self.acceleration)

    def getTarget(self, targets):
        self.targetFlag = -1
        for enemies in targets[:]:
            if self.targetFlag == -1:
                self.targetFlag = 0
                self.target = enemies
            elif (enemies.acceleration * enemies.hullAgility) > (self.target.acceleration * self.target.hullAgility):
                self.target = enemies

def DummyMissile(Missile):

    def __init__(self, source, weapon, size, direction):

        Missile.__init__(self, source, weapon, size, direction)

    def applyForce(self):
        if abs(self.ySpeed) < self.maxSpeed:
            self.ySpeed += self.acceleration

        if self.targetFlag != -1:
            if self.target.rect.centerx > self.rect.centerx and abs(self.xSpeed) < self.maxSpeed:
                self.xSpeed += (self.acceleration / 12)
            if self.target.rect.centerx < self.rect.centerx and abs(self.xSpeed) < self.maxSpeed:
                self.xSpeed -= (self.acceleration / 12)

    def getTarget(self, targets):
        self.targetFlag = -1
        for enemies in targets[:]:
            if self.targetFlag == -1:
                self.targetFlag = 0
                self.target = enemies
            elif (enemies.acceleration * enemies.hullAgility) < (self.target.acceleration * self.target.hullAgility):
                self.target = enemies
            
                
