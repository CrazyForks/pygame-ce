#!/usr/bin/env python
"""pygame.examples.chimp

This simple example is used for the line-by-line tutorial
that comes with pygame. It is based on a 'popular' web banner.
Note there are comments here, but for the full explanation,
follow along in the tutorial.
"""

# Import Modules
import os

import pygame

if not pygame.font:
    print("Warning, fonts disabled")
if not pygame.mixer:
    print("Warning, sound disabled")

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, "data")


# functions to create our resources
def load_image(name, colorkey=None, scale=1):
    fullname = os.path.join(data_dir, name)
    image = pygame.image.load(fullname)
    image = image.convert()

    image = pygame.transform.scale_by(image, scale)

    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pygame.RLEACCEL)
    return image, image.get_rect()


def load_sound(name):
    class NoneSound:
        def play(self):
            pass

    if not pygame.mixer.get_init():
        return NoneSound()

    fullname = os.path.join(data_dir, name)
    sound = pygame.mixer.Sound(fullname)

    return sound


# classes for our game objects
class Fist(pygame.sprite.Sprite):
    """moves a clenched fist on the screen, following the mouse"""

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image, self.rect = load_image("fist.webp", -1)
        self.fist_offset = (-235, -80)
        self.punching = False

    def update(self):
        """move the fist based on the mouse position"""
        pos = pygame.mouse.get_pos()
        self.rect.topleft = pos
        self.rect.move_ip(self.fist_offset)
        if self.punching:
            self.rect.move_ip(15, 25)

    def punch(self, target):
        """returns true if the fist collides with the target"""
        if not self.punching:
            self.punching = True
            hitbox = self.rect.inflate(-5, -5)
            return hitbox.colliderect(target.rect)

    def unpunch(self):
        """called to pull the fist back"""
        self.punching = False


class Chimp(pygame.sprite.Sprite):
    """moves a monkey critter across the screen. it can spin the
    monkey when it is punched."""

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image, self.rect = load_image("chimp.webp", -1, 4)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = 10, 90
        self.move = 18
        self.dizzy = False

    def update(self):
        """walk or spin, depending on the monkeys state"""
        if self.dizzy:
            self._spin()
        else:
            self._walk()

    def _walk(self):
        """move the monkey across the screen, and turn at the ends"""
        newpos = self.rect.move((self.move, 0))
        if not self.area.contains(newpos):
            if self.rect.left < self.area.left or self.rect.right > self.area.right:
                self.move = -self.move
                newpos = self.rect.move((self.move, 0))
                self.image = pygame.transform.flip(self.image, True, False)
        self.rect = newpos

    def _spin(self):
        """spin the monkey image"""
        center = self.rect.center
        self.dizzy = self.dizzy + 12
        if self.dizzy >= 360:
            self.dizzy = False
            self.image = self.original
        else:
            rotate = pygame.transform.rotate
            self.image = rotate(self.original, self.dizzy)
        self.rect = self.image.get_rect(center=center)

    def punched(self):
        """this will cause the monkey to start spinning"""
        if not self.dizzy:
            self.dizzy = True
            self.original = self.image


def main():
    """this function is called when the program starts.
    it initializes everything it needs, then runs in
    a loop until the function returns."""
    # Initialize Everything
    pygame.init()
    screen = pygame.display.set_mode((1280, 480), pygame.SCALED)
    pygame.display.set_caption("Monkey Fever")
    pygame.mouse.set_visible(False)

    # Create The Background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((170, 238, 187))

    # Put Text On The Background, Centered
    font = pygame.Font(None, 64)
    text = font.render("Pummel The Chimp, And Win $$$", True, (10, 10, 10))
    textpos = text.get_rect(centerx=background.get_width() / 2, y=10)
    background.blit(text, textpos)

    # Display The Background
    screen.blit(background, (0, 0))
    pygame.display.flip()

    # Prepare Game Objects
    whiff_sound = load_sound("whiff.wav")
    punch_sound = load_sound("punch.wav")
    chimp = Chimp()
    fist = Fist()
    all_sprites = pygame.sprite.Group(chimp, fist)
    clock = pygame.Clock()

    # Main Loop
    going = True
    while going:
        clock.tick(60)

        # Handle Input Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                going = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                going = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if fist.punch(chimp):
                    punch_sound.play()  # punch
                    chimp.punched()
                else:
                    whiff_sound.play()  # miss
            elif event.type == pygame.MOUSEBUTTONUP:
                fist.unpunch()

        all_sprites.update()

        # Draw Everything
        screen.blit(background, (0, 0))
        all_sprites.draw(screen)
        pygame.display.flip()

    pygame.quit()


# Game Over


# this calls the 'main' function when this script is executed
if __name__ == "__main__":
    main()
