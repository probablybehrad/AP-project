"""
game_skeleton.py

اسکلت خالی پروژه.
این فایل فقط "قرارداد" بین اعضای تیمه: اسم کلاس‌ها، متدها و پارامترهاشون.


هدف: هرکس بدونه بقیه چه متدهایی صدا می‌زنن، تا بتونه مستقل کار کنه

مسئولیت‌ها:
    نفر ۱ -> GameObject, Player, Game
    نفر ۲ -> Target, spawn_random_target, check_hit
    نفر ۳ -> PowerUp ها, PowerUpSpawner
    نفر ۴ -> NameInputScreen, HUD, ResultScreen


صفحه بازی 1000 طول و 600 عرضه
"""

import pygame


# ============================================================
# نفر ۱
# ============================================================
class GameObject:
    """کلاس والد مشترک همه‌ی اشیاء بازی."""

    def __init__(self, x: int, y: int, image: pygame.Surface = None):
        pass

    @property
    def position(self):
        pass

    @position.setter
    def position(self, new_pos):
        pass

    @property
    def is_active(self):
        pass

    def deactivate(self):
        pass

    def update(self, *args, **kwargs):
        pass

    def draw(self, screen: pygame.Surface):
        pass

    def get_rect(self) -> pygame.Rect:
        pass


class Player(GameObject):
    """بازیکن: نام، رنگ، تیر، زمان، امتیاز، نشانگر."""

    def __init__(self, name: str, color: str, start_x: int, start_y: int,
                initial_bullets: int, initial_time: int):
        pass

    @property
    def name(self):
        pass

    @property
    def color(self):
        pass

    @property
    def bullets(self):
        pass

    @property
    def time_left(self):
        pass

    @property
    def score(self):
        pass

    @property
    def cursor_pos(self):
        pass

    def can_shoot(self) -> bool:
        pass

    def move_cursor(self, dx: int, dy: int, bounds: tuple):
        pass

    def shoot(self) -> bool:
        pass

    def add_bullets(self, amount: int):
        pass

    def add_time(self, seconds: float):
        pass

    def add_score(self, points: int):
        pass

    def tick_time(self, dt: float):
        pass

    def update(self, *args, **kwargs):
        pass

    def draw(self, screen):
        pass


# ============================================================
# نفر ۲
# ============================================================
class Target(GameObject):
    """سیبل. با شلیک موفق امتیاز می‌ده."""

    def __init__(self, x: int, y: int, image=None):
        pass

    def on_hit(self, player: Player, last_shot_distance: float = None):
        pass

    def update(self, *args, **kwargs):
        pass


def spawn_random_target(screen_width: int, screen_height: int, image=None) -> Target:
    pass


def check_hit(cursor_pos: tuple, target: Target) -> bool:
    pass


# ============================================================
# نفر ۳
# ============================================================
class PowerUp(Target):
    """
    والد مشترک آیتم‌های اضافه (طبق الزام پروژه، از Target ارث می‌بره).
    حداقل ۳ کلاس فرزند از این باید ساخته بشه
    (مثلا ExtraAmmoPowerUp, ExtraTimePowerUp, OpponentDebuffPowerUp).
    """

    def __init__(self, x: int, y: int, image=None):
        pass

    def on_hit(self, player: Player, last_shot_distance: float = None):
        pass


class PowerUpSpawner:
    """زمان‌بندی ظاهر شدن آیتم‌ها روی صفحه."""

    def __init__(self, spawn_interval_seconds: float):
        pass

    def update(self, dt: float, screen_width: int, screen_height: int,
                player1: Player = None, player2: Player = None):
        pass


# ============================================================
# نفر ۴
# ============================================================
class NameInputScreen:
    """صفحه‌ی ورود نام دو بازیکن."""

    def __init__(self, screen: pygame.Surface):
        pass

    def handle_event(self, event):
        pass

    def draw(self):
        pass

    @property
    def is_done(self) -> bool:
        pass

    def get_names(self):
        pass


class HUD:
    """نمایش نام، رنگ، تیر، زمان، امتیاز حین بازی."""

    def __init__(self, screen: pygame.Surface, font: pygame.font.Font = None):
        pass

    def draw(self, player1: Player, player2: Player):
        pass


class ResultScreen:
    """صفحه پایانی: نمایش نتیجه و برنده."""

    def __init__(self, screen: pygame.Surface, font: pygame.font.Font = None):
        pass

    def draw(self, player1: Player, player2: Player):
        pass


# ============================================================
# نفر ۱: کلاس اصلی بازی
# ============================================================
class Game:
    STATE_NAME_INPUT = "name_input"
    STATE_PLAYING = "playing"
    STATE_RESULT = "result"

    def __init__(self):
        pass

    def _start_game(self, name1: str, name2: str):
        pass

    def _handle_events(self):
        pass

    def _update(self, dt: float):
        pass

    def _draw(self):
        pass

    def run(self):
        pass


if __name__ == "__main__":
    Game().run()
