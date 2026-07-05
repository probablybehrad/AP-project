import pygame


class Game:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height


    def start_game(self, p1: str, p2: str):
        pygame.init()
        screen = pygame.display.set_mode((600, 1000))
        pygame.display.set_caption(" ") #games title
        screen.fill(()) #screen color
        clock = pygame.time.Clock()
        
        #color
        #font
        #sound


class Player(Game):
    def __init__(self, x, y, name, color, bullet, time):
        super().__init__(x, y, 20, 20) #پیکسل بازیکن هارو ثابت باید بگیریم(بعدا خواستیم تغییر میدیم)
        self.name = name
        self.color = color
        self.bullet = bullet
        self.time = time

    def status(self):
        pass


#main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #keybord buttons status


#draw
pygame.display.update()

pygame.quit()