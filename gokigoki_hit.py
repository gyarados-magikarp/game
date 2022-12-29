import tkinter as tk
import random
from PIL import Image, ImageTk

WINDOW_HEIGHT = 600  # ウィンドウの高さ
WINDOW_WIDTH = 600   # ウィンドウの幅
image_size_h=0#敵画像の高さ
image_size_w=0#敵画像の横幅

HUMAN_Y = 550       # 自機のy座標

BULLET_HEIGHT = 10  # 弾の縦幅
BULLET_WIDTH = 2    # 弾の横幅
BULLET_SPEED = 10   # 弾のスピード(10 ms)




class human:  # 人

    def __init__(self, x, y=HUMAN_Y):
        self.x = x
        self.y = y
        self.draw()
        self.bind()

    def draw(self):
        cv.create_image(
            self.x, self.y, image=human_tkimg, tag="human")

    def bind(self):
        cv.tag_bind("human", "<ButtonPress-3>", self.pressed)
        cv.tag_bind("human", "<Button1-Motion>", self.dragged)

    def pressed(self, event):
        mybullet = MyBullet(event.x, self.y)
        mybullet.draw()
        mybullet.shoot()

    def dragged(self, event):
        dx = event.x - self.x
        self.x, self.y = cv.coords("human")
        cv.coords("human", self.x+dx, self.y)
        self.x = event.x

   

class MyBullet:  # 自分の弾

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self):
        cv.create_rectangle(
            self.x-BULLET_WIDTH, self.y+BULLET_HEIGHT, self.x+BULLET_WIDTH, self.y-BULLET_HEIGHT, fill="blue",tag="bullet")

    def shoot(self):
        if self.y >= 0:
            cv.move("bullet", 0, -BULLET_HEIGHT)
            self.y -= BULLET_HEIGHT
            self.hit()
            root.after(BULLET_SPEED, self.shoot)
    
    def hit(self):
        if Enemy.enemy_x-(image_size_w/2)<=self.x<=Enemy.enemy_x+(image_size_w/2):
            if Enemy.enemy_y-(image_size_h/2)<=self.y<=Enemy.enemy_y+(image_size_h/2):
                cv.destroy()
                cv2 = tk.Canvas(root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg="white")
                label=tk.Label(cv2,text="撃退成功！！",anchor=tk.CENTER,font=("MSゴシック", "40", "bold"),bg="red",fg="white")
                label.place(x=WINDOW_WIDTH/2, y=WINDOW_HEIGHT/2, anchor=tk.CENTER)
                cv2.pack()
                
                

#ゴキブリ
class Enemy:
    enemy_x=0
    enemy_y=0
    def __init__(self,x,y):
        self.x=x
        self.y=y
        Enemy.enemy_x=x
        Enemy.enemy_y=y
        self.draw()

    def draw(self):
        cv.create_image(self.x, self.y, image=gokiburi_tkimg,tag="enemy")
        self.moving()
        

    def moving(self):
        #幅94.高さ67
        self.dx=random.uniform(-50,50)
        self.dy=random.uniform(-50,50)
        Enemy.enemy_x=Enemy.enemy_x+self.dx
        Enemy.enemy_y=Enemy.enemy_y+self.dy
        if WINDOW_WIDTH<Enemy.enemy_x or Enemy.enemy_x<0 or Enemy.enemy_y<0 or (WINDOW_HEIGHT/2)<Enemy.enemy_y:
            Enemy.enemy_x=Enemy.enemy_x-self.dx
            Enemy.enemy_y=Enemy.enemy_y-self.dy
            root.after(100, self.moving)
        else:
            cv.move("enemy",self.dx,self.dy)
            root.after(100, self.moving)



if __name__ == "__main__":
    # 初期描画
    root = tk.Tk()
    root.title("ゴキブリ退治")
    cv = tk.Canvas(root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg="white")
    cv.pack()

    # 画像の読み込み
    human_img = Image.open("human.png")
    human_tkimg = ImageTk.PhotoImage(human_img)
    gokiburi_img = Image.open("gokiburi.png")
    gokiburi_tkimg = ImageTk.PhotoImage(gokiburi_img)
    image_size_w,image_size_h=gokiburi_img.size

    # メニューバー
    menubar = tk.Menu(root)
    root.configure(menu=menubar)
    menubar.add_command(label="逃げる", underline=0, command=root.quit)

    # インスタンス生成
    human(WINDOW_WIDTH//2, HUMAN_Y)

    #ゴキブリ出現
    Enemy(random.uniform(0,600),random.uniform(0,WINDOW_HEIGHT/2))
 
    

    root.mainloop()