from pygame import *
from race_game_classes import *
from random import randint
import sys
from race_game_levels import *
import json
angle = 90
default = {
    'lv1' : '0:0',
    'lv2' : '0:0', 
    'lv1t' : 999,
    'lv2t' : 999
}
best_time = {
    'lv1' : '0:0',
    'lv2' : '0:0', 
    'lv1t' : 999,
    'lv2t' : 999
}
with open('best_time.json', 'r', encoding='utf-8') as file:
    best_time = json.load(file)

seconds = 0
lapsToWin = 1
complete = False
inGame = False
mn = 0
completeScreen = False
laps_completed = 0
checkpoints_activated = 0
mixer.pre_init(44100, -16, 1, 512)
level = level1
level_display = 'Уровень 1'
SIZE = (700, 500)
FPS = 60
win = display.set_mode(SIZE)
display.set_caption('race_game')
clock = time.Clock()
background = Surface(SIZE)
background.fill((150, 150, 150))
goToLevel = False
exitFromLevel = False
levelChangeMenu = False
carChangeMenu = False
spd = 1
xal = 0
yal = 0
mil = 0
sec = 0
mn = 0
inMenu = True
font.init()
font1 = font.SysFont('Arial Black', 70)
font2 = font.SysFont('Arial Black', 20)
font3 = font.SysFont('Arial', 40)
font4 = font.SysFont('Impact', 60)
menu_background = transform.scale(image.load('sprites/background_img.png'), (SIZE[0], SIZE[1]))#Surface(SIZE)
#
car_1 = ['car_1', 7]
cur_car = car_1
car1_available = True
car1_text = 'Доступно'
car1_text2 = ''
car_2 = ['car_2', 8]
car2_available = False
car2_text = 'Уровень 1'
car2_text2 = 'за 2:00'
car_3 = ['car_3', 9]
car3_available = False
car3_text = 'Уровень 2'
car3_text2 = 'за 2:00'
#
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
#
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
#buttons
buttons = sprite.Group()
menu_buttons = list()
menu_buttons_labs = list()
levelChange_buttons = list()
levelChange_labs = list()
completeScreen_buttons = list()
completeScreen_labs = list()
carChangeButtons = list()
carChangeLabs1 = list()
carChangeLabs2 = list()
PlayButton = Button(400, 40, 250, 100, 'sprites/button1.png')
LevelChangeButton = Button(400, 140, 250, 100, 'sprites/button1.png')
Level1_ChangeButton = Button(50, 130, 200, 250, 'sprites/tablet.png')
Level2_ChangeButton = Button(275, 130, 200, 250, 'sprites/tablet.png')
LevelChangeBack = Button(20, 20, 104, 54, 'sprites/button1.png')
completeRestart = Button(70, 350, 250, 100, 'sprites/button1.png')
completeMenuButton = Button(370, 350, 250, 100, 'sprites/button1.png')
carChangeButton = Button(400, 240, 250, 100, 'sprites/button1.png')
car1ChangeButton = Button(30, 130, 200, 250, 'sprites/tablet.png')
car2ChangeButton = Button(255, 130, 200, 250, 'sprites/tablet.png')
progressResetButton = Button(500, 20, 200, 70, 'sprites/button1.png')
car3ChangeButton = Button(480, 130, 200, 250, 'sprites/tablet.png')
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
completeRestartLab = ButLabel(completeRestart.x, completeRestart.y, completeRestart.width, completeRestart.height)
completeRestartLab.set_text('Заново', 30)
completeMenuLab = ButLabel(completeMenuButton.x, completeMenuButton.y, completeMenuButton.width, completeMenuButton.height)
completeMenuLab.set_text('Меню', 30)
carChangeLab = ButLabel(carChangeButton.x, carChangeButton.y, carChangeButton.width, carChangeButton.height)
carChangeLab.set_text('Автомобили', 22)
car1ChangeLab1 = ButLabel(car1ChangeButton.x, car1ChangeButton.y, car1ChangeButton.width, car1ChangeButton.height)
car1ChangeLab1.set_text(car1_text, 22)
car1ChangeLab2 = ButLabel(car1ChangeButton.x, car1ChangeButton.y, car1ChangeButton.width, car1ChangeButton.height)
car1ChangeLab2.set_text(car1_text2, 22)
car2ChangeLab1 = ButLabel(car2ChangeButton.x, car2ChangeButton.y, car2ChangeButton.width, car2ChangeButton.height)
car2ChangeLab1.set_text(car2_text, 22)
car2ChangeLab2 = ButLabel(car2ChangeButton.x, car2ChangeButton.y, car2ChangeButton.width, car2ChangeButton.height)
car2ChangeLab2.set_text(car2_text2, 22)
car3ChangeLab1 = ButLabel(car3ChangeButton.x, car3ChangeButton.y, car3ChangeButton.width, car3ChangeButton.height)
car3ChangeLab1.set_text(car3_text, 22)
car3ChangeLab2 = ButLabel(car3ChangeButton.x, car3ChangeButton.y, car3ChangeButton.width, car3ChangeButton.height)
car3ChangeLab2.set_text(car3_text2, 22)
progressResetLab = ButLabel(progressResetButton.x, progressResetButton.y, progressResetButton.width, progressResetButton.height)
progressResetLab.set_text('Сбросить прогресс', 15)
menu_buttons.append(PlayButton)
menu_buttons.append(LevelChangeButton)
menu_buttons.append(carChangeButton)
levelChange_buttons.append(Level1_ChangeButton)
levelChange_buttons.append(Level2_ChangeButton)
levelChange_buttons.append(LevelChangeBack)
completeScreen_buttons.append(completeRestart)
completeScreen_buttons.append(completeMenuButton)
carChangeButtons.append(car1ChangeButton)
carChangeButtons.append(car2ChangeButton)
carChangeButtons.append(car3ChangeButton)
carChangeButtons.append(progressResetButton)
###
menu_buttons_labs.append(PlayButtonLab)
menu_buttons_labs.append(LevelChangeButtonLab)
menu_buttons_labs.append(carChangeLab)
levelChange_labs.append(Level1_ChangeButtonLab)
levelChange_labs.append(Level2_ChangeButtonLab)
completeScreen_labs.append(completeRestartLab)
completeScreen_labs.append(completeMenuLab)
carChangeLabs1.append(car1ChangeLab1)
carChangeLabs1.append(car2ChangeLab1)
carChangeLabs1.append(car3ChangeLab1)
carChangeLabs2.append(car1ChangeLab2)
carChangeLabs2.append(car2ChangeLab2)
carChangeLabs2.append(car3ChangeLab2)
carChangeLabs1.append(progressResetLab)
buttons.add(PlayButton)
buttons.add(LevelChangeButton)
buttons.add(Level1_ChangeButton)
buttons.add(Level2_ChangeButton)
buttons.add(LevelChangeBack)
buttons.add(completeRestart)
buttons.add(completeMenuButton)
buttons.add(carChangeButton)
buttons.add(car1ChangeButton)
buttons.add(car2ChangeButton)
buttons.add(progressResetButton)
buttons.add(car3ChangeButton)
#############################

race_time = '0'
levelObjGroup = sprite.Group()
sprite_group = sprite.Group()
blocks = sprite.Group()
boxes = sprite.Group()
physic_props = sprite.Group()
interface_display = sprite.Group()
checkpoints = sprite.Group()
level_display_lab = font2.render(level_display, True, (250, 250, 250))
laps_display = font3.render(str(laps_completed) + '/2', True, (250, 250, 250))
time_display = font3.render(str(mn) + ':' + str(sec), True, (250, 250, 250))
race_time_display = font4.render('ВРЕМЯ: ' + str(race_time), True, (250, 250, 250))
race_time_tablet = Button(136, 5, 430, 335, 'sprites/tablet.png')
finishLabel = font4.render('ФИНИШ', True, (250, 250, 250))





tk = 0
game = True
while game:
    if exitFromLevel:
        for i in levelObjGroup:
            i.kill()
        exitFromLevel = False
        ch1.pause()
        ch2.pause()
    kpr = key.get_pressed()
    if inGame:
        win.blit(background, (0, 0))
        mil +=1
        if mil == FPS:
            sec += 1
            mil = 0
            seconds += 1
        if sec == FPS:
            mn += 1
            sec = 0
            
        for i in sprite_group:
            win.blit(i.image, camera.apply(i))

        tk += 1
        #
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
                    #if i.ableToCollide and (prop.hspeed >0 or prop.vspeed >0):
                        #i.change_speed_momental(prop.hspeed, prop.vspeed)
                    #elif (i.vspeed > 0 or i.hspeed > 0) and prop.ableToCollide:
                        #prop.change_speed_momental(i.hspeed, i.vspeed)
                    if i.ableToCollide and (prop.hspeed > i.hspeed or prop.vspeed > i.vspeed):
                        i.change_speed_momental(prop.hspeed, prop.vspeed)
                    elif (i.vspeed > prop.vspeed or i.hspeed > prop.hspeed) and prop.ableToCollide:
                        prop.change_speed_momental(i.hspeed, i.vspeed)
        check_collides = sprite.spritecollide(car1, checkpoints, False)
        for i in check_collides:
            if not i.activate:
                i.activate = True
                checkpoints_activated += 1
        if finish.activate:
            if level == level1:
                checkpoints_amount = level1_checkpoints
            elif level == level2:
                checkpoints_amount = level2_checkpoints
            if checkpoints_activated >= checkpoints_amount:
                laps_completed += 1
                checkpoints_activated = 0
                for i in checkpoints:
                    i.activate = False
            elif checkpoints_activated < checkpoints_amount:
                checkpoints_activated -=1
                finish.activate = False
        if laps_completed == lapsToWin:
            complete = True
        
        #
        if kpr[K_UP]:
            yal = -1
            car1.inMove = True
            if car1.img !='sprites/' + cur_car[0] +'_up.png' and not car1.onTouch:
                car1.img_change('sprites/' + cur_car[0] +'_up.png', 30, 60)#26, 52
        if kpr[K_DOWN]:
            yal = 1
            car1.inMove = True
            if car1.img !='sprites/' + cur_car[0] +'_down.png' and not car1.onTouch:
                car1.img_change('sprites/' + cur_car[0] +'_down.png', 30, 60)
            angle = 180
        if kpr[K_LEFT]:
            xal = -1
            car1.inMove = True
            if car1.img !='sprites/' + cur_car[0] +'_left.png' and not car1.onTouch:
                car1.img_change('sprites/' + cur_car[0] +'_left.png', 60, 30)
            angle = 270
        if kpr[K_RIGHT]:
            xal = 1
            car1.inMove = True
            if car1.img !='sprites/' + cur_car[0] +'_right.png' and not car1.onTouch:
                car1.img_change('sprites/' + cur_car[0] +'_right.png', 60, 30)
            angle = 90
        car1.diagonal_move_check()
                
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
        speed_display_lab = font2.render('Скорость: ', True, (255, 255, 255))
        laps_display = font3.render('Круги: ' + str(laps_completed) + '/' + str(lapsToWin), True, (250, 250, 250))
        time_display = font3.render(str(mn) + ':' + str(sec), True, (250, 250, 250))
        win.blit(speed_display_lab, (SIZE[0] - 460,SIZE[1] - 100))
        win.blit(speed_display_num, (SIZE[0] - 460,SIZE[1] - 90))
        win.blit(laps_display, (SIZE[0]- 150, 5))
        win.blit(time_display, (SIZE[0]- 65, 45))
        interface_display.draw(win)
        speedometer.update(car1)
        race_time = str(mn) + ':' + str(sec)

    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == MOUSEBUTTONDOWN and e.button == 1:
            ex, ey = e.pos
            for i in buttons:
                if i.collidepoint(ex, ey) == 1:
                    clock.tick(15)
                    if inMenu and i == PlayButton:
                        if not goToLevel:
                            goToLevel = True
                            inMenu = False
                    elif inMenu and i == LevelChangeButton:
                        levelChangeMenu = True
                        inMenu = False
                    elif levelChangeMenu and i == Level1_ChangeButton:
                        Level1_ChangeButton.image = transform.scale(image.load('sprites/tablet_pressed.png'), (Level1_ChangeButton.width, Level1_ChangeButton.height))#color((75, 175, 175))
                        Level2_ChangeButton.image = transform.scale(image.load('sprites/tablet.png'), (Level2_ChangeButton.width, Level2_ChangeButton.height))
                        level = level1
                    elif levelChangeMenu and i == Level2_ChangeButton:
                        Level2_ChangeButton.image = transform.scale(image.load('sprites/tablet_pressed.png'), (Level2_ChangeButton.width, Level2_ChangeButton.height))
                        Level1_ChangeButton.image = transform.scale(image.load('sprites/tablet.png'), (Level1_ChangeButton.width, Level1_ChangeButton.height))
                        level = level2
                    elif (levelChangeMenu or carChangeMenu) and i == LevelChangeBack:
                        levelChangeMenu = False
                        carChangeMenu = False
                        inMenu = True
                    elif completeScreen and i == completeRestart:
                        goToLevel = True
                        completeScreen = False
                    elif completeScreen and i == completeMenuButton:
                        inMenu = True
                        completeScreen = False
                    elif inMenu and i == carChangeButton:
                        carChangeMenu = True
                        inMenu = False
                    elif carChangeMenu and i == car1ChangeButton:
                        cur_car = car_1
                        car1ChangeButton.image = transform.scale(image.load('sprites/tablet_pressed.png'), (car1ChangeButton.width, car1ChangeButton.height))
                        car2ChangeButton.image = transform.scale(image.load('sprites/tablet.png'), (car2ChangeButton.width, car2ChangeButton.height))
                        car3ChangeButton.image = transform.scale(image.load('sprites/tablet.png'), (car3ChangeButton.width, car3ChangeButton.height))

                    elif carChangeMenu and i == car2ChangeButton and car2_available:
                        cur_car = car_2
                        car2ChangeButton.image = transform.scale(image.load('sprites/tablet_pressed.png'), (car2ChangeButton.width, car2ChangeButton.height))
                        car1ChangeButton.image = transform.scale(image.load('sprites/tablet.png'), (car1ChangeButton.width, car1ChangeButton.height))
                        car3ChangeButton.image = transform.scale(image.load('sprites/tablet.png'), (car3ChangeButton.width, car3ChangeButton.height))

                    elif carChangeMenu and i == car3ChangeButton and car3_available:
                        cur_car = car_3
                        car3ChangeButton.image = transform.scale(image.load('sprites/tablet_pressed.png'), (car3ChangeButton.width, car3ChangeButton.height))
                        car2ChangeButton.image = transform.scale(image.load('sprites/tablet.png'), (car2ChangeButton.width, car2ChangeButton.height))
                        car1ChangeButton.image = transform.scale(image.load('sprites/tablet.png'), (car1ChangeButton.width, car1ChangeButton.height))

                    elif carChangeMenu and i == progressResetButton:
                        with open('best_time.json', 'w', encoding='utf-8') as file:
                            json.dump(default, file)
                        with open('best_time.json', 'r', encoding='utf-8') as file:
                            best_time = json.load(file)
                        cur_car = car_1
        if e.type == KEYDOWN and e.key == K_ESCAPE and inGame:
            exitFromLevel = True
            inGame=False
            inMenu = True
                        
    #
    if goToLevel:
        mil = 0
        sec = 0
        mn = 0
        seconds = 0
        if level == level1:
            carx = 150
            cary = 200
        elif level == level2:
            carx = 500
            cary = 150
        goToLevel = False
        inGame = True
        total_level_width = len(level[0]) * 40
        total_level_height = len(level) * 40
        camera = Camera(camera_func, total_level_width, total_level_height)
        car1 = Car('sprites/' + cur_car[0] +'_right.png', carx, cary, cur_car[1], 60, 30)
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
                elif col == 'n':
                    checkpoint = Checkpoint(x, y, 240, 240)
                    levelObjGroup.add(checkpoint)
                    checkpoints.add(checkpoint)
                elif col == 'e':
                    finish = Checkpoint(x, y, 40, 280)
                    levelObjGroup.add(finish)
                    checkpoints.add(finish)
                elif col == 's':
                    finish_decor = Block('sprites/finish.png', x, y, blsize, blsize)
                    levelObjGroup.add(finish_decor)
                    sprite_group.add(finish_decor)
                elif col == '1':
                    right_arrow = Block('sprites/arrow_right.png', x, y, blsize, blsize)
                    levelObjGroup.add(right_arrow)
                    sprite_group.add(right_arrow)
                elif col == '2':
                    up_arrow = Block('sprites/arrow_up.png', x, y, blsize, blsize)
                    levelObjGroup.add(up_arrow)
                    sprite_group.add(up_arrow)
                elif col == '3':
                    left_arrow = Block('sprites/arrow_left.png', x, y, blsize, blsize)
                    levelObjGroup.add(left_arrow)
                    sprite_group.add(left_arrow)
                elif col == '4':
                    down_arrow = Block('sprites/arrow_down.png', x, y, blsize, blsize)
                    levelObjGroup.add(down_arrow)
                    sprite_group.add(down_arrow)
                elif col == '5':
                    horisontal_line = Block('sprites/line_h.png', x, y, blsize, blsize)
                    levelObjGroup.add(horisontal_line)
                    sprite_group.add(horisontal_line)
                elif col == '6':
                    vertical_line = Block('sprites/line_v.png', x, y, blsize, blsize)
                    levelObjGroup.add(vertical_line)
                    sprite_group.add(vertical_line)
                x += blsize
            y += blsize
            x = 0
        speedometer = Speedometer(0, SIZE[1]- 100, 240, 180)
        interface_display.add(speedometer)
        levelObjGroup.add(speedometer)
        if level == level1:
            lapsToWin = level1_lapsToWin
        elif level == level2:
            lapsToWin = level2_lapsToWin
        
    if inMenu:
        win.blit(menu_background, (0, 0))
        for i in menu_buttons:
            i.fl(win)
        for i in menu_buttons_labs:
            i.draw(50, 25, win)
        if level == level1:
            level_display = 'Уровень 1'
        elif level == level2:
            level_display = 'Уровень 2'
        level_display_lab = font2.render(level_display, True, (250, 250, 250))
        win.blit(level_display_lab, (LevelChangeButton.rect.left + 70, LevelChangeButton.rect.bottom - 45))
    
    if levelChangeMenu:
        win.blit(menu_background, (0, 0))
        for i in levelChange_buttons:
            i.fl(win)
        for i in levelChange_labs:
            i.draw(20, 100, win)
        LevelChangeBackLab.draw(14, 12, win)
    
    if complete:
        inGame = False
        exitFromLevel = True
        completeScreen = True
        complete = False
        laps_completed = 0
        race_time_display = font4.render('время - ' + str(race_time), True, (250, 250, 250))
        if level == level1:
            if seconds < best_time['lv1t']:
                best_time['lv1'] = race_time
                best_time['lv1t'] = seconds
                with open('best_time.json', 'w', encoding='utf-8') as file:
                    json.dump(best_time, file)
            lv = 'lv1'
        elif level == level2:
            if seconds < best_time['lv2t']:
                best_time['lv2'] = race_time
                best_time['lv2t'] = seconds
                with open('best_time.json', 'w', encoding='utf-8') as file:
                    json.dump(best_time, file)
            lv = 'lv2'
        besttimelab = font3.render('лучшее время:' + best_time[lv], True, (250, 250, 250))

    if completeScreen:
        win.blit(menu_background, (0, 0))
        for i in completeScreen_buttons:
            i.fl(win)
        for i in completeScreen_labs:
            i.draw(60, 25, win)
        race_time_tablet.fl(win)
        win.blit(race_time_display, (190, 75))
        win.blit(finishLabel, (250, 20))
        win.blit(besttimelab, (200, 190))

    if carChangeMenu:
        if best_time['lv1t'] <= 120 and not car2_available:
            car2_available = True
            car2ChangeLab1.set_text('Доступно', 22)
            car2ChangeLab2.set_text('', 0)
        elif best_time['lv1t'] > 120 and car2_available:
            car2ChangeLab1.set_text(car2_text, 22)
            car2ChangeLab2.set_text(car2_text2, 22)
            car2_available = False
        elif best_time['lv2t'] <= 120 and not car3_available:
            car3_available = True
            car3ChangeLab1.set_text('Доступно', 22)
            car3ChangeLab2.set_text('', 0)
        elif best_time['lv2t'] > 120 and car3_available:
            car3ChangeLab1.set_text(car3_text, 22)
            car3ChangeLab2.set_text(car3_text2, 22)
            car3_available = False
        win.blit(menu_background, (0, 0))
        for i in carChangeButtons:
            i.fl(win)
        for i in carChangeLabs1:
            i.draw(20, 25, win)
        for i in carChangeLabs2:
            i.draw(20, 50, win)
        win.blit(transform.scale(image.load('sprites/car_1_right.png'), (100, 50)), (car1ChangeButton.x + 40, car1ChangeButton.y + 130))
        win.blit(transform.scale(image.load('sprites/car_2_right.png'), (100, 50)), (car2ChangeButton.x + 40, car2ChangeButton.y + 130))
        win.blit(transform.scale(image.load('sprites/car_3_right.png'), (100, 50)), (car3ChangeButton.x + 40, car3ChangeButton.y + 130))
        LevelChangeBack.fl(win)
        LevelChangeBackLab.draw(14, 12, win)



    clock.tick(FPS)
    
    display.update()