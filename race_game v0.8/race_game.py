from pygame import *
from race_game_classes import *
from random import randint

SIZE = (700, 500)
win = display.set_mode(SIZE)
display.set_caption('race_game')
clock = time.Clock()
background = Surface(SIZE)
background.fill((150, 150, 150))
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
SnoMove.set_volume(0.2)
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
car1 = GameSprite('sprites/up.png', 150, 100, 7, 26, 52)#26, 35

level = ['--------------------------------------------------------------------------------------------gggggggg',
         '- ==                                 c                             ==                      ---pggggg',
         '- =                                                                                          =--gpgg',
         '-                                                                                               -ggg',
         '-=                                                                                               -gg',
         '-==                                                                             c                -wg',
         '---------              --------------------------------------------------------------  c          -g',
         'gfgggw-             ----     ---wgggggggwggggggggggg-------          ------ggggpgggwg---b         -g',
         'fgpgg-            --==         --gggggggggggffgggg--          c    c       ---gggggggggg--      c -g',
         'gggg-            -               -gggpgggggfgfggg-       c                    ---ggggggggg-       b-',
         'gggg-           -                 -ggggggggpgggg-   c                            --gggggggg-       -',
         'ggwg-         --c          c       -gggggggggggg-                  ==              -ggggggw-      c-',
         'ggg-         -g-          --        -ggggggggggg-             ------------          -ggggggg-      -',
         'wgg-         -g-       =--gp-        -gpgggggggg-           --gwgggggggggg-          -gggggg-      -',
         'gg-         -g-        -ggggp-        -gggggggg-b          -ggggggggggggwgg-          ---gg-       -',
         'gg-         -g-       =-ggggg-         --gggg--           -ggpggggggggggggg-             --        -',
         'gg-  c   c  -g-       -gpggggg-          ----==           -ggggggggggggggggg-                      -',
         'g-         -gg-       -gggpfgg-                          b-gggggggggggggggpg-                     --',
         'w-========-pgg-       -ggggffgg-                         -gggggggggpggggggggg-                   -g-',
         'g-        -gpg-       -ggggggggg-                        -gggggggggggggggggggg--=            == -pg-',
         'g-=       -ggg-        -ggggggggg--                     -gggggggggggggggggggpggg--- b        ==-ggg-',
         'g-=        -gg-        -gggggggggwg----        ==  -----ggggwgggggggggggggggggggggg-----------------',
         'gg-        -gg-         -ggggggggggpggg------------gggpggggggg------------------------gggggggggwgggg',
         'gg-        -ggg-         -------------------------------------==                    ==----gggggggggg',
         'gp-         -gg-                        bb                    ==                     =    ---ggpgggg',
         'gg-         -ggg-b==                                                                         --ggggg',
         'ggg-         -fgg--=                                                                           -gggg',
         'ggg-          -fggg---                                       b --------------------             -ggg',
         'ggg-           -ffgggg-----------------------------------------gggggpgggggggggggggg---          -ggg',
         'pggg-           ---gfgggggggwggggggggggggpggggg-----==        b--------ggggggggggggggg-          -gg',
         'gggg-              ---fpggggggggggggggggggg----     =                  ---ggggggggggggg-         -gg',
         'ggggg-                ---gpggggffgggggggg--=                              -gggggwgggggg-         -gg',
         'gggggg--                 ---ggggfgggggg--                b                 --ggggggggg-         -ggg',
         'gggggpgg--                  ---gggggg--              --------                ---gggg--  c    c  -ggg',
         'gggggggggg---                  ---gg- c          ----gggggggg---                ----            -ggg',
         'ggggggggggpgg---                 =--      c   ---gggggggggpggggg--               =             -gwgg',
         'ggggggggggggggpg---                         --gggggggggggggggggggg-                            -gggg',
         'ggggggggggggggggggg---                     -gwggggggggggggggggggggg-                         =-ggpgg',
         'ggggggpggggggggggggggg---                 -ggggggggggggggpgggggggwgg--                      --gggggg',
         'ggggggggggggggfgffggggggg---            --gpgggggggggggggggggggggggggg---=               ---gggggggg',
         'gggggggggggggggffgggggggpggg----     ---ggggggggggggggggggggggggggggggggg----        ----ggggggggggg',
         'gggggggggggggggggggggggggggggggg-----gggggggggggggggggggggggggggggggggggggggg--------ggggggggggggggg',
         'gggggggggggggggggggggggggggggggggggggggggggggggggggggpggggggggggggggggggggggggggggggpggggggggggggggg']

total_level_width = len(level[0]) * 40
total_level_height = len(level) * 40
camera = Camera(camera_func, total_level_width, total_level_height)

sprite_group = sprite.Group()
blocks = sprite.Group()
boxes = sprite.Group()
physic_props = sprite.Group()
x = 0
y = 0
blsize = 40
for row in level:
    for col in row:
        if col == '-':
            block = Block('sprites/bricks.png',x, y, blsize, blsize)
            sprite_group.add(block)
            blocks.add(block)
        elif col == 'c':
            conus = PhysicsProp('sprites/conus.png', x, y, blsize, blsize)
            sprite_group.add(conus)
            physic_props.add(conus)
        elif col == '=':
            box = Block('sprites/box1.png', x, y, blsize, blsize)
            sprite_group.add(box)
            boxes.add(box)
        elif col == 'b':
            rbar = randint(1,2)
            barrel = Block('sprites/barrels' + str(rbar) + '.png', x, y, blsize, blsize)
            sprite_group.add(barrel)
            blocks.add(barrel)
        elif col == 'g':
            clear_grass = Block('sprites/clear_grass.png', x, y, 40, 40)
            sprite_group.add(clear_grass)
        elif col == 'p':
            rpaper = randint(1,2)
            grass_with_paper = Block('sprites/grass_paper' + str(rpaper) + '.png', x, y, 40, 40)
            sprite_group.add(grass_with_paper)
        elif col == 'w':
            rwheels = randint(1,4)
            grass_with_wheels = Block('sprites/grass_with_wheels' + str(rwheels) + '.png', x, y, 40, 40)
            sprite_group.add(grass_with_wheels)
        elif col == 'f':
            rflow = randint(1,4)
            grass_with_flowers = Block('sprites/grass_with_flowers' + str(rflow) + '.png', x, y, 40, 40)
            sprite_group.add(grass_with_flowers)
        x += blsize
    y += blsize
    x = 0
#Создание надписей
font.init()
font1 = font.SysFont('Arial Black', 70)
speed_display_num = font1.render(str(car1.display_speed), True, (250, 250, 250))
font2 = font.SysFont('Arial Black', 20)
speed_display_lab = font2.render('Скорость:', True, (255, 255, 255))

ang = 0


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
    phys_collides = sprite.spritecollide(car1, physic_props, False)
    for i in phys_collides:
        i.change_speed_momental(car1.hspeed, car1.vspeed)
        if not i.onTouch:
            car1.vspeed -= car1.vspeed//3
            car1.hspeed -= car1.hspeed//3
    for prop in physic_props:
        if sprite.spritecollide(prop, blocks, False):
            bl = sprite.spritecollide(prop, blocks, False)
            for blcl in bl:
                prop.wall_collide(blcl)
    #Управление автомобилем
    kpr = key.get_pressed()
    if kpr[K_UP]:
        yal = -1
        car1.inMove = True
        if car1.img !='sprites/up.png' and not car1.onTouch:
            car1.img_change('sprites/up.png', 26, 52)#26, 35
    if kpr[K_DOWN]:
        yal = 1
        car1.inMove = True
        if car1.img !='sprites/down.png' and not car1.onTouch:
            car1.img_change('sprites/down.png', 26, 52)
    if kpr[K_LEFT]:
        xal = -1
        car1.inMove = True
        if car1.img !='sprites/left.png' and not car1.onTouch:
            car1.img_change('sprites/left.png', 52, 26)
    if kpr[K_RIGHT]:
        xal = 1
        car1.inMove = True
        if car1.img !='sprites/right.png' and not car1.onTouch:
            car1.img_change('sprites/right.png', 52, 26)
        
    if tk == 5:
        car1.changespeed(xal, yal)
        tk = 0
        if car1.inMove == False:
            ch1.unpause()
            ch2.stop()
            speedUp_onPlay = False
        if car1.inMove == True:
            if not speedUp_onPlay:
                ch2 = SspeedUp.play(-1)
            ch2.unpause()
            ch1.pause()
            speedUp_onPlay = True
        for i in physic_props:
            i.change_speed()
    physic_props.update()
    win.blit(car1.image, camera.apply(car1))
    camera.update(car1)
    speed_display_num = font1.render(str(car1.display_speed),True, (250, 250, 250))
    car1.onTouch = False
    car1.keys()
    xal = 0
    yal = 0
    car1.inMove = False
    win.blit(speed_display_lab, (2,390))
    win.blit(speed_display_num, (2,410))

    clock.tick(60)
    
    display.update()