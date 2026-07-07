class ExtraAmmoPowerUp(Target):
    # آیتم خشاب اضافی.
    # با شلیک موفق، تعدادی تیر به بازیکن اضافه می‌شود.

    def __init__(self, x: int, y: int, image=None, bullets_amount: int = 5):
        super().__init__(x, y, image)
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
