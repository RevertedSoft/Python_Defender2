print ('Importing libraries.')
import os, sys, pygame, copy

from decimal import Decimal
from pygame.locals import *
from . import player,ship,menus,bullets,equipment,aiship,aiscripts

from .globals import *


def main():
    #initialize pygame
    ('Initializing Pygame.')
    pygame.init()

    #add an enemy[TEST]
    computerList = []
    theEnemy1 = ship.findShip('Python', SHIPS)
    enemyShip1 = aiship.AiShip((windowWidth/2, 10), copy.deepcopy(theEnemy1), [copy.deepcopy(WEAPONS[0])], [copy.deepcopy(REACTORS[0])], [copy.deepcopy(SHIELDS[0])], [copy.deepcopy(ENGINES[0])], 'aggresor', 'enemy')
    computerList.append(enemyShip1)
    theEnemy2 = ship.findShip('Niohoggr', SHIPS)
    enemyShip2 = aiship.AiShip((windowWidth/3, 10), copy.deepcopy(theEnemy2), [copy.deepcopy(WEAPONS[5]), copy.deepcopy(WEAPONS[5]), copy.deepcopy(WEAPONS[5])], [copy.deepcopy(REACTORS[2]),copy.deepcopy(REACTORS[2]),copy.deepcopy(REACTORS[2]),copy.deepcopy(REACTORS[2]),copy.deepcopy(REACTORS[2]),copy.deepcopy(REACTORS[2]),copy.deepcopy(REACTORS[2])], [copy.deepcopy(SHIELDS[3]),copy.deepcopy(SHIELDS[3]), copy.deepcopy(SHIELDS[3]), copy.deepcopy(SHIELDS[3])], [copy.deepcopy(ENGINES[2]), copy.deepcopy(ENGINES[2])], 'cautious', 'enemy')
    computerList.append(enemyShip2)
    theEnemy3 = ship.findShip('Fafnir', SHIPS)
    enemyShip3 = aiship.AiShip((windowWidth/4, 10), copy.deepcopy(theEnemy3), [copy.deepcopy(WEAPONS[4]), copy.deepcopy(WEAPONS[4]), copy.deepcopy(WEAPONS[4])], [copy.deepcopy(REACTORS[2]),copy.deepcopy(REACTORS[2]),copy.deepcopy(REACTORS[2]),copy.deepcopy(REACTORS[2]),copy.deepcopy(REACTORS[2])], [copy.deepcopy(SHIELDS[2]), copy.deepcopy(SHIELDS[2]), copy.deepcopy(SHIELDS[2])], [copy.deepcopy(ENGINES[2])], 'aggresor','enemy')
    computerList.append(enemyShip3)

    while True:
        # set up the player object
        playerObj = player.Player((int(windowWidth / 2) - (15), windowHeight - 60))
        # take the player to the welcome menu, where they can select a ship
        playerShip = ship.findShip(menus.welcomeMenu().text, SHIPS)
        playerObj.setupShip(playerShip)

        # take the player to the ship menu, where they can select equipment for the ship
        menus.shipMenu(playerObj)
        # calculate the players attributes as they come out of the menu
        playerObj.getShipSpeed()
        playerObj.getShipReactorPower()
        playerObj.getShipShieldPower()

        while True:

            #combatSurf.fill(BLACK)
            combatSurf.blit(backgroundRect, (0,0))

            for event in pygame.event.get():
                if event.type == QUIT:
                    terminate()

                if event.type == KEYDOWN:
                    if event.key == K_a:
                        playerObj.movingLeft = True
                        playerObj.movingRight = False

                    if event.key == K_d:
                        playerObj.movingRight = True
                        playerObj.movingLeft = False

                    if event.key == K_SPACE:
                        playerObj.isFiring = True


                if event.type == KEYUP:
                    if event.key == K_m:
                        menus.shipMenu(playerObj)
                        playerObj.getShipSpeed()
                        playerObj.getShipReactorPower()
                        playerObj.getShipShieldPower()


                    if event.key == K_a:
                        playerObj.movingLeft = False

                    if event.key == K_d:
                        playerObj.movingRight = False

                    if event.key == K_SPACE:
                        playerObj.isFiring = False

                        
            #move the players ship and apply any changes to capacitor, shields, and speed as needed
            playerObj.rechargeShields()
            playerObj.rechargeCapacitor()
            playerObj.changeSpeed()
            playerObj.move(windowWidth, windowHeight)

            #move the computer ships and apply any changes to capacitor, shields, and speed as needed
            for computers in computerList[:]:
                computers.rechargeShields()
                computers.rechargeCapacitor()
                computers.changeSpeed()
                computers.move(windowWidth, windowHeight)
                computers.getTarget([playerObj])
                aiscripts.aiBehaviour(computers)
            #move the computer ships and apply any changes to capacitor, shields, and speed as needed
            for drones in playerObj.droneList[:]:
                drones.rechargeShields()
                drones.rechargeCapacitor()
                drones.changeSpeed()
                drones.move(windowWidth, windowHeight)
                drones.getTarget(computerList)
                aiscripts.aiBehaviour(drones)
                
            # add bullet objects if the player is firing
            for weapons in playerObj.weaponList[:]:
                weapons.currentReload += 1
                if playerObj.isFiring:
                    if weapons.currentReload >= weapons.fireRate and weapons.reactorUse <= playerObj.currentCapacitor:
                        if weapons.weaponType == 'cannon' or weapons.weaponType == 'laser':
                            playerObj.bulletList.append(bullets.Bullet(playerObj, weapons, 3, 'up'))
                        if weapons.weaponType == 'missile':# and len(computerList) > 0:
                            playerObj.missileList.append(bullets.Missile(computers, weapons, 5, 'up'))
                        playerObj.currentCapacitor -= weapons.reactorUse
                        weapons.currentReload = 0
                    #end if statement
                #end if statement

            #move and draw the bullets, remove if off screen, move before adding so that lasers will fire off the ship
            for bullet in playerObj.bulletList[:]:
                bulletRemoved = False # this is to prevent the list from trying to remove a bullet twice... which causes a crash
                #if bullet.type == 'cannon':
                if bullet.type == 'cannon':
                    bullet.moveBullet()
                elif bullet.type == 'laser':# lasers behave differently than cannon porjectiles
                    bullet.moveLaser()
                for computers in computerList[:]:
                    if computers.currentShield > 0:#if the computers shield is active, hit that first
                        if bullet.didBulletHit(computers.shieldRect):
                            computers.currentShield -= bullet.damage
                            if bullet.type == 'cannon' and not bulletRemoved:
                                playerObj.bulletList.remove(bullet)#remove the bullet if it hit
                                bulletRemoved = True
                            #end if statement
                            if computers.currentShield <= 0 and computers.shieldResetCount <= 0:
                                computers.shieldResetCount = FPS * 3# this sets a timer, the shield wont recharge til the timer is back to 0
                            #end if statement
                        #end if statement
                    elif bullet.didBulletHit(computers.rect):
                        computers.hullPoints -= bullet.damage
                        if bullet.type == 'cannon' and not bulletRemoved:
                            playerObj.bulletList.remove(bullet)
                            bulletRemoved = True
                        #end if statement
                    #end if statement
                #end for statement

                if bullet.type == 'laser':
                    if bullet.lifeTime <= 0:
                        playerObj.bulletList.remove(bullet)# this will remove lasers if their lifetime drops to 0 or less
                        bulletRemoved = True
                    #end if statement
                #end if statement
                if bullet.positionY < -10 and not bulletRemoved:
                    playerObj.bulletList.remove(bullet)# this removes any bullets that are off the screen, don't need to track these anymore
                    bullet.remove()
                #end if statement
                bullet.drawBullet(combatSurf)# draw the bullet if it has not been removed
            #end for loop

            #move missiles and check for hits
            for missile in playerObj.missileList[:]:
                missileRemoved = False

                missile.getTarget(computerList)
                missile.applyForce()
                missile.moveMissile()

                for computers in computerList[:]:
                    if computers.currentShield > 0:
                        if missile.didMissileHit(computers.shieldRect):
                            if not missileRemoved:
                                computers.currentShield -= missile.damage
                            
                                playerObj.missileList.remove(missile)
                                missileRemoved = True

                                if computers.currentShield <= 0 and computers.shieldResetCount <= 0:
                                    computers.shieldResetCount = FPS * 3# this sets a timer, the shield wont recharge til the timer is back to 0

                    elif missile.didMissileHit(computers.rect):
                        if not missileRemoved:
                            computers.hullPoints -= missile.damage
                            playerObj.missileList.remove(missile)
                            missileRemoved = True

                if missile.positionY < -10 and not missileRemoved:
                    playerObj.missileList.remove(missile)

                missile.drawMissile(combatSurf)
                        

#####################################################AI WEAPON TEST#############################################################################
            # add bullet objects if the player is firing
            for computers in computerList[:]:
                for weapons in computers.weaponList[:]:
                    weapons.currentReload += 1
                    if computers.isFiring:
                        if weapons.currentReload >= weapons.fireRate and weapons.reactorUse <= computers.currentCapacitor:
                            if weapons.weaponType == 'cannon' or weapons.weaponType == 'laser':
                                computers.bulletList.append(bullets.Bullet(computers, weapons, 3, 'down'))
                            if weapons.weaponType == 'missile':
                                computers.missileList.append(bullets.Missile(computers, weapons, 5, 'down'))
                            computers.currentCapacitor -= weapons.reactorUse
                            weapons.currentReload = 0
                        #end if statement
                    #end if statement

                #move and draw the bullets, remove if off screen, move before adding so that lasers will fire off the ship
                for bullet in computers.bulletList[:]:
                    bulletRemoved = False # this is to prevent the list from trying to remove a bullet twice... which causes a crash
                    #if bullet.type == 'cannon':
                    if bullet.type == 'cannon':
                        bullet.moveBullet()
                    elif bullet.type == 'laser':# lasers behave differently than cannon porjectiles
                        bullet.moveLaser()
                    ##for computers in computerList[:]:
                    if playerObj.currentShield > 0:#if the computers shield is active, hit that first
                        if bullet.didBulletHit(playerObj.shieldRect):
                            playerObj.currentShield -= bullet.damage
                            if bullet.type == 'cannon' and not bulletRemoved:
                                computers.bulletList.remove(bullet)#remove the bullet if it hit
                                bulletRemoved = True
                            #end if statement
                            if playerObj.currentShield <= 0 and playerObj.shieldResetCount <= 0:
                                playerObj.shieldResetCount = FPS * 3# this sets a timer, the shield wont recharge til the timer is back to 0
                            #end if statement
                        #end if statement
                    elif bullet.didBulletHit(playerObj.rect):
                        playerObj.hullPoints -= bullet.damage
                        if bullet.type == 'cannon' and not bulletRemoved:
                            computers.bulletList.remove(bullet)
                            bulletRemoved = True
                    for drones in playerObj.droneList[:]:#Check if they hit drones
                        if drones.currentShield > 0:#if the computers shield is active, hit that first
                            if bullet.didBulletHit(drones.shieldRect):
                                drones.currentShield -= bullet.damage
                                if bullet.type == 'cannon' and not bulletRemoved:
                                    computers.bulletList.remove(bullet)#remove the bullet if it hit
                                    bulletRemoved = True
                                #end if statement
                                if drones.currentShield <= 0 and drones.shieldResetCount <= 0:
                                    drones.shieldResetCount = FPS * 3# this sets a timer, the shield wont recharge til the timer is back to 0
                                #end if statement
                            #end if statement
                        elif bullet.didBulletHit(drones.rect):
                            drones.hullPoints -= bullet.damage
                            if bullet.type == 'cannon' and not bulletRemoved:
                                computers.bulletList.remove(bullet)
                                bulletRemoved = True
                        #end if statement
                    #end if statement
                #end for statement

                    if bullet.type == 'laser':
                        if bullet.lifeTime <= 0:
                            computers.bulletList.remove(bullet)# this will remove lasers if their lifetime drops to 0 or less
                            bulletRemoved = True
                        #end if statement
                    #end if statement
                    if bullet.positionY > windowHeight + 10 and not bulletRemoved:
                        computers.bulletList.remove(bullet)# this removes any bullets that are off the screen, don't need to track these anymore
                        bullet.remove()
                    #end if statement
                    bullet.drawBullet(combatSurf)# draw the bullet if it has not been removed
            #end for loop

                #move missiles and check for hits
                for missile in computers.missileList[:]:
                    missileRemoved = False

                    missile.getTarget([playerObj])
                    missile.applyForce()
                    missile.moveMissile()

                    #for computers in computerList[:]:
                    if playerObj.currentShield > 0:
                        if missile.didMissileHit(playerObj.shieldRect):
                            if not missileRemoved:
                                playerObj.currentShield -= missile.damage
                            
                                computers.missileList.remove(missile)
                                missileRemoved = True

                                if playerObj.currentShield <= 0 and playerObj.shieldResetCount <= 0:
                                    playerObj.shieldResetCount = FPS * 3# this sets a timer, the shield wont recharge til the timer is back to 0

                    elif missile.didMissileHit(playerObj.rect):
                        if not missileRemoved:
                            playerObj.hullPoints -= missile.damage
                            computers.missileList.remove(missile)
                            missileRemoved = True

                    for drones in playerObj.droneList[:]:
                        if drones.currentShield > 0:
                            if missile.didMissileHit(drones.shieldRect):
                                if not missileRemoved:
                                    drones.currentShield -= missile.damage
                                
                                    computers.missileList.remove(missile)
                                    missileRemoved = True

                                    if drones.currentShield <= 0 and drones.shieldResetCount <= 0:
                                        drones.shieldResetCount = FPS * 3# this sets a timer, the shield wont recharge til the timer is back to 0

                        elif missile.didMissileHit(drones.rect):
                            if not missileRemoved:
                                drones.hullPoints -= missile.damage
                                computers.missileList.remove(missile)
                                missileRemoved = True

                    if missile.positionY < -10 and not missileRemoved:
                        playerObj.missileList.remove(missile)

                    missile.drawMissile(combatSurf)

#####################################################AI WEAPON TEST#############################################################################

#####################################################AI WEAPON TEST#############################################################################
            # add bullet objects if the player is firing
            for drones in playerObj.droneList[:]:
                for weapons in drones.weaponList[:]:
                    weapons.currentReload += 1
                    if drones.isFiring:
                        if weapons.currentReload >= weapons.fireRate and weapons.reactorUse <= drones.currentCapacitor:
                            if weapons.weaponType == 'cannon' or weapons.weaponType == 'laser':
                                drones.bulletList.append(bullets.Bullet(drones, weapons, 3, 'up'))
                            if weapons.weaponType == 'missile':
                                drones.missileList.append(bullets.Missile(computers, weapons, 5, 'up'))
                            drones.currentCapacitor -= weapons.reactorUse
                            weapons.currentReload = 0
                        #end if statement
                    #end if statement

                #move and draw the bullets, remove if off screen, move before adding so that lasers will fire off the ship
                for bullet in drones.bulletList[:]:
                    bulletRemoved = False # this is to prevent the list from trying to remove a bullet twice... which causes a crash
                    #if bullet.type == 'cannon':
                    if bullet.type == 'cannon':
                        bullet.moveBullet()
                    elif bullet.type == 'laser':# lasers behave differently than cannon porjectiles
                        bullet.moveLaser()
                    for computers in computerList[:]:
                        ##for computers in computerList[:]:
                        if computers.currentShield > 0:#if the computers shield is active, hit that first
                            if bullet.didBulletHit(computers.shieldRect):
                                computers.currentShield -= bullet.damage
                                if bullet.type == 'cannon' and not bulletRemoved:
                                    drones.bulletList.remove(bullet)#remove the bullet if it hit
                                    bulletRemoved = True
                                #end if statement
                                if computers.currentShield <= 0 and computers.shieldResetCount <= 0:
                                    computers.shieldResetCount = FPS * 3# this sets a timer, the shield wont recharge til the timer is back to 0
                                #end if statement
                            #end if statement
                        elif bullet.didBulletHit(computers.rect):
                            computers.hullPoints -= bullet.damage
                            if bullet.type == 'cannon' and not bulletRemoved:
                                drones.bulletList.remove(bullet)
                                bulletRemoved = True
                            #end if statement
                        #end if statement
                    #end for statement

                    if bullet.type == 'laser':
                        if bullet.lifeTime <= 0:
                            drones.bulletList.remove(bullet)# this will remove lasers if their lifetime drops to 0 or less
                            bulletRemoved = True
                        #end if statement
                    #end if statement
                    if bullet.positionY > windowHeight + 10 and not bulletRemoved:
                        drones.bulletList.remove(bullet)# this removes any bullets that are off the screen, don't need to track these anymore
                        bullet.remove()
                    #end if statement
                    bullet.drawBullet(combatSurf)# draw the bullet if it has not been removed
            #end for loop

                #move missiles and check for hits
                for missile in drones.missileList[:]:
                    missileRemoved = False

                    missile.getTarget(computerList)
                    missile.applyForce()
                    missile.moveMissile()

                    for computers in computerList[:]:
                        if computers.currentShield > 0:
                            if missile.didMissileHit(computers.shieldRect):
                                if not missileRemoved:
                                    computers.currentShield -= missile.damage
                                
                                    drones.missileList.remove(missile)
                                    missileRemoved = True
                                    break

                                    if computers.currentShield <= 0 and computers.shieldResetCount <= 0:
                                        computers.shieldResetCount = FPS * 3# this sets a timer, the shield wont recharge til the timer is back to 0

                        elif missile.didMissileHit(computers.rect):
                            if not missileRemoved:
                                computers.hullPoints -= missile.damage
                                drones.missileList.remove(missile)
                                missileRemoved = True
                                break

                        if missile.positionY < -10 and not missileRemoved:
                            drones.missileList.remove(missile)
                            break

                        missile.drawMissile(combatSurf)

            for computers in computerList[:]:
                if computers.hullPoints <= 0:# if any ships hull points are less than 0, destroy them
                    computerList.remove(computers)
                    pass
                pygame.draw.rect(combatSurf, GREEN, computers.rect)# draw the computer
                if computers.currentShield > 0:# if the computer has a shield, draw that too
                    pygame.draw.circle(combatSurf, BLUE, computers.shieldPosition, computers.shieldRadius, 1)
                #end if statement
            #end for loop

            for drones in playerObj.droneList[:]:
                if drones.hullPoints <= 0:# if any ships hull points are less than 0, destroy them
                    playerObj.droneList.remove(drones)
                    playerObj.currentDrones -= 1
                    pass
                pygame.draw.rect(combatSurf, WHITE, drones.rect)# draw the computer
                if drones.currentShield > 0:# if the computer has a shield, draw that too
                    pygame.draw.circle(combatSurf, BLUE, drones.shieldPosition, drones.shieldRadius, 1)
                #end if statement
            #end for loop

            pygame.draw.rect(combatSurf, GREY, playerObj.rect)# draw the players ship
            
            if playerObj.currentShield > 0:# if the players shield is active, draw that too
                pygame.draw.circle(combatSurf, BLUE, playerObj.shieldPosition, playerObj.shieldRadius, 1)
            #end if statement

            # draw a rect to the combat surface to display the reactors level
            if playerObj.currentCapacitor > 0:
                reactorRectLength = ((playerObj.currentCapacitor / playerObj.maxCapacitor) * 100)
                pygame.draw.rect(combatSurf, YELLOW, pygame.Rect(0,windowHeight - 16,reactorRectLength,15))
            #end if statement
            # draw a rect to the combat surface to display the shields level
            if playerObj.currentShield > 0:
                shieldRectLength = ((playerObj.currentShield / playerObj.maxShield) * 100)
                pygame.draw.rect(combatSurf, BLUE, pygame.Rect(110,windowHeight - 16,shieldRectLength,15))
            #end if statement

            windowSurface.blit(combatSurf, combatSurfRect)# blit the combat surface to the windowSurface

            pygame.display.update()
            fpsClock.tick(FPS)

