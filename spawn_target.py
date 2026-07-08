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
        
    def shoot(self):
        if self.bullet <= 0:
            return None
        self.bullet -= 1

        if self.name == "p1":
            x = self.rect.right
        else:
            x = self.rect.left
        y = self.rect.centery

        self.cursor_visible = True
        return Bullet(x, y, self.cursor_x, self.cursor_y)
    
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
    
    
        if self.cursor_visible:
            pygame.draw.circle(screen, color, (self.cursor_x, self.cursor_y), 10)


class Bullet():
    def __init__(self, start_x, start_y, target_x, target_y):
        self.radius = 10
        self.speed = 7
        self.rect = pygame.Rect(0, 0, 20, 20)
        self.rect.center = (start_x, start_y)
        dx = target_x - start_x
        dy = target_y - start_y
        distance = (dx**2 + dy**2) ** 0.5
        if distance == 0:
            distance = 1
        self.vx = dx / distance
        self.vy = dy / distance

    def move(self):
        self.rect.x += self.vx * self.speed
        self.rect.y += self.vy * self.speed

    def draw(self,screen):
        pygame.draw.circle(screen, (255, 255, 0), self.rect.center, self.radius)

    def is_outside(self):
        return (
            self.rect.right < 0 or
            self.rect.left > 1000 or
            self.rect.bottom < 0 or
            self.rect.top > 600
            )


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

bullets = []


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
                    bullet = player1.shoot()
                    if bullet:
                        bullets.append(bullet)
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
                    bullet = player2.shoot()
                    if bullet:
                        bullets.append(bullet)
                elif event.key == pygame.K_UP:
                    player2.move_cursor(0, -30)
                elif event.key == pygame.K_DOWN:
                    player2.move_cursor(0, 30)
                elif event.key == pygame.K_LEFT:
                    player2.move_cursor(-50, 0)
                elif event.key == pygame.K_RIGHT:
                    player2.move_cursor(50, 0)

#bullet movement
        for bullet in bullets[:]:
            bullet.move()
            if bullet.is_outside():
                bullets.remove(bullet)

#draw
        screen.blit(background, (0,0))
        player1.draw(screen)
        player2.draw(screen)

        for target in targets:
            target.draw(screen)

        for bullet in bullets:
            bullet.draw(screen)

#bullet Count Display
        txt1 = font.render(f"{player1.name}: {player1.bullet}", True, (255,255,255))
        txt2 = font.render(f"{player2.name}: {player2.bullet}", True, (255,255,255))
        screen.blit(txt1, (10, 10))
        screen.blit(txt2, (10, 50))
        pygame.display.update()
        clock.tick(60)

    pygame.quit()

run_game()