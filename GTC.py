import os
import sys
import pygame as pg

os.chdir(os.path.dirname(os.path.abspath(__file__)))


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
    def __init__(self,img):
        super().__init__()
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.center = (250,300)


class Item(pg.sprite.Sprite):
    """
    出現する現金のクラス
    現金のグラフィックの違いや価値の違いは今後実装する
    """
    def __init__(self,img):
        super().__init__()
        self.image = img
        self.rect = self.image.get_rect()


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
    screen = pg.display.set_mode((800, 600))
    clock  = pg.time.Clock()
    bg_img = pg.image.load("fig/pg_bg.jpg")
    bg_img_2 = pg.transform.flip(bg_img,True,False)
    ko_img = pg.image.load("fig/3.png")
    car = Car(ko_img)

    emys = pg.sprite.Group()
    exps = pg.sprite.Group()
    en_img = pg.image.load("fig/0.png")
    emys.add(Enemy(en_img))
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

        if len(pg.sprite.spritecollide(car,emys,False)) != 0:
            if car.state == "normal":
                for hit in pg.sprite.spritecollide(car,emys,False):
                    exps.add(Explosion(hit,100))
                car.state = "hit"
                car.life -= 1
                if car.life == 0:
                    return
        

        car.update(key_lst,screen)
        emys.update()
        emys.draw(screen)
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