import pygame, sys
from pygame.locals import *
import json, time

#initialising pygame
pygame.init()

class main:
    
    """ ----- Variables ----- """

    # Colors
    white = (255, 255, 255)
    black = (0, 0, 0)
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    yellow = (255, 255, 0)
    aqua = (0, 255, 255)
    pink = (255, 0, 255)

    # Fonts
    font_montserrat_bold = pygame.font.Font("assets/textures/fonts/montserratbold.ttf", 32)
    font_montserrat_bold_small = pygame.font.Font("assets/textures/fonts/montserratbold.ttf", 20)

    # Settings
    FPS = 60
    FramePerSec = pygame.time.Clock()

    w = 800
    h = 600

    surface = pygame.display.set_mode((w, h), pygame.RESIZABLE)
    SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.get_surface().get_size()

    TITLE = "Böb Clicker"

    # Images
    bob_img = None
    bob_img_rect = None
    background_img = None

    # Game variables
    name = None
    bobs = None
    bobster = None
    bobSlaves = None

    # Other
    name_input_box = None
    input_boxes = None
    code_input = ''
    code_input_rect = pygame.Rect(10, h - 42, 140, 32)
    input_rect_color = pygame.Color('chartreuse4')
    code_data = None
    code_data_value = []

    """ ----- Code ----- """

    def __init__(self):

        if False == pygame.get_init():
            self.log("PyGame not yet initialized.")
            pygame.init()
            self.log("PyGame initialized.")
        
        self.surface.fill(self.white)

        self.log("Creating display surface area (%s x %s)." % (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        pygame.display.set_caption(self.TITLE)
        self.log("Setting title to \"%s\"" % (self.TITLE) + ".")

        self.bob_img = pygame.image.load("assets/textures/bob/bob.png")
        self.bob_img = pygame.transform.scale(self.bob_img, (500, 500))
        self.bob_img_rect = self.bob_img.get_rect(center = (self.w / 2, self.h / 2))
        self.background_img = pygame.image.load("assets/textures/background/background.png")
        self.log("Setting up images")

        self.bobs = self.get_config("bobs")
        self.bobster = self.get_config("bobster")
        self.name = self.get_config("name")
        self.log("Getting values from config file. (assets/settings/config.json)")

        # self.name_input_box = input_box(10, self.h - 42, 140, 32)
        # self.input_boxes = [self.name_input_box]

        self.get_codes()

    def get_codes(self):
        codeFile = open("codes.txt", "r")
        self.code_data = codeFile.readlines()
        self.code_data = map(lambda s: s.strip(), self.code_data)
        # code_data = self.code_data
        # for line in code_data:
        #     self.code_data_value.append(int(line.strip().split('-')[-1]))

    def get_config(self, item):
        with open("assets/settings/config.json", "r") as configFileR:
            data = json.load(configFileR)

        if item == "bobs":
            data = data["bobs"]
            return data
        
        elif item == "bobster":
            data = data["bobster"]
            return data
        
        elif item == "name":
            data = data["name"]
            return data
        configFileR.close()
        
    def save_config(self):
        configFileData = {
            "bobs" : self.bobs,
            "bobster" : self.bobster,
            "name" : self.name
        }

        with open("assets/settings/config.json", "w") as configFileW:
            json.dump(configFileData, configFileW)
            configFileW.close()
        self.log("Böbs: %s, Böbster: %s, Name: %s" % (self.bobs, self.bobster, self.name))

    def log(self, message):
        print("[%s]: %s" % (str(self.__class__), str(message)))

    def start(self):
        pygame.event.pump()
        self.log(self.code_data_value)
        self.log(self.code_data)
        
        while True:

            self.surface.blit(self.background_img, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.save_config()
                    pygame.quit()
                    sys.exit()
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F11:
                        pygame.display.toggle_fullscreen()

                    elif event.key == pygame.K_BACKSPACE:
                        self.code_input = self.code_input[:-1]
                        backPressed = True

                    elif event.key == pygame.K_SPACE:
                        self.bobs = self.bobs + self.bobster

                    elif event.key == pygame.K_RETURN:
                        if self.code_input in self.code_data:
                            self.log("Works")
                            self.log(self.code_data_value)
                            self.code_input = ''
                    
                    else:
                        if len(self.code_input) < 22:
                            self.code_input += event.unicode
                            backPressed = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Set the x, y postions of the mouse click
                    x, y = event.pos
                    if self.bob_img.get_rect(center = (self.w / 2, self.h / 2)).collidepoint(x, y):
                        self.bobs = self.bobs + self.bobster

                elif len(self.code_input) == 5 or len(self.code_input) == 11 or len(self.code_input) == 17:
                    if backPressed == True:
                        pass
                    else:
                        self.code_input += '-'

            bob_text = self.font_montserrat_bold.render("Böbs: %s" % (self.bobs), True, self.black)
            self.surface.blit(bob_text, (10, 10))
            bobster_text = self.font_montserrat_bold.render("Böbster: %s" % (self.bobster), True, self.black)
            self.surface.blit(bobster_text, (10, 47))

            self.surface.blit(self.bob_img, self.bob_img_rect)

            name_text = self.font_montserrat_bold.render("Redeem your code:", True, self.black)
            self.surface.blit(name_text, (10, self.h - 77))

            pygame.draw.rect(self.surface, self.input_rect_color, self.code_input_rect)
            txt_surface = self.font_montserrat_bold.render(self.code_input , True, (255, 255, 255))
            self.surface.blit(txt_surface, (self.code_input_rect.x + 5, self.code_input_rect.y - 5))
            self.code_input_rect.w = max(140, txt_surface.get_width() + 10)

            self.get_codes()

            self.FramePerSec.tick(self.FPS)
            pygame.display.update()


""" ----- Start code ----- """

if __name__ == "__main__":
    game = main()
    game.start()
