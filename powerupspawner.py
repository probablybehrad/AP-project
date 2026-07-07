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

        powerup = random.choice(["ammo", "time", "debuff"])

        if powerup == "ammo":
            return ExtraAmmoPowerUp(x, y)

        elif powerup == "time":
            return ExtraTimePowerUp(x, y)

        else:
            opponent = random.choice([player1, player2])
            return OpponentDebuffPowerUp(x, y, opponent=opponent)
