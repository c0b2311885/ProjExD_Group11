import os
import sys
import pygame as pg
import random 

os.chdir(os.path.dirname(os.path.abspath(__file__)))

class Car(pg.sprite.Sprite):
    """
    ゲームキャラクター（こうかとん）に関するクラス
    """
    delta = {  # 押下キーと移動量の辞書
        pg.K_UP: (0, -1),
        pg.K_DOWN: (0, +1),
        pg.K_LEFT: (-1, 0),
        pg.K_RIGHT: (+1, 0),
    }

    def __init__(self, img):
        """
        こうかとん画像Surfaceを生成する
        引数1 num：こうかとん画像ファイル名の番号
        引数2 xy：こうかとん画像の位置座標タプル
        """
        super().__init__()
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.center = (200, 300)
        self.hyper_life = 0
    
    def update(self, key_lst: list[bool], screen: pg.Surface):
        sum_mv = [0, 0]
        for k, mv in __class__.delta.items():
            if key_lst[k]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        self.rect.move_ip(sum_mv)
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

def main():
    pg.display.set_caption("はばたけ！こうかとん")
    screen = pg.display.set_mode((800, 600))
    clock  = pg.time.Clock()
    bg_img = pg.image.load("fig/pg_bg.jpg")
    bg_img_2 = pg.transform.flip(bg_img,True,False)
    ko_img = pg.image.load("fig/3.png")
    ko_img = pg.transform.flip(ko_img,True,False)
    car = Car(ko_img)
    tmr = 0
    items = pg.sprite.Group()
    emys = pg.sprite.Group()
    score = 0

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: return
        x = tmr%3200
        screen.blit(bg_img, [-x, 0])
        screen.blit(bg_img_2,[-x+1600,0])
        screen.blit(bg_img, [-x+3200, 0])
        screen.blit(bg_img_2,[-x+4800,0])
        key_lst = pg.key.get_pressed()
        if tmr % 200 == 0:
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
        items.update()
        items.draw(screen)
        emys.update()
        emys.draw(screen)
        car.update(key_lst, screen)
        pg.display.update()
        tmr += 1        
        clock.tick(200)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()