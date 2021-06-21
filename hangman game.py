#---------------------------------------------------------
# File Name: hangman.py                               
# Description: Starter for Hangman project - ICS3U    
#---------------------------------------------------------
from os import system
import random
import pygame

# initialize global variables/constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED   = (255, 0, 0)
PINK  = (255, 153, 255)
GREEN = (90, 240, 75)
BLUE  = (0, 100, 255)
LIGHT_BLUE = (102, 255, 255)

pygame.init()
bttn_font = pygame.font.SysFont("arial", 20)
guess_font = pygame.font.SysFont("monospace", 24)
clue_font = pygame.font.SysFont("monospace", 16)
#currentScreen = "Category Screen"
usedLetters = ''
base_folder = "d:/Learning/Python/Hangman/"
#winSound = pygame.mixer.Sound("winSound.wav")
#winSound.set_volume(0.2)
alphabet = "ABCDEFGHIJKLMNOPRSTUV"
# button functions
def createButtons():
    x = 98
    y = 400
    buttons = []
    for bttn in range(26):
        buttons.append((x,y))
        x += 42
        if bttn == 12:
            x = 98
            y += 42
    print(buttons)
    return buttons

def drawButtons(buttons):
    for i,xy in enumerate(buttons):
        letterToRender = chr(i + 65)
        if letterToRender in usedLetters and letterToRender not in puzzle2:
            pygame.draw.circle(win, RED, xy, 15, 0)
        elif letterToRender in usedLetters and letterToRender in puzzle2:
            pygame.draw.circle(win, BLUE, xy, 15, 0)
        else:    
            pygame.draw.circle(win, WHITE, xy, 15, 0)
        pygame.draw.circle(win, BLACK, xy, 15, 1)
        letterSurface = bttn_font.render(letterToRender, True, BLACK)
        win.blit(letterSurface,(xy[0]-letterSurface.get_width()//2,xy[1]-letterSurface.get_height()//2))

def clickButton(mp, buttons):
    global usedLetters
    for i,xy in enumerate(buttons):
        a = mp[0] - xy[0]
        b = mp[1] - xy[1]
        c = (a**2 + b**2)**.5
        if c <= 15:
            letter = chr(65 + i)
            print('You clicked the button:', letter)
            return i
    return -1

# hangman image and puzzle functions
def loadHangmanImages():
    hmImages = []
    for imageIndex in range(7):
        fileName = base_folder + 'hangman' + str(imageIndex) + '.png'
        hmImages.append(pygame.image.load(fileName))
    return hmImages

def loadPuzzles():
    puzzles = [[],[],[]]
    puzzleFile =  open(base_folder + 'hangman_puzzles.txt','r')

    for p in puzzleFile:
        nextP = p.strip().split(',')
        pIndex = int(nextP[0])-1
        puzzles[pIndex].append([nextP[1], nextP[2]])

    puzzleFile.close()
    return puzzles

def getRandomPuzzle(pCategory, puzzles):
    randIndex = random.randrange(0, 6)
    randPuzzle = puzzles[pCategory][randIndex]
    print("Puzzle: ", randPuzzle[0])
    print("Clue: ", randPuzzle[1])
    return randPuzzle

#def randomPuzz():
#    while True:
#        pCategory = int(input("Enter Category: "))
#        randIndex = random.randrange(0,6)
#        randPuzzle = puzzles[pCategory][randIndex]

# displaying hangman functions
def initializeGuess(puzzle):
    guess = ''
    for c in puzzle:
        if c == ' ':
            guess += ' '
        else:
            guess += '_'
    return guess

def spacedOut(guess):
    spaceString = ''
    for c in guess:
        spaceString += c + ' '
    return spaceString

def drawGuess():
    guessSurface = guess_font.render(spacedOut(guess), True, BLACK)
    x = (win.get_width() - guessSurface.get_width())//2
    win.blit(guessSurface, (x,270))
    clueSurface = clue_font.render(clue, True, BLACK)
    x = (win.get_width() - clueSurface.get_width())//2
    win.blit(clueSurface,(x,320))

def updateGuess(letterGuess, guess, puzzle):
    letter = chr(letterGuess + 65)
    newGuess = ''
    global wrongCount
    if letter not in puzzle and wrongCount < 6 and letter in alphabet:
        wrongCount += 1
    for c in enumerate(puzzle):
        print(c)
        if letter == c[1]:
            newGuess += c[1]
        else:
            newGuess += guess[c[0]]
    return newGuess

# draw rectangular buttons
categoryButtons = [[(56,200,160,80), 'Books'],
                   [(271,200,160,80), 'English Idioms'],
                   [(486,200,160,80), 'Pre-2000s Bands']]
menuButtons = [[(56,60,160,80), 'Menu'],
               [(56,160,160,80), 'Play Again']]

def drawrRectangularButtons(buttons):
    for button in buttons:
        pygame.draw.rect(win, BLUE, button[0], 0)
        pygame.draw.rect(win, WHITE, button[0], 3)
        text_surface = bttn_font.render(button[1], True, WHITE)
        x = button[0][0] + (button[0][2] - text_surface.get_width()) // 2
        y = button[0][1] + (button[0][3] - text_surface.get_height()) // 2
        win.blit(text_surface, (x, y))

def categoryButtonClick(mp, buttons):
    for i, b in enumerate(buttons):
        if pygame.Rect(b[0]).collidepoint(mp):
            return i
    return -1

def drawFinal():
    message = ''
    global gameOver
    if wrongCount == 6:
        message = 'YOU LOST!'
        gameOver = True
    if guess == puzzle2:
        message = 'YOU WON!'
        gameOver = True
        
    surface = guess_font.render(message, True, BLACK)
    x = win.get_width() - surface.get_width() - 50
    win.blit(surface, (x, 220))

# function that redraws all objects
def redrawGameWindow(buttons, screen):
    win.fill(GREEN)
    # code to draw things goes here
    if screen == True: # currentScreen == "Category Screen":
        drawrRectangularButtons(categoryButtons)
    else:
        #currentScreen = "Game Screen"
        drawButtons(buttons)
        drawGuess()
        drawFinal()
        win.blit(hmImages[wrongCount],(270,20))
        if gameOver == True:
            drawrRectangularButtons(menuButtons)

    pygame.display.update()
    
# the main program begins here
win = pygame.display.set_mode((700,480))
buttons = createButtons()
wrongCount = 0
puzzles = loadPuzzles()
#buttonIndex = []
hmImages = loadHangmanImages()
inPlay = True
categoryScreen = True
randomPuzzle = []
guess = ''
puzzle2 = ''
gameOver = False
    
while inPlay:
    redrawGameWindow(buttons, categoryScreen)
    pygame.time.delay(10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            inPlay = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            clickPos = pygame.mouse.get_pos()

            if gameOver == True:
                break
            buttonIndex = clickButton(clickPos, buttons)
            
            clickedLetter = chr(65 + buttonIndex)
            if clickedLetter in usedLetters:
                break
            else:
                usedLetters += clickedLetter
            
            if categoryScreen != True: # "Game Screen":
                guess = updateGuess(buttonIndex, guess, puzzle2)
            else: # "Category Screen"
                category = categoryButtonClick(clickPos, categoryButtons)
                randomPuzzle = getRandomPuzzle(category, puzzles)
                puzzle2 = randomPuzzle[0]
                clue = randomPuzzle[1]
                guess = initializeGuess(puzzle2)
                categoryScreen = False

pygame.quit()
