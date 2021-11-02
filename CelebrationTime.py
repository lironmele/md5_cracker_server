import pygame
import random
import threading
import time
from pygame import mixer

def get_rand_colour():
    colour_r = random.randint(0,255)
    colour_g = random.randint(0,255)
    colour_b = random.randint(0,255)
    return (colour_r,colour_g,colour_b)

def celebrate():
    threading.Thread(target=hooray).start()

def hooray():
    screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    pygame.display.set_caption("Rainbow!")
    clock = pygame.time.Clock()

    done = False
    counter = 0
    colour = get_rand_colour()
    start = time.time()
    
    # playsound
    mixer.init()
    mixer.music.load('sound.wav')
    mixer.music.play()


    while time.time() - start < 5:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        counter += 1
        if counter > 3:
            colour = get_rand_colour()
            counter = 0

        screen.fill(colour)
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

def main():
    celebrate()

if __name__ == '__main__':
    main()
    input()
