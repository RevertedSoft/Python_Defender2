import pygame
from pygame.locals import *

from . import player

from .globals import *

# this module will display all menus, menus will act as surfaces, and be blitted to the windowSurface each cycle

def shipMenu(playerShip):

    hoveringButton = ''# this is the button the players cursor is currently hovering over
    selectedEquipment = ''# this is the currently selected equipment, if the add button is clicked, it will add this equipment to the players ship
    selectedCategory = 'weapon'

    while True:

        mousePos = pygame.mouse.get_pos()
        
        

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == KEYUP:
                if event.key == K_m:
                    return

            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    if hoveringButton != '':
                        #handle the different button events depending on what the buttons text is (the purpose is related)
                        if hoveringButton.text == 'Add' and selectedEquipment != '':
                            if selectedCategory != 'drone':
                                playerShip.addEquipment(selectedEquipment)
                            else:
                                playerShip.addDrone(selectedEquipment)
                                

                        elif hoveringButton.text == 'Remove':
                            if selectedEquipment != '':
                                if selectedCategory != 'drone':
                                    if selectedEquipment.equipType == 'weapon':
                                        for weapons in playerShip.weaponList:
                                            if selectedEquipment.name == weapons.name:
                                                playerShip.weaponList.remove(weapons)
                                                playerShip.nodesUsed -= 1
                                                break
                                    elif selectedEquipment.equipType == 'reactor':
                                        for reactors in playerShip.reactorList:
                                            if selectedEquipment.name == reactors.name:
                                                playerShip.reactorList.remove(reactors)
                                                playerShip.nodesUsed -= 1
                                                break
                                    elif selectedEquipment.equipType == 'shield':
                                        for shields in playerShip.shieldList:
                                            if selectedEquipment.name == shields.name:
                                                playerShip.shieldList.remove(shields)
                                                playerShip.nodesUsed -= 1
                                                break
                                    elif selectedEquipment.equipType == 'engine':
                                        for engines in playerShip.engineList:
                                            if selectedEquipment.name == engines.name:
                                                playerShip.engineList.remove(engines)
                                                playerShip.nodesUsed -= 1
                                                break
                                            
                                elif selectedCategory == 'drone':
                                    for drones in playerShip.droneList:
                                        if selectedEquipment.name == drones.ship.name:
                                            playerShip.droneList.remove(drones)
                                            playerShip.currentDrones -= 1
                                            break
                        elif hoveringButton.text == 'Weapons':
                            selectedCategory = 'weapon'
                        elif hoveringButton.text == 'Reactors':
                            selectedCategory = 'reactor'
                        elif hoveringButton.text == 'Shields':
                            selectedCategory = 'shield'
                        elif hoveringButton.text == 'Engines':
                            selectedCategory = 'engine'
                        elif hoveringButton.text == 'Drones':
                            selectedCategory = 'drone'
                        else:
                            if selectedCategory == 'weapon':
                                for weapons in WEAPONS[:]:      
                                    if hoveringButton.text == weapons.name:
                                        selectedEquipment = weapons
                                        print(selectedEquipment)
                            elif selectedCategory == 'reactor':
                                for reactors in REACTORS[:]:      
                                    if hoveringButton.text == reactors.name:
                                        selectedEquipment = reactors
                                        print(selectedEquipment)
                            elif selectedCategory == 'shield':
                                for shields in SHIELDS[:]:      
                                    if hoveringButton.text == shields.name:
                                        selectedEquipment = shields
                                        print(selectedEquipment)
                            elif selectedCategory == 'engine':
                                for engines in ENGINES[:]:      
                                    if hoveringButton.text == engines.name:
                                        selectedEquipment = engines
                                        print(selectedEquipment)
                            elif selectedCategory == 'drone':
                                for drones in DRONES[:]:      
                                    if hoveringButton.text == drones.name:
                                        selectedEquipment = drones
                                        print(selectedEquipment)
                            
                    
        # the button list holds all the buttons that are to be tracked in the menu
        buttonList = []

        # set up the ship menu surface, drawing to software surfaces is faster than drawing to hardware
        shipMenuWidth = windowWidth
        shipMenuHeight = windowHeight
        shipMenuSurf = pygame.Surface((shipMenuWidth, shipMenuHeight))
        shipMenuRect = pygame.Rect(0,0, shipMenuWidth, shipMenuHeight)

        # set up the size of the menu's buttons, along with the spacing between themseleves and the borders
        shipMenuButtonSize = int(shipMenuWidth / 20)
        shipMenuButtonSpacing = int(shipMenuButtonSize + 2)

        # set up the x and y margins the equipment buttons will follow
        shipMenuEquipmentXMargin = shipMenuRect.right - shipMenuButtonSpacing
        shipMenuEquipmentYMargin = shipMenuRect.top + shipMenuButtonSpacing

        # set up the x and y margins for the players equipment
        shipMenuPlayerXMargin = shipMenuRect.left + 2
        shipMenuPlayerYMargin = shipMenuRect.top + shipMenuButtonSpacing

        # set up the Add button and the Remove button, these buttons will be used to add and remove equipment to/from the ship
        shipMenuAddButtonRect = pygame.Rect(shipMenuWidth - (shipMenuButtonSize * 2), shipMenuHeight - shipMenuButtonSize, shipMenuButtonSize, shipMenuButtonSize)
        buttonList.append(Button(shipMenuAddButtonRect, 'Add', DARKGREY, BLUE))
        shipMenuRemoveButtonRect = pygame.Rect(shipMenuButtonSize, shipMenuHeight - shipMenuButtonSize, shipMenuButtonSize, shipMenuButtonSize)
        buttonList.append(Button(shipMenuRemoveButtonRect, 'Remove', DARKGREY, RED))

        #make the weapon category button
        shipMenuWeaponButtonRect = pygame.Rect(shipMenuButtonSpacing * 2, 1, shipMenuButtonSize, shipMenuButtonSize)
        buttonList.append(Button(shipMenuWeaponButtonRect, 'Weapons', DARKGREY, RED))

        #make the reactor category button
        shipMenuReactorButtonRect = pygame.Rect(shipMenuButtonSpacing * 3, 1, shipMenuButtonSize, shipMenuButtonSize)
        buttonList.append(Button(shipMenuReactorButtonRect, 'Reactors', DARKGREY, YELLOW))

        #make the shield category button
        shipMenuShieldButtonRect = pygame.Rect(shipMenuButtonSpacing * 4, 1, shipMenuButtonSize, shipMenuButtonSize)
        buttonList.append(Button(shipMenuShieldButtonRect, 'Shields', DARKGREY, BLUE))

        #make the engine category button
        shipMenuEngineButtonRect = pygame.Rect(shipMenuButtonSpacing * 5, 1, shipMenuButtonSize, shipMenuButtonSize)
        buttonList.append(Button(shipMenuEngineButtonRect, 'Engines', DARKGREY, GREEN))

        #make the drone category button
        shipMenuDroneButtonRect = pygame.Rect(shipMenuButtonSpacing * 6, 1, shipMenuButtonSize, shipMenuButtonSize)
        buttonList.append(Button(shipMenuDroneButtonRect, 'Drones', DARKGREY, WHITE))

        # refresh the screen
        shipMenuSurf.fill(GREY)

        buttonCount = 0
        # depending on the selectedCategory, the buttons will be created
        if selectedCategory == 'weapon':
            for weapons in WEAPONS[:]:
                weaponRect = pygame.Rect(shipMenuEquipmentXMargin, shipMenuEquipmentYMargin * buttonCount, shipMenuButtonSize, shipMenuButtonSize)
                weaponButton = Button(weaponRect, weapons.name, DARKGREY, RED)
                buttonList.append(weaponButton)
                buttonCount += 1
            buttonCount = 0
            for weapons in playerShip.weaponList[:]:
                weaponRect = pygame.Rect(shipMenuPlayerXMargin, shipMenuPlayerYMargin * buttonCount, shipMenuButtonSize, shipMenuButtonSize)
                weaponButton = Button(weaponRect, weapons.name, DARKGREY, RED)
                buttonList.append(weaponButton)
                buttonCount += 1

        elif selectedCategory == 'reactor':
            for reactors in REACTORS[:]:
                reactorRect = pygame.Rect(shipMenuEquipmentXMargin, shipMenuEquipmentYMargin * buttonCount, shipMenuButtonSize, shipMenuButtonSize)
                reactorButton = Button(reactorRect, reactors.name, DARKGREY, YELLOW)
                buttonList.append(reactorButton)
                buttonCount += 1
            buttonCount = 0
            for reactors in playerShip.reactorList[:]:
                reactorRect = pygame.Rect(shipMenuPlayerXMargin, shipMenuPlayerYMargin * buttonCount, shipMenuButtonSize, shipMenuButtonSize)
                reactorButton = Button(reactorRect, reactors.name, DARKGREY, YELLOW)
                buttonList.append(reactorButton)
                buttonCount += 1

        elif selectedCategory == 'shield':
            for shields in SHIELDS[:]:
                shieldRect = pygame.Rect(shipMenuEquipmentXMargin, shipMenuEquipmentYMargin * buttonCount, shipMenuButtonSize, shipMenuButtonSize)
                shieldButton = Button(shieldRect, shields.name, DARKGREY, BLUE)
                buttonList.append(shieldButton)
                buttonCount += 1
            buttonCount = 0
            for shields in playerShip.shieldList[:]:
                shieldRect = pygame.Rect(shipMenuPlayerXMargin, shipMenuPlayerYMargin * buttonCount, shipMenuButtonSize, shipMenuButtonSize)
                shieldButton = Button(shieldRect, shields.name, DARKGREY, BLUE)
                buttonList.append(shieldButton)
                buttonCount += 1

        elif selectedCategory == 'engine':
            for engines in ENGINES[:]:
                engineRect = pygame.Rect(shipMenuEquipmentXMargin, shipMenuEquipmentYMargin * buttonCount, shipMenuButtonSize, shipMenuButtonSize)
                engineButton = Button(engineRect, engines.name, DARKGREY, GREEN)
                buttonList.append(engineButton)
                buttonCount += 1
            buttonCount = 0
            for engines in playerShip.engineList[:]:
                engineRect = pygame.Rect(shipMenuPlayerXMargin, shipMenuPlayerYMargin * buttonCount, shipMenuButtonSize, shipMenuButtonSize)
                engineButton = Button(engineRect, engines.name, DARKGREY, GREEN)
                buttonList.append(engineButton)
                buttonCount += 1

        elif selectedCategory == 'drone':
            for drones in DRONES[:]:
                droneRect = pygame.Rect(shipMenuEquipmentXMargin, shipMenuEquipmentYMargin * buttonCount, shipMenuButtonSize, shipMenuButtonSize)
                droneButton = Button(droneRect, drones.name, DARKGREY, WHITE)
                buttonList.append(droneButton)
                buttonCount += 1
            buttonCount = 0
            for drones in playerShip.droneList[:]:
                droneRect = pygame.Rect(shipMenuPlayerXMargin, shipMenuPlayerYMargin * buttonCount, shipMenuButtonSize, shipMenuButtonSize)
                droneButton = Button(droneRect, drones.name, DARKGREY, WHITE)
                buttonList.append(droneButton)
                buttonCount += 1

        buttonFound = False
        for buttons in buttonList[:]:
            if buttons.buttonActive(mousePos):
                hoveringButton = buttons
                buttonFound = True
            elif not buttonFound:
                hoveringButton = ''# if the player isn't hovering over a button, clear the variable

        for buttons in buttonList[:]:# draw each button in the list
            buttons.drawButton(shipMenuSurf)

        #the title text of the menu screen    
        shipMenuTitleText = drawText('Ship Menu', font, shipMenuSurf, shipMenuRect.centerx - 10, 0, GREEN)

        shipNameText = drawText(playerShip.name, font, shipMenuSurf, shipMenuWidth / 8, shipMenuHeight / 4, BLACK)
        shipHealthText = drawText('Hull Strength:' + str(playerShip.hullPoints), font, shipMenuSurf, shipMenuWidth / 8, (shipMenuHeight / 4) + 15, BLACK)
        shipNodesText = drawText('Open Nodes: ' + str(playerShip.hullNodes - playerShip.nodesUsed), font, shipMenuSurf, shipMenuWidth / 8, (shipMenuHeight / 4) + 30, BLACK)
        droneBayText = drawText('Drone Bay: ' + str(playerShip.droneBay - playerShip.currentDrones), font, shipMenuSurf, shipMenuWidth / 8, (shipMenuHeight / 4) + 45, BLACK)
        exitText = drawText('Press the "m" key to exit from the menu.', font, shipMenuSurf, shipMenuRect.centerx - 80,16, GREEN)

        shipMenuRect.right = windowWidth
        shipMenuRect.top = 0

        # blit the menus surface to the hardware surface
        windowSurface.blit(shipMenuSurf, shipMenuRect)

        pygame.display.update()
        fpsClock.tick(FPS)

def welcomeMenu():
    hoveringButton = ''# this is the button the players cursor is currently hovering over
    selectedShip = 'Python'

    while True:
        mousePos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == KEYUP:
                pass

            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    if hoveringButton != '':
                        return hoveringButton

        # the button list holds all the buttons that are to be tracked in the menu
        buttonList = []

        # set up the ship menu surface, drawing to software surfaces is faster than drawing to hardware
        welcomeMenuWidth = windowWidth
        welcomeMenuHeight = windowHeight
        welcomeMenuSurf = pygame.Surface((welcomeMenuWidth, welcomeMenuHeight))
        welcomeMenuRect = pygame.Rect(0,0, welcomeMenuWidth, welcomeMenuHeight)

        # set up the size of the menu's buttons, along with the spacing between themseleves and the borders
        welcomeMenuButtonSize = int(welcomeMenuWidth / 20)
        welcomeMenuButtonSpacing = int(welcomeMenuButtonSize + 2)

        # set up the x and y margins the equipment buttons will follow
        welcomeMenuEquipmentXMargin = welcomeMenuRect.left
        welcomeMenuEquipmentYMargin = welcomeMenuRect.top + welcomeMenuButtonSpacing

        welcomeMenuSurf.fill(GREY)

        buttonCount = 0
        for ships in SHIPS[:]:
            shipRect = pygame.Rect(welcomeMenuEquipmentXMargin, (welcomeMenuEquipmentYMargin * buttonCount) + (welcomeMenuHeight / 8), welcomeMenuButtonSize, welcomeMenuButtonSize)
            shipButton = Button(shipRect, ships.name, DARKGREY, GREEN)
            shipButtonDisplay = drawText('Hull points: %s, Hull nodes: %s, Drone Bay: %s, Hull agility: %s' % (ships.hullPoints, ships.hullNodes, ships.droneBay, ships.hullAgility), font, welcomeMenuSurf, welcomeMenuEquipmentXMargin + welcomeMenuButtonSpacing, (welcomeMenuEquipmentYMargin * buttonCount) + (welcomeMenuHeight / 8) + (welcomeMenuButtonSize / 3), BLACK) 
            buttonList.append(shipButton)
            buttonCount += 1

        buttonFound = False
        for buttons in buttonList[:]:
            if buttons.buttonActive(mousePos):
                hoveringButton = buttons
                buttonFound = True
            elif not buttonFound:
                hoveringButton = ''# if the player isn't hovering over a button, clear the variable

        for buttons in buttonList[:]:# draw each button in the list
            buttons.drawButton(welcomeMenuSurf)

        welcomeMenuTitleText = drawText('Please select a ship to continue.', font, welcomeMenuSurf, 0, 0, GREEN)

        welcomeMenuRect.right = windowWidth
        welcomeMenuRect.top = 0

        # blit the menus surface to the hardware surface
        windowSurface.blit(welcomeMenuSurf, welcomeMenuRect)

        pygame.display.update()
        fpsClock.tick(FPS)
            
        

class Button:
    
    #make a button object
    def __init__(self, rect, text, color, textColor):
        self.rect = rect
        self.text = text
        self.color = color
        self.textColor = textColor

    #check if the button is currently active in respect to the mouse
    def buttonActive(self, mousePos):
        if self.rect.collidepoint(mousePos):
            self.color = LIGHTBLUE
            return True
        else:
            self.color = DARKGREY
            return False

    #draw the button using its attributes
    def drawButton(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        drawText(self.text, font, surface, self.rect.left, self.rect.centery, self.textColor)

    #draw a tooltip near the button
    def drawTooltip(self, surface):
        pass
    
