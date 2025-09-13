#Aboxs1.0
import tkinter as tk
from PIL import Image, ImageTk
from tkinter.filedialog import askdirectory
import time
from tkinter import messagebox
import glob
import os
import random
import pyautogui
import datetime
# 全局变量保留图像引用（防止被回收）
images = {}

def start_drag(event):
    root._drag_data = {"x": event.x, "y": event.y}

def drag(event):
    new_x = root.winfo_x() + (event.x - root._drag_data["x"])
    new_y = root.winfo_y() + (event.y - root._drag_data["y"])
    root.geometry(f"+{new_x}+{new_y}")

def c1(event):
    print('c1_is_ok')
    pass

    if event.num == 3:  # 检查右键点击事件
        #print('1')
        #root2.deiconify()
        global counter
        counter += 1
        if counter % 2 == 1:
            #print('1')
            root2.deiconify()
            root2.geometry(
                "+{}+{}".format(root.winfo_x(), root.winfo_y() - 230))
        else:
            #print('2')
            root2.withdraw()
            #root3.withdraw()

# 定义通用悬停事件生成函数（高阶函数）
def create_hover_effect(button, normal_img_key, hover_img_key):
    def on_enter(event):
        button.config(image=images[hover_img_key])  # 悬停时切换为增大图片

    def on_leave(event):
        button.config(image=images[normal_img_key])  # 离开时恢复原始图片
    return on_enter, on_leave

#c31工具
def c31():
    root2.withdraw()
    root3.deiconify()
    root3.geometry(
        "+{}+{}".format(root.winfo_x(), root.winfo_y() - 220))

def asd():
    root2.withdraw()
    root3.withdraw()

def exit1():
    os._exit(0)

root = tk.Tk()
counter = 0
root.resizable(False, False)  # 禁止调整大小
root.overrideredirect(True)  # 去掉标题栏和边框
root.attributes('-alpha', 1)  # 设置整个窗口的透明度
root.lift()  #提升窗口到顶层
root.attributes('-topmost', True)  # 设置窗口置顶
root.configure(bg='black')
root.wm_attributes('-transparentcolor', 'black')
#加载动图并进行缩小
gif1 = ".//img/box3_2.png"
#gif1 = ".//img/box2_1.png"
image = Image.open(gif1)
#228,240-114,120
#Image.Resampling.NEAREST (0): 最近邻滤波
#Image.Resampling.LANCZOS (1): Lanczos滤波
#Image.Resampling.BILINEAR (2): 双线性滤波
#Image.Resampling.BICUBIC (3): 双三次插值滤波
#Image.Resampling.BOX (4): 包围盒滤波
#Image.Resampling.HAMMING (5): Hamming窗滤波
# 可以通过将代码中的‘ANTIALIAS’替换为‘BILINEAR’或‘BICUBIC’来解决该问题
#image = image.resize((114, 120), Image.Resampling.BOX)  #电脑python运行不了改成这个
#image = image.resize((200, 200), Image.BOX)
#image = image.resize((135, 135), Image.BOX)
# 去掉上方代码可直接使用原始图像创建PhotoImage对象
photo = ImageTk.PhotoImage(image)
a1 = (tk.Button(root, image=photo, highlightthickness=0, bd=0))
a1.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
root.bind('<Button>', c1)  # 绑定按钮的鼠标点击事件
# root.wm_attributes('-transparentcolor', 'white')
#拖拽功能的实现
root.bind("<Button-1>", start_drag)
root.bind("<B1-Motion>", drag)


#-------root2

#root2 = tk.Tk()
root2 = tk.Toplevel(root)
# 加载图像并存储到全局字典（关键修改）
'''
image_paths = {
    "p21": "./img/aboxs1.png",
    "p211": "./img/aboxs1_1.png",
    "p22": "./img/aboxs2.png",
    "p221": "./img/aboxs2_1.png",
    "p23": "./img/aboxs3.png",
    "p231": "./img/aboxs3_1.png",
    "p24": "./img/aboxs4.png",
    "p241": "./img/aboxs4_1.png"
}
for name, path in image_paths.items():
    img = Image.open(path)
    images[name] = ImageTk.PhotoImage(img)  # 存储到全局字典
'''
root2.overrideredirect(True)  # 去掉标题栏和边框
root2.attributes('-alpha', 0.85)
# root2.configure(bg='lightblue')
root2.configure(bg='white')
root2.geometry("258x278")
root2.withdraw()
#l21 = (tk.Label(root2, text='ABoxs', font=("Verdana", 15, "bold"), highlightthickness=0, bd=0, bg='white'))
l21 = tk.Label(root2, text='测试', font=("Verdana", 15, "bold"), highlightthickness=0, bd=0, bg='white')
l21.place(relx=0.2, rely=0.1, anchor=tk.CENTER)
l22 = tk.Label(root2, text='bicart', font=("Verdana", 8), highlightthickness=0, bd=0, bg='white')
l22.place(relx=0.5, rely=0.95, anchor=tk.CENTER)
images["exit"] = ImageTk.PhotoImage(Image.open("./img/exit.png"))
images["exit1"] = ImageTk.PhotoImage(Image.open("./img/exit_1.png"))
b25 = tk.Button(root2, image=images["exit"], highlightthickness=0, bd=0,command=exit1)
b25.place(relx=0.93, rely=0.93, anchor=tk.CENTER)
'''
g21 = ".//img/aboxs1.png"
g22 = ".//img/aboxs2.png"
g23 = ".//img/aboxs3.png"
g24 = ".//img/aboxs4.png"
g211 = ".//img/aboxs1_1.png"
g221 = ".//img/aboxs2_1.png"
g231 = ".//img/aboxs3_1.png"
g241 = ".//img/aboxs4_1.png"
img21 = Image.open(g21)
img22 = Image.open(g22)
img23 = Image.open(g23)
img24 = Image.open(g24)
img211 = Image.open(g211)
img221 = Image.open(g221)
img231 = Image.open(g231)
img241 = Image.open(g241)
p21 = ImageTk.PhotoImage(img21)
p22 = ImageTk.PhotoImage(img22)
p23 = ImageTk.PhotoImage(img23)
p24 = ImageTk.PhotoImage(img24)

p211 = ImageTk.PhotoImage(img211)
p221 = ImageTk.PhotoImage(img221)
p231 = ImageTk.PhotoImage(img231)
p241 = ImageTk.PhotoImage(img241)
'''
images["p21"] = ImageTk.PhotoImage(Image.open("./img/aboxs1.png"))
images["p211"] = ImageTk.PhotoImage(Image.open("./img/aboxs1_1.png"))
images["p22"] = ImageTk.PhotoImage(Image.open("./img/aboxs2.png"))
images["p221"] = ImageTk.PhotoImage(Image.open("./img/aboxs2_1.png"))
images["p23"] = ImageTk.PhotoImage(Image.open("./img/aboxs3.png"))
images["p231"] = ImageTk.PhotoImage(Image.open("./img/aboxs3_1.png"))
images["p24"] = ImageTk.PhotoImage(Image.open("./img/aboxs4.png"))
images["p241"] = ImageTk.PhotoImage(Image.open("./img/aboxs4_1.png"))
b21 = tk.Button(root2, image=images["p21"], highlightthickness=0, bd=0,command=c31)
b21.place(relx=0.3, rely=0.38, anchor=tk.CENTER)
# 按钮变量为None ： b21 = tk.Button(...).place(...) 中,
# place() 方法会直接放置组件并返回 None ，导致 b21 变量实际为 None 。
# 后续调用 b21.config() 和 b21.bind() 会抛出 AttributeError: 'NoneType' object has no attribute 'config' 。
# b21.config(image=p21)
b22 = tk.Button(root2, image=images["p22"], highlightthickness=0, bd=0)
b22.place(relx=0.7, rely=0.38, anchor=tk.CENTER)
b23 = tk.Button(root2, image=images["p23"], highlightthickness=0, bd=0)
b23.place(relx=0.3, rely=0.75, anchor=tk.CENTER)
b24 = tk.Button(root2, image=images["p24"], highlightthickness=0, bd=0)
b24.place(relx=0.7, rely=0.75, anchor=tk.CENTER)


#------root3-工具
root3 = tk.Toplevel(root)
root3.resizable(False, False)  # 禁止调整大小
root3.attributes('-alpha', 1)  # 设置整个窗口的透明度
#root.attributes('-topmost', True)  # 设置窗口置顶----------2025.6.19
root3.lift() #提升窗口到顶层
root3.configure(bg='black')
root3.geometry("400x500")
root3.title('ABoxs 工具')
#root.wm_attributes('-transparentcolor', 'black')
root3.protocol("WM_DELETE_WINDOW", asd)
l31 = tk.Label(root3, text='ABoxs 工具', font=("Verdana", 15, "bold"), highlightthickness=0,
            bd=0, fg='#4682B4',bg='black').pack()
l32 = tk.Label(root3, text='右键盒子关闭本窗口', highlightthickness=0,
            bd=0, fg='#4682B4',bg='black').pack()
#,command=c31
b31 = tk.Button(root3, text='取色器', font=('', 9),fg='#dfdfdf',
                highlightthickness=0, bd=0, bg='#4682B4', pady=6).pack(pady=7)
b32 = tk.Button(root3, text='随心记', font=('', 9),fg='#dfdfdf',
                highlightthickness=0, bd=0, bg='#4682B4', pady=6).pack(pady=7)
b33 = tk.Button(root3, text='时间顺序排序命名文件', font=('', 9),fg='#dfdfdf',
                highlightthickness=0, bd=0, bg='#4682B4', pady=6).pack(pady=7)
root3.withdraw()

#------root31-取色器
root31 = tk.Toplevel(root3)


# 动态绑定所有按钮的事件（假设按钮和图片键存在对应关系）
buttons_info = [
    (b21, "p21", "p211"),   # (按钮对象, 正常图片键, 悬停图片键)
    (b22, "p22", "p221"),
    (b23, "p23", "p231"),
    (b24, "p24", "p241"),
    (b25, "exit", "exit1"),
]
for btn, normal_key, hover_key in buttons_info:
    enter_func, leave_func = create_hover_effect(btn, normal_key, hover_key)
    btn.bind("<Enter>", enter_func)
    btn.bind("<Leave>", leave_func)
root.mainloop()
