# -*- coding: utf-8 -*-
# !/usr/bin/python
'''
Created on May 31, 2014
@author: yuanzi
'''
import random
import sys
import time
import math
import pygame
from pygame.locals import *
import numpy as np

GRID = 100
TITLE = 100
COUNT = 4
SPACING = 10
GRID_SPACING = 10
TEXT = 25


def main():
    # 初始化pygame
    pygame.init()
    map = Map(8)
    image = Image()
    settings = Settings()
    screen = pygame.display.set_mode((470, 620))

    pygame.mixer.init()
    game_music = './petard.wav'
    pygame.mixer.music.load(game_music)
    pygame.mixer.music.play()

    pygame.display.set_caption("2048")
    icon_res = 'images/2048.jpg'
    icon = pygame.image.load(icon_res).convert_alpha()
    pygame.display.set_icon(icon)

    left_move, right_move, up_move, down_move = False, False, False, False

    # 游戏界面布局
    title = pygame.Surface((180, 100))
    time_grid = pygame.Surface((100, 55))
    record_grid = pygame.Surface((100, 55))
    regret_grid = pygame.Surface((112, 40))
    grid_back = pygame.Surface((450, 450))

    grid1 = 100
    count = 4
    grid_spacing = 10

    # 设置颜色
    grid = [pygame.Surface((GRID, GRID)) for i in range(12)]
    grid[0].fill((119, 110, 101))
    grid[1].fill((238, 228, 218))
    grid[2].fill((238, 225, 201))
    grid[3].fill((243, 178, 122))
    grid[4].fill((246, 150, 100))
    grid[5].fill((247, 124, 95))
    grid[6].fill((247, 95, 59))
    grid[7].fill((237, 208, 115))
    grid[8].fill((237, 204, 98))
    grid[9].fill((237, 201, 80))
    grid[10].fill((237, 197, 63))
    grid[11].fill((237, 194, 46))

    # 游戏计时
    times = 0
    TIMER = pygame.USEREVENT + 1
    pygame.time.set_timer(TIMER, 1000)
    times_suspend = times

    score_block = pygame.Surface((400, 100))
    score_block.fill((119, 110, 101))

    # 设置字体
    map_font = pygame.font.Font(None, int(GRID * 2 / 3))
    time_font = pygame.font.Font(None, int(TITLE * 2 / 3))

    game_2048 = False

    # 读取记录文件
    f = open('record.txt')
    line = f.readline()
    line = line.strip('\n')
    record_list = []
    while line:
        num = line
        record_list.append(num)
        line = f.readline()
    f.close()
    for i in range(5):
        record_list[i] = int(record_list[i])

    while True:

        screen.fill([255, 255, 255])
        map.mouse_x, map.mouse_y = pygame.mouse.get_pos()

        # 判断事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # close the game
                sys.exit()

            elif event.type == TIMER:
                times = times + 1

            # keyboard operation
            elif event.type == pygame.KEYDOWN:
                pressed_keys = pygame.key.get_pressed()
                if pressed_keys[K_a] or pressed_keys[K_LEFT] or pressed_keys[
                    K_KP4]:
                    left_move = True
                elif pressed_keys[K_d] or pressed_keys[K_RIGHT] or \
                        pressed_keys[K_KP6]:
                    right_move = True
                elif pressed_keys[K_w] or pressed_keys[K_UP] or pressed_keys[
                    K_KP8]:
                    up_move = True
                elif pressed_keys[K_s] or pressed_keys[K_DOWN] or pressed_keys[
                    K_KP2]:
                    down_move = True

            # mouse operation
            elif event.type == pygame.MOUSEBUTTONUP:
                map.mousebuttondown = False

            # click to switch status
            elif event.type == pygame.MOUSEBUTTONDOWN:
                map.mousebuttondown = True

                # 开始界面
                if map.game_status == 'start':
                    if if_collidepoint(image.turn_rect_list[0], map.mouse_x,
                                       map.mouse_y):  # click "开始游戏"
                        map.game_status = "gaming"

                        # 根据难度设置格数
                        if map.game_difficulty == '难度:简单':
                            grid1 = 100
                            count = 4
                            grid_spacing = 10
                        elif map.game_difficulty == '难度:普通':
                            grid1 = 68
                            count = 6
                            grid_spacing = 6
                        elif map.game_difficulty == '难度:困难':
                            grid1 = 49.5
                            count = 8
                            grid_spacing = 6
                        grid = [pygame.Surface((grid1, grid1)) for i in
                                range(12)]
                        grid[0].fill((119, 110, 101))
                        grid[1].fill((238, 228, 218))
                        grid[2].fill((238, 225, 201))
                        grid[3].fill((243, 178, 122))
                        grid[4].fill((246, 150, 100))
                        grid[5].fill((247, 124, 95))
                        grid[6].fill((247, 95, 59))
                        grid[7].fill((237, 208, 115))
                        grid[8].fill((237, 204, 98))
                        grid[9].fill((237, 201, 80))
                        grid[10].fill((237, 197, 63))
                        grid[11].fill((237, 194, 46))

                        game_music = './Kojiro chrysanthemum in the summer.mp3'
                        pygame.mixer.music.load(game_music)
                        pygame.mixer.music.play()

                        map_font = pygame.font.Font(None, int(grid1 * 2 / 3))

                        record = 0
                        show(map, screen, grid, grid1, count, grid_spacing,
                             map_font, score_block,
                             time_font, times, record_list[0])
                        map.add(count)
                        map.add(count)
                        times = 0
                        show(map, screen, grid, grid1, count, grid_spacing,
                             map_font, score_block,
                             time_font, times, record_list[0])

                    elif if_collidepoint(image.turn_rect_list[8], map.mouse_x,
                                         map.mouse_y):  # click "游戏规则"
                        map.game_status = 'show_rules'
                    elif if_collidepoint(image.turn_rect_list[10], map.mouse_x,
                                         map.mouse_y):
                        map.change_difficulty()
                    elif if_collidepoint(image.turn_rect_list[9], map.mouse_x,
                                         map.mouse_y):
                        map.game_status = 'record'
                    elif if_collidepoint(image.turn_rect_list[1], map.mouse_x,
                                         map.mouse_y):  # click "退出游戏"
                        sys.exit()

                # 排行榜界面
                elif map.game_status == 'record':
                    map.game_status = "start"

                # 规则界面
                elif map.game_status == 'show_rules':
                    map.game_status = "start"

                # 游戏中
                elif map.game_status == 'gaming':
                    # 返回键
                    if if_collidepoint(image.turn_rect_list[2], map.mouse_x,
                                       map.mouse_y):
                        times_suspend = times
                        map.game_status = 'suspend'

                        pygame.mixer.music.pause()

                    if map.over(count):
                        map.game_status = 'game_over'

                # 暂停状态
                elif map.game_status == 'suspend':
                    if if_collidepoint(image.turn_rect_list[3], map.mouse_x,
                                       map.mouse_y):
                        times = times_suspend
                        map.game_status = "gaming"

                        pygame.mixer.music.unpause()

                    elif if_collidepoint(image.turn_rect_list[4], map.mouse_x,
                                         map.mouse_y):
                        main()
                    elif if_collidepoint(image.turn_rect_list[5], map.mouse_x,
                                         map.mouse_y):
                        sys.exit()

                # 死亡时
                elif map.game_status == 'game_over':
                    map.game_status = 'start'
                    game_music = './petard.wav'
                    pygame.mixer.music.load(game_music)
                    pygame.mixer.music.play()
                # if if_collidepoint(image.turn_rect_list[6], map.mouse_x,
                #                    map.mouse_y):
                #     # main()
                #     map.game_status = "start"
                # elif if_collidepoint(image.turn_rect_list[7], map.mouse_x,
                #                      map.mouse_y):
                #     sys.exit()

        # 绘画
        # image.show_backpic(settings, screen)
        # image.show_white(settings, screen)

        # 游戏中
        if map.game_status == 'gaming':
            if up_move:
                map.moveUp(count)
                up_move = False
            elif down_move:
                map.moveDown(count)
                down_move = False
            elif left_move:
                map.moveLeft(count)
                left_move = False
            elif right_move:
                map.moveRight(count)
                right_move = False
            if (show(map, screen, grid, grid1, count, grid_spacing, map_font,
                     score_block, time_font, times, record_list[0])):
                times_suspend = times
                map.game_status = 'game_over'
            image.show_menu_logo(settings, screen)

        # 开始界面显示
        elif map.game_status == 'start':
            image.show_backpic(settings, screen)

            image.show_font(screen, "开始游戏", [settings.screen_width * 0.11,
                                             settings.screen_height * 0.78],
                            map.mouse_x, map.mouse_y, map)
            image.show_font(screen, "游戏介绍", [settings.screen_width * 0.61,
                                             settings.screen_height * 0.78],
                            map.mouse_x, map.mouse_y, map)
            image.show_font(screen, map.game_difficulty,
                            [settings.screen_width * 0.11,
                             settings.screen_height * 0.88],
                            map.mouse_x, map.mouse_y, map)
            image.show_font(screen, "排行榜", [settings.screen_width * 0.61,
                                            settings.screen_height * 0.88],
                            map.mouse_x, map.mouse_y, map)
            image.show_font(screen, "退出游戏", [settings.screen_width * 0.61,
                                             settings.screen_height * 0.98],
                            map.mouse_x, map.mouse_y, map)

        # 规则界面显示

        elif map.game_status == 'show_rules':
            image.show_rules_pic(screen)

            # 待修改
            # 绘画字
            font = pygame.font.SysFont('SimHei', 25, italic=True)
            s = font.render(('鼠标点击空白处返回'), True, [255, 255, 255])
            turn_rect = s.get_rect()
            turn_rect.bottomleft = [settings.screen_width * 0.51,
                                    settings.screen_height * 1]
            # 绘制
            screen.blit(s, turn_rect)

        # 排行榜界面
        elif map.game_status == 'record':
            image.show_record_pic(screen)
            for i in range(5):
                record_tras = str(record_list[i])
                # if (record_list[i] > 59):
                #    record_tras = str(record_list[i] // 60) + ':' + str(
                #        record_list[i] % 60)
                font = pygame.font.SysFont('SimHei', 35)
                s = font.render(record_tras, True, [0, 0, 0])
                turn_rect = s.get_rect()
                turn_rect.center = [342.5, 138 + 106 * i]
                screen.blit(s, turn_rect)
            font = pygame.font.SysFont('SimHei', 25, italic=True)
            s = font.render(('鼠标点击空白处返回'), True, [0, 191, 255])
            turn_rect = s.get_rect()
            turn_rect.bottomleft = [settings.screen_width * 0.51,
                                    settings.screen_height * 1]
            screen.blit(s, turn_rect)

        if map.game_status == 'game_over':
            if (not (game_2048)):
                image.game_over(settings, screen)
            elif (map.score > record_list[4]):
                image.success(settings, screen)
            else:
                record_list[4] = map.score
                for i in range(4):
                    if (record_list[4 - i] > record_list[3 - i]):
                        record_middle = record_list[3 - i]
                        record_list[3 - i] = record_list[4 - i]
                        record[4 - i] = record_middle
                    else:
                        break
                f = 'record.txt'
                with open(f, 'w') as file:
                    for i in range(5):
                        file.write(str(record[i]) + '\n')
                    file.close()
                map.game_status = 'record'

        if map.game_status == 'suspend':
            image.show_suspend_gray(settings, screen)

            image.show_font(screen, "继续游戏", [settings.screen_width * 0.06,
                                             settings.screen_height * 0.2],
                            map.mouse_x, map.mouse_y, map)

            image.show_font(screen, "退回主菜单", [settings.screen_width * 0.06,
                                              settings.screen_height * 0.35],
                            map.mouse_x, map.mouse_y, map)

            image.show_font(screen, "直接退出", [settings.screen_width * 0.06,
                                             settings.screen_height * 0.5],
                            map.mouse_x, map.mouse_y, map)

        # 特殊光标
        map.show_mouse_point(screen)
        pygame.mouse.set_visible(False)

        # 刷新pygame显示层
        pygame.display.flip()


# 地图的类
class Map:
    def __init__(self, size):
        self.size = size
        self.score = 0
        self.game_status = 'start'
        self.game_difficulty = '难度:简单'
        self.game_over_picture_end = False
        self.mouse_direction = [0, 0]
        self.mousebuttondown = False
        self.map = [[0 for i in range(size)] for i in range(size)]

    def show_mouse_point(self, screen):
        if self.mousebuttondown:
            pic = pygame.image.load('images/小图标/26.bmp')
        else:
            pic = pygame.image.load('images/小图标/25.bmp')
        rect = pic.get_rect()
        rect.center = [self.mouse_x, self.mouse_y]
        screen.blit(pic, rect)

    def death_picture(self, map, player):
        if not self.game_over_picture_end:

            list = [40, 40, 40]
            for i in range(3):
                if player.color[i] >= 40:
                    player.color[i] -= 4
            if player.color[0] <= list[0] and player.color[1] <= list[1] and \
                    player.color[2] <= list[2]:
                self.game_over_picture_end = True

    # 新增2或4，有1/4概率产生4
    def add(self, grid1):
        while True:
            p = random.randint(0, grid1 * grid1 - 1)
            if self.map[int(p / grid1)][p % grid1] == 0:
                x = random.randint(0, 3) > 0 and 2 or 4
                # self.mapint[int(p / self.grid1)][p % self.grid1] =  x
                self.map[int(p / grid1)][p % grid1] = x
                self.score += x
                break

    # 地图向左靠拢，其他方向的靠拢可以通过适当旋转实现，返回地图是否更新
    def adjust(self, grid1):
        changed = False
        for a in self.map:
            b = []
            last = 0
            for v in a:
                if v != 0:
                    if v == last:
                        b.append(b.pop() << 1)
                        last = 0
                    else:
                        b.append(v)
                        last = v
            b += [0] * (grid1 - len(b))
            for i in range(grid1):
                if a[i] != b[i]:
                    changed = True
            a[:] = b
        return changed

    # 逆时针旋转地图90度
    def rotate90(self, grid1):
        self.map = [[self.map[c][r] for c in range(grid1)] for r in
                    reversed(range(grid1))]

    # 判断游戏结束
    def over(self, grid1):
        for r in range(grid1):
            for c in range(grid1):
                if self.map[r][c] == 0:
                    return False
        for r in range(grid1):
            for c in range(grid1 - 1):
                if self.map[r][c] == self.map[r][c + 1]:
                    return False
        for r in range(grid1 - 1):
            for c in range(grid1):
                if self.map[r][c] == self.map[r + 1][c]:
                    return False
        return True

    def moveUp(self, grid1):
        self.rotate90(grid1)
        if self.adjust(grid1):
            self.add(grid1)
        self.rotate90(grid1)
        self.rotate90(grid1)
        self.rotate90(grid1)

    def moveRight(self, grid1):
        self.rotate90(grid1)
        self.rotate90(grid1)
        if self.adjust(grid1):
            self.add(grid1)
        self.rotate90(grid1)
        self.rotate90(grid1)

    def moveDown(self, grid1):
        self.rotate90(grid1)
        self.rotate90(grid1)
        self.rotate90(grid1)
        if self.adjust(grid1):
            self.add(grid1)
        self.rotate90(grid1)

    def moveLeft(self, grid1):
        if self.adjust(grid1):
            self.add(grid1)

    def show_how_many_score(self, screen):
        font = pygame.font.SysFont('SimHei', 45)
        s = font.render(str(self.score), True, [120, 120, 150])
        turn_rect = s.get_rect()
        turn_rect.topright = [390, 10]

    def show_miangame_back(self, screen, record):

        # 记录时间转换
        record_tras = str(record)
        # if (record > 59):
        #    record_tras = str(record // 60) + ':' + str(record % 60)

        # 游戏界面布局
        title = pygame.Surface((180, TITLE))
        time_grid = pygame.Surface((GRID, 55))
        record_grid = pygame.Surface((115, 55))
        regret_grid = pygame.Surface((112, 40))
        grid_back = pygame.Surface((GRID * COUNT + GRID_SPACING * (
                COUNT + 1), GRID * COUNT + GRID_SPACING * (
                                            COUNT + 1)))

        title_font = pygame.font.SysFont('FangSong', 74, bold=True)
        title_text = title_font.render(('2048'), True, [119, 110, 101])
        title_rect = title_text.get_rect()
        title_rect.center = [345, 50]
        screen.blit(title_text, title_rect)

        time_grid.fill((187, 173, 160))
        screen.blit(time_grid, (235, 92.5))
        time_font = pygame.font.SysFont('SimHei', 15)
        time_text = time_font.render(('分数'), True, [238, 228, 218])
        time_rect = time_text.get_rect()
        time_rect.center = [287.5, 105]
        screen.blit(time_text, time_rect)

        record_grid.fill((187, 173, 160))
        screen.blit(record_grid, (345, 92.5))
        record_best_font = pygame.font.SysFont('SimHei', 15)
        record_best_text = record_best_font.render(('最佳'), True,
                                                   [238, 228, 218])
        record_best_rect = record_best_text.get_rect()
        record_best_rect.center = [401.5, 105]
        screen.blit(record_best_text, record_best_rect)
        record_font = pygame.font.SysFont('SimHei', 35)
        record_text = record_font.render(record_tras, True, [255, 255, 255])
        record_rect = record_text.get_rect()
        record_rect.center = [401.5, 130]
        screen.blit(record_text, record_rect)

        tips_font = pygame.font.SysFont('SimHei', 17)
        tips_text = tips_font.render('尽可能达到更高的分数吧！', True, (119, 110, 101))
        tips_rect = tips_text.get_rect()
        tips_rect.bottomleft = [10, 120]
        screen.blit(tips_text, tips_rect)

        tips_font = pygame.font.SysFont('SimHei', 17)
        tips_text = tips_font.render('游戏时间：', True, (119, 110, 101))
        tips_rect = tips_text.get_rect()
        tips_rect.bottomleft = [10, 140]
        screen.blit(tips_text, tips_rect)

        grid_back.fill((187, 173, 160))
        screen.blit(grid_back, (10, 160))

    def change_difficulty(self):
        list = ['难度:简单', '难度:普通', '难度:困难']
        if self.game_difficulty == list[0]:
            self.game_difficulty = list[1]
        elif self.game_difficulty == list[1]:
            self.game_difficulty = list[2]
        elif self.game_difficulty == list[2]:
            self.game_difficulty = list[0]


class Settings():

    def __init__(self):
        # 帧数
        self.fps_number = 85

        # 屏幕大小
        self.screen_width = 470
        self.screen_height = 620


class Image():

    def __init__(self):
        self.turn_rect_list = [i for i in range(20)]

        self.menu_logo_pointed = False

        self.afterimage = [i for i in range(12)]

    def show_backpic(self, settings, screen):
        # 背景
        back_pic = pygame.image.load('images/2048 - backpicture.jpg')
        back_rect = back_pic.get_rect()

        screen.blit(back_pic, [0, 0])

    def show_white(self, settings, screen):
        # 模糊背景

        back_pic = pygame.image.load('images/1.bmp')

        back_rect = back_pic.get_rect()

        screen.blit(back_pic, [0, 0])

    def show_title_pic(self, screen):
        # 背景

        pic = pygame.image.load('images/2048.jpg')
        rect = pic.get_rect()
        rect.center = [100, 100]
        screen.blit(pic, rect)

    def show_record_pic(self, screen):
        # 排行榜
        pic = pygame.image.load('images/record - backpicture.jpg')
        rect = pic.get_rect()
        rect.center = [235, 310]
        screen.blit(pic, rect)

    def show_little_white(self, screen):
        # 死亡时小白框
        pic = pygame.image.load('images/4.bmp')
        rect = pic.get_rect()
        rect.center = [320, 350]
        screen.blit(pic, rect)

    def show_suspend_gray(self, settings, screen):
        # 暂停的灰色背景

        back_pic = pygame.image.load('images/3.bmp')

        back_rect = back_pic.get_rect()

        screen.blit(back_pic, [0, 0])

    def game_over(self, settings, screen):

        back_pic = pygame.image.load('images/game over.bmp')

        back_rect = back_pic.get_rect()

        screen.blit(back_pic, [0, 0])

    def success(self, settings, screen):

        back_pic = pygame.image.load('images/success.bmp')

        back_rect = back_pic.get_rect()

        screen.blit(back_pic, [0, 0])

    def show_menu_logo(self, settings, screen):
        # 返回键
        if self.menu_logo_pointed:
            back_pic = pygame.image.load('images/小图标/1.bmp')
        else:
            back_pic = pygame.image.load('images/小图标/2.bmp')

        back_rect = back_pic.get_rect()

        screen.blit(back_pic, [10, 10])

        self.turn_rect_list[2] = back_rect

    def show_rules_pic(self, screen):
        pic = pygame.image.load('images/rule.bmp')
        rect = pic.get_rect()
        screen.blit(pic, [0, 0])

        # pic = pygame.image.load('images/未分类/2.bmp')
        # rect = pic.get_rect()
        # rect.center = [200, 275]
        # screen.blit(pic, rect)

    def show_font(self, screen, content, font_pos, mouse_x, mouse_y, map):
        # 绘画字

        font = pygame.font.SysFont('SimHei', 35)
        s = font.render((content), True, [0, 0, 0])
        turn_rect = s.get_rect()
        turn_rect.bottomleft = font_pos

        # 碰撞变色
        if if_collidepoint(turn_rect, mouse_x, mouse_y):
            color = [180, 170, 150]
            font_pos[0] += 15
        else:
            color = [100, 100, 100]

        s = font.render((content), True, color)
        turn_rect = s.get_rect()
        turn_rect.bottomleft = font_pos

        # 绘制
        screen.blit(s, turn_rect)

        if content == "开始游戏":
            self.turn_rect_list[0] = turn_rect
        elif content == "退出游戏":
            self.turn_rect_list[1] = turn_rect
        elif content == "继续游戏":
            self.turn_rect_list[3] = turn_rect
        elif content == "退回主菜单":
            self.turn_rect_list[4] = turn_rect
        elif content == "直接退出":
            self.turn_rect_list[5] = turn_rect

        elif content == "返回主菜单":
            self.turn_rect_list[6] = turn_rect
        elif content == "结束游戏":
            self.turn_rect_list[7] = turn_rect

        elif content == "游戏介绍":
            self.turn_rect_list[8] = turn_rect
        elif content == "排行榜":
            self.turn_rect_list[9] = turn_rect
        elif content == map.game_difficulty:
            self.turn_rect_list[10] = turn_rect


def if_collidepoint(turn_rect, mouse_x, mouse_y):
    if turn_rect.collidepoint(mouse_x, mouse_y):
        return True


# 更新屏幕
def show(map, screen, grid, grid1, count, grid_spacing, map_font, score_block,
         time_font, times, record):
    game_over = False
    map.show_miangame_back(screen, record)
    for i in range(count):
        for j in range(count):
            if map.map[i][j] == 0:
                screen.blit(grid[0],
                            (SPACING + grid_spacing * (j + 1) + grid1 * j,
                             SPACING + TITLE + TEXT * 2 + grid_spacing * (
                                     i + 1) + grid1 * i))
            elif map.map[i][j] == 2:
                screen.blit(grid[1],
                            (SPACING + grid_spacing * (j + 1) + grid1 * j,
                             SPACING + TITLE + TEXT * 2 + grid_spacing * (
                                     i + 1) + grid1 * i))
            elif map.map[i][j] == 4:
                screen.blit(grid[2],
                            (SPACING + grid_spacing * (j + 1) + grid1 * j,
                             SPACING + TITLE + TEXT * 2 + grid_spacing * (
                                     i + 1) + grid1 * i))
            elif map.map[i][j] == 8:
                screen.blit(grid[3],
                            (SPACING + grid_spacing * (j + 1) + grid1 * j,
                             SPACING + TITLE + TEXT * 2 + grid_spacing * (
                                     i + 1) + grid1 * i))
            elif map.map[i][j] == 16:
                screen.blit(grid[4],
                            (SPACING + grid_spacing * (j + 1) + grid1 * j,
                             SPACING + TITLE + TEXT * 2 + grid_spacing * (
                                     i + 1) + grid1 * i))
            elif map.map[i][j] == 32:
                screen.blit(grid[5],
                            (SPACING + grid_spacing * (j + 1) + grid1 * j,
                             SPACING + TITLE + TEXT * 2 + grid_spacing * (
                                     i + 1) + grid1 * i))
            elif map.map[i][j] == 64:
                screen.blit(grid[6],
                            (SPACING + grid_spacing * (
                                    j + 1) + grid1 * j,
                             SPACING + TITLE + TEXT * 2 + grid_spacing * (
                                     i + 1) + grid1 * i))
            elif map.map[i][j] == 128:
                screen.blit(grid[7],
                            (SPACING + grid_spacing * (
                                    j + 1) + grid1 * j,
                             SPACING + TITLE + TEXT * 2 + grid_spacing * (
                                     i + 1) + grid1 * i))
            elif map.map[i][j] == 256:
                screen.blit(grid[8],
                            (SPACING + grid_spacing * (
                                    j + 1) + grid1 * j,
                             SPACING + TITLE + TEXT * 2 + grid_spacing * (
                                     i + 1) + grid1 * i))
            elif map.map[i][j] == 512:
                screen.blit(grid[9],
                            (SPACING + grid_spacing * (
                                    j + 1) + grid1 * j,
                             SPACING + TITLE + TEXT * 2 + grid_spacing * (
                                     i + 1) + grid1 * i))
            elif map.map[i][j] == 1024:
                screen.blit(grid[10],
                            (SPACING + grid_spacing * (
                                    j + 1) + grid1 * j,
                             SPACING + TITLE + TEXT * 2 + grid_spacing * (
                                     i + 1) + grid1 * i))
            else:
                screen.blit(grid[11],
                            (
                                SPACING + grid_spacing * (
                                        j + 1) + grid1 * j,
                                SPACING + TITLE + TEXT * 2 + grid_spacing * (
                                        i + 1) + grid1 * i))
            game_2048 = True

            if map.map[i][j] != 0:
                map_text = map_font.render(str(map.map[i][j]), True,
                                           (106, 90, 205))
                text_rect = map_text.get_rect()
                text_rect.center = (
                    SPACING + grid_spacing * (j + 1) + grid1 * j + grid1 / 2,
                    SPACING + TITLE + TEXT * 2 + grid_spacing * (
                            i + 1) + grid1 * i + grid1 / 2)
                screen.blit(map_text, text_rect)

    times_tras = str(times)
    if (times > 59):
        times_tras = str(times // 60) + ':' + str(times % 60)

    times_font = pygame.font.SysFont('SimHei', 35)
    times_text = times_font.render(str(map.score), True, [255, 255, 255])
    times_rect = times_text.get_rect()
    times_rect.center = [287.5, 130]
    screen.blit(times_text, times_rect)

    times_font = pygame.font.SysFont('SimHei', 17)
    times_text = times_font.render(str(times_tras), True, (119, 110, 101))
    times_rect = times_text.get_rect()
    times_rect.bottomleft = [110, 140]
    screen.blit(times_text, times_rect)

    if (map.over(count)):
        return True
    return False



main()
