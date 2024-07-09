import os
import sys
import pygame as pg

os.chdir(os.path.dirname(os.path.abspath(__file__)))


def main():
    pg.display.set_caption("はばたけ！こうかとん")
    screen = pg.display.set_mode((800, 600))
    clock  = pg.time.Clock()
    bg_img = pg.image.load("fig/road4.jpg")#背景の描画
    bg_img_2 = pg.transform.flip(bg_img,True,False)
    ko_img = pg.image.load("fig/car.png")#車の描画
    ko_img = pg.transform.flip(ko_img,True,False)#車の画像の反転
    ko_rect = ko_img.get_rect() #こうかとんのRect抽出
    ko_rect.center = 300, 200
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: return
        x = tmr%3706
        screen.blit(bg_img, [-x, 0])
        screen.blit(bg_img_2,[-x+1853,0])
        screen.blit(bg_img, [-x+3706, 0])
        screen.blit(bg_img_2,[-x+5559,0])
        key_lst = pg.key.get_pressed()
        mx = 0
        my = 0
        if key_lst[pg.K_UP]:
            my = -1
        if key_lst[pg.K_DOWN]:
            my = 1
        if key_lst[pg.K_LEFT]:
            mx = -1
        if key_lst[pg.K_RIGHT]:
            mx = 1
        ko_rect.move_ip((mx,my))
        screen.blit(ko_img, ko_rect) #こうかとんRectの貼り付け

        pg.display.update()
        tmr += 1        
        clock.tick(200)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()