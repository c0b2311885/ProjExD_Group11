import os
import sys
import pygame as pg
import random 
import time

WIDTH = 800 # ゲームウィンドウの幅
HEIGHT = 600 # ゲームウィンドウの高さ
os.chdir(os.path.dirname(os.path.abspath(__file__)))


class DisplayScore:
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


def check_bound(obj_rct: pg.Rect) -> tuple[bool, bool]:
    """
    オブジェクトが画面内or画面外を判定し，真理値タプルを返す関数
    引数：こうかとんや爆弾，ビームなどのRect
    戻り値：横方向，縦方向のはみ出し判定結果（画面内：True／画面外：False）
    """
    yoko, tate = True, True
    if obj_rct.left < 150 or 300 < obj_rct.right:  # 横幅の移動を制限
        yoko = False
    if obj_rct.top < 0 or 600 < obj_rct.bottom:
        tate = False
    return yoko, tate



class Car(pg.sprite.Sprite):
    """
    主人公のクラス
    引数:主人公の画像のSurface
    衝突時に減るライフを設定する
    """

    delta = {  # 押下キーと移動量の辞書
        pg.K_UP: (0, -1),
        pg.K_DOWN: (0, +1),
        pg.K_LEFT: (-1, 0),
        pg.K_RIGHT: (+1, 0),
    }

    def __init__(self,img:pg.Surface):
        super().__init__()
        self.image = img
        self.rect = self.image.get_rect()
        self.life = 3
        self.inv_time = 500
        self.state = "normal"
        self.rect.center = (200,300)
    
    def update(self,key_list,screen):
        sum_mv = [0,0]
        for k, mv in __class__.delta.items():
            if key_list[k]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        self.rect.move_ip(sum_mv)
        if check_bound(self.rect) != (True,True):
            self.rect.move_ip(-sum_mv[0],-sum_mv[1])
        if self.state != "normal":
            self.image.set_alpha(128)
            if self.inv_time > 0:
                self.inv_time -= 1
            else:
                self.state = "normal"
                self.inv_time = 500
        else:
            self.image.set_alpha(255)
        screen.blit(self.image, self.rect)


class Enemy(pg.sprite.Sprite):
    """
    出現する敵のクラス
    ランダムで出現するなどの処理は今後実装する
    """
    def __init__(self):
        super().__init__()
        self.image = pg.image.load(f"fig/enemy.png")
        self.image = pg.transform.scale(self.image, (150, 100))
        self.image = pg.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect()
        self.rect.x = 800
        self.rect.y = random.randint(0, 600-50)
        self.speed = 2
    
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()


class Item(pg.sprite.Sprite):
    """
    出現する現金のクラス
    現金のグラフィックの違いや価値の違いは今後実装する
    """
    imgs = [pg.image.load(f"fig/cash{i}.png") for i in range(1, 4)]

    def __init__(self):
        super().__init__()
        self.luck = random.randint(1, 100)
        if self.luck < 70:
            self.image = __class__.imgs[2]
            self.score = 1
        elif self.luck < 90:
            self.image = __class__.imgs[1]
            self.score = 10
        else:
            self.image = __class__.imgs[0]
            self.score = 20
        self.image = pg.transform.scale(self.image, (66, 66))
        self.rect = self.image.get_rect()
        self.rect.x = 800
        self.rect.y = random.randint(0, 600-50)
        self.speed = 1
    
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()


class Explosion(pg.sprite.Sprite):
    """
    爆発に関するクラス
    """
    def __init__(self, obj:Enemy, life: int):
        """
        爆弾が爆発するエフェクトを生成する
        引数1 obj：爆発するBombまたは敵機インスタンス
        引数2 life：爆発時間
        """
        super().__init__()
        img = pg.image.load(f"fig/explosion.gif")
        self.imgs = [img, pg.transform.flip(img, 1, 1)]
        self.image = self.imgs[0]
        self.rect = self.image.get_rect(center=obj.rect.center)
        self.life = life

    def update(self):
        """
        爆発時間を1減算した爆発経過時間_lifeに応じて爆発画像を切り替えることで
        爆発エフェクトを表現する
        """
        self.life -= 1
        self.image = self.imgs[self.life//10%2]
        if self.life < 0:
            self.kill()


def main():
    pg.display.set_caption("はばたけ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
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
    ko_img = pg.image.load("fig/3.png")
    car = Car(ko_img)

    emys = pg.sprite.Group()
    exps = pg.sprite.Group()
    emys.add(Enemy())
    tmr = 0
    items = pg.sprite.Group()
    emys = pg.sprite.Group()
    score = 0

    while True:
        display_score = DisplayScore()
        display_score.update()

        for event in pg.event.get():#イベントが起こった時の処理
            if event.type == pg.QUIT: return

        x = tmr%3706#画面がループするようにする処理
        screen.blit(bg_img, [-x, 0])#この一連のブリットで背景がループしても違和感がないようにする。
        screen.blit(bg_img_2,[-x+1853,0])
        screen.blit(bg_img, [-x+3706, 0])
        screen.blit(bg_img_2,[-x+5559,0])
        key_lst = pg.key.get_pressed()#keyごとの処理を行うための下準備
        if tmr % 1000 == 0:
            item = Item()
            items.add(item)
        if tmr % 200 == 0:
            emys.add(Enemy())
        if tmr // 5000 >= 1:
            if tmr % 300 == 0:
                emys.add(Enemy())
        if tmr // 10000 >= 1:
            if tmr % 150 == 0:
                emys.add(Enemy())
        for item in pg.sprite.spritecollide(car, items, True):
            score += item.score
        if len(pg.sprite.spritecollide(car,emys,False)) != 0:
            if car.state == "normal":
                for hit in pg.sprite.spritecollide(car,emys,False):
                    exps.add(Explosion(hit,100))
                car.state = "hit"
                car.life -= 1
                if car.life == 0:
                    big_font = pg.font.Font(None,100)
                    font = pg. font.Font(None,50)
                    image_1 = big_font.render("YOU ARRESTED!!",True,(255,0,0))
                    image_2 = font.render("You returned your cash...",True,(0,0,0))
                    screen.blit(image_1,[100,200])
                    screen.blit(image_2,[190,300])
                    pg.display.update()
                    time.sleep(5)
                    return
        items.update()
        items.draw(screen)
        emys.update()
        emys.draw(screen)
        car.update(key_lst, screen)
        exps.update()
        exps.draw(screen)
        pg.display.update()
        tmr += 1
        clock.tick(200)
    

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
