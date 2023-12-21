import pygame

class Score:

    def __init__(self):
        self.score = 0
        self.font = pygame.font.SysFont("Arial", 24)
    
    def update_score(self):
        self.score += 1
        print(self.score)

    def show_score(self):
        return self.font.render(f"Score: {self.score}", True, (255,0,0))