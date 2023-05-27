from pygame import sprite
from pygame.image import load
from pygame import transform
from pygame import Rect
from random import randint
class Block(sprite.Sprite):
    def __init__(self, img, x, y, width, height):
        super().__init__()
        self.image = transform.scale(load(img), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.ableToCollide = True

    def break_col(self):
        randbr = randint(1,4)
        self.ableToCollide = False
        self.image = transform.scale(load('sprites/box_broked' + str(randbr) + '.png'), (40, 40))


class GameSprite(sprite.Sprite):
    def __init__(self, pl_image, x1, y1, speedL, spriteW, spriteH):
        super().__init__()
        self.image = transform.scale(load(pl_image), (spriteW, spriteH))
        self.rect = self.image.get_rect()
        self.rect.x = x1
        self.rect.y = y1
        self.hspeed = 0
        self.vspeed = 0
        self.speedL = speedL
        self.center = self.rect.center
        self.img = pl_image
        self.onTouch = False
        self.display_speed = 0
        self.inMove = False

    def reset(self):
        win.blit(self.image, (self.rect.x, self.rect.y))

    def img_change(self, img, spriteW, spriteH):
        self.image = transform.scale(load(img), (spriteW, spriteH))
        self.rect = self.image.get_rect()
        self.rect.center = self.center
        self.img = img
    '''def rot_center(self, angle):
        self.image = transform.rotate(self.image, angle)
        self.rect = self.image.get_rect(center = self.rect.center)
        #self.rect.center = self.center
        #return rot_image,rot_rect'''

    def keys(self):
        self.rect.y += self.vspeed
        self.rect.x += self.hspeed
        self.center = self.rect.center
        self.display_speed = int(round((self.hspeed**2 + self.vspeed**2)**0.5, 1)*10)

    def changespeed(self, xal, yal):
        if xal > 0:
            if self.hspeed < self.speedL:
                self.hspeed += 1
        if xal < 0:
            if self.hspeed > -self.speedL:
                self.hspeed -= 1
        if yal > 0:
            if self.vspeed < self.speedL:
                self.vspeed += 1
        if yal < 0:
            if self.vspeed > -self.speedL:
                self.vspeed -= 1
        if xal == 0:
            if self.hspeed < 0:
                self.hspeed += 1
            if self.hspeed > 0:
                self.hspeed -= 1
        if yal == 0:
            if self.vspeed < 0:
                self.vspeed += 1
            if self.vspeed > 0:
                self.vspeed -= 1

    def wall_collide(self, wall):
        self.vspeed = 0
        self.hspeed = 0
        self.onTouch = True

class PhysicsProp(sprite.Sprite):
    def __init__(self, img, x, y, width, height):
        super().__init__()
        self.image = transform.scale(load(img), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.hspeed = 0
        self.vspeed = 0
        self.inMove = False
        self.onTouch = False

    def update(self):
        if self.inMove:
            self.rect.x += self.hspeed
            self.rect.y += self.vspeed
        if self.hspeed == self.vspeed == 0:
            self.inMove = False

    def change_speed_momental(self, new_hspeed, new_vspeed):
        if not self.onTouch:
            self.vspeed = new_vspeed
            self.hspeed = new_hspeed
            self.inMove = True
            self.rect.x += self.hspeed
            self.rect.y += self.vspeed

    def change_speed(self):
        if self.inMove:
            if self.vspeed > 0:
                self.vspeed -= 1
            if self.vspeed < 0:
                self.vspeed += 1
            if self.hspeed > 0:
                self.hspeed -=1
            if self.hspeed < 0:
                self.hspeed +=1

    def wall_collide(self, wall):
        self.vspeed = 0
        self.hspeed = 0
        self.onTouch = True

class Camera:
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return (target.rect.move(self.state.topleft))

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)