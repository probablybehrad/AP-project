import sqlite3
import pygame
import sys


def init_db():
    conn = sqlite3.connect('leaderboard.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scores (id INTEGER PRIMARY KEY AUTOINCREMENT, player_name TEXT, score INTEGER
        )
    ''')
    conn.commit()
    conn.close()


def save_score(name, score):
    conn = sqlite3.connect('leaderboard.db')
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO leaderboard (player_name, score) VALUES (?, ?)', (name, score))
    conn.commit()
    conn.close()


def get_top_scores(limit=5):
    conn = sqlite3.connect('leaderboard.db')
    cursor = conn.cursor()
    cursor.execute(
        'SELECT player_name, score FROM leaderboard ORDER BY score DESC LIMIT ?', (limit,))
    results = cursor.fetchall()
    conn.close()
    return results


def show_leaderboard(screen):
    try:
        font = pygame.font.Font(r' ', 20)  # میتونیم فونت رو تغییر بدیم
        title_font = pygame.font.Font(r' ', 30)
    except:
        font = pygame.font.Font(None, 20)
        title_font = pygame.font.Font(None, 30)

    try:
        bg = pygame.image.load(' ')  # عکس رو قرارمیدیم
        bg = pygame.transform.scale(
            bg, (screen.get_width(), screen.get_height()))
    except:
        bg = None

    scores = get_top_scores(5)

    running = True
    while running:
        # Draw background
        if bg:
            screen.blit(bg, (0, 0))
        else:
            screen.fill((50, 50, 70))  # این مقدار ها میتونن تغییر کنن

        # بخش دوم و سوم میتونن تغییر کنن
        title = title_font.render("Leaderboard", True, (128, 0, 128))
        # میتونه عوض بشه(موقعیت قرارگیری متن)
        screen.blit(title, (screen.get_width()//2 - title.get_width()//2, 50))

        # Draw scores
        y = 150  # موقعیت عمودی(قابل تغییر)
        for i, (name, score) in enumerate(scores, 1):
            color = (255, 215, 0) if i == 1 else (192, 192, 192) if i == 2 else (
                205, 127, 50) if i == 3 else (255, 255, 255)
            # رنگ هارو میتونیم عوض کنیم
            text = font.render(f"{i}. {name}: {score}", True, color)
            screen.blit(text, (screen.get_width()//2 -
                        text.get_width()//2, y))  # قابل تغییر
            y += 60

        # Instruction
        inst = font.render("Press B to go back", True,
                           (255, 0, 0))  # قابل تغییر
        screen.blit(inst, (screen.get_width()//2 - inst.get_width() //
                    2, screen.get_height() - 50))  # قابل تغییر

        pygame.display.update()

        # کد خارج شدن از برنامه
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_b:
                running = False


init_db()
