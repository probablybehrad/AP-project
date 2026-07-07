import math


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





#کم کردن زمان بازیکن در هر فریم

def tick_time(self, dt):
    self._time_left = max(0, self._time_left - dt)

    