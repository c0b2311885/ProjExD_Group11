import pygame as pg
import random

# 初期化
pg.init()

# 画面の設定
screen_width = 800
screen_height = 600
screen = pg.display.set_mode((screen_width, screen_height))
pg.display.set_caption('Random Objects')

# 色の設定
white = (255, 255, 255)

# 現金のクラス
class Item(pg.sprite.Sprite):
    """
    出現する現金のクラス
    現金のグラフィックの違いや価値の違いは今後実装する
    """
    def __init__(self):
        super().__init__()
        self.image = pg.image.load("fig/cash.png")
        self.rect = self.image.get_rect()
        self.rect.x = screen_width
        self.rect.y = random.randint(0, screen_height - self.rect.height)
        self.speed = 10
    
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:  # 画面外に出たら削除
            self.kill()

# スプライトグループの設定
all_sprites = pg.sprite.Group()

# メインループ
running = True

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    # 新しい現金を追加
    if random.randint(0, 20) == 0:  # 低い確率で新しい現金を追加
        item = Item()
        all_sprites.add(item)

    # 画面を白でクリア
    screen.fill(white)

    # スプライトグループの更新と描画
    all_sprites.update()
    all_sprites.draw(screen)

    # 画面の更新
    pg.display.flip()

    # 速度調整
    pg.time.Clock().tick(30)

pg.quit()
