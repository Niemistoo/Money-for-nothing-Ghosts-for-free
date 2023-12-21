import pygame
import sys
from game_objects import *
from score import *
import random
import time

pygame.display.set_caption("Money for nothing - Ghosts for free")

class Game:
    def __init__(self):
        pygame.init()
        self.WIDTH = 800
        self.HEIGHT = 600
        self.BG_IMAGE = pygame.image.load("level_background.png")
        self.WIN = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.CLOCK = pygame.time.Clock()
        self.FPS = 60
        self.new_game()
        self.hit_timer = time.perf_counter()
        self.game_on = True

    def new_game(self):
        self.player = Player(self)
        self.score = Score()
        self.ghosts = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.HUD = HUD(self.WIN, self.player)

        self.map = Map(self.WIDTH, self.HEIGHT)
        self.map.add_platform(0, self.HEIGHT - 90, 300, 10)
        self.map.add_platform(0, self.HEIGHT - 190, 300, 10)
        self.map.add_platform(0, self.HEIGHT - 290, 300, 10)
        self.map.add_platform(0, self.HEIGHT - 390, 300, 10)
        self.map.add_platform(0, self.HEIGHT - 490, 300, 10)

        self.map.add_platform(500, self.HEIGHT - 90, 300, 10)
        self.map.add_platform(500, self.HEIGHT - 190, 300, 10)
        self.map.add_platform(500, self.HEIGHT - 290, 300, 10)
        self.map.add_platform(500, self.HEIGHT - 390, 300, 10)
        self.map.add_platform(500, self.HEIGHT - 490, 300, 10)

        self.add_coin()

    def update(self):
    
        self.ghosts.update()
        self.player.update()
        self.coins.update()
        self.check_ghost_collision()
        self.check_platform_collision()
        self.check_coin_collision()

    
    def draw(self):
        self.WIN.fill("white")
        self.WIN.blit(self.BG_IMAGE, (0,0))

        self.player.draw()
        self.map.draw(self.WIN)
        self.ghosts.draw(self.WIN)
        self.coins.draw(self.WIN)
        self.HUD.draw()


        pygame.display.flip()
        self.CLOCK.tick(self.FPS)

    def check_event(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def run(self):
        while True:
            if len(self.ghosts) < 1:
                self.add_ghost()
            self.check_event()
            self.update()
            self.draw()

    def add_ghost(self):
        x = self.WIDTH // 2
        y = self.HEIGHT // 2
        speed = random.choice([2, 5])  # Random speed
        ghost = Ghost(x, y, speed, self.player.rect)
        self.ghosts.add(ghost)

    def add_coin(self):
        y_positions = [0, 90, 190, 290, 390, 490]
        x = random.randint(0, 800)
        y = self.HEIGHT - random.choice(y_positions)
        coin = Coin(x, y)
        self.coins.add(coin)

    def check_ghost_collision(self):
        self.player.rect = self.player.get_rect()
        for ghost in self.ghosts:
            if self.player.rect.colliderect(ghost.rect) and time.perf_counter() - self.hit_timer > 3:
                print(time.perf_counter() - self.hit_timer)
                print("osuma")
                self.hit_timer = time.perf_counter()
                self.player.health -= 1
                if self.player.health <= 0:
                    self.game_on = False
                    print("GAME OVER")

    def check_platform_collision(self):

        self.player.apply_gravity()
        self.player.rect = self.player.get_rect()
        
        for platform in self.map.platforms:
            if platform.rect.colliderect(self.player.rect) and self.player.rect.bottom >= platform.rect.top and self.player.direction.y > 0:
                if self.player.direction.y > 0:
                    if self.player.rect.bottom - platform.rect.top - self.player.direction.y  <= 0:
                        self.player.y_position = platform.rect.top - self.player.image_height
                        self.player.direction.y = 0
                        self.player.on_platform = True
                
                else:
                    self.player.on_platform = False
                    
        if self.player.rect.bottom >= self.HEIGHT:
            self.player.y_position = self.HEIGHT - self.player.image_height
            self.player.direction.y = 0
            self.player.on_platform = True

    def check_coin_collision(self):
        for coin in self.coins:
            if coin.rect.colliderect(self.player.rect) and self.game_on:
                coin.kill()
                self.score.update_score()
                self.add_coin()

if __name__ == "__main__":
    game = Game()
    game.run()
