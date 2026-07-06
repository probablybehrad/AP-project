import pygame
import random
# from classes.powerup import PowerUp
# from config import *

# کنترل آیتم های اضافه


class PowerUpManager:

    def __init__(self):
        self.powerups = []
        self.last_spawn_time = 0
        self.spawn_interval = POWERUP_SPAWN_INTERVAL
        self.max_powerups = MAX_POWERUPS_ON_SCREEN

    def update(self, current_time):
        # تولید آیتم جدید
        if (current_time - self.last_spawn_time > self.spawn_interval and
                len(self.powerups) < self.max_powerups):

            if random.random() < 0.7:  # ۷۰٪ شانس تولید
                self.spawn_powerup()

            self.last_spawn_time = current_time

        # به‌روزرسانی آیتم‌های موجود
        for powerup in self.powerups[:]:
            powerup.update()
            if not powerup.is_active():
                self.powerups.remove(powerup)
# تولید یک آیتم  جدید

    def spawn_powerup(self):
        powerup = PowerUp()
        self.powerups.append(powerup)
        return powerup
# بررسی برخورد آیتم ها با بازیکنان

    def check_collisions(self, players):
        messages = []

        for powerup in self.powerups[:]:
            if not powerup.is_active():
                continue

            for player in players:
                if not player.alive:
                    continue

                # برخورد
                if powerup.get_rect().colliderect(player.get_rect()):
                    message = powerup.on_hit(player)
                    messages.append(message)
                    self.powerups.remove(powerup)
                    break

        return messages
# رسم تمام آیتم ها

    def draw(self, screen):
        for powerup in self.powerups:
            powerup.draw(screen)
# بازنشانی

    def reset(self):
        self.powerups.clear()
        self.last_spawn_time = 0
