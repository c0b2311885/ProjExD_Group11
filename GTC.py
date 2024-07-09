import os
import sys
import pygame as pg

WIDTH = 800 # ゲームウィンドウの幅
HEIGHT = 600 # ゲームウィンドウの高さ
os.chdir(os.path.dirname(os.path.abspath(__file__)))


class Score:
    """
    現金を集めた数をスコアとして表示するクラス
    """
    def __init__(self):
        self.font = pg.font.Font(None, 50)
        self.color = (0, 0, 255)
        self.value = 0
        self.image = self.font.render(f"Score: {self.value}", 0, self.color)
        self.rect = self.image.get_rect()
        self.rect.center = 100, HEIGHT - 50

    def update(self, screen: pg.Surface):
        self.image = self.font.render(f"Score: {self.value}", 0, self.color)
        screen.blit(self.image, self.rect)


class Enemy(pg.sprite.Sprite):
    """
    出現する敵のクラス
    ランダムで出現するなどの処理は今後実装する
    """
    def __init__(self,img):
        super().__init__()
        self.image = img
        self.rect = self.image.get_rect()


class Item(pg.sprite.Sprite):
    """
    出現する現金のクラス
    現金のグラフィックの違いや価値の違いは今後実装する
    """
    def __init__(self,img):
        super().__init__()
        self.image = img
        self.rect = self.image.get_rect()
        

def main():
    pg.display.set_caption("はばたけ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
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