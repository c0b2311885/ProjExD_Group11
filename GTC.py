import os
import sys
import pygame as pg

os.chdir(os.path.dirname(os.path.abspath(__file__)))

pg.mixer.init()

class SE:
    def __init__(self):
        """
        SEをロードする初期化
        """
        self.se = pg.mixer.Sound("fig/お金を落とす2.mp3")

    def play_sound(self):
        self.se.play()



def main():
    mt=0
    pg.mixer.music.load("fig/カーチェイス!!.mp3")  # BGMをロード
    pg.mixer.music.play(-1) 
    pg.display.set_caption("はばたけ！こうかとん")
    screen = pg.display.set_mode((800, 600))
    clock  = pg.time.Clock()
    bg_img = pg.image.load("fig/pg_bg.jpg")
    bg_img_2 = pg.transform.flip(bg_img,True,False)
    ko_img = pg.image.load("fig/3.png")
    ko_img = pg.transform.flip(ko_img,True,False)
    ko_rect = ko_img.get_rect() #こうかとんのRect抽出
    ko_rect.center = 300, 200
    tmr = 0
    while True:

        for event in pg.event.get():
            if event.type == pg.QUIT: return
        x = tmr%3200
        screen.blit(bg_img, [-x, 0])
        screen.blit(bg_img_2,[-x+1600,0])
        screen.blit(bg_img, [-x+3200, 0])
        screen.blit(bg_img_2,[-x+4800,0])
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