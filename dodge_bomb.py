import math
import random
import sys

import pygame as pg

#練習4
dalta = {
    pg.K_UP: (0,-1),
    pg.K_DOWN: (0,+1),
    pg.K_LEFT: (-1,0),
    pg.K_RIGHT: (+1,0),
}

def check_bound(scr_rct: pg.Rect, obj_rct:pg.Rect) -> tuple[bool, bool]:
    """
    オブジェクトが画面内or画面外を判定し、真理値タプルを返す関数
    引数1：画面SurfaceのRectです
    引数2：こうかとん、または、爆弾SurfaceのRect
    戻り値：横方向、縦方向のはみだし判定結果(画面内：True/画面外：False)
    """
    yoko, tate = True, True
    if obj_rct.left < scr_rct.left or scr_rct.right < obj_rct.right:
        yoko=False
    if obj_rct.top < scr_rct.top or scr_rct.bottom < obj_rct.bottom:
        tate=False
    return yoko,tate

#追加機能4(未完成)
def update_bomb(bomb_rect, kk_rect):
    diff_vec = kk_rect.centerx - bomb_rect.centerx, kk_rect.centery - bomb_rect.centery
    norm = math.sqrt(diff_vec[0] ** 2 + diff_vec[1] ** 2)
    if norm != 0:
        norm_diff_vec = diff_vec[0] / norm, diff_vec[1] / norm
    else:
        norm_diff_vec = 0, 0
    speed = 5
    new_x = bomb_rect.centerx + int(speed * norm_diff_vec[0])
    new_y = bomb_rect.centery + int(speed * norm_diff_vec[1])
    if norm < 500:
        new_x += int(0.5 * speed * norm_diff_vec[0])
        new_y += int(0.5 * speed * norm_diff_vec[1])
    bomb_rect.centerx = new_x
    bomb_rect.centery = new_y
    return bomb_rect,kk_rect


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((1400, 700))
    clock = pg.time.Clock()
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")
    bb_imgs=[]
    kk_img = pg.image.load("ex02/fig/3.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
    bb_img = pg.Surface((20,20))
    pg.draw.circle(bb_img,(255,0,0),(10,10),10)  #練習Ⅰ
    bb_img.set_colorkey((0,0,0))  #練習Ⅰ
    x, y = random.randint(0,1600), random.randint(0,900)  #練習2
    screen.blit(bb_img, [x,y]) #練習2
    vx,vy=+1,+1
    bb_rct = bb_img.get_rect()
    bb_rct.center = x, y
    kk_rct=kk_img.get_rect()  #練習4
    kk_rct.center=900,400  #練習4
    tmr=0




    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return 0

        tmr += 1

        key_lst = pg.key.get_pressed()
        for k, mv in dalta.items():
            if key_lst[k]:
                kk_rct.move_ip(mv)
        if check_bound(screen.get_rect(), kk_rct) != (True, True):
            for k, mv in dalta.items():
                if key_lst[k]:
                    kk_rct.move_ip(-mv[0], -mv[1])

        screen.blit(bg_img, [0, 0])
        screen.blit(kk_img, kk_rct ) #練習4
        bb_rct.move_ip(vx,vy)  #練習3
        yoko, tate = check_bound(screen.get_rect(), bb_rct)
        if not yoko:  #横方向にはみ出ていたら
            vx *= -1
        if not tate:  #縦方向にはみ出ていたら
            vy *= -1
        screen.blit(bb_img, bb_rct)  #練習3
        if kk_rct.colliderect(bb_rct):  #練習6
            return


# 追加機能2
        for r in range(1,11):
            bb_img=pg.Surface((20*r,20*r))
            pg.draw.circle(bb_img,(255,0,0),(10*r,10*r),10*r)
            bb_imgs.append(bb_img)
            bb_img.set_colorkey((0,0,0))
        bb_img=bb_imgs[min(tmr//1000,9)]
        pg.display.update()
        clock.tick(1000)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()