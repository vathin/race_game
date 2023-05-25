from pygame import *

SIZE = (640, 480)
win = display.set_mode(SIZE)
display.set_caption('racetest1')
clock = time.Clock()
background = Surface(SIZE)
background.fill((100, 250, 100))
spd = 1
xal = 0
yal = 0


class GameSprite(sprite.Sprite):
    def __init__(self, pl_image, x1, y1, speedL, spriteW, spriteH):
        super().__init__()
        self.image = transform.scale(image.load(pl_image), (spriteW, spriteH))

        self.rect = self.image.get_rect()
        self.rect.x = x1
        self.rect.y = y1
        self.InMove = False
        self.hspeed = 0
        self.vspeed = 0
        self.speedL = speedL

    def reset(self):
        win.blit(self.image, (self.rect.x, self.rect.y))

    def img_change(self, img, spriteW, spriteH):
        self.image = transform.scale(image.load(img), (spriteW, spriteH))

    def keys(self):
        self.rect.y += self.vspeed
        self.rect.x += self.hspeed

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

    def wall_collide(self):
        self.hspeed = self.hspeed // 2
        self.hspeed = -self.hspeed
        self.rect.x += self.hspeed
        self.vspeed = self.vspeed // 2
        self.vspeed = -self.vspeed
        self.rect.y += self.vspeed


class Block(sprite.Sprite):
    def __init__(self, img, width, height, x, y):
        super().__init__()
        self.image = transform.scale(image.load(img), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Camera:
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return (target.rect.move(self.state.topleft))

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


def camera_func(camera, target_rect):
    l = -target_rect.x + SIZE[0] / 2
    t = -target_rect.y + SIZE[1] / 2

    w = camera.width
    h = camera.height
    l = min(0, l)
    l = max(-(camera.width - SIZE[0]), l)
    t = max(-(camera.height - SIZE[1]), t)
    t = min(0, t)

    return Rect(l, t, w, h)


car1 = GameSprite('up.png', 50, 50, 5, 26, 35)

level = ['-----------------------------------------',
         '-     -                       ------ ----',
         '-     -                       ------ ----',
         '-     -                               ---',
         '-     -               -                 -',
         '-     -                                 -',
         '-     -                                 -',
         '-     -                                 -',
         '-     -                                 -',
         '-     -                                 -',
         '-     -                                 -',
         '-     -                                 -',
         '-     -                                 -',
         '-     -                       -         -',
         '-     -                       -         -',
         '-     -                       -         -',
         '-      -                     -          -',
         '-      -                     -          -',
         '-       -                   -           -',
         '-        --               --            -',
         '-          ---------------              -',
         '-                                       -',
         '-                                       -',
         '-                                       -',
         '-----------------------------------------']

total_level_width = len(level[0]) * 40
total_level_height = len(level) * 40
camera = Camera(camera_func, total_level_width, total_level_height)

blocksgr = sprite.Group()


def make_level(level):
    x = 0
    y = 0
    for row in level:
        for col in row:
            if col == '-':
                new_block = Block('block.png', 40, 40, x, y)
                blocksgr.add(new_block)
            x += 40
        y += 40
        x = 0


make_level(level)

tk = 0
game = True
while game:
    win.blit(background, (0, 0))

    #blocksgr.draw(win)
    #car1.reset()

    for sprite in blocksgr:
        win.blit(sprite.image, camera.apply(sprite))
    win.blit(car1.image, camera.apply(car1))
    for e in event.get():
        if e.type == QUIT:
            game = False
    tk += 1
    kpr = key.get_pressed()
    if kpr[K_UP]:
        yal = -1
        car1.img_change('up.png', 26, 35)
    if kpr[K_DOWN]:
        yal = 1
        car1.img_change('down.png', 26, 35)
    if kpr[K_LEFT]:
        xal = -1
        car1.img_change('left.png', 35, 26)
    if kpr[K_RIGHT]:
        xal = 1
        car1.img_change('right.png', 35, 26)
    if tk == 5:
        car1.changespeed(xal, yal)
        tk = 0
    camera.update(car1)
    #if sprite.spritecollide(car1, blocksgr):
    #    car1.wall_collide()


    car1.keys()
    xal = 0
    yal = 0



    clock.tick(60)
    display.update()