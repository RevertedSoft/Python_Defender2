import pygame
from pygame.locals import *

from .globals import *

def aiBehaviour(entity):
    if entity.target != '':
    
        if entity.behaviour == 'aggresor':# this is the aggresor script, this script is balls out aggressive
            
            if entity.rect.centerx < entity.target.rect.centerx:# - target.ship.hullWidth:
                entity.movingRight = True
                entity.movingLeft = False
            elif entity.rect.centerx > entity.target.rect.centerx:# + target.ship.hullWidth:
                entity.movingLeft = True
                entity.movingRight = False
            if entity.currentSpeed >= ((entity.acceleration * entity.hullAgility) * abs(entity.rect.centerx - entity.target.rect.centerx))*30:
                entity.movingLeft = False
                entity.movingRight = False
            if entity.facing == 'down':
                if entity.rect.bottom < (windowHeight - (windowHeight/4)) - entity.hullHeight:
                    entity.movingDown = True
            elif entity.facing == 'up':
                #pass##################NEED TO ADD AI HERE
                if entity.rect.top > (windowHeight - (windowHeight /4)) + entity.hullHeight:
                    entity.movingUp = True
            if entity.rect.centerx > (entity.target.rect.left - (entity.target.hullWidth * 2)) and entity.rect.centerx < (entity.target.rect.right + (entity.target.hullWidth * 2)):
                entity.isFiring = True
            else:
                entity.isFiring = False

        if entity.behaviour == 'cautious':# this is the cautious script

            if entity.currentShield >= (entity.maxShield / 2):# the ai will move to attack while it has at least 50% shields
                if entity.rect.centerx < entity.target.rect.centerx:# - target.ship.hullWidth:
                    entity.movingRight = True
                    entity.movingLeft = False
                elif entity.rect.centerx > entity.target.rect.centerx:# + target.ship.hullWidth:
                    entity.movingLeft = True
                    entity.movingRight = False
                if entity.currentSpeed >= ((entity.acceleration * entity.hullAgility) * abs(entity.rect.centerx - entity.target.rect.centerx))*30:
                    entity.movingLeft = False
                    entity.movingRight = False

            else: # if the shields are bellow 50% the ai will try to move away
                if entity.rect.centerx < entity.target.rect.centerx:# - target.ship.hullWidth:
                    entity.movingRight = False
                    entity.movingLeft = True
                elif entity.rect.centerx > entity.target.rect.centerx:# + target.ship.hullWidth:
                    entity.movingLeft = False
                    entity.movingRight = True
                

            if entity.currentCapacitor > (entity.maxCapacitor / 4): #the ai will try to reserve capacitor for reacharging its shields
                if entity.rect.centerx > (entity.target.rect.left - (entity.target.hullWidth * 2)) and entity.rect.centerx < (entity.target.rect.right + (entity.target.hullWidth * 2)):
                    entity.isFiring = True
                else:
                    entity.isFiring = False
            else:
                entity.isFiring = False

        if entity.behaviour == 'basic':# this is the cautious script

            #if entity.currentShield >= (entity.maxShield / 2):# the ai will move to attack while it has at least 50% shields
            if entity.rect.centerx < entity.target.rect.centerx:# - target.ship.hullWidth:
                entity.movingRight = True
                entity.movingLeft = False
            elif entity.rect.centerx > entity.target.rect.centerx:# + target.ship.hullWidth:
                entity.movingLeft = True
                entity.movingRight = False
            if entity.currentSpeed >= ((entity.acceleration * entity.hullAgility) * abs(entity.rect.centerx - entity.target.rect.centerx))*30:
                entity.movingLeft = False
                entity.movingRight = False

    ##    else: # if the shields are bellow 50% the ai will try to move away
    ##        if entity.rect.centerx < target.rect.centerx:# - target.ship.hullWidth:
    ##            entity.movingRight = False
    ##            entity.movingLeft = True
    ##        elif entity.rect.centerx > target.rect.centerx:# + target.ship.hullWidth:
    ##            entity.movingLeft = False
    ##            entity.movingRight = True
                

            if entity.currentCapacitor > (entity.maxCapacitor / 4): #the ai will try to reserve capacitor for reacharging its shields
                if entity.rect.centerx > (entity.target.rect.left - (entity.target.hullWidth * 2)) and entity.rect.centerx < (entity.target.rect.right + (entity.target.hullWidth * 2)):
                    entity.isFiring = True
                else:
                    entity.isFiring = False
            else:
                entity.isFiring = False
