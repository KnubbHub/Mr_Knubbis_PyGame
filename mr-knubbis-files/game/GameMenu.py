import pygame
import pygame_menu     

class GameMenu:
    # Colors
    white=(255, 255, 255)
    black=(0, 0, 0)
    gray=(50, 50, 50)
    red=(255, 0, 0)
    green=(0, 255, 0)
    blue=(0, 0, 255)
    yellow=(255, 255, 0)
    sea=(17, 69, 136)
    brown=(69, 36, 21)

    # Configs
    font = pygame_menu.font.FONT_FRANCHISE
    background_color = None
    title_color = None
    menuitem_color = None
    active_menuitem_color = None
    hide_after = None
    disable_selection = False
    FPS = None

    # Surface
    surface = None

    # Internals
    title = ""
    menu = []
    selected = 0

    def __init__(self, title, menu, 
                background_color = None, 
                title_color = None,
                menuitem_color = None,
                active_menuitem_color = None,
                hide_after = None,
                disable_selection = False,
                FPS = 60):

        if background_color:
            self.background_color = background_color
        else:
            self.background_color = self.sea

        if title_color:
            self.title_color = title_color
        else:
            self.title_color = self.gray

        if menuitem_color:
            self.menuitem_color = menuitem_color
        else:
            self.menuitem_color = self.black

        if active_menuitem_color:
            self.active_menuitem_color = active_menuitem_color
        else:
            self.active_menuitem_color = self.brown

        self.hide_after = hide_after

        self.disable_selection = disable_selection
        if self.disable_selection:
            self.selected = -1

        self.FPS = FPS

        if False == pygame.get_init():
            self.log("PyGame not yet initialized.")
            pygame.init()
            self.log("PyGame initialized.")

            self.surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.SCREEN_WIDTH, self.SCREEN_HEIGHT = pygame.display.get_surface().get_size()
            self.log("Creating display surface area (%s x %s)." % (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        else:
            self.surface = pygame.display.get_surface()
            self.SCREEN_WIDTH, self.SCREEN_HEIGHT = pygame.display.get_surface().get_size()
            self.log("Retrieving display surface area (%s x %s)." % (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        self.log("Setting title to %s" % str(title))
        self.title = str(title)
        
        self.log("Setting up menu (%s)" % (str(menu)))
        self.menu = menu
        selected = 0

    def log(self, message):
        print("[%s]: %s" % (str(self.__class__), str(message)))

    def text_format(self, message, textFont, textSize, textColor):
        newFont=pygame.font.Font(textFont, textSize)
        newText=newFont.render(message, 0, textColor)
        return newText

    def show(self):
        if self.hide_after:
            self.log("Configured to hide after %s seconds" % (str(self.hide_after)))
            starttime = pygame.time.get_ticks()
            #pygame.time.set_timer(HIDE, self.hide_after)

        while True:
            for event in pygame.event.get():
                if pygame.QUIT == event.type:
                    self.log("QUIT event. Exiting ...")
                    pygame.quit()
                    quit()

                if self.hide_after:
                    if (pygame.time.get_ticks() - starttime) > (self.hide_after*1000):
                        self.log("Time to hide.")
                        return None

                if self.disable_selection:
                    continue

                if pygame.KEYDOWN == event.type:
                    if pygame.K_UP == event.key:
                        self.log("Key UP pressed. \"%s\"[%s] selected." % (self.menu[self.selected], self.selected))
                        self.selected -= 1
                        if self.selected < 0:
                            self.selected = len(self.menu) - 1
                    if pygame.K_DOWN == event.key:
                        self.log("Key DOWN pressed. \"%s\"[%s] selected." % (self.menu[self.selected], self.selected))
                        self.selected += 1
                        if self.selected >= len(self.menu):
                            self.selected = 0
                    if pygame.K_RETURN == event.key:
                        self.log("Selected \"%s\"[%s]." % (self.menu[self.selected], self.selected))
                        return self.menu[self.selected]

            #self.log("Setting background color to %s" % str(self.background_color))
            self.surface.fill(self.background_color)

            w, h = pygame.display.get_surface().get_size()
            #self.log("Window size is %s x %s" % (str(w), str(h)))

            #self.log("Setting title to \"%s\"" % (self.title))
            height = h*0.1
            title = self.text_format("%s" % (self.title), self.font, int(h*0.2), self.title_color)
            self.surface.blit(title, (w/2 - (title.get_rect()[2]/2), height))

            height = h*0.5
            if len(self.menu) > 3:
                fontsize = int((h*0.5)/len(self.menu))
            else:
                fontsize = int(h*0.07)
            i = 0
            for menuitem in self.menu:
                #self.log("Adding menuitem: %s" % (menuitem))
                if self.selected == i:
                    color = self.active_menuitem_color
                else:
                    color = self.menuitem_color
                tf = self.text_format("%s" % (str(menuitem)), self.font, fontsize, color)
                self.surface.blit(tf, (w/2 - (tf.get_rect()[2]/2), height))
                height += int(fontsize*0.8)
                i += 1

            #self.log("Update display")
            pygame.display.update()
            pygame.time.Clock().tick(50)



if __name__ == "__main__":
    pygame.init()
    s = pygame.display.set_mode((640, 380))
    GM = GameMenu(s, "Min meny", ["Ett", "Två", "Tre"])

    while True:
        val = GM.show()
        print("Valet blev: %s" % (str(val)))
    


