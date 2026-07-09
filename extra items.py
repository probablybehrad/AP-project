import pygame
import random
import math


pygame.init()
screen = pygame.display.set_mode((1000,600))
pygame.display.set_caption("shooter game")
background = pygame.image.load("image/s_sonic_worldpage_hero_hz_3840x2160-54a03f41.jpg.webp")
background = pygame.transform.scale(background, (1000,600))


def calculate_extra_points(last_shot_pos, new_shot_pos):
   # محاسبه امتیاز اضافه بر اساس فاصله دو شلیک.

    if last_shot_pos is None:
        return 0

    distance = math.sqrt(
        (new_shot_pos[0] - last_shot_pos[0]) ** 2 +
        (new_shot_pos[1] - last_shot_pos[1]) ** 2
    )

    if distance >= 400:
        return 5
    elif distance >= 300:
        return 4
    elif distance >= 200:
        return 3
    elif distance >= 100:
        return 2
    elif distance >= 50:
        return 1

    return 0


class PowerUpSpawner:
    def __init__(self, spawn_interval_seconds=8.0):
        self._spawn_interval = spawn_interval_seconds
        self._elapsed = 0

    def update(self, dt, screen_width, screen_height, player1=None, player2=None):
        self._elapsed += dt

        if self._elapsed < self._spawn_interval:
            return None

        self._elapsed = 0

        x = random.randint(20, screen_width - 70)
        y = random.randint(20, screen_height - 70)

        powerup = random.choice(["aim", "time", "debuff"])

        if powerup == "aim":
            return ExtraAimPowerUp(x, y)

        elif powerup == "time":
            return ExtraTimePowerUp(x, y)

        else:
            opponent = random.choice([player1, player2])
            return OpponentDebuffPowerUp(x, y, opponent=opponent)


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

    def add_time(self, sec):
        self.time += sec

    def add_bullets(self, amount):
        self.bullet += amount

        #کم کردن زمان بازیکن در هر فریم
    def tick_time(self, dt):
        self.time_left = max(0, self._time_left - dt)

        self.player1.tick_time(dt)
        self.player2.tick_time(dt)

        if self.check_game_over():
            self._running = False
        
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
    def __init__(self, path, x, y, x_center, y_center):
        super().__init__(path, x, y, x_center, y_center)
        self.score = random.randint(1, 5)
        self.is_active = True

    def deactivate(self):
        self.is_active = False

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
            self.rect.x,
            self.rect.y,
            existing_targets
        )

        self.rect.center = (x, y)
        self.is_active = True


class OpponentDebuffPowerUp(Target):
   # آیتم منفی.
   # با شلیک به این آیتم، زمان حریف کاهش پیدا می‌کند.

    def __init__(self, path, x, y, opponent=None, penalty_time=3):
        super().__init__(path, x, y)
        self._opponent = opponent
        self._penalty_time = penalty_time

    @property
    def opponent(self):
        return self._opponent

    @property
    def penalty_time(self):
        return self._penalty_time

    def on_hit(self, player, last_shot_distance=None):
        if self._opponent is not None:
            self._opponent.add_time(-self._penalty_time)

        self.deactivate()

    def update(self, *args, **kwargs):
        pass


class ExtraAimPowerUp(Target):
    # آیتم خشاب اضافی.
    # با شلیک موفق، تعدادی تیر به بازیکن اضافه می‌شود.

    def __init__(self, path, x: int, y: int, bullets_amount: int = 5):
        super().__init__(path, x, y)
        self._bullets_amount = bullets_amount

    @property
    def bullets_amount(self):
        return self._bullets_amount

    def on_hit(self, player: Player, last_shot_distance: float = None):
        # در صورت برخورد موفق:
        # - تعداد تیرهای بازیکن افزایش پیدا می‌کند.
        # - آیتم از صفحه حذف می‌شود.

        player.add_bullets(self._bullets_amount)
        self.deactivate()

    def update(self, *args, **kwargs):
        # فعلاً رفتار خاصی ندارد.
        # در صورت نیاز می‌توان بعداً انیمیشن یا حرکت به آن اضافه کرد.
        pass


class ExtraTimePowerUp(Target):
   # آیتم زمان اضافی.
   # با شلیک موفق، زمان بازیکن افزایش پیدا می‌کند.

    def __init__(self, path, x: int, y: int, seconds_amount: float = 10):
        super().__init__(path, x, y)
        self._seconds_amount = seconds_amount

    @property
    def seconds_amount(self):
        return self._seconds_amount

    def on_hit(self, player: Player, last_shot_distance: float = None):
       # در صورت برخورد موفق:
       # - زمان بازیکن افزایش پیدا می‌کند.
       # - آیتم از صفحه حذف می‌شود.

        player.add_time(self._seconds_amount)
        self.deactivate()

    def update(self, *args, **kwargs):
       # فعلاً رفتار خاصی ندارد.
       # در صورت نیاز می‌توان بعداً انیمیشن یا حرکت به آن اضافه کرد.
        pass


#instance
player1 = Player("image/SRCTails.webp", 200, 200, 100, 480, "p1", 10, 60)
player2 = Player("image/images.jpg", 280, 230, 900, 480, "p2", 10, 60)

targets = []
images = ["image/bomb.png", "image/bomb1.png","image/bomb2.png"]
for image in images:
    x, y = Target.random_pos(1000, 600, 60, 60, targets)
    targets.append(Target(image, 60, 60, x, y))


def check_game_over():
    if (player1.time == 0 or player1.bullet == 0) and (player2.bullet == 0 or player2.time == 0):
            return True
    return False
    

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

        if check_game_over():
            running = False            

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