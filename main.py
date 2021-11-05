import pygame
from sys import exit

pygame.init()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("pong graphics/Pong player.png").convert_alpha()
        self.rect = self.image.get_rect(center=(950, 300))

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_s] or keys[pygame.K_DOWN] and self.rect.bottom <= 600:
            self.rect.top += 5
        if keys[pygame.K_w] or keys[pygame.K_UP] and self.rect.top >= 0:
            self.rect.bottom -= 5

    def update(self):
        self.input()


class CPU(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("pong graphics/Pong player.png").convert_alpha()
        self.rect = self.image.get_rect(center=(50, 300))

    def ai(self):
        if ball.sprite.rect.y < self.rect.y:
            self.rect.y -= 2
        if ball.sprite.rect.y > self.rect.y and self.rect.bottom <= 600:
            self.rect.y += 3

    def update(self):
        self.ai()


class Ball(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("pong graphics/Pong ball.png").convert_alpha()
        self.rect = self.image.get_rect(center=(500, 300))

        self.movement_speed_x = 2
        self.movement_speed_y = 1
        self.go_down = True
        self.go_right = True

    player_score = 0
    cpu_score = 0

    def collision(self):
        if pygame.sprite.spritecollide(self, player_1, False):
            self.go_right = False
            self.movement_speed_x = 4
            self.movement_speed_y = self.movement_speed_y + 0.25

        if pygame.sprite.spritecollide(self, cpu, False):
            self.go_right = True
            self.movement_speed_x = 4
            self.movement_speed_y = self.movement_speed_y + 0.25

    def reset(self):
        self.rect.x = 500
        self.movement_speed_x = 2
        self.movement_speed_y = 1

    def movement(self):

        if self.go_right:
            self.rect.x += self.movement_speed_x

        if not self.go_right:
            self.rect.x -= self.movement_speed_x

        if self.rect.x >= 1000:
            self.reset()
            Ball.cpu_score += 1

        if self.rect.x <= 0:
            self.reset()
            Ball.player_score += 1

        if self.go_down:
            self.rect.y += self.movement_speed_y
            if self.rect.bottom >= 600:
                self.go_down = False

        if not self.go_down:
            self.rect.y -= self.movement_speed_y
            if self.rect.top <= 0:
                self.go_down = True

    def update(self):
        self.collision()
        self.movement()


pygame.display.set_caption("Pong")
screen = pygame.display.set_mode((1000, 600))

player_1 = pygame.sprite.GroupSingle()
player_1.add(Player())

ball = pygame.sprite.GroupSingle()
ball.add(Ball())

cpu = pygame.sprite.GroupSingle()
cpu.add(CPU())

font = pygame.font.Font(None, 70)

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    screen.fill("Black")
    pygame.draw.line(screen, "White", (500, 0), (500, 600))

    player_1.draw(screen)
    player_1.update()

    ball.draw(screen)
    ball.update()

    cpu.draw(screen)
    cpu.update()

    player_score_surface = font.render(str(Ball.player_score), False, "White")
    screen.blit(player_score_surface, (525, 50))

    cpu_score_surface = font.render(str(Ball.cpu_score), False, "White")
    screen.blit(cpu_score_surface, (450, 50))

    pygame.display.update()
    clock.tick(60)
