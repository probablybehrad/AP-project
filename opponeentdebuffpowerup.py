class OpponentDebuffPowerUp(Target):

   # آیتم منفی.
   # با شلیک به این آیتم، زمان حریف کاهش پیدا می‌کند.

    def __init__(self, x, y, image=None, opponent=None, penalty_time=3):
        super().__init__(x, y, image)
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
