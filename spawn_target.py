import pygame
import random

pygame.init()
screen = pygame.display.set_mode((1000,600))
pygame.display.set_caption("shooter game")
background = pygame.image.load("image/s_sonic_worldpage_hero_hz_3840x2160-54a03f41.jpg.webp")
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
        
        self.cursor_x = random.randint(50, 950)
        self.cursor_y = random.randint(50, 550)
        self.cursor_visible = False
        
        self.shots = []
        
    def shoot(self):
        if self.bullet > 0:
            self.bullet -= 1
            self.cursor_visible = True  
            self.shots.append((self.cursor_x, self.cursor_y))
            return True
        return False
    
    def move_cursor(self, dx, dy):
        self.cursor_x += dx
        self.cursor_y += dy
        self.cursor_x = max(20, min(980, self.cursor_x))
        self.cursor_y = max(20, min(580, self.cursor_y))
        self.cursor_visible = False
    
    def draw(self, screen):
        super().draw(screen)
        
        if self.name == "p1" : color = pygame.Color("#F74825")
        else: color = pygame.Color("#F73BBD")
    
        for shot_x, shot_y in self.shots:
            pygame.draw.circle(screen, color, (shot_x, shot_y), 6)
    
        if self.cursor_visible:
            pygame.draw.circle(screen, color, (self.cursor_x, self.cursor_y), 6)


class Target(GameObject):
    def __init__(self, path, width, height, center_x, center_y):
        super().__init__(path, width, height, center_x, center_y)
        self.score = random.randint(1, 5)
        self.is_active = True

    @staticmethod
    def random_pos(screen_width, screen_height,
                    target_width, target_height,
                    existing_targets,
                    margin=20,
                    min_distance=80):

        while True:
            x = random.randint(
                margin,
                screen_width - target_width - margin
            )

            y = random.randint(
                margin,
                screen_height - target_height - margin
            )

            if Target.is_position_far_enough(
                x,
                y,
                existing_targets,
                min_distance
            ):
                return x, y

    @staticmethod
    def is_position_far_enough(x: int, y: int, existing_targets: list, min_distance: int):
        for target in existing_targets:
            if not target.is_active:
                continue
            tx = target.rect.centerx
            ty = target.rect.centery
            dx = x - tx
            dy = y - ty
            distance_sq = dx * dx + dy * dy
            if distance_sq < (min_distance * min_distance):
                return False
        return True
    
    def respawn(self, screen_width, screen_height, existing_targets):

        x, y = Target.random_pos(
            screen_width,
            screen_height,
            self.rect.width,
            self.rect.height,
            existing_targets
        )

        self.rect.center = (x, y)
        self.is_active = True


#instance
player1 = Player("image/SRCTails.webp", 200, 200, 100, 480, "p1", 10, 60)
player2 = Player("image/images.jpg", 280, 230, 900, 480, "p2", 10, 60)

targets = []
images = ["image/bomb.png", "image/bomb1.png","image/bomb2.png"]
for image in images:
    x, y = Target.random_pos(1000, 600, 60, 60, targets)
    targets.append(Target(image, 60, 60, x, y))


#RUN 
def run_game():
    clock = pygame.time.Clock()
    running = True
    font = pygame.font.SysFont(None, 36)


    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            #player1 movement
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player1.shoot()
                elif event.key == pygame.K_w:
                    player1.move_cursor(0, -30)
                elif event.key == pygame.K_s:
                    player1.move_cursor(0, 30)
                elif event.key == pygame.K_a:
                    player1.move_cursor(-50, 0)
                elif event.key == pygame.K_d:
                    player1.move_cursor(50, 0)
            
            #player2 movement
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    player2.shoot()
                elif event.key == pygame.K_UP:
                    player2.move_cursor(0, -30)
                elif event.key == pygame.K_DOWN:
                    player2.move_cursor(0, 30)
                elif event.key == pygame.K_LEFT:
                    player2.move_cursor(-50, 0)
                elif event.key == pygame.K_RIGHT:
                    player2.move_cursor(50, 0)

#draw
        screen.blit(background, (0,0))
        player1.draw(screen)
        player2.draw(screen)
        for target in targets:
            target.draw(screen)

#bullet Count Display
        txt1 = font.render(f"{player1.name}: {player1.bullet}", True, (255,255,255))
        txt2 = font.render(f"{player2.name}: {player2.bullet}", True, (255,255,255))
        screen.blit(txt1, (10, 10))
        screen.blit(txt2, (10, 50))
        pygame.display.update()
        clock.tick(60)

    pygame.quit()

run_game()