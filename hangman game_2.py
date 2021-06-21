# Header ------------------------------------------------
# Program: Hangman Game
# Author: Liza Nisenbaum
# Date: June 21, 2021                               
# Description: This program is a Hangman game
#---------------------------------------------------------
import pygame
pygame.init()
import random
 
# initialize global variables/constants 
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED   = (255, 0, 0)
PINK  = (255, 153, 255)
GREEN = (90, 240, 100)
PURPLE = (141, 128, 186)
DARK_PURPLE  = (140, 85, 170)
LIGHT_BLUE = (150, 230, 255)

bttn_font = pygame.font.SysFont("arial", 20)
guess_font = pygame.font.SysFont("monospace", 24)
clue_font = pygame.font.SysFont("monospace", 16)
usedLetters = ""
usedPuzzles = []
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
base_folder = "d:/Learning/Python/Hangman/"
#winSound = pygame.mixer.Sound("winSound.wav")
#winSound.set_volume(0.2)
#loseSound = pygame.mixer.Sound("loseSound.wav")
#loseSound.set_volume(0.2)

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
    return buttons

def drawButtons(buttons):
    for i,xy in enumerate(buttons):
        pygame.draw.circle(win, WHITE, xy, 15, 0)
        pygame.draw.circle(win, BLACK, xy, 15, 1)
        letterToRender = chr(i+65)
        if letterToRender in usedLetters and letterToRender not in puzzle2:
            pygame.draw.circle(win, RED, xy, 15, 0)
            pygame.draw.circle(win, BLACK, xy, 15, 1)
            letterSurface = bttn_font.render(letterToRender, True, BLACK)
            win.blit(letterSurface,(xy[0]-letterSurface.get_width()//2,xy[1]-letterSurface.get_height()//2))
            
        elif letterToRender in usedLetters and letterToRender in puzzle2:
            pygame.draw.circle(win, PINK, xy, 15, 0)
            pygame.draw.circle(win, BLACK, xy, 15, 1)
            letterSurface = bttn_font.render(letterToRender, True, BLACK)
            win.blit(letterSurface,(xy[0]-letterSurface.get_width()//2,xy[1]-letterSurface.get_height()//2))
        else:
            hover = pygame.mouse.get_pos()
            a = hover[0] - xy[0]
            b = hover[1] - xy[1]
            c = (a**2 + b**2)**.5
            if c <= 15:
                pygame.draw.circle(win,DARK_PURPLE,xy,15,0)
                pygame.draw.circle(win, BLACK, xy, 15, 1)
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
            letter = chr(65+i)
            print('You clicked on the button:', letter)
            return i
    return -1

# Functions that load happy and sad hangman imageS
def loadHangmanImages():
    hmImages = []
    for imageIndex in range(7):
        fileName = base_folder + 'hangman' + str(imageIndex) + '.png'
        hmImages.append(pygame.image.load(fileName))
    return hmImages

# Functions that load puzzles
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
    randIndex = random.randrange(0,6)
    randPuzzle = puzzles[pCategory][randIndex]
    print("Puzzle: ", randPuzzle[0])
    print("Clue: ", randPuzzle[1])
    return randPuzzle

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
        if letter == c[1]:
            newGuess += c[1]
        else:
            newGuess += guess[c[0]]
    return newGuess

# draw rectangular buttons
catButtons = [[(56,200,160,80), 'Books'],
              [(271,200,160,80), 'English Idioms'],
              [(486,200,160,80), 'Pre-2000s Bands']]

menuButtons = [[(56,60,160,80), 'MENU'],
              [(56,160,160,80), 'PLAY AGAIN']]

def drawRectangularButtons(buttons):
    for b in buttons:
        hover = pygame.mouse.get_pos()
        if b[0][0]+b[0][2] > hover[0] > b[0][0] and b[0][1]+b[0][3] > hover[1] > b[0][1]:
            pygame.draw.rect(win,DARK_PURPLE,b[0],0)
            txtSurface = bttn_font.render(b[1],True,WHITE)
        else:
            pygame.draw.rect(win,PURPLE,b[0],0)
            txtSurface = bttn_font.render(b[1],True,WHITE)
        pygame.draw.rect(win,WHITE,b[0],3)
        x = b[0][0] + (b[0][2] - txtSurface.get_width()) // 2
        y = b[0][1] + (b[0][3] - txtSurface.get_height()) // 2
        win.blit(txtSurface,(x,y))

def rectangleButtonClick(mp, buttons):
    for i,b in enumerate(buttons):
        if pygame.Rect(b[0]).collidepoint(mp):
            print ("Button clicked: ", i)
            return i
    return -1

# final surface function
def drawFinal(guess, puzzle):
    global gameOver
    global categoryScreen

    if wrongCount == 6:
        lostSurface = guess_font.render("YOU LOST!",True,BLACK)
        x = (win.get_width() - lostSurface.get_width())-50
        win.blit(lostSurface,(x,220))
        #loseSound.play()
        gameOver = True
                
    if guess == puzzle:
        wonSurface = guess_font.render("YOU WIN!",True,BLACK)
        x = (win.get_width() - wonSurface.get_width())-50
        win.blit(wonSurface,(x,220))
        #winSound.play()
        gameOver = True

    if gameOver == True:
        drawRectangularButtons(menuButtons)
        click_pos = pygame.mouse.get_pos()
        btn_index = rectangleButtonClick(click_pos, menuButtons)
        if btn_index == 0:
            categoryScreen = True
        elif btn_index == 1:
            categoryScreen = False
        #reset_game()
        
# function that redraws all objects
def redrawGameWindow(buttons, screen):
    #global categoryScreen
    #global gameOver
    #global usedLetters
    win.fill(PINK)
    # code to draw things goes here
    if screen == True:
        drawRectangularButtons(catButtons)
    else:
        drawButtons(buttons)
        drawGuess()
        drawFinal(guess, puzzle2)
        win.blit(hmImages[wrongCount],(270,20))
 
    pygame.display.update()
    
def reset_game():
    global usedLetters
    global gameOver
    global randomPuzz
    global guess
    global puzzle2
    global wrongCount

    gameOver = False
    usedLetters = ""
    randomPuzz = []
    guess = ''
    puzzle2 = ''
    wrongCount = 0

# the main program begins here
win = pygame.display.set_mode((700,480))
buttons = createButtons()
puzzles = loadPuzzles()
hmImages = loadHangmanImages()

reset_game()
inPlay = True
categoryScreen = True

while inPlay:
    redrawGameWindow(buttons, categoryScreen)
    pygame.time.delay(10)            

    for event in pygame.event.get():
        if event.type == pygame.QUIT:   
            inPlay = False              
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
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
            if categoryScreen == False:
                guess = updateGuess(buttonIndex, guess, puzzle2)
            else:
                category = rectangleButtonClick(clickPos, catButtons)
                randomPuzz = getRandomPuzzle(category, puzzles)
                puzzle2 = randomPuzz[0]
                clue = randomPuzz[1]
                guess = initializeGuess(puzzle2)
                categoryScreen = False

pygame.quit() 
