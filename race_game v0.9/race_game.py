from pygame import *
from race_game_classes import *
from random import randint
import sys
from race_game_levels import *
inGame = False
mixer.pre_init(44100, -16, 1, 512)
level = level1
level_display = 'Уровень 1'
SIZE = (700, 500)
win = display.set_mode(SIZE)
display.set_caption('race_game')
clock = time.Clock()
background = Surface(SIZE)
background.fill((150, 150, 150))
goToLevel = False
exitFromLevel = False
levelChangeMenu = False
spd = 1
xal = 0
yal = 0
inMenu = True
font.init()
font1 = font.SysFont('Arial Black', 70)
font2 = font.SysFont('Arial Black', 20)
menu_background = Surface(SIZE)
menu_background.fill((100, 150, 200))
                    
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
#создание кнопок и надписей
buttons = sprite.Group()
menu_buttons = list()
menu_buttons_labs = list()
levelChange_buttons = list()
levelChange_labs = list()
PlayButton = Button(400, 10, 250, 100, (100, 200, 200), 'sprites/button_pre.png')
LevelChangeButton = Button(400, 150, 250, 100, (100, 200, 200), 'sprites/button_pre.png')
Level1_ChangeButton = Button(50, 100, 200, 250, (125, 225, 200))
Level2_ChangeButton = Button(275, 100, 200, 250, (125, 225, 200))
LevelChangeBack = Button(20, 20, 104, 54, (100, 200, 200), 'sprites/button_pre.png')
PlayButtonLab = ButLabel(PlayButton.x, PlayButton.y, PlayButton.width, PlayButton.height)
PlayButtonLab.set_text('ИГРАТЬ', 30)
LevelChangeButtonLab = ButLabel(LevelChangeButton.x, LevelChangeButton.y, LevelChangeButton.width, LevelChangeButton.height)
LevelChangeButtonLab.set_text('Выбор уровня', 20)
Level1_ChangeButtonLab = ButLabel(Level1_ChangeButton.x, Level1_ChangeButton.y, Level1_ChangeButton.width, Level1_ChangeButton.height)
Level1_ChangeButtonLab.set_text('Уровень 1', 30)
Level2_ChangeButtonLab = ButLabel(Level2_ChangeButton.x, Level2_ChangeButton.y, Level2_ChangeButton.width, Level2_ChangeButton.height)
Level2_ChangeButtonLab.set_text('Уровень 2', 30)
LevelChangeBackLab = ButLabel(LevelChangeBack.x, LevelChangeBack.y, LevelChangeBack.width, LevelChangeBack.height)
LevelChangeBackLab.set_text('Назад', 20)
menu_buttons.append(PlayButton)
menu_buttons.append(LevelChangeButton)
levelChange_buttons.append(Level1_ChangeButton)
levelChange_buttons.append(Level2_ChangeButton)
levelChange_buttons.append(LevelChangeBack)
menu_buttons_labs.append(PlayButtonLab)
menu_buttons_labs.append(LevelChangeButtonLab)
levelChange_labs.append(Level1_ChangeButtonLab)
levelChange_labs.append(Level2_ChangeButtonLab)
buttons.add(PlayButton)
buttons.add(LevelChangeButton)
buttons.add(Level1_ChangeButton)
buttons.add(Level2_ChangeButton)
buttons.add(LevelChangeBack)
######################################################################
levelObjGroup = sprite.Group()
sprite_group = sprite.Group()
blocks = sprite.Group()
boxes = sprite.Group()
physic_props = sprite.Group()
interface_display = sprite.Group()
level_display_lab = font2.render(level_display, True, (250, 250, 250))


carx = 150
cary = 100



tk = 0
game = True
while game:
    if exitFromLevel:
        for i in levelObjGroup:
            i.kill()
        exitFromLevel = False
        ch1.pause()
        ch2.pause()
        ch3.pause()
        ch4.pause()
    kpr = key.get_pressed()
    if inGame:
        win.blit(background, (0, 0))
        for i in sprite_group:
            win.blit(i.image, camera.apply(i))

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
                if car1.hspeed >3 or car1.vspeed >3:
                    car1.vspeed = car1.vspeed//3
                    car1.hspeed = car1.hspeed//3
        for prop in physic_props:
            if sprite.spritecollide(prop, blocks, False):
                bl = sprite.spritecollide(prop, blocks, False)
                for blcl in bl:
                    prop.wall_collide(blcl)
            if sprite.spritecollide(prop, physic_props, False):
                prop_to_propcoll = sprite.spritecollide(prop, physic_props, False)
                for i in prop_to_propcoll:
                    if i.ableToCollide and (prop.hspeed >0 or prop.vspeed >0):
                        i.change_speed_momental(prop.hspeed, prop.vspeed)
                    elif (i.vspeed > 0 or i.hspeed > 0) and prop.ableToCollide:
                        prop.change_speed_momental(i.hspeed, i.vspeed)
        
        #Управление автомобилем
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
        car1.diagonal_move_check(xal, yal)
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
        for i in physic_props:
            win.blit(i.image, camera.apply(i))
        win.blit(car1.image, camera.apply(car1))
        camera.update(car1)
        speed_display_num = font1.render(str(car1.display_speed),True, (250, 250, 250))
        car1.onTouch = False
        car1.keys()
        xal = 0
        yal = 0
        car1.inMove = False
        speed_display_num = font1.render(str(car1.display_speed), True, (250, 250, 250))
        speed_display_lab = font2.render('Скорость:', True, (255, 255, 255))
        win.blit(speed_display_lab, (SIZE[0] - 460,SIZE[1] - 100))
        win.blit(speed_display_num, (SIZE[0] - 460,SIZE[1] - 90))
        interface_display.draw(win)
        speedometer.update(car1)

    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == MOUSEBUTTONDOWN and e.button == 1:
            ex, ey = e.pos
            for i in buttons:
                if i.collidepoint(ex, ey) == 1:
                    clock.tick(15)
                    if inMenu and i == PlayButton and not levelChangeMenu:
                        if not goToLevel and not inGame:
                            goToLevel = True
                            inMenu = False
                    elif inMenu and i == LevelChangeButton:
                        if not goToLevel and not inGame and not levelChangeMenu:
                            levelChangeMenu = True
                            LevelChangeBack.color(LevelChangeBack.fcolor)
                    elif inMenu and levelChangeMenu and i == Level1_ChangeButton:
                        Level1_ChangeButton.color((75, 175, 175))
                        if level == level2:
                            Level2_ChangeButton.color(Level2_ChangeButton.fcolor)
                        level = level1
                    elif inMenu and levelChangeMenu and i == Level2_ChangeButton:
                        Level2_ChangeButton.color((75, 175, 175))
                        if level == level1:
                            Level1_ChangeButton.color(Level1_ChangeButton.fcolor)
                        level = level2
                    elif inMenu and levelChangeMenu and i == LevelChangeBack:
                        levelChangeMenu = False
                        LevelChangeButton.color(LevelChangeButton.fcolor)
        if e.type == KEYDOWN and e.key == K_ESCAPE and inGame:
            exitFromLevel = True
            inGame=False
            inMenu = True
                        
    #Переход на игровой уровень
    if goToLevel:
        if level == level1:
            carx = 150
            cary = 100
        elif level == level2:
            carx = 500
            cary = 150
        goToLevel = False
        inGame = True
        total_level_width = len(level[0]) * 40
        total_level_height = len(level) * 40
        camera = Camera(camera_func, total_level_width, total_level_height)
        car1 = GameSprite('sprites/right.png', carx, cary, 7, 52, 26)
        sprite_group = sprite.Group()
        blocks = sprite.Group()
        boxes = sprite.Group()
        physic_props = sprite.Group()
        interface_display = sprite.Group()
        levelObjGroup.add(car1)
        levelObjGroup.add(camera)
        x = 0
        y = 0
        blsize = 40
        for row in level:
            for col in row:
                if col == '-':
                    block = Block('sprites/bricks.png',x, y, blsize, blsize)
                    sprite_group.add(block)
                    blocks.add(block)
                    levelObjGroup.add(block)
                elif col == '=':
                    box = Block('sprites/box1.png', x, y, blsize, blsize)
                    sprite_group.add(box)
                    boxes.add(box)
                    levelObjGroup.add(box)
                elif col == 'b':
                    rbar = randint(1,2)
                    barrel = Block('sprites/barrels' + str(rbar) + '.png', x, y, blsize, blsize)
                    sprite_group.add(barrel)
                    blocks.add(barrel)
                    levelObjGroup.add(barrel)
                elif col == 'g':
                    clear_grass = Block('sprites/clear_grass.png', x, y, 40, 40)
                    sprite_group.add(clear_grass)
                    levelObjGroup.add(clear_grass)
                elif col == 'p':
                    rpaper = randint(1,2)
                    grass_with_paper = Block('sprites/grass_paper' + str(rpaper) + '.png', x, y, 40, 40)
                    sprite_group.add(grass_with_paper)
                    levelObjGroup.add(grass_with_paper)
                elif col == 'w':
                    rwheels = randint(1,4)
                    grass_with_wheels = Block('sprites/grass_with_wheels' + str(rwheels) + '.png', x, y, 40, 40)
                    sprite_group.add(grass_with_wheels)
                    levelObjGroup.add(grass_with_wheels)
                elif col == 'f':
                    rflow = randint(1,4)
                    grass_with_flowers = Block('sprites/grass_with_flowers' + str(rflow) + '.png', x, y, 40, 40)
                    sprite_group.add(grass_with_flowers)
                    levelObjGroup.add(grass_with_flowers)
                elif col == 'u':
                    grass_f_up = Block('sprites/grass_from_up.png', x, y, 40, 40)
                    sprite_group.add(grass_f_up)
                    levelObjGroup.add(grass_f_up)
                elif col == 'd':
                    grass_f_down = Block('sprites/grass_from_down.png', x, y, 40, 40)
                    sprite_group.add(grass_f_down)
                    levelObjGroup.add(grass_f_down)
                elif col == 'l':
                    grass_f_left = Block('sprites/grass_from_left.png', x, y, 40, 40)
                    sprite_group.add(grass_f_left)
                    levelObjGroup.add(grass_f_left)
                elif col == 'r':
                    grass_f_right = Block('sprites/grass_from_right.png', x, y, 40, 40)
                    sprite_group.add(grass_f_right)
                    levelObjGroup.add(grass_f_right)
                elif col == 'c':
                    conus = PhysicsProp('sprites/conus.png', x, y, blsize, blsize)
                    physic_props.add(conus)
                    levelObjGroup.add(conus)
                x += blsize
            y += blsize
            x = 0
        speedometer = Speedometer(0, SIZE[1]- 100, 240, 180)
        interface_display.add(speedometer)
        levelObjGroup.add(speedometer)
        
        
    if inMenu and not inGame:
        win.blit(menu_background, (0, 0))
        for i in menu_buttons:
            i.color(i.fill_color)
            i.fl(win)
        for i in menu_buttons_labs:
            i.draw(50, 25, win)
        if level == level1:
            level_display = 'Уровень 1'
        elif level == level2:
            level_display = 'Уровень 2'
        PlayButtonLab.set_text('ИГРАТЬ', 30)
        level_display_lab = font2.render(level_display, True, (250, 250, 250))
        win.blit(level_display_lab, (LevelChangeButton.rect.left, LevelChangeButton.rect.bottom))
    
    if levelChangeMenu and not inGame:
        win.blit(menu_background, (0, 0))
        for i in levelChange_buttons:
            i.color(i.fill_color)
            i.fl(win)
        for i in levelChange_labs:
            i.draw(20, 100, win)
        LevelChangeBackLab.draw(14, 12, win)


    clock.tick(60)
    
    display.update()