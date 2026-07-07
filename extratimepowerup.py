class ExtraTimePowerUp(Target):
   # آیتم زمان اضافی.
   # با شلیک موفق، زمان بازیکن افزایش پیدا می‌کند.

    def __init__(self, x: int, y: int, image=None, seconds_amount: float = 10):
        super().__init__(x, y, image)
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
