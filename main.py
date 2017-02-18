#!/usr/bin/env python
# -*- coding:utf-8 -*-

import pygame
from pygame.locals import *
import os
import sys

SCR_RECT = Rect(0,0,400,400)

vx = 0

#main関数
def main():
    pygame.init()
    screen = pygame.display.set_mode(SCR_RECT.size)
    pygame.display.set_caption(u"ブロック崩し")

    #スプライトグループを作成して登録
    all = pygame.sprite.RenderUpdates()
    Paddle.containers = all
    #パドル作成
    paddle = Paddle()

    #ゲームループ
    clock = pygame.time.Clock()
    while True:
        clock.tick(60)
        screen.fill((0,0,0))

        all.update()
        all.draw(screen)
        pygame.display.update()

        #イベント処理
        for event in pygame.event.get():
            if event.type == QUIT:#終了処理
                pygame.quit()
                sys.exit()

#画像読み込み用関数
def load_image(filename, colorkey=None):
    filename = os.path.join("data", filename)
    try:
        image = pygame.image.load(filename)
    except pygame.error, message:
        print "Cannot load image", filename
        raise SystemExit, message
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

#パドルクラス
class Paddle(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.image,self.rect = load_image("paddle.png")
        self.rect.bottom = SCR_RECT.bottom
    def update(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_RIGHT]:
            self.rect.x += 5;
        elif pressed_keys[K_LEFT]:
            self.rect.x -= 5;
        self.rect.clamp_ip(SCR_RECT)

#起動時処理
if __name__ == "__main__" :
    main()
