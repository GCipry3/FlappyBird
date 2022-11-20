import random

import pygame
import sys

import pygame.time

(WIDTH, HEIGHT) = (500, 750)
pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
ASSETS = "assets/"

clock = pygame.time.Clock()

SCORE_FONT = pygame.font.SysFont("comicsans", 80)
END_FONT = pygame.font.SysFont("comicsans", 60)


class Bird:
    def __init__(self):
        self.img = pygame.image.load(ASSETS + "bird.png")
        self.x = 25
        self.y = HEIGHT // 2
        self.cnt = 0
        self.vel = 0

    def move(self):
        self.cnt += 1

        dy = (3 / 2) * (self.cnt ** 2) + self.vel * self.cnt

        if dy >= 16:
            dy = 16  # to stop the downward acceleration after it reaches 16

        if dy < 0:
            dy -= 2  # to jump higher

        self.y += dy

    def jump(self):
        self.vel = -10
        self.cnt = 0

    def draw(self):
        window.blit(self.img, (self.x, self.y))

    def get_mask(self):
        return pygame.mask.from_surface(self.img)


class Pipe:
    def __init__(self, x):
        self.img = pygame.image.load(ASSETS + "tube.png")
        self.img = pygame.transform.scale(self.img, (100, 600))
        self.x = x
        self.vel = 5

        self.BOTTOM_PIPE = self.img
        self.TOP_PIPE = pygame.transform.flip(self.img, flip_x=False, flip_y=True)

        gap = 200

        self.height = random.randrange(50, 350)
        self.top_y = self.height - self.TOP_PIPE.get_height()
        self.bottom_y = self.height + gap

        self.passed_flag = False

    def move(self):
        self.x -= self.vel

    def draw(self):
        window.blit(self.BOTTOM_PIPE, (self.x, self.bottom_y))
        window.blit(self.TOP_PIPE, (self.x, self.top_y))

    def get_top_mask(self):
        return pygame.mask.from_surface(self.TOP_PIPE)

    def get_bottom_mask(self):
        return pygame.mask.from_surface(self.BOTTOM_PIPE)

    def get_top_offset(self, bird_x, bird_y):
        return self.x - bird_x, self.top_y - bird_y

    def get_bottom_offset(self, bird_x, bird_y):
        return self.x - bird_x, self.bottom_y - bird_y


class FlappyBirdGame:
    def __init__(self):
        self.bird = Bird()
        self.bg_img = pygame.image.load(ASSETS + "background.jpeg")
        self.keyboard_timer = 0
        self.pipes = [Pipe(WIDTH)]
        self.removed_pipes = []

    def draw(self):
        window.blit(self.bg_img, (0, 0))
        self.bird.draw()
        for pipe in self.pipes:
            pipe.draw()

    def move(self):
        self.bird.move()
        for pipe in self.pipes:
            pipe.move()

    def lose_check(self):
        if self.bird.y >= HEIGHT - 50 or self.bird.y <= 0:
            return True

        for pipe in self.pipes:
            if self.bird.get_mask().overlap(pipe.get_top_mask(), pipe.get_top_offset(self.bird.x, self.bird.y)):
                return True
            if self.bird.get_mask().overlap(pipe.get_bottom_mask(), pipe.get_bottom_offset(self.bird.x, self.bird.y)):
                return True

        return False

    def start_screen(self):
        start_game = False

        start_text = END_FONT.render("Press space to start", True, (255, 255, 255))
        while not start_game:
            for i in pygame.event.get():
                if i.type == pygame.QUIT:
                    sys.exit()
                if i.type == pygame.KEYDOWN:
                    if i.key == pygame.K_SPACE:
                        start_game = not start_game

            window.blit(self.bg_img, (0, 0))

            window.blit(start_text, ((WIDTH - start_text.get_width()) / 2, 300))

            pygame.display.flip()

    def play(self):
        self.start_screen()

        playing = True
        while playing:
            pygame.time.delay(30)
            clock.tick(60)
            for i in pygame.event.get():
                if i.type == pygame.QUIT:
                    sys.exit()
                if i.type == pygame.KEYDOWN:
                    if i.key == pygame.K_SPACE:
                        self.bird.jump()

            self.move()
            self.draw()

            add_pipe = False
            removed_pipe = None
            for pipe in self.pipes:
                if not pipe.passed_flag and self.bird.x > pipe.x + pipe.img.get_width() + 25:
                    pipe.passed_flag = True
                    removed_pipe = pipe
                    add_pipe = True

            if removed_pipe is not None:
                self.pipes.remove(removed_pipe)
                self.removed_pipes.append(removed_pipe)

            if add_pipe:
                self.pipes.append(Pipe(WIDTH))

            playing = not self.lose_check()

            pygame.display.flip()

        self.endgame()

    def endgame(self):
        restart_game = False

        restart_text = END_FONT.render("Press space to restart", True, (255, 0, 255))
        score = SCORE_FONT.render("Your score is {}".format(len(self.removed_pipes)), True, (255, 255, 255))
        while not restart_game:
            for i in pygame.event.get():
                if i.type == pygame.QUIT:
                    sys.exit()
                if i.type == pygame.KEYDOWN:
                    if i.key == pygame.K_SPACE:
                        restart_game = True

            window.blit(self.bg_img, (0, 0))

            window.blit(score, ((WIDTH - score.get_width()) / 2, 300))
            window.blit(restart_text, ((WIDTH - restart_text.get_width()) / 2, 500))

            pygame.display.flip()


def main():
    while True:
        game = FlappyBirdGame()
        game.play()


if __name__ == '__main__':
    main()
