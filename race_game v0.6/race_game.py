from pygame import *
from race_game_classes import *

SIZE = (640, 480)
win = display.set_mode(SIZE)
display.set_caption('race_game')
clock = time.Clock()
background = Surface(SIZE)
background.fill((100, 250, 100))
spd = 1
xal = 0
yal = 0

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


car1 = GameSprite('up.png', 50, 50, 7, 26, 35)

level = ['---------------------------------------------------',
         '-                                                 -',
         '-                                                 -',
         '-                                                 -',
         '-                                                 -',
         '----------------------------------                -',
         '-                                                 -',
         '-                                                 -',
         '-                                                 -',
         '-                                                 -',
         '-                ----------------------------------',
         '-                                                 -',
         '-                                                 -',
         '-                                                 -',
         '-                                                 -',
         '----------------------------------                -',
         '-                                                 -',
         '-                                                 -',
         '-                                                 -',
         '-                                                 -',
         '-                ----------------------------------',
         '-                                                 -',
         '-                                                 -',
         '-                                                 -',
         '-                                                 -',
         '---------------------------------------------------']

total_level_width = len(level[0]) * 40
total_level_height = len(level) * 40
camera = Camera(camera_func, total_level_width, total_level_height)

sprite_group = sprite.Group()
sprite_group.add(car1)
blocks = sprite.Group()

x = 0
y = 0
for row in level:
    for col in row:
        if col == '-':
            block = Block('block.png',x, y, 40, 40 )
            sprite_group.add(block)
            blocks.add(block)
        x += 40
    y += 40
    x = 0

block1 = Block('block.png', 70, 70, 40, 40)
font.init()
font1 = font.SysFont('Arial Black', 70)
speed_display_num = font1.render(str(car1.display_speed), True, (250, 250, 250))
font2 = font.SysFont('Arial Black', 20)
speed_display_lab = font2.render('Скорость:', True, (255, 255, 255))

tk = 0
game = True
while game:
    win.blit(background, (0, 0))
    
    for i in sprite_group:
        win.blit(i.image, camera.apply(i))
    
    #win.blit(car1.image, camera.apply(car1))
    for e in event.get():
        if e.type == QUIT:
            game = False
    tk += 1
    block_collides = sprite.spritecollide(car1, blocks, False)
    for i in block_collides:
        car1.wall_collide(i)
    kpr = key.get_pressed()

    if kpr[K_UP]:
        yal = -1
        if car1.img !='up.png' and not car1.onTouch:
            car1.img_change('up.png', 26, 35)
    if kpr[K_DOWN]:
        yal = 1
        if car1.img !='down.png' and not car1.onTouch:
            car1.img_change('down.png', 26, 35)
    if kpr[K_LEFT]:
        xal = -1
        if car1.img !='left.png' and not car1.onTouch:
            car1.img_change('left.png', 35, 26)
    if kpr[K_RIGHT]:
        xal = 1
        if car1.img !='right.png' and not car1.onTouch:
            car1.img_change('right.png', 35, 26)
    if tk == 5:
        car1.changespeed(xal, yal)
        tk = 0
    camera.update(car1)
    car1.onTouch = False
    car1.keys()
    xal = 0
    yal = 0
    speed_display_num = font1.render(str(car1.display_speed),True, (250, 250, 250))
    win.blit(speed_display_lab, (2,375))
    win.blit(speed_display_num, (2,390))

    clock.tick(60)
    display.update()