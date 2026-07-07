import pygame

#ساخت محیط اولیه بازی
pygame.init()
screen = pygame.display.set_mode((1000,600))
pygame.display.set_caption("shooter game")
background = pygame.image.load("s_sonic_worldpage_hero_hz_3840x2160-54a03f41.jpg.webp")
background = pygame.transform.scale(background, (1000,600))


class GameObject:
    def __init__(self, path, x, y, x_center, y_center):
        self.image = pygame.image.load(path)
        self.image = pygame.transform.scale(self.image, (x , y))
        self.rect = self.image.get_rect()
        self.rect.center = (x_center, y_center)
    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Player(GameObject):
    def __init__(self, path, x, y, x_center, y_center, name, bullet, time):
        super().__init__(path, x, y, x_center, y_center)

        self.name = name
        self.bullet = bullet
        self.time = time
        self.score = 0


class Target(GameObject):
    def __init__(self):
        pass


class Item(Target):
    def __init__(self):
        super().__init__()
        pass


#نمونه
p1 = Player("SRCTails.webp", 200, 200, 100, 480, "p1", 10, 60)
p2 = Player("1783424683639.jpg", 280, 230, 900, 480, "p2", 10, 60)


def run_game():
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.blit(background, (0,0))
        p1.draw(screen)
        p2.draw(screen)
        clock.tick(60)
        pygame.display.update()

    pygame.quit()

run_game()
