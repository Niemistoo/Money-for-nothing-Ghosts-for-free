import pygame
import math

class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game

        self.image = pygame.image.load("player.png")
        self.image_width = self.image.get_width()
        self.image_height = self.image.get_height()
        self.x_position = game.WIDTH // 2
        self.y_position = game.HEIGHT - self.image_height
        self.rect = pygame.Rect(self.x_position +25, self.y_position +6, 15, 58)

        self.direction = pygame.math.Vector2(0,0)
        self.step = False

        self.speed = 5
        self.gravity = 1
        self.jump_speed = -15

        self.on_platform = True

        self.health = 3
    
    def update(self):
        self.get_input()
        self.move()
    
    def get_rect(self):
        return pygame.Rect(self.x_position +25, self.y_position +6, 15, 58) # Rect with fixed hitbox
    
    def move(self):
        if self.direction.x < 0:
            self.x_position -= self.speed

        if self.direction.x > 0:
            self.x_position += self.speed
        
        if self.x_position + self.image_width < 0:      # If player crosses window border, append from other side
            self.x_position = self.game.WIDTH

        if self.x_position > self.game.WIDTH:
            self.x_position = -self.image_width
        

    def apply_gravity(self):
        if self.direction.y < 20:
            self.direction.y += self.gravity
        self.y_position += self.direction.y

    def jump(self): 
        self.direction.y = self.jump_speed
    
    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.direction.x = -1
        elif keys[pygame.K_RIGHT]:
            self.direction.x = 1
        else:
            self.direction.x = 0

        if keys[pygame.K_UP]:
            if self.on_platform == True:
                self.jump()
                self.on_platform = False

    def draw(self):
        if self.direction.x < 0:
            if self.step == False:
                self.image = pygame.image.load("player_L.png")
                self.step = True
            elif self.step == True:
                self.image = pygame.image.load("player_LS.png")
                self.step = False

        if self.direction.x > 0:
            self.image = pygame.transform.flip(self.image, True, False)
            if self.step == False:
                self.image = pygame.image.load("player_L.png")
                self.image = pygame.transform.flip(self.image, True, False)
                self.step = True
            elif self.step == True:
                self.image = pygame.image.load("player_LS.png")
                self.image = pygame.transform.flip(self.image, True, False)
                self.step = False

        if self.direction.x == 0:    # Draw player standing image
            self.image = pygame.image.load("player.png")
        
        
        self.game.WIN.blit(self.image, (self.x_position, self.y_position))

    def get_player_health(self):
        return self.health
    
class Ghost(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, direction):
        super().__init__()
        self.image = pygame.image.load("hirvio.png")
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = speed
        self.angle = math.atan2(direction.y - self.rect.centery, direction.x - self.rect.centerx) # player position angle when ghost added

    def update(self):
        self.rect.x += self.speed * math.cos(self.angle)
        self.rect.y += self.speed * math.sin(self.angle)
        self.check_ghost_position()


    def check_ghost_position(self):
        if self.rect.right < 0 or self.rect.left > 800 or self.rect.bottom < 0 or self.rect.top > 600:
            self.kill()

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("kolikko.png")
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x, y)

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((0, 0, 0))  # platform color
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

class Map:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.platforms = []

    def add_platform(self, x, y, width, height):
        platform = Platform(x, y, width, height)
        self.platforms.append(platform)

    def draw(self, screen):
        for platform in self.platforms:
            screen.blit(platform.image, platform.rect)

class HUD:
    def __init__(self, WIN, player):
        self.WIN = WIN
        self.player = player

    def update(self):
        pass

    def draw(self):
        self.draw_player_health()

    def draw_player_health(self):
        player_health = self.player.get_player_health()
        if player_health == 3:
            pygame.draw.circle(self.WIN, "green", (30, 30), 10)
            pygame.draw.circle(self.WIN, "green", (60, 30), 10)
            pygame.draw.circle(self.WIN, "green", (90, 30), 10)
        elif player_health == 2:
            pygame.draw.circle(self.WIN, "green", (30, 30), 10)
            pygame.draw.circle(self.WIN, "green", (60, 30), 10)
            pygame.draw.circle(self.WIN, "red", (90, 30), 10)
        elif player_health == 1:
            pygame.draw.circle(self.WIN, "green", (30, 30), 10)
            pygame.draw.circle(self.WIN, "red", (60, 30), 10)
            pygame.draw.circle(self.WIN, "red", (90, 30), 10)
