import pygame
import sys
from constants import *
from logger import log_state
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from logger import log_event
from shot import Shot


pygame.font.init()
font = pygame.font.Font(None, 36)


def draw_score(screen, score, high_score):
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    high_score_text = font.render(f"High Score: {high_score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    screen.blit(high_score_text, (10, 50))

def get_asteroid_points(radius):
    # adjust these thresholds to match your actual radii
    if radius > ASTEROID_MIN_RADIUS * 2:
        return 20      # large
    elif radius > ASTEROID_MIN_RADIUS:
        return 50      # medium
    else:
        return 100     # small
    
def show_game_over(screen, final_score, high_score):
    screen.fill((0, 0, 0))  # Black background
    
    # Create the text
    game_over_font = pygame.font.Font(None, 74)
    score_font = pygame.font.Font(None, 48)
    
    game_over_text = game_over_font.render("GAME OVER", True, (255, 0, 0))  # Red text
    final_score_text = score_font.render(f"Final Score: {final_score}", True, (255, 255, 255))
    high_score_text = score_font.render(f"High Score: {high_score}", True, (255, 255, 255))
    
    # Center the text on screen
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 200))
    screen.blit(final_score_text, (SCREEN_WIDTH // 2 - final_score_text.get_width() // 2, 300))
    screen.blit(high_score_text, (SCREEN_WIDTH // 2 - high_score_text.get_width() // 2, 360))
    
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
            if event.type == pygame.KEYDOWN:
                waiting = False
    
def load_high_score():
    try:
        with open("highscore.txt", "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return 0  # If file doesn't exist, high score is 0
    except ValueError:
        return 0  # If file is corrupted, reset to 0

def save_high_score(score):
    with open("highscore.txt", "w") as file:
        file.write(str(score))

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    print("Starting Asteroids with pygame version:", pygame.version.ver)
    print("Screen width:", SCREEN_WIDTH)
    print("Screen height:", SCREEN_HEIGHT)
    clock = pygame.time.Clock()
    dt = 0
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    Player.containers = (updatable, drawable)
    Asteroid.containers = (updatable, drawable, asteroids)
    AsteroidField.containers = (updatable)
    Shot.containers = (updatable, drawable, shots)
    new_field = AsteroidField()
    player_one = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    score = 0
    high_score = load_high_score()
    

    while True: 
        dt = clock.tick(60) /  1000
        for event in pygame.event.get():
    	    if event.type == pygame.QUIT:
                return
        log_state() 
        screen.fill("black")
        updatable.update(dt)  
        
        for thing in asteroids:
            for shot in shots:
                if shot.collides_with(thing):
                    log_event("asteroid_shot")
                    shot.kill()
                    score += get_asteroid_points(thing.radius)
                    thing.split()
                    thing.kill()
        for thing in asteroids:
            if thing.collides_with(player_one):
                log_event("player_hit")
                print("Game over!")     
     
                if score > high_score:
                    high_score = score
                    save_high_score(high_score)
                show_game_over(screen, score, high_score)
                sys.exit()


                    
            
        for object in drawable:
            object.draw(screen)

        draw_score(screen, score, high_score)
        pygame.display.flip()
       

if __name__ == "__main__":
    main() 
