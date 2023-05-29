from pygame import sprite
from pygame.image import load
from pygame import transform
from pygame import Rect
from random import randint
from pygame import font
from pygame import draw
from pygame import Surface

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


class Car(sprite.Sprite):
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
        self.diagonalMoving = False

    def img_change(self, img, spriteW, spriteH):
        self.image = transform.scale(load(img), (spriteW, spriteH))
        self.rect = self.image.get_rect()
        self.rect.center = self.center
        self.img = img

    def diagonal_move_check(self):
        self.diagonalMoving = False
        if self.hspeed != 0 and self.vspeed != 0:
            self.diagonalMoving = True

    def keys(self):
        curhspeed = self.hspeed
        curvspeed = self.vspeed
        if self.hspeed <0:
            h = -1
        else:
            h = 1
        if self.vspeed <0:
            v = -1
        else:
            v = 1
        if self.diagonalMoving:
            vector = (((v*self.vspeed)**2 + (h*self.hspeed)**2)**0.5)
            print(vector)
            if vector >= self.speedL:
                curhspeed = h*(round((self.speedL**2 - v*self.vspeed**2)**0.5))
                curvspeed = v*(round((self.speedL**2 - h*self.hspeed**2)**0.5))
        self.rect.y += curvspeed
        self.rect.x += curhspeed
        self.center = self.rect.center
        self.display_speed = int(round((curhspeed**2 + curvspeed**2)**0.5, 1)*10)

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
        self.ableToCollide = True

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
        self.ableToCollide = False
        
class Speedometer(sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = transform.scale(load('sprites/speedometer/speedometer0.png'), (width, height))
        self.width = width
        self.height = height
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, target):
        if target.display_speed < 10:
            spd = 0
        elif 20 > target.display_speed >= 10:
            spd = 10
        elif 30 > target.display_speed >= 20:
            spd = 20
        elif 40 >target.display_speed >= 30:
            spd = 30
        elif 50 >target.display_speed >= 40:
            spd = 40
        elif 60 >target.display_speed >= 50:
            spd = 50
        elif 70 >target.display_speed >= 60:
            spd = 60
        elif 80 >target.display_speed >= 70:
            spd = 70
        elif 90 >target.display_speed >= 80:
            spd = 80
        elif 100 > target.display_speed >= 90:
            spd = 90
        elif 110 > target.display_speed >= 100:
            spd = 100
        elif 120 >target.display_speed >= 110:
            spd = 110
        elif 130 > target.display_speed >= 120:
            spd = 120
        elif target.display_speed >= 130:
            spd = 130
        self.image = transform.scale(load('sprites/speedometer/speedometer' + str(spd) + '.png'), (self.width, self.height))
        
class Button(sprite.Sprite):
    def __init__(self, x, y, width, height, img):
        super().__init__()
        self.img = img
        self.image = transform.scale(load(img), (width, height))
        self.rect = Rect(x, y, width, height)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    
    def fl(self, fill_surface):
        fill_surface.blit(self.image, (self.x, self.y))

    
    def collidepoint(self, x, y):
        return self.rect.collidepoint(x,y)


class ButLabel():
    def __init__(self, x, y, width, height):
        self.rect = Rect(x, y, width, height)
        self.rect.x = x
        self.rect.y = y
    def set_text(self, text, fsize, text_color = (250, 250, 250)):
        self.text = text
        self.image = font.SysFont('Arial Black', fsize).render(text, True, text_color)

    def draw(self, shift_x, shift_y, fill_surface):
        fill_surface.blit(self.image, (self.rect.x + shift_x, self.rect.y + shift_y))


class Checkpoint(sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = Surface((0,0))
        self.rect = Rect(x, y, width, height)
        self.activate = False


class Camera(sprite.Sprite):
    def __init__(self, camera_func, width, height):
        super().__init__()
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return (target.rect.move(self.state.topleft))

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)