#!/usr/bin/env python
# -*- coding:utf-8 -*-

import pygame
from pygame.locals import *
import os
import sys

SCR_RECT = Rect(0,0,400,400)

#main関数
def main():
    pygame.init()
    screen = pygame.display.set_mode(SCR_RECT.size)
    pygame.display.set_caption(u"ブロック崩し")

    #スプライトグループを作成して登録
    all = pygame.sprite.RenderUpdates()
    Paddle.containers = all
    Ball.containers = all
    #パドル作成(自動的にspriteに追加)
    paddle = Paddle()
    #ボール作成(自動的にspriteに追加)
    Ball(paddle)

    #ゲームループ
    clock = pygame.time.Clock()
    while True:
        clock.tick(60)
        screen.fill((0,0,0))
        #spriteの更新
        all.update()
        all.draw(screen)
        #画面の更新
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

#ボールクラス
class Ball(pygame.sprite.Sprite):
    SPEED = 5
    def __init__(self,paddle):
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.image,self.rect = load_image("Ball.png")
        self.move_x = self.move_y = 0
        self.paddle = paddle
        self.update = self.start
    def start(self):
        #パドルの中央に配置
        self.rect.centerx = self.paddle.rect.centerx
        self.rect.bottom = self.paddle.rect.top
        #spacekey入力で移動開始
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_SPACE]:
            self.move_x = self.SPEED
            self.move_y = -self.SPEED
            #updateをmoveに変更
            self.update = self.move
    def move(self):
        #ボール移動
        self.rect.centerx += self.move_x
        self.rect.centery += self.move_y
        #衝突の判定
        #左の壁との衝突
        if self.rect.left < SCR_RECT.left:
            self.rect.left = SCR_RECT.left
            self.move_x = -self.move_x
        #右の壁との衝突
        if self.rect.right > SCR_RECT.right:
            self.rect.right = SCR_RECT.right
            self.move_x = -self.move_x
        #上の壁との衝突
        if self.rect.top < SCR_RECT.top:
            self.rect.top = SCR_RECT.top
            self.move_y = -self.move_y
        #パドルとの衝突
        if self.rect.colliderect(self.paddle.rect) and self.move_y > 0:
            self.move_y = -self.move_y
        #画面の下側との衝突(落とした場合)
        if self.rect.top > SCR_RECT.bottom:
            self.update = self.start

#起動時処理
if __name__ == "__main__" :
    main()
