import random

import pygame
import sys

import pygame.time

(WIDTH, HEIGHT) = (500, 750)
pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
ASSETS = "assets/"

clock = pygame.time.Clock()


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
        self.pipes = [Pipe(400)]

    def draw(self):
        window.blit(self.bg_img, (0, 0))
        self.bird.draw()
        for pipe in self.pipes:
            pipe.draw()

    def play(self):
        playing = True
        while playing:
            pygame.time.delay(30)
            clock.tick(60)
            for i in pygame.event.get():
                if i.type == pygame.QUIT:
                    playing = False
                if i.type == pygame.KEYDOWN:
                    if i.key == pygame.K_SPACE:
                        self.bird.jump()

            self.bird.move()
            for pipe in self.pipes:
                pipe.move()
            self.draw()
            pygame.display.flip()

        pygame.quit()


def main():
    game = FlappyBirdGame()
    game.play()


if __name__ == '__main__':
    main()
