from pygame import *
from race_game_classes import *

SIZE = (640, 480)
win = display.set_mode(SIZE)
display.set_caption('race_game')
clock = time.Clock()
background = Surface(SIZE)
background.fill((100, 250, 100))
mixer.pre_init(44100, -16, 1, 512)
spd = 1
xal = 0
yal = 0

#Звуки
mixer.init()
SspeedUp = mixer.Sound('sounds/speedUp.ogg')
SnoMove = mixer.Sound('sounds/noMove.ogg')
Scollide = mixer.Sound('sounds/collide.ogg')
SBoxBreak = mixer.Sound('sounds/box_break.ogg')
speedUp_onPlay = False
collide_onPlay = False
SnoMove.set_volume(0.3)
SspeedUp.set_volume(0.1)
Scollide.set_volume(0.5)
SBoxBreak.set_volume(0.1)
ch1 = SnoMove.play(-1)
ch2 = SspeedUp.play()
ch3 = Scollide.play()
ch4 = SBoxBreak.play()
ch1.pause()
ch2.pause()
ch3.pause()
ch4.pause()
#Камера
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

#Создание уровня и объектов
car1 = GameSprite('sprites/up.png', 80, 80, 7, 26, 50)#26, 35

level = ['---------------------------------------------------',
         '-                                               ==-',
         '-                                                =-',
         '-=                                                -',
         '-==                                ==             -',
         '--------------------------------------            -',
         '-==                                               -',
         '-=                                                -',
         '-                                                =-',
         '-            =                                  ==-',
         '-           =--------------------------------------',
         '-            =                                    -',
         '-                                                 -',
         '-   =                                             -',
         '-   ==                                           =-',
         '--------------------------------------=           -',
         '-                                                 -',
         '-                                                 -',
         '-                                                =-',
         '-=           ==                                 ==-',
         '-           =--------------------------------------',
         '-                                                 -',
         '-                                                 -',
         '-=                                                -',
         '-==                                               -',
         '---------------------------------------------------']

total_level_width = len(level[0]) * 40
total_level_height = len(level) * 40
camera = Camera(camera_func, total_level_width, total_level_height)

sprite_group = sprite.Group()
blocks = sprite.Group()
boxes = sprite.Group()
x = 0
y = 0
for row in level:
    for col in row:
        if col == '-':
            block = Block('sprites/block.png',x, y, 40, 40 )
            sprite_group.add(block)
            blocks.add(block)
        elif col == '=':
            box = Block('sprites/box1.png', x, y, 40, 40)
            sprite_group.add(box)
            boxes.add(box)
        x += 40
    y += 40
    x = 0
#Создание надписей
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
    
    
    for e in event.get():
        if e.type == QUIT:
            game = False
    tk += 1
    #Проверка столкновений
    block_collides = sprite.spritecollide(car1, blocks, False)
    for i in block_collides:
        car1.wall_collide(i)
    if block_collides != [] and not collide_onPlay:
        ch3 = Scollide.play()
        collide_onPlay = True
    elif block_collides == []:
        collide_onPlay = False
    box_collides = sprite.spritecollide(car1, boxes, False)
    for i in box_collides:
        if i.ableToCollide == True:
            ch4 = SBoxBreak.play()
            car1.wall_collide(i)
            i.break_col()
    #Управление автомобилем
    kpr = key.get_pressed()
    if kpr[K_UP]:
        yal = -1
        car1.inMove = True
        if car1.img !='sprites/up.png' and not car1.onTouch:
            car1.img_change('sprites/up.png', 26, 50)#26, 35
    if kpr[K_DOWN]:
        yal = 1
        car1.inMove = True
        if car1.img !='sprites/down.png' and not car1.onTouch:
            car1.img_change('sprites/down.png', 26, 50)
    if kpr[K_LEFT]:
        xal = -1
        car1.inMove = True
        if car1.img !='sprites/left.png' and not car1.onTouch:
            car1.img_change('sprites/left.png', 50, 26)
    if kpr[K_RIGHT]:
        xal = 1
        car1.inMove = True
        if car1.img !='sprites/right.png' and not car1.onTouch:
            car1.img_change('sprites/right.png', 50, 26)
    if tk == 5:
        car1.changespeed(xal, yal)
        tk = 0
        if car1.inMove == False:
            ch1.unpause()
            #ch2.pause()
            ch2.stop()
            speedUp_onPlay = False
        if car1.inMove == True:
            if not speedUp_onPlay:
                ch2 = SspeedUp.play(-1)
            ch2.unpause()
            ch1.pause()
            speedUp_onPlay = True
    win.blit(car1.image, camera.apply(car1))
    camera.update(car1)
    speed_display_num = font1.render(str(car1.display_speed),True, (250, 250, 250))
    car1.onTouch = False
    car1.keys()
    xal = 0
    yal = 0
    car1.inMove = False
    win.blit(speed_display_lab, (2,375))
    win.blit(speed_display_num, (2,390))

    clock.tick(60)
    
    display.update()