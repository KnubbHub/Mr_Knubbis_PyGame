#Imports
import pygame, sys, pygame_menu
from pygame.locals import *
import random, time, os
from GameMenu import GameMenu
#import PySimpleGUI 
#import moviepy
#from moviepy.editor import *

"""
pygame.display.set_caption('Mr: Knubbis')

clip = VideoFileClip('video\\video.mp4')

os.environ["SDL_VIDEO_CENTERED"] = "1"

clip.preview()

for event in pygame.event.get():
    if event.type == KEYDOWN:
      if event.key == K_ESCAPE:
             break
"""
class Enemy(pygame.sprite.Sprite):
    game = None

    def __init__(self, game):
        super().__init__()
        self.game = game
        self.image = pygame.image.load("assets\\mr-knubbis\\textures\\player-enemy\\Enemy.png")
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.surf = pygame.Surface((42, 70))
        self.rect = self.surf.get_rect(center = (self.game.SCREEN_WIDTH, self.game.SCREEN_HEIGHT - 60))

    def move(self):
        global score
        self.rect.move_ip(-self.game.SPEED, 0)
        if (self.rect.left < 0):
            self.game.score += 1
            self.rect.right = 0
            self.rect.center = (self.game.SCREEN_WIDTH, self.game.SCREEN_HEIGHT - 60)


class Player(pygame.sprite.Sprite):
    game = None

    def __init__(self, game):
        super().__init__() 
        self.game = game
        self.image = pygame.image.load("assets\\mr-knubbis\\textures\\player-enemy\\Player.png")
        self.image = pygame.transform.scale(self.image, (70, 70))
        self.surf = pygame.Surface((40, 75))
        self.rect = self.surf.get_rect(center = (40, self.game.SCREEN_HEIGHT - 60))

        # Jump related
        self.isjump = False
        self.mass = 6
        self.velocity = 5
       
    def move(self):
        pressed_keys = pygame.key.get_pressed()
        pressed_mouse = pygame.mouse.get_pressed()
        if self.rect.left > 0:
              if pressed_keys[K_LEFT]:
                  self.rect.move_ip(-10, 0)
        if self.rect.right < self.game.SCREEN_WIDTH:        
              if pressed_keys[K_RIGHT]:
                  self.rect.move_ip(10, 0)
        if not self.isjump:
            if pressed_keys[K_SPACE] or pressed_mouse[0]:
                self.isjump = True
                pygame.time.set_timer(self.game.JUMPING, 100)

    def isJumping(self):
    	return self.isjump

    def jumpMove(self):
        # calculate force (F). F = 1 / 2 * mass * velocity ^ 2.
        F =(1 / 2)*self.mass*(self.velocity**2)
           
        # change in the y co-ordinate
        #y-= F
        self.rect.move_ip(0, 1*(-F))
           
        # decreasing velocity while going up and become negative while coming down
        self.velocity -= 1
           
        # object reached its maximum height
        if self.velocity < 0:
            # negative sign is added to counter negative velocity
            self.mass = -6
   
        # objected reaches its original state
        if self.velocity == -6:
            # making isjump equal to false 
            self.isjump = False
            pygame.time.set_timer(self.game.JUMPING, 0)
            # setting original values to v and m
            self.velocity = 5
            self.mass = 6

class Knubbis:
    # Colors
    white=(255, 255, 255)
    black=(0, 0, 0)
    gray=(50, 50, 50)
    red=(255, 0, 0)
    green=(0, 255, 0)
    blue=(0, 0, 255)
    yellow=(255, 255, 0)

    font = None
    font_small = None

    FPS = None
    FramePerSec = None
    SCREEN_WIDTH = None
    SCREEN_HEIGHT = None
    surface = None

    TITLE = None
    SPEED = None
    DIFFICULTY = None
    DIFFICULTY_OPT = None
    NAME = None
    score = None

    INC_SPEED = None
    JUMPING = None 

    def __init__(self):
        if False == pygame.get_init():
            self.log("PyGame not yet initialized.")
            pygame.init()
            self.log("PyGame initialized.")

        self.log("Setting frame rate.")
        self.FramePerSec = pygame.time.Clock()
        self.FPS = 60

        self.log("Setting up fonts.")
        self.font = pygame.font.SysFont("Verdana", 60)
        self.font_small = pygame.font.SysFont("Verdana", 20)

        self.surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = pygame.display.get_surface().get_size()
        self.log("Creating display surface area (%s x %s)." % (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        self.TITLE = "Mr: Knubbis"
        pygame.display.set_caption(self.TITLE)
        self.log("Setting title to \"%s\"" % (self.TITLE))

        self.log("Setting score to 0.")
        self.score = 0

        self.log("Setting speed to 5.")
        self.SPEED = 5

        self.log("Setting difficulty to 0,3, difficulty_opt to 1.")
        self.DIFFICULTY = 0.3
        self.DIFFICULTY_OPT = 1

        self.log("Setting name to default.")
        self.NAME = "Mr: Knubbis"

        self.log("Setting user event for increasing speed.")
        self.INC_SPEED = pygame.USEREVENT + 1
        pygame.time.set_timer(self.INC_SPEED, 1000)

        self.log("Setting user event for jumping.")
        self.JUMPING = pygame.USEREVENT + 2
        pygame.time.set_timer(self.JUMPING, 0)

    def log(self, message):
        print("[%s]: %s" % (str(self.__class__), str(message)))

    def set_difficulty(self, value, difficulty):
        self.log("Setting difficulty to %s (%s)" % (value, difficulty))
        self.DIFFICULTY = difficulty
        self.DIFFICULTY_OPT = value

    def set_volume(self, value):
        self.log("Setting volume to %s" % (value/100))
        pygame.mixer.music.set_volume(value/100)

    def set_name(self, value):
        self.log("Setting name to %s" % (value))
        self.NAME = value

    def get_highscore(self):
        self.log("Visar highscore.")
        self.log("Läser in highscore från fil.")
        file = "highscore.txt"
        f = open(file, "r")
        try:
            highscore = int(f.read())
        except:
            highscore = 0
        f.close()
        return int(highscore)

        """
        self.log("Visar highscore.")
        HSM = GameMenu("Högsta poäng", ["%s" % (highscore), "<-- Back to home"], background_color=GameMenu.sea, title_color=GameMenu.gray)
        while True:
            val = HSM.show()
            if "<-- Back to home" == val:
                self.log("Showing main menu.")
            break
        """

    def start(self):
        self.log("Creating menu Theme")
        mytheme = pygame_menu.themes.THEME_BLUE.copy()
        mytheme.background_color = (62, 149, 195)
        myfont = 'assets\\mr-knubbis\\textures\\font\\Retro.ttf'
        mytheme.title_font = myfont
        mytheme.title_font_size = 72
        mytheme.widget_font = myfont
        mytheme.widget_font_size = 72
        mytheme.title_font_shadow = True
        mytheme.widget_font_shadow = True
        mytheme.widget_font_color = (0, 0, 0)
        mytheme.title_font_color = (0, 30, 40)
        mytheme.widget_shadow_font_color = (0, 0, 0)
        mytheme.title_font_shadow_color = (0, 30, 40)
        mytheme.widget_url_color = (255, 0, 0)

        self.log("Creating about menu")
        about_menu = pygame_menu.Menu("About", self.SCREEN_WIDTH, self.SCREEN_HEIGHT,
               theme=mytheme )

        #about_menu.add.url('https://www.youtube.com/dream', 'YouTube')
        about_menu.add.button('Back', pygame_menu.events.BACK)

        self.log("Creating settings menu")
        settings_menu = pygame_menu.Menu("Settings", self.SCREEN_WIDTH, self.SCREEN_HEIGHT,
                       theme=mytheme )

        settings_menu.add.text_input('Name: ', default=self.NAME, onchange=self.set_name)
        settings_menu.add.selector('Difficulty :', [('Easy', 0.1), ('Normal', 0.3), ('Hard', 1.0)], 
            onchange=self.set_difficulty, default=self.DIFFICULTY_OPT)
        settings_menu.add.range_slider('Volume', pygame.mixer.music.get_volume()*100, (0, 100), 1,
                      rangeslider_id='range_slider',
                      onchange=self.set_volume,
                      value_format=lambda x: str(int(x)))
        settings_menu.add.button('Back', pygame_menu.events.BACK)

        self.log("Creating highscore menu")
        highscore_menu = pygame_menu.Menu("Highscore", self.SCREEN_WIDTH, self.SCREEN_HEIGHT,
               theme=mytheme )

        #highscore_menu.add.label("%s high" % (self.NAME()))
        highscore_menu.add.label("Highscore: %s" % (self.get_highscore()))
        highscore_menu.add.button('Back', pygame_menu.events.BACK)

        self.log("Creating main menu for the first time.")
        menu = pygame_menu.Menu("Mr: Knubbis", self.SCREEN_WIDTH, self.SCREEN_HEIGHT,                   
            theme=mytheme )

        menu.add.button('Play', self.run_game)
        menu.add.button('Highscore', highscore_menu)
        menu.add.button('About', about_menu)
        menu.add.button('Settings', settings_menu) 
        menu.add.button('Quit', pygame_menu.events.EXIT)

        # self.log("Game Music On.")
        # pygame.mixer.music.load('music\\music.wav')
        # pygame.mixer.music.play(-1, 0.0)

        menu.mainloop(self.surface)
        """
        while True:
            self.log("Showing main menu.")
            val = GM.show()

            if "Start" == val or "Försök igen" == val:
                self.log("Request to start the game.")
                self.run_game()

            elif "Avsluta" == val:
                self.log("Request to quit the game")
                pygame.quit()
                quit()

            if "Högsta poäng" == val:
                self.log("Visar highscore.")
                self.log("Läser in highscore från fil.")
                file = "highscore.txt"
                f = open(file, "r")
                highscore = f.read()
                f.close()
                self.log("Visar highscore.")
                HSM = GameMenu("Högsta poäng", ["%s" % (highscore), "<-- Back to home"], background_color=GameMenu.sea, title_color=GameMenu.gray)
                while True:
                    val = HSM.show()
                    if "<-- Back to home" == val:
                        self.log("Showing main menu.")
                    break
            
            if "Inställningar" == val:
                self.log("Visar inställningar.")
                self.Settings()
                self.Slider()
        """

        #self.log("Recreating main menu.")
        #GM = GameMenu("Mr: Knubbis", ["Försök igen", "Högsta poäng", "Inställningar", "Avsluta"], background_color=GameMenu.sea, title_color=GameMenu.gray)

    def run_game(self):
        self.log("Game On.")

        self.log("Setting score to 0.")
        self.score = 0

        self.log("Setting background image.")
        background = pygame.image.load("assets\\mr-knubbis\\textures\\background\\background.png")
        background = pygame.transform.scale(background, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        self.log("White background.")
        self.surface.fill(self.white)

        self.log("Setting up a Player and an Enemy.")       
        P1 = Player(self)
        E1 = Enemy(self)

        self.log("Adding Player and Enemy to a group of sprites.")
        enemies = pygame.sprite.Group()
        enemies.add(E1)
        all_sprites = pygame.sprite.Group()
        all_sprites.add(P1)
        all_sprites.add(E1)

        self.log("Game loop begins.")
        while True:
            for event in pygame.event.get():
                if event.type == self.JUMPING:
                    self.log("Player jumps.")
                    P1.jumpMove()
                if event.type == self.INC_SPEED:
                    self.log("Speed increases.")
                    self.SPEED += self.DIFFICULTY     
                if event.type == QUIT:
                    self.log("Quit. Exiting ...")
                    pygame.quit()
                    sys.exit()

            #self.log("Show background.")
            self.surface.blit(background, (0,0))

            #self.log("Show score.")
            scores = self.font.render(str(self.score), True, Knubbis.black)
            self.surface.blit(scores, (30,30))

            #self.log("Update position of Player and Enemy.")
            for entity in all_sprites:
                self.surface.blit(entity.image, entity.rect)
                entity.move()

            if pygame.sprite.spritecollideany(P1, enemies):
                # self.log("Stopping Game Music.")
                # pygame.mixer.music.stop()

                self.log("Collision occurs between Player and Enemy.")
                pygame.mixer.Sound('assets\\mr-knubbis\\sounds\\die\\die.wav').play()
                time.sleep(0.45)

                self.log("Show game over screen and score (%s)." % (str(self.score)))
                GM = GameMenu("Game Over", ["%s got score: %s" % (self.NAME, self.score)], background_color=GameMenu.red, menuitem_color=GameMenu.black, title_color=GameMenu.black, disable_selection=True, hide_after=3)
                GM.show()
                f = open('highscore.txt', 'r', encoding = 'utf-8')
                try:
                    existing_highscore = int(f.read())
                    f.close()
                    self.log("Existing highscore is %s" % (existing_highscore))
                except IOError as e:
                    self.log("Failed to retreive existing highscore.\n%s" % (e))
                    existing_highscore = 0

                if int(self.score) > int(existing_highscore):
                    self.log("Writing new highscore to file")
                    with open('highscore.txt', 'w', encoding = 'utf-8') as f:
                        f.write("%s" % (str(self.score)))
                        f.close()

                self.log("Clean up all sprites.")
                for entity in all_sprites:
                    entity.kill()

                self.log("Game is over. Return ...")
                 
                # self.log("Game Music On.")
                # pygame.mixer.music.load('music\\music.wav')
                # pygame.mixer.music.play(-1, 0.0)
                
                return
            
            #self.log("Update screen and continue with loop (FPS:%s)." % (self.FPS))
            pygame.display.update()
            self.FramePerSec.tick(self.FPS)



if __name__ == "__main__":
    game = Knubbis()
    game.start()
    

