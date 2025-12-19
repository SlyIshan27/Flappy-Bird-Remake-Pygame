import pygame
import sys
import random
from pygame.locals import * #For Mouse Inputs and code
from pygame import mixer #For music
from textDisplay import TextDisplay
#Functions:

#MusicPlayer Function to play random songs/music
def MusicPlayer():
    global CurrentSong, Instrumentals
    RandomSong = random.choice(Instrumentals) #Makes a random choice of the song list
    while RandomSong == CurrentSong:
        RandomSong = random.choice(Instrumentals)
    CurrentSong = RandomSong
    pygame.mixer.music.load(RandomSong)
    mixer.music.set_volume(0.4) #Sets the volume
    pygame.mixer.music.play() # Plays the song

#Had to make a muted version of the music player so whenever the song switches the music stays muted
def MusicPlayerMuted():
    global CurrentSong, Instrumentals
    RandomSong = random.choice(Instrumentals)
    while RandomSong == CurrentSong:
        RandomSong = random.choice(Instrumentals)
    CurrentSong = RandomSong
    pygame.mixer.music.load(RandomSong)
    mixer.music.set_volume(0.0) #Sets the volume
    pygame.mixer.music.play()
# A function which resets the game in certain scenarios ex.(Player exits out of easy mode but then wants to go back, the game then gets reseted)
def FlappyBirdRestart():
    global gameOver, pipeRandomizer, redBirdRect, movement, PlayerScore, blueBirdRect
    gameOver = True
    pipeRandomizer.clear()
    redBirdRect.center = (100,300)
    blueBirdRect.center = (100,300)
    movement = 0
    PlayerScore = 0
# Function which makes the ground keep moving to the human eye but in reality, it just keeps re-drawing the ground certain pixels to the right
def continuedGround():
    screen.blit(ground,(groundPos, 640))
    screen.blit(ground,(groundPos + 550, 640))
    screen.blit(ground,(groundPos + 1100,640))
# Spawns pipes function with random lengths to the right of the screen
def spawnPipe():
    randomObject = random.choice(ObstacleHeightList)
    randomObjectTop = random.choice(ObstacleHeightTopList)
    bottomObject = pipeImage.get_rect(midtop = (687,randomObject))
    topObject = pipeImage.get_rect(midbottom = (687,randomObjectTop - 315))
    return bottomObject, topObject
# This Functions works on the pipe movement and moves the pipes around
def pipeMovement(movePipe):
    for pipe in movePipe:
        pipe.centerx += -5
    return movePipe
#Drawing of the pipes function
def pipeDrawing(movePipe):
    for pipe in movePipe:
        if pipe.bottom >= 850:
            screen.blit(pipeImage,pipe)
        else:
            flipObject = pygame.transform.flip(pipeImage, False,True) #This line of code basically flips the pipe image (This is the top pipe line as the original image imported is for the bottom pipes)
            screen.blit(flipObject,pipe)
#Collision failure function, checks if the bird hits a pipe or hits the ground so then it makes sure the game is over.
def collisionFailure(movePipe):
    global Scored
    for pipe in movePipe:
        if redBirdRect.colliderect(pipe) or blueBirdRect.colliderect(pipe): #pipe collision code
            Scored = True
            DeathEffect.play() #Playing of the death sound
            return False
    if redBirdRect.top <= -100: #Giving the user a little bit of wiggle room so it can fly a little bit above the screen, if it flys too high the game will be over.
        Scored = True
        DeathEffect.play()
        return False
    if redBirdRect.bottom >= 645: #Code for when it hits the ground
        Scored = True
        DeathEffect.play()
        return False
    if blueBirdRect.top <= -100: #These if statements are for the blue bird collisions
        Scored = True
        DeathEffect.play()
        return False
    if blueBirdRect.bottom >= 645:
        Scored = True
        DeathEffect.play()
        return False
    
    return True
#Bird Rotation Mechanics Function
def rotateBird(roBird):
    BirdNew = pygame.transform.rotozoom(roBird,movement * 3, 0.8) #This line of code rotates the bird at certain angle with the birds movement also making sure not to mess up the movement.
    return BirdNew 
#Red Bird Animation (Flapping Wings)
def redBirdAnimate():
    BirdNew = redBirdList[redBirdCalculation] #Cycles through the different red bird images
    BirdNewRect = BirdNew.get_rect(center = (100,redBirdRect.centery))
    return BirdNew,BirdNewRect
#Blue Bird Animation
def blueBirdAnimate():
    BirdNew = blueBirdList[blueBirdCalculation] #Cycles through the different blue bird images
    BirdNewRect = BirdNew.get_rect(center = (100,blueBirdRect.centery))
    return BirdNew,BirdNewRect
#Score function
def score(game_state):
    if game_state == 'mainGame':  #Displays Score Text and Pause Button text while in game
        scoreText = gameFont.render(f'Score: {int(PlayerScore)}',True,(0,255,255))
        PauseText = gameFont3.render("Press P to Pause", False, CYAN)
        scoreRect = scoreText.get_rect(center = (275,100))
        PauseRect = PauseText.get_rect(center = (275,25))    
        screen.blit(scoreText,scoreRect)
        screen.blit(PauseText,PauseRect)
    if game_state == 'gameOver': #Displays score and highscore text. Also, a restart image when the user dies.
        scoreText = gameFont.render(f'Score: {int(PlayerScore)}',True,(0,255,255))
        scoreRect = scoreText.get_rect(center = (275,100))  
        screen.blit(scoreText,scoreRect)

        highText = gameFont.render(f'High Score: {int(PlayerHigh)}',True,(0,255,255))
        highRect = highText.get_rect(center = (275,175))  
        screen.blit(highText,highRect)

        EndingText = fontTitle3.render("Press B to go back to main menu",False, MAGENTA)
        EndingTextRect = EndingText.get_rect()
        EndingTextRect.center = (140,25)
        screen.blit(EndingText, EndingTextRect)
        EndingText2 = fontTitle3.render("Press Q to Quit",False, MAGENTA)
        EndingTextRect2 = EndingText2.get_rect()
        EndingTextRect2.center = (475,25)
        screen.blit(EndingText2, EndingTextRect2)
#HighScore Code Function, if users score is higher than it's high score, the player score = the highscore.
def HighScore(PlayerScore,PlayerHigh):
    if PlayerScore > PlayerHigh:
        PlayerHigh = PlayerScore
    return PlayerHigh
#Checks if the bird makes it through the pipe successfully, if it does the user gets one point
def scoreCheck():
    global PlayerScore, Scored
    if pipeRandomizer:
        for pipe in pipeRandomizer:
            if  82 < pipe.centerx < 92 and Scored:
                PlayerScore += 1 #If it does then the user gets a point and then sets the loop to false to make sure no errors happen
                Scored = False
            if pipe.centerx < 0:
                Scored = True

#This code makes it so the music and sounds are not delayed
pygame.mixer.pre_init(44100,-16,1, 1024)
pygame.init()

#Screen size
screen = pygame.display.set_mode((550,680), 0)
#Caption
pygame.display.set_caption("Flappy Bird Remake - Ishan Lakhotia")
#FPS Shortcut
clock = pygame.time.Clock()
#Fonts which I imported and I used
gameFont = pygame.font.Font('src/Heroes Legend.ttf',20)
gameFont2 = pygame.font.Font('src/Heroes Legend.ttf',35)
gameFont3 = pygame.font.Font('src/Heroes Legend.ttf',15)

#Getting the width and height and setting other width/height variables
width = screen.get_width()
height = screen.get_height()
centreX = width/2
centreY = height/2
screenCentre = (centreX, centreY)
textDisplay = TextDisplay()
#Colours
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
CYAN = (0,255,255)
MAGENTA = (255,0,255)
YELLOW = (255,255,0)
GREY = (200, 200, 200)
MidnightSlatBlue = (123, 104, 238)
bg_color = pygame.Color('grey12')
BlueViolet = (138,43,226)
Chocolate = (210,105,30)
TURQUOISE = (0,206,209)
NAVY = (0,0,128)

#Music Variables
pygame.mixer.music.load("src/Ice Cube - It Was A Good Day (Instrumental).wav")
pygame.mixer.music.load("src/This Dj - Warren G.wav")
#List of all the music which I used
Instrumentals = ["src/Ice Cube - It Was A Good Day (Instrumental).wav", "src/This Dj - Warren G.wav"]
#Variable for the MusicPlayer
CurrentSong = None

#Sounds I used (Flap and Death Sounds)
FlapEffect = pygame.mixer.Sound("src/wingFlap.wav")
DeathEffect = pygame.mixer.Sound("src/DeathEffect.wav")

#Movement variables which controlled birds movement
gravity = 0.25
movement = 0
#Loop for the gameOver Screen
gameOver = True


#Score Variables
PlayerScore = 0
PlayerHigh = 0
Scored = True

#Images:

#Intro Background
IntroBackground = pygame.image.load("src/night.png").convert() #.convert() Allows the image to be transformed
IntroBackground = pygame.transform.scale2x(IntroBackground) #This resizes the image so it fits the screen, makes it 2x bigger

#Background 
background = pygame.image.load("src/night.png").convert()
background = pygame.transform.scale2x(background)

#Ground Image
ground = pygame.image.load("src/ground.png").convert()
ground = pygame.transform.scale2x(ground) #Adjusted the ground image size to the fit the screen properly

#End game/ game over message image
ReadyOver = pygame.image.load("src/Ready.png").convert_alpha() #.convert_alpha converts the image to the same pixel format to the screen
ReadyOver = pygame.transform.scale(ReadyOver,(300,400)) #adjusting the size of the gameover message image (this time not 2x bigger)
ReadyOverRect = ReadyOver.get_rect(center = (275,435))

#ground variable to help with ground movement
groundPos = 0
#mx, my = pygame.mouse.get_pos()

#Red Bird Image import and sizing
redBirdMid = pygame.image.load("src/redbirdMid.png").convert_alpha()
redBirdMid = pygame.transform.scale2x(redBirdMid)
redBirdUp = pygame.image.load("src/redbirdUp.png").convert_alpha()
redBirdUp = pygame.transform.scale2x(redBirdUp)
redBirdDown = pygame.image.load("src/redbirdDown.png").convert_alpha()
redBirdDown = pygame.transform.scale2x(redBirdDown)
#List of 3 the variations of the red bird
redBirdList = [redBirdDown,redBirdMid,redBirdUp]
#Variable for the calculations for the bird flap animation (Just setting it for zero)
redBirdCalculation = 0  
#Bird and bird position variables
redBird = redBirdList[redBirdCalculation]
redBirdRect = redBird.get_rect(center = (100,300))

#Blue Bird Image imports and sizing
blueBirdMid = pygame.image.load("src/bluebirdMid.png").convert_alpha()
blueBirdMid = pygame.transform.scale2x(blueBirdMid)
blueBirdUp = pygame.image.load("src/bluebirdUp.png").convert_alpha()
blueBirdUp = pygame.transform.scale2x(blueBirdUp)
blueBirdDown = pygame.image.load("src/bluebirdDown.png").convert_alpha()
blueBirdDown = pygame.transform.scale2x(blueBirdDown)
#List of the 3 Variations of the blue bird
blueBirdList = [blueBirdDown,blueBirdMid,blueBirdUp]
#Variable for the calculations for the bird flap animation (Just setting it for zero)
blueBirdCalculation = 0
#Bird and bird position variables  
blueBird = blueBirdList[blueBirdCalculation]
blueBirdRect = blueBird.get_rect(center = (100,300))


#This sets the speed of the bird animation when it is flapping it's wings
FlapSpeed = pygame.USEREVENT + 1
pygame.time.set_timer(FlapSpeed, 210)




#Importing Pipe images
pipeImage = pygame.image.load("src/pipeRed.png").convert()
pipeImage = pygame.transform.scale2x(pipeImage)
#Code which sets the pipes properly and at the right time
Spawn = pygame.USEREVENT
pygame.time.set_timer(Spawn, 1250)
#A list which is used later on to make the random pipe lengths spawn and work efficiently
pipeRandomizer = []
#The lengths of the bottom pipe
ObstacleHeightList = [575,525,600]
#The lengths of the top pipe
ObstacleHeightTopList = [450,515,500]
#Defualt Fonts Used:
fontTitle = pygame.font.SysFont("comicsansms", 30,italic=True)
fontTitle2 = pygame.font.SysFont("comicsansms", 15,italic=True)
fontTitle3 = pygame.font.SysFont("comicsansms", 18,italic=True)
fontTitleBold = pygame.font.SysFont("comicsansms",20, bold =True)

#Different Loops for different sections of the game
instructions = False
game = False
gameBlue = False
mediumBlue = False
medium = False
hardBlue = False
hard = False
birdPickerEasy = False
birdPickerMedium = False
birdPickerHard = False

#Game Features Loops (Pause and Mute)
Muted = False
Paused = False
PausedBlue = False
PausedMedium = False
PausedMediumBlue = False
PausedHard = False
PausedHardBlue = False

#main and the starting screen loop
intro = True
main = True

#Mouse Loops 
click = False

click2 = False

click3 = False

click4 = False

# main loop
while main:
    MusicPlayer() #Calling the Music Player to play music
    for event in pygame.event.get(): 
        if event.type ==pygame.QUIT: 
            main = False 
        
    #Mute Button code to check if the music is muted
    if Muted == True:
        MusicPlayerMuted()
    else:
        MusicPlayer()
    
    #Starting Screen Loop Code
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  #Inputs
                main = False
                intro = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    main = False
                    intro = False
                elif event.key == pygame.K_m: #Mute
                    mixer.music.set_volume(0.0)
                    Muted = True
                elif event.key == pygame.K_u: #Unmute
                    mixer.music.set_volume(0.4)
                    Muted = False
            if event.type == FlapSpeed: #Making the bird flap it's wing!
                if redBirdCalculation < 2:
                    redBirdCalculation += 1
                else:
                    redBirdCalculation = 0
            
                redBird,IntroBirdRect = redBirdAnimate()
            
        
        #Background
        screen.blit(IntroBackground, (0,0))
        
        #Getting the Mouse Position
        mx, my = pygame.mouse.get_pos()

        #Text Code
        textTitle = gameFont2.render("Flappy Bird", False, CYAN)
        textTitle2 = gameFont.render("Play Easy Mode",False, MAGENTA)
        textTitle3 = gameFont.render("Play Medium Mode", False, GREEN)
        textTitle4 = gameFont.render("Play Hard Mode",False, Chocolate)
        textTitle5 = gameFont.render("Instructions",False, WHITE)
        textTitle6 = gameFont.render("Quit",False, WHITE)
        textRect = textTitle.get_rect()
        #textRect2 = textTitle2.get_rect()
        button1 = pygame.Rect(160, 285, 250, 35)
        button2 = pygame.Rect(145, 355, 292, 35)
        button3 = pygame.Rect(160, 425, 255, 35)
        button4 = pygame.Rect(325, 640, 245, 35)
        button5 = pygame.Rect(25, 640, 77, 35)
        IntroBirdRect = redBird.get_rect()
        textRect.center = (centreX, 100)
        #textRect2.center = (centreX,350)
        IntroBirdRect.center = (centreX,550)
        screen.blit(textTitle, textRect)
        screen.blit(textTitle2, button1)
        screen.blit(textTitle3, button2)
        screen.blit(textTitle4, button3)
        screen.blit(textTitle5, button4)
        screen.blit(textTitle6, button5)
        screen.blit(redBird,IntroBirdRect)
        #Mouse Input Code
        if button1.collidepoint((mx, my)):
            if click:
                intro = False
                birdPickerEasy = True
                click = False
                click2 = False
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                click = True
        if button2.collidepoint((mx, my)):
            if click:
                intro = False
                birdPickerMedium = True
                click = False
                click3 = False
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                click = True
        if button3.collidepoint((mx, my)):
            if click:
                intro = False
                birdPickerHard = True
                click = False
                click4 = False
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                click = True
        if button4.collidepoint((mx, my)):
            if click:
                intro = False
                instructions = True
                click = False
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                click = True
        if button5.collidepoint((mx, my)):
            if click:
                main = False
                intro = False
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                click = True        
        
        pygame.display.flip()

    #Instruction Screen Loop
    while instructions:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #Inputs
                main = False
                instructions = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    main = False
                    instructions = False
                elif event.key == pygame.K_b:
                    instructions = False
                    intro = True
                    click = False #Setting this to false so the mouse input will work properly when user goes back
                elif event.key == pygame.K_m:
                    mixer.music.set_volume(0.0)
                    Muted = True
                elif event.key == pygame.K_u:
                    mixer.music.set_volume(0.4)
                    Muted = False
            if event.type == FlapSpeed:  #Bird Animation to make bird Flap wings
                if redBirdCalculation < 2:
                    redBirdCalculation += 1
                else:
                    redBirdCalculation = 0
            
                redBird,InstructBirdRect = redBirdAnimate()


        #Background
        screen.fill(bg_color)

        #Text Code
        textDisplay.instructions(screen)
        InstructBirdRect = redBird.get_rect()
        InstructBirdRect.center = (centreX, 100)
        screen.blit(redBird,InstructBirdRect)
        
        pygame.display.flip()
    
    #Bird Colour Picker Loops for all the gamemodes:
    
    while birdPickerEasy:
        clock.tick(120)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main = False
                birdPickerEasy = False
            if event.type == pygame.KEYDOWN: #Inputs
                if event.key == pygame.K_q:
                    main = False
                    birdPickerEasy = False
                elif event.key == pygame.K_b:
                    intro = True
                    birdPickerEasy = False
                    click2 = False
                    click = False
                elif event.key == pygame.K_m:
                    mixer.music.set_volume(0.0)
                    Muted = True
                elif event.key == pygame.K_u:
                    mixer.music.set_volume(0.4)
                    Muted = False
            if event.type == FlapSpeed: #Bird Animation
                if blueBirdCalculation < 2:
                    blueBirdCalculation += 1
                else:
                    blueBirdCalculation = 0
            
                blueBird,birdPickerRectBlue = blueBirdAnimate()           
            if event.type == FlapSpeed:
                if redBirdCalculation < 2:
                    redBirdCalculation += 1
                else:
                    redBirdCalculation = 0
            
                redBird,birdPickerRectRed = redBirdAnimate()
        
        #Mouse Position
        mx2, my2 = pygame.mouse.get_pos()

        #Background
        screen.fill(bg_color)

        #Text Code
        textDisplay.birdPicker(screen)
        textTitleRect2 = pygame.Rect(120,300,57,95)
        textTitleRect3 = pygame.Rect(370,300,57,95)
        birdPickerRectBlue = blueBird.get_rect()
        birdPickerRectRed = redBird.get_rect()
        birdPickerRectBlue.center = (150,370)
        birdPickerRectRed.center = (400,370)
        screen.blit(blueBird, birdPickerRectBlue)
        screen.blit(redBird, birdPickerRectRed)

        #Mouse Inputs
        if textTitleRect2.collidepoint((mx2,my2)):
            if click2:
                gameBlue = True
                birdPickerEasy = False
                FlappyBirdRestart()
                click2 = False
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click2 = True
        if textTitleRect3.collidepoint((mx2,my2)):
            if click2:
                game = True
                birdPickerEasy = False
                FlappyBirdRestart()
                click2 = False
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click2 = True

        pygame.display.flip()

    while birdPickerMedium:
        clock.tick(120)
        for event in pygame.event.get(): #Inputs
            if event.type == pygame.QUIT:
                main = False
                birdPickerMedium = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    main = False
                    birdPickerMedium = False
                elif event.key == pygame.K_b:
                    birdPickerMedium = False
                    intro = True
                    click3 = False
                    click =  False
                elif event.key == pygame.K_m:
                    mixer.music.set_volume(0.0)
                    Muted = True
                elif event.key == pygame.K_u:
                    mixer.music.set_volume(0.4)
                    Muted = False
            if event.type == FlapSpeed: #Bird Animations
                if blueBirdCalculation < 2:
                    blueBirdCalculation += 1
                else:
                    blueBirdCalculation = 0
            
                blueBird,birdPickerRectBlue = blueBirdAnimate()           
            if event.type == FlapSpeed:
                if redBirdCalculation < 2:
                    redBirdCalculation += 1
                else:
                    redBirdCalculation = 0
            
                redBird,birdPickerRectRed = redBirdAnimate()
        
        #Mouse Position
        mx3, my3 = pygame.mouse.get_pos()

        #Background
        screen.fill(bg_color)

        #Text Code
        textDisplay.birdPicker(screen)
        textTitleRect2 = pygame.Rect(120,300,57,95)
        textTitleRect3 = pygame.Rect(370,300,57,95)
        birdPickerRectBlue = blueBird.get_rect()
        birdPickerRectRed = redBird.get_rect()
        birdPickerRectBlue.center = (150,370)
        birdPickerRectRed.center = (400,370)
        screen.blit(blueBird, birdPickerRectBlue)
        screen.blit(redBird, birdPickerRectRed)

        #Mouse Inputs
        if textTitleRect2.collidepoint((mx3,my3)):
            if click3:
                mediumBlue = True
                birdPickerMedium = False
                FlappyBirdRestart()
                click3 = False
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click3 = True
        if textTitleRect3.collidepoint((mx3,my3)):
            if click3:
                medium = True
                birdPickerMedium = False
                FlappyBirdRestart()
                click3 = False
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click3 = True

        pygame.display.flip()
    
    while birdPickerHard:
        clock.tick(120)
        for event in pygame.event.get(): #Inputs
            if event.type == pygame.QUIT:
                main = False
                birdPickerHard = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    main = False
                    birdPickerHard = False
                elif event.key == pygame.K_b:
                    birdPickerHard = False
                    intro = True
                    click4 = False
                    click = False
                elif event.key == pygame.K_m:
                    mixer.music.set_volume(0.0)
                    Muted = True
                elif event.key == pygame.K_u:
                    mixer.music.set_volume(0.4)
                    Muted = False
            if event.type == FlapSpeed: #Bird Animation
                if blueBirdCalculation < 2:
                    blueBirdCalculation += 1
                else:
                    blueBirdCalculation = 0
            
                blueBird,birdPickerRectBlue = blueBirdAnimate()           
            if event.type == FlapSpeed:
                if redBirdCalculation < 2:
                    redBirdCalculation += 1
                else:
                    redBirdCalculation = 0
            
                redBird,birdPickerRectRed = redBirdAnimate()
        
        #Mouse Position
        mx4, my4 = pygame.mouse.get_pos()

        #Background
        screen.fill(bg_color)

        #Text Code
        textDisplay.birdPicker(screen)
        textTitleRect2 = pygame.Rect(120,300,57,95)
        textTitleRect3 = pygame.Rect(370,300,57,95)
        birdPickerRectBlue = blueBird.get_rect()
        birdPickerRectRed = redBird.get_rect()
        birdPickerRectBlue.center = (150,370)
        birdPickerRectRed.center = (400,370)
        screen.blit(blueBird, birdPickerRectBlue)
        screen.blit(redBird, birdPickerRectRed)

        #Mouse Inputs
        if textTitleRect2.collidepoint((mx4,my4)):
            if click4:
                hardBlue = True
                birdPickerHard = False
                FlappyBirdRestart()
                click4 = False
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click4 = True
        if textTitleRect3.collidepoint((mx4,my4)):
            if click4:
                hard = True
                birdPickerHard = False
                FlappyBirdRestart()
                click4 = False
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click4 = True
        
        pygame.display.flip()

    #All the different gamemode loop code (Easy,medium,hard for both red and blue bird):
    
    while game:
        clock.tick(125) #Speed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main = False
                game = False
            if event.type == pygame.KEYDOWN: #Inputs
                if event.key == pygame.K_q:
                    main = False
                    game = False
                elif event.key == pygame.K_b:
                    game = False
                    intro = True
                    click = False
                elif event.key == pygame.K_p: #Pause Screen
                    game = False
                    Paused = True
                elif event.key == pygame.K_m:
                    mixer.music.set_volume(0.0)
                    Muted = True
                elif event.key == pygame.K_u:
                    mixer.music.set_volume(0.4)
                    Muted = False
                if event.key == pygame.K_SPACE and gameOver: #This makes the bird fly a certain distance up whenever space bar is pressed
                    movement = 0
                    movement += -10
                    FlapEffect.play() #Flap Sound Is played
                if event.key == pygame.K_SPACE and gameOver == False: #Restart input, restarts the game when space is pressed
                    gameOver = True
                    pipeRandomizer.clear()
                    redBirdRect.center = (100,300)
                    movement = 0
                    PlayerScore = 0
            if event.type == FlapSpeed: #Bird Animation
                if redBirdCalculation < 2:
                    redBirdCalculation += 1
                else:
                    redBirdCalculation = 0
            
                redBird,redBirdRect = redBirdAnimate()
            
            #Pipe spawning code
            if event.type == Spawn:
                pipeRandomizer.extend(spawnPipe()) #This line makes and adds all the elements of an iterable ex. Like a list or string. (PipeRandomizer is a list)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and gameOver: #Mouse input for the bird (User can press anywhere on the screen)
                    movement = 0
                    movement += -10
                    FlapEffect.play()
                if event.button == 1 and gameOver == False: #Mouse input to restart user can press anywhere on the screen to restart.
                    #event.button == 1
                    gameOver = True
                    pipeRandomizer.clear()
                    redBirdRect.center = (100,300)
                    movement = 0
                    PlayerScore = 0
        
        #Background
        screen.blit(background,(0,0))

        #During the game code to call the certain functions
        if gameOver:
            redBirdRect.centery += movement #Bird Movement functions being called
            rotated = rotateBird(redBird)
            movement += gravity
            screen.blit(rotated,redBirdRect)

            pipeRandomizer = pipeMovement(pipeRandomizer) #Pipe and Collision functions being called
            pipeDrawing(pipeRandomizer)
            gameOver = collisionFailure(pipeRandomizer)
            
            scoreCheck()  #Scoring functions being called
            score('mainGame')
        else:
            PlayerHigh = HighScore(PlayerScore,PlayerHigh) #GameOver screen functions being Called
            score('gameOver')
            screen.blit(ReadyOver,ReadyOverRect)

        #This keeps drawing the ground to the right
        groundPos += -1
        continuedGround()
        
        if groundPos <= -550:
            groundPos = 0

        pygame.display.update()

    #Blue Bird Version
    while gameBlue:
        clock.tick(125) #Speed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main = False
                gameBlue = False
            if event.type == pygame.KEYDOWN: #Inputs
                if event.key == pygame.K_q:
                    main = False
                    gameBlue = False
                elif event.key == pygame.K_b:
                    gameBlue = False
                    intro = True
                    click = False
                elif event.key == pygame.K_p:
                    gameBlue = False
                    PausedBlue = True
                elif event.key == pygame.K_m:
                    mixer.music.set_volume(0.0)
                    Muted = True
                elif event.key == pygame.K_u:
                    mixer.music.set_volume(0.4)
                    Muted = False
                if event.key == pygame.K_SPACE and gameOver: #Movement Inputs
                    movement = 0
                    movement += -10
                    FlapEffect.play()
                if event.key == pygame.K_SPACE and gameOver == False: #Restart Inputs
                    gameOver = True
                    pipeRandomizer.clear()
                    blueBirdRect.center = (100,300)
                    movement = 0
                    PlayerScore = 0
            if event.type == FlapSpeed: #Bird Animation
                if blueBirdCalculation < 2:
                    blueBirdCalculation += 1
                else:
                    blueBirdCalculation = 0

                blueBird,blueBirdRect = blueBirdAnimate()
            
            #Pipe Spawning
            if event.type == Spawn:
                pipeRandomizer.extend(spawnPipe())
            if event.type == pygame.MOUSEBUTTONDOWN: #Mouse Inputs
                if event.button == 1 and gameOver:
                    movement = 0
                    movement += -10
                    FlapEffect.play()
                if event.button == 1 and gameOver == False:
                    #event.button == 1
                    gameOver = True
                    pipeRandomizer.clear()
                    blueBirdRect.center = (100,300)
                    movement = 0
                    PlayerScore = 0
        
        screen.blit(background,(0,0))

        #Calling Functions in if statements
        if gameOver:
            blueBirdRect.centery += movement
            rotated = rotateBird(blueBird)
            movement += gravity
            screen.blit(rotated,blueBirdRect)

            pipeRandomizer = pipeMovement(pipeRandomizer)
            pipeDrawing(pipeRandomizer)
            gameOver = collisionFailure(pipeRandomizer)
            
            scoreCheck() 
            score('mainGame')
        else:
            PlayerHigh = HighScore(PlayerScore,PlayerHigh)
            score('gameOver')
            screen.blit(ReadyOver,ReadyOverRect)

        #Ground Code
        groundPos += -1
        continuedGround()
        
        if groundPos <= -550:
            groundPos = 0

        pygame.display.update()


    #Medium Mode Loops

    while medium:
        clock.tick(135) #Speed is faster now
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main = False
                medium = False
            if event.type == pygame.KEYDOWN: #Inputs
                if event.key == pygame.K_q:
                    main = False
                    medium = False
                elif event.key == pygame.K_b:
                    medium = False
                    intro = True
                    click = False
                elif event.key == pygame.K_p:
                    medium = False
                    PausedMedium = True
                elif event.key == pygame.K_m:
                    mixer.music.set_volume(0.0)
                    Muted = True
                elif event.key == pygame.K_u:
                    mixer.music.set_volume(0.4)
                    Muted = False
                if event.key == pygame.K_SPACE and gameOver: #Movement Inputs
                    movement = 0
                    movement += -11 #Bird Flies higher now whenever you press the space or right click button
                    FlapEffect.play()
                if event.key == pygame.K_SPACE and gameOver == False: #Restart Inputs
                    gameOver = True
                    pipeRandomizer.clear()
                    redBirdRect.center = (100,300)
                    movement = 0
                    PlayerScore = 0
            if event.type == FlapSpeed: #Bird animation
                if redBirdCalculation < 2:
                    redBirdCalculation += 1
                else:
                    redBirdCalculation = 0
            
                redBird,redBirdRect = redBirdAnimate()
            
            #Pipe Spawning
            if event.type == Spawn:
                pipeRandomizer.extend(spawnPipe())
            if event.type == pygame.MOUSEBUTTONDOWN: #Mouse Inputs
                if event.button == 1 and gameOver:
                    movement = 0
                    movement += -11
                    FlapEffect.play()
                if event.button == 1 and gameOver == False:
                    #event.button == 1
                    gameOver = True
                    pipeRandomizer.clear()
                    redBirdRect.center = (100,300)
                    movement = 0
                    PlayerScore = 0
        
        #Background
        screen.blit(background,(0,0))

        #Calling Functions in if statments
        if gameOver:
            redBirdRect.centery += movement
            rotated = rotateBird(redBird)
            movement += gravity
            screen.blit(rotated,redBirdRect)

            pipeRandomizer = pipeMovement(pipeRandomizer)
            pipeDrawing(pipeRandomizer)
            gameOver = collisionFailure(pipeRandomizer)
            
            scoreCheck() 
            score('mainGame')
        else:
            PlayerHigh = HighScore(PlayerScore,PlayerHigh)
            score('gameOver')
            screen.blit(ReadyOver,ReadyOverRect)
            

        #Ground Code
        groundPos += -1
        continuedGround()
        
        if groundPos <= -550:
            groundPos = 0

        pygame.display.update()    

    #Blue Version
    while mediumBlue:
        clock.tick(135)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main = False
                mediumBlue = False
            if event.type == pygame.KEYDOWN: #Inputs
                if event.key == pygame.K_q:
                    main = False
                    mediumBlue = False
                elif event.key == pygame.K_b:
                    mediumBlue = False
                    intro = True
                    click = False
                elif event.key == pygame.K_p:
                    mediumBlue = False
                    PausedMediumBlue = True
                elif event.key == pygame.K_m:
                    mixer.music.set_volume(0.0)
                    Muted = True
                elif event.key == pygame.K_u:
                    mixer.music.set_volume(0.4)
                    Muted = False
                if event.key == pygame.K_SPACE and gameOver: #Movement Inputs
                    movement = 0
                    movement += -11
                    FlapEffect.play()
                if event.key == pygame.K_SPACE and gameOver == False: #Restart Input
                    gameOver = True
                    pipeRandomizer.clear()
                    blueBirdRect.center = (100,300)
                    movement = 0
                    PlayerScore = 0
            if event.type == FlapSpeed: #Bird Animation
                if blueBirdCalculation < 2:
                    blueBirdCalculation += 1
                else:
                    blueBirdCalculation = 0

                blueBird,blueBirdRect = blueBirdAnimate()
            
            #Pipe spawning
            if event.type == Spawn:
                pipeRandomizer.extend(spawnPipe())
            if event.type == pygame.MOUSEBUTTONDOWN: #Mouse Inputs
                if event.button == 1 and gameOver:
                    movement = 0
                    movement += -11
                    FlapEffect.play()
                if event.button == 1 and gameOver == False:
                    #event.button == 1
                    gameOver = True
                    pipeRandomizer.clear()
                    blueBirdRect.center = (100,300)
                    movement = 0
                    PlayerScore = 0
        
        #Background
        screen.blit(background,(0,0))

        #Calling Certain Functions in if statements
        if gameOver:
            blueBirdRect.centery += movement
            rotated = rotateBird(blueBird)
            movement += gravity
            screen.blit(rotated,blueBirdRect)

            pipeRandomizer = pipeMovement(pipeRandomizer)
            pipeDrawing(pipeRandomizer)
            gameOver = collisionFailure(pipeRandomizer)
            
            scoreCheck() 
            score('mainGame')
        else:
            PlayerHigh = HighScore(PlayerScore,PlayerHigh)
            score('gameOver')
            screen.blit(ReadyOver,ReadyOverRect)

        #Ground Code
        groundPos += -1
        continuedGround()
        
        if groundPos <= -550:
            groundPos = 0

        pygame.display.update()

    #Hard Game Loop
    #Blue Version
    while hardBlue:
        clock.tick(150) #Speed is faster for this mode
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main = False
                hardBlue = False
            if event.type == pygame.KEYDOWN: #Inputs
                if event.key == pygame.K_q:
                    main = False
                    hardBlue = False
                elif event.key == pygame.K_b:
                    hardBlue = False
                    intro = True
                    click = False
                elif event.key == pygame.K_p:
                    hardBlue = False
                    PausedHardBlue = True
                elif event.key == pygame.K_m:
                    mixer.music.set_volume(0.0)
                    Muted = True
                elif event.key == pygame.K_u:
                    mixer.music.set_volume(0.4)
                    Muted = False
                if event.key == pygame.K_SPACE and gameOver: #Movement Inputs
                    movement = 0
                    movement += -12 #Flys higher whenever the bird flying controls are pressed
                    FlapEffect.play()
                if event.key == pygame.K_SPACE and gameOver == False: #Restart Input
                    gameOver = True
                    pipeRandomizer.clear()
                    blueBirdRect.center = (100,300)
                    movement = 0
                    PlayerScore = 0
            if event.type == FlapSpeed: #Bird Animation
                if blueBirdCalculation < 2:
                    blueBirdCalculation += 1
                else:
                    blueBirdCalculation = 0

                blueBird,blueBirdRect = blueBirdAnimate()
            
            #Pipe spawning
            if event.type == Spawn:
                pipeRandomizer.extend(spawnPipe())
            if event.type == pygame.MOUSEBUTTONDOWN: #Mouse Inputs
                if event.button == 1 and gameOver:
                    movement = 0
                    movement += -12
                    FlapEffect.play()
                if event.button == 1 and gameOver == False: 
                    #event.button == 1
                    gameOver = True
                    pipeRandomizer.clear()
                    blueBirdRect.center = (100,300)
                    movement = 0
                    PlayerScore = 0
        
        #Background
        screen.blit(background,(0,0))

        #Calling Functions in if statements
        if gameOver:
            blueBirdRect.centery += movement
            rotated = rotateBird(blueBird)
            movement += gravity
            screen.blit(rotated,blueBirdRect)

            pipeRandomizer = pipeMovement(pipeRandomizer)
            pipeDrawing(pipeRandomizer)
            gameOver = collisionFailure(pipeRandomizer)
            
            scoreCheck() 
            score('mainGame')
        else:
            PlayerHigh = HighScore(PlayerScore,PlayerHigh)
            score('gameOver')
            screen.blit(ReadyOver,ReadyOverRect)


        #Ground Code
        groundPos += -1
        continuedGround()
        
        if groundPos <= -550:
            groundPos = 0

        pygame.display.update()

    #Red Version of hard
    while hard:
        clock.tick(150)#Speed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main = False
                hard = False
            if event.type == pygame.KEYDOWN: #Inputs
                if event.key == pygame.K_q:
                    main = False
                    hard = False
                elif event.key == pygame.K_b:
                    hard = False
                    intro = True
                    click = False
                elif event.key == pygame.K_p:
                    hard = False
                    PausedHard = True
                elif event.key == pygame.K_m:
                    mixer.music.set_volume(0.0)
                    Muted = True
                elif event.key == pygame.K_u:
                    mixer.music.set_volume(0.4)
                    Muted = False
                if event.key == pygame.K_SPACE and gameOver: #Movement Inputs
                    movement = 0
                    movement += -12
                    FlapEffect.play()
                if event.key == pygame.K_SPACE and gameOver == False: #Restart Inputs
                    gameOver = True
                    pipeRandomizer.clear()
                    redBirdRect.center = (100,300)
                    movement = 0
                    PlayerScore = 0
            if event.type == FlapSpeed: #Bird Animation
                if redBirdCalculation < 2:
                    redBirdCalculation += 1
                else:
                    redBirdCalculation = 0
            
                redBird,redBirdRect = redBirdAnimate()
            
            #Pipe Spawning
            if event.type == Spawn:
                pipeRandomizer.extend(spawnPipe())
            if event.type == pygame.MOUSEBUTTONDOWN: #Mouse Inputs
                if event.button == 1 and gameOver:
                    movement = 0
                    movement += -12
                    FlapEffect.play() 
                if event.button == 1 and gameOver == False:
                    #event.button == 1
                    gameOver = True
                    pipeRandomizer.clear()
                    redBirdRect.center = (100,300)
                    movement = 0
                    PlayerScore = 0
        
        #Background
        screen.blit(background,(0,0))

        #Calling Functions in an if statement
        if gameOver:
            redBirdRect.centery += movement
            rotated = rotateBird(redBird)
            movement += gravity
            screen.blit(rotated,redBirdRect)

            pipeRandomizer = pipeMovement(pipeRandomizer)
            pipeDrawing(pipeRandomizer)
            gameOver = collisionFailure(pipeRandomizer)
            
            scoreCheck() 
            score('mainGame')
        else:
            PlayerHigh = HighScore(PlayerScore,PlayerHigh)
            score('gameOver')
            screen.blit(ReadyOver,ReadyOverRect)

        #Ground code
        groundPos += -1
        continuedGround()
        
        if groundPos <= -550:
            groundPos = 0

        pygame.display.update()  

    #Pause Menu Loops
    while Paused:
        current_time = pygame.time.get_ticks()
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                main = False
                Paused = False 
            if event.type == pygame.KEYDOWN: #Inputs
                if event.key == pygame.K_c: #Unpauses the game
                    Paused = False
                    game = True
                elif event.key == pygame.K_m: #Mute
                    mixer.music.set_volume(0.0)
                    Muted = True
                elif event.key == pygame.K_u: #Unmute
                    mixer.music.set_volume(0.4)
                    Muted = False
        
        #Background
        screen.fill(bg_color)

        #Text Code
        textDisplay.paused(screen)

        pygame.display.update()
    
    while PausedBlue:
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                main = False
                PausedBlue = False 
            if event.type == pygame.KEYDOWN: #Inputs
                if event.key == pygame.K_c:
                    PausedBlue = False
                    gameBlue = True
                elif event.key == pygame.K_m:
                    mixer.music.set_volume(0.0)
                    Muted = True
                elif event.key == pygame.K_u:
                    mixer.music.set_volume(0.4)
                    Muted = False
        
        #Background
        screen.fill(bg_color)

        #Text Code
        textDisplay.paused(screen)

        pygame.display.update()
    
    while PausedMedium:
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                main = False
                PausedMedium = False 
            if event.type == pygame.KEYDOWN: #Inputs
                if event.key == pygame.K_c:
                    PausedMedium = False
                    medium = True
                elif event.key == pygame.K_m:
                    mixer.music.set_volume(0.0)
                    Muted = True
                elif event.key == pygame.K_u:
                    mixer.music.set_volume(0.4)
                    Muted = False
        
        #Background
        screen.fill(bg_color)

        #Text Code
        textDisplay.paused(screen)
        pygame.display.update()
    
    while PausedMediumBlue:
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                main = False
                PausedMediumBlue = False 
            if event.type == pygame.KEYDOWN: #Inputs
                if event.key == pygame.K_c:
                    PausedMediumBlue = False
                    mediumBlue = True
                elif event.key == pygame.K_m:
                    mixer.music.set_volume(0.0)
                    Muted = True
                elif event.key == pygame.K_u:
                    mixer.music.set_volume(0.4)
                    Muted = False
        
        #Background
        screen.fill(bg_color)

        #Text Code
        textDisplay.paused(screen)
        pygame.display.update()
    
    while PausedHard:
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                main = False
                PausedHard = False 
            if event.type == pygame.KEYDOWN: #Inputs
                if event.key == pygame.K_c:
                    PausedHard = False
                    hard = True
                elif event.key == pygame.K_m:
                    mixer.music.set_volume(0.0)
                    Muted = True
                elif event.key == pygame.K_u:
                    mixer.music.set_volume(0.4)
                    Muted = False
        
        #Background
        screen.fill(bg_color)

        #Text Code
        textDisplay.paused(screen)
        pygame.display.update()
    
    while PausedHardBlue:
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                main = False
                PausedHardBlue = False 
            if event.type == pygame.KEYDOWN: #Inputs
                if event.key == pygame.K_c:
                    PausedHardBlue = False
                    hardBlue = True
                elif event.key == pygame.K_m:
                    mixer.music.set_volume(0.0)
                    Muted = True
                elif event.key == pygame.K_u:
                    mixer.music.set_volume(0.4)
                    Muted = False
        
        #Background
        screen.fill(bg_color)

        #Text Code
        textDisplay.paused(screen)
        pygame.display.update()

#Closing the program and code
pygame.quit()
sys.exit()