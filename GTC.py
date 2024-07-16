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
        """
        音声の再生
        """
        self.se.play()


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
    screen = pg.display.set_mode((800, 600))
    clock  = pg.time.Clock()
    bg_img = pg.image.load("fig/road4.jpg")#背景の描画
    bg_img_2 = pg.transform.flip(bg_img,True,False)
    ko_img = pg.image.load("fig/car.png")#車の描画
    ko_img = pg.transform.flip(ko_img,True,False)#車の画像の反転
    ko_rect = ko_img.get_rect() #車のRect抽出
    ko_rect.center = 300, 200#中央を指定
    tmr = 0
    pg.mixer.music.load("fig\カーチェイス!!.mp3")  # BGMをロード
    pg.mixer.music.play(-1)  # BGMを再生
    while True:
        for event in pg.event.get():#イベントが起こった時の処理
            if event.type == pg.QUIT: return
        x = tmr%3706#画面がループするようにする処理
        screen.blit(bg_img, [-x, 0])#この一連のブリットで背景がループしても違和感がないようにする。
        screen.blit(bg_img_2,[-x+1853,0])
        screen.blit(bg_img, [-x+3706, 0])
        screen.blit(bg_img_2,[-x+5559,0])
        key_lst = pg.key.get_pressed()#keyごとの処理を行うための下準備
        mx = 0#x軸への移動量の初期化
        my = 0#y軸への移動量の初期化
        if key_lst[pg.K_UP]:
            my = -1
        if key_lst[pg.K_DOWN]:
            my = 1
        if key_lst[pg.K_LEFT]:
            mx = -1
        if key_lst[pg.K_RIGHT]:
            mx = 1
        ko_rect.move_ip((mx,my))
        screen.blit(ko_img, ko_rect) #車Rectの貼り付け
        pg.display.update()
        tmr += 1        
        clock.tick(200)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()