import math
import random
import time
import pygame
pygame.init()

WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AIM Trainer")

TARGET_INCREMENT = 400
TARGET_EVENT = pygame.USEREVENT
TARGET_PADDING = 30

BG_COLOR = (0, 25, 40)
LIVES = 5
TOP_BAR_HEIGHT = 40

LABEL_FONT = pygame.font.SysFont("comicsans", 20)

def choose_difficulty():
    print("Choose difficulty: (1) Easy  (2) Medium  (3) Hard")
    choice = input("Enter 1, 2, or 3: ").strip()
    if choice == "1":
        return 1.5 
    elif choice == "3":
        return 0.7  
    else:
        return 1.0  

class Target:
    MAX_SIZE = 30
    GROWTH_RATE = 0.5
    COLOR = (255, 0, 0)
    SECOND_COLOR = (255, 255, 255)

    def __init__(self, x, y, scale=1.0):
        self.x = x
        self.y = y
        self.size = 0
        self.grow = True
        self.scale = scale

    def update(self):
        if self.size + self.GROWTH_RATE > self.MAX_SIZE:
            self.grow = False
        if self.grow:
            self.size += self.GROWTH_RATE
        else:
            self.size -= self.GROWTH_RATE

    def draw(self, win):
        scaled_size = math.ceil(self.size * self.scale)
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), scaled_size)
        pygame.draw.circle(win, self.SECOND_COLOR, (self.x, self.y), math.ceil(scaled_size * 0.8))
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), math.ceil(scaled_size * 0.6))
        pygame.draw.circle(win, self.SECOND_COLOR, (self.x, self.y), math.ceil(scaled_size * 0.4))

    def collide(self, x, y):
        dist = math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)
        return dist <= self.size * self.scale

def draw(win, targets):
    win.fill(BG_COLOR)
    for target in targets:
        target.draw(win)

def format_time(secs):
    milli = math.floor(int(secs*1000) % 1000 / 100)
    seconds = int(round(secs % 60, 1))
    minutes = int(secs // 60)
    return f"{minutes:02d}:{seconds:02d}.{milli}"

def draw_top_bar(win, elapsed_time, target_pressed, misses):
    pygame.draw.rect(win, "grey", (0, 0, WIDTH, TOP_BAR_HEIGHT))
    time_label = LABEL_FONT.render(f"Time:{format_time(elapsed_time)}", 1, "black")

    speed = round(target_pressed/elapsed_time, 1) if elapsed_time > 0 else 0
    speed_label = LABEL_FONT.render(f"Speed:{speed} t/s", 1, "black")

    hits_label = LABEL_FONT.render(f"Hits:{target_pressed}", 1, "black")
    lives_label = LABEL_FONT.render(f"COUNTDOWN:{LIVES - misses}", 1, "black")

    win.blit(time_label, (5, 5))
    win.blit(speed_label, (150, 5))
    win.blit(hits_label, (300, 5))
    win.blit(lives_label, (500, 5))

def end_screen(win, target_pressed, elapsed_time, clicks):
    win.fill(BG_COLOR)
    time_label = LABEL_FONT.render(f"Time:{format_time(elapsed_time)}", 1, "black")

    speed = round(target_pressed/elapsed_time, 1) if elapsed_time > 0 else 0
    speed_label = LABEL_FONT.render(f"Speed:{speed} t/s", 1, "white")

    hits_label = LABEL_FONT.render(f"Hits:{target_pressed}", 1, "white")

    accuracy = round(target_pressed/clicks * 100, 1) if clicks > 0 else 0
    accuracy_label = LABEL_FONT.render(f"Accuracy:{accuracy}", 1, "white")

    win.blit(time_label, (get_middle(time_label), 100))
    win.blit(speed_label, (get_middle(speed_label), 200))
    win.blit(hits_label, (get_middle(hits_label), 300))
    win.blit(accuracy_label, (get_middle(accuracy_label), 400))

    message_label = LABEL_FONT.render("Press any key to quit. Great job!", 1, "yellow")
    win.blit(message_label, (get_middle(message_label), 500))

    pygame.display.update()

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                quit()

def get_middle(surface):
    return WIDTH/2 - surface.get_width()/2

def main():
    scale = choose_difficulty()
    run = True
    targets = []
    clock = pygame.time.Clock()

    target_pressed = 0
    clicks = 0
    start_time = time.time()
    misses = 0

    pygame.time.set_timer(TARGET_EVENT, TARGET_INCREMENT)

    while run:
        clock.tick(60)
        elapsed_time = time.time() - start_time
        click = False
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == TARGET_EVENT:
                x = random.randint(TARGET_PADDING, WIDTH - TARGET_PADDING)
                y = random.randint(TARGET_PADDING + TOP_BAR_HEIGHT, HEIGHT - TARGET_PADDING)
                target = Target(x, y, scale)  
                targets.append(target)

            if event.type == pygame.MOUSEBUTTONDOWN:
                clicks += 1
                click = True

        for target in targets[:]:
            target.update()
            if target.size <= 0:
                targets.remove(target)
                misses += 1

            if click and target.collide(*mouse_pos):
                targets.remove(target)
                target_pressed += 1

        if misses >= LIVES:
            end_screen(win, target_pressed, elapsed_time, clicks)
            break

        draw(win, targets)
        draw_top_bar(win, elapsed_time, target_pressed, misses)
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
