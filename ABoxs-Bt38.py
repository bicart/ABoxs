#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件名：ABox-Bt38.py

Copyright (C) 2025 @bicart

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import tkinter as tk
from PIL import Image, ImageTk
from tkinter.filedialog import askdirectory
from tkinter import filedialog
import time
from tkinter import messagebox
import glob
import os
import random
import pyautogui
import datetime
import keyboard
import re
import sys
import json
#优化38
# 在ABoxs-Bt38.py顶部导入
# 在文件顶部添加ABSG导入
try:
    from absg_module import create_absg_interface
    ABSG_AVAILABLE = True
    print("ABSG模块加载成功")
except ImportError as e:
    ABSG_AVAILABLE = False
    print(f"ABSG模块不可用: {e}")
except Exception as e:
    ABSG_AVAILABLE = False
    print(f"加载ABSG模块时出错: {e}")

# 全局变量
root = None
root32 = None  # 初始为None，表示尚未创建
#优化37s1
# from datetime import datetime
# 全局变量保留图像引用（防止被回收）
images = {}
# 全局变量（加上_0后缀）
current_frame_0 = 0
loop_count_0 = 0
x_0 = 0
y_0 = 0
frames_000 = []  # 存储000.gif的所有帧
frames_www = []  # 存储WWW.gif的所有帧
frames_qqq = []  # 存储QQQ.gif的所有帧
current_gif_mode = "000"  # "000", "www"
www_played = False
idle_timer = None
last_activity_time = 0
# 全局状态变量-取色器-编号31
is_active = False
root31 = None
result_list = None
status_label = None
status_label2 = None
script_dir = os.path.dirname(os.path.abspath(__file__))
#33
task_entry_33 = None
#filter_var_33 = tk.StringVar(value="all")
task_listbox_33 = None
stats_label_33 = None
data_dir_33 = "data"
data_file_33 = os.path.join(data_dir_33, "todo_items.json")
# 确保data目录存在-33-to_do_list-todo_items.json
if not os.path.exists(data_dir_33):
    os.makedirs(data_dir_33)

# 时间获取模块
# 获取当前时间
now = datetime.datetime.now()
# 获取当前时间的小时数
hour = now.hour
day = now.day
data_tan1 = os.path.join(script_dir, 'data')
file_path_tan1 = os.path.join(data_tan1, 'tan1.txt')
day=str(day)
with open(file_path_tan1, "r") as file:
    tan1 = file.read()
if tan1 == day:
    pass
else:
    with open("tan1.txt", "w") as file:
        file.write(day)
    # 弹窗出现（本来是隐藏的）

def start_drag(event):
    root._drag_data = {"x": event.x, "y": event.y}

def drag(event):
    new_x = root.winfo_x() + (event.x - root._drag_data["x"])
    new_y = root.winfo_y() + (event.y - root._drag_data["y"])
    root.geometry(f"+{new_x}+{new_y}")

def c1(event):
    print('c1_is_ok')
    #pass
    global www_played
    reset_idle_timer()  # 添加这行：重置空闲计时器
    if current_gif_mode != "www" and frames_www:
        switch_to_www()
        www_played = True


    if event.num == 3:  # 检查右键点击事件
        #print('1')
        #root2.deiconify()
        global counter
        counter += 1
        if counter % 2 == 1:
            #print('1')
            root2.deiconify()
            root2.geometry(
                "+{}+{}".format(root.winfo_x(), root.winfo_y() - 260))
        else:
            #print('2')
            root2.withdraw()
            #root3.withdraw()

# 定义通用悬停事件生成函数（高阶函数）
'''
def create_hover_effect(button, normal_img_key, hover_img_key):
    def on_enter(event):
        button.config(image=images[hover_img_key])  # 悬停时切换为增大图片

    def on_leave(event):
        button.config(image=images[normal_img_key])  # 离开时恢复原始图片
    return on_enter, on_leave
'''
def create_hover_effect_safe(button, normal_img_key, hover_img_key):
    """安全的悬停效果函数，避免KeyError"""
    
    def on_enter(event):
        try:
            if hover_img_key in images and images[hover_img_key] is not None:
                button.config(image=images[hover_img_key])
            else:
                print(f"警告: 图片键 '{hover_img_key}' 不存在")
        except Exception as e:
            print(f"悬停效果出错: {e}")
    
    def on_leave(event):
        try:
            if normal_img_key in images and images[normal_img_key] is not None:
                button.config(image=images[normal_img_key])
            else:
                print(f"警告: 图片键 '{normal_img_key}' 不存在")
        except Exception as e:
            print(f"悬停效果出错: {e}")
    
    return on_enter, on_leave
# c31工具
def c31():
    root2.withdraw()
    root3.deiconify()
    root3.geometry(
        "+{}+{}".format(root.winfo_x(), root.winfo_y() - 220))

#c311
def c311():
    root31.deiconify()

# c311-编号31取色器-4def-5def?_更新c32时注
def start_capture():
    global is_active
    is_active = True
    status_label.config(text="状态：已开始")
def stop_capture():
    global is_active
    is_active = False
    status_label.config(text="状态：已停止")
def check_key_press():
    if keyboard.is_pressed('e') and is_active:
        capture_colors()  # 触发采样
    root31.after(100, check_key_press)  # 循环检测按键
#Bt33新增
def get_text_color(hex_color):
    """根据背景色亮度返回合适的文字颜色（黑色或白色）"""
    # 去除#号并转换为RGB
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)

    # 计算亮度（使用常见的亮度公式）
    brightness = (0.299 * r + 0.587 * g + 0.114 * b)

    # 如果亮度低于128，使用白色文字，否则使用黑色文字
    return "white" if brightness < 128 else "black"
def capture_colors():
    # 清空旧记录
    result_list.delete(0, tk.END)
    try:
        # 获取鼠标位置
        x, y = pyautogui.position()
        # 截取3x3区域
        screenshot = pyautogui.screenshot(region=(x-1, y-1, 3, 3))
        colors = screenshot.getcolors(9)  # 获取最多100种颜色
        # 计算并显示结果
        result_list.insert(0, f"坐标:({x},{y}) 3x3区域颜色（共{len(colors)}种）:")
        for count, (r, g, b) in colors:
            hex_color = f"#{r:02x}{g:02x}{b:02x}"
            #result_list.insert(0, f"{hex_color} (出现{count}次)")
            # 创建带颜色块的文本
            color_display = f"  {hex_color} (出现{count}次)"
            index = result_list.size()
            result_list.insert(0, color_display)
            # 设置该项的背景色和文字颜色
            text_color = get_text_color(hex_color)
            result_list.itemconfig(0, {'bg': hex_color, 'fg': text_color})
        # 保持最多10条记录
        if result_list.size() > 10:
            result_list.delete(tk.END)

    except:
        result_list.insert(0, "采样失败：超出屏幕范围或权限不足")


def update_color(event):
    # 获取输入的颜色代码
    color_code = entry.get().strip()
    # 正则验证16进制颜色格式（以#开头，6位十六进制字符）
    pattern = r'^#([A-Fa-f0-9]{6})$'
    if re.match(pattern, color_code):
        # 有效颜色：设置按钮背景色
        color_btn.config(bg=color_code)
        # 根据背景色设置按钮文字颜色
        text_color = get_text_color(color_code)
        color_btn.config(fg=text_color)
        status_label2.config(text="有效颜色", fg="green")
    else:
        # 无效颜色：按钮恢复默认色，显示提示
        color_btn.config(bg="#f0f0f0")  # 默认浅灰色
        if color_code:  # 非空输入时提示错误
            status_label2.config(text="无效颜色格式\n示例：#FF0088", fg="red")
        else:
            status_label2.config(text="")

#c32-弹窗及弹窗设置
# m1歌单启用判断
# m2歌单文件夹路径
# m3选择弹窗背景图片
# m5模式启用判断
# m6模式文件夹路径
# go32，调出32界面，也就是32的设置
def go32():
    root321.withdraw()
    root32.deiconify()
# open=打开，select=选择，folder=文件夹
def open_selected_folder():
    selected_folder = folder_listbox323.get(tk.ACTIVE)
    if selected_folder:
        os.startfile(selected_folder)


def open_selected_folder2():
    selected_folder2 = folder_listbox322.get(tk.ACTIVE)
    if selected_folder2:
        os.startfile(selected_folder2)

# newgd=new歌单


def newgd():
    folder_prefix = "g"  # 文件夹名称的前缀
    folder_count = 1  # 文件夹数量
    # 检查并添加缺失的文件夹
    for i in range(1, folder_count + 1):
        folder_name = f"{folder_prefix}{i}"
        if not os.path.exists(folder_name):
            os.mkdir(folder_name)
            print(f"文件夹 {folder_name} 创建成功！")

    # 查找已存在的文件夹数量，并添加下一个缺失的文件夹
    next_folder_number = folder_count + 1
    while True:
        next_folder_name = f"{folder_prefix}{next_folder_number}"
        if not os.path.exists(next_folder_name):
            os.mkdir(next_folder_name)
            print(f"文件夹 {next_folder_name} 创建成功！")
            break
        next_folder_number += 1
    # print(next_folder_name)
    os.startfile(next_folder_name)
    time.sleep(5)
    messagebox.showinfo(
        "创建新歌单文件夹引导", "现在打开的这个文件夹，就是你的新歌单文件夹，请记住文件夹名为"+next_folder_name+'。现在你可以把音乐放在这个文件夹——'+next_folder_name+'里面了。记得要去自定义歌单中启用。')
    messagebox.showinfo(
        "创建新歌单文件夹引导", '现在请点击一下界面，程序即将重启。')
    os.system('cq.vbs')
    os._exit(0)
# newms=new模式


def newms():
    folder_prefix = "a"  # 文件夹名称的前缀

    folder_count = 1  # 文件夹数量
    # 检查并添加缺失的文件夹
    for i in range(1, folder_count + 1):
        folder_name = f"{folder_prefix}{i}"
        if not os.path.exists(folder_name):
            os.mkdir(folder_name)
            print(f"文件夹 {folder_name} 创建成功！")

    # 查找已存在的文件夹数量，并添加下一个缺失的文件夹
    next_folder_number = folder_count + 1
    while True:
        next_folder_name = f"{folder_prefix}{next_folder_number}"
        if not os.path.exists(next_folder_name):
            os.mkdir(next_folder_name)
            print(f"文件夹 {next_folder_name} 创建成功！")
            break
        next_folder_number += 1
    # print(next_folder_name)
    os.startfile(next_folder_name)
    time.sleep(3)
    messagebox.showinfo(
        "创建新模式文件夹引导", "现在打开的这个文件夹，就是你的新模式文件夹，请记住文件夹名为"+next_folder_name+'。现在你可以把音乐放在这个文件夹——'+next_folder_name+'里面了。记得要去自定义模式中启用。')
    # root3.destroy()
    # root2.deiconify()
    # global folder_listbox
    messagebox.showinfo(
        "创建新模式文件夹引导", '现在请点击一下界面，程序即将重启。')
    os.system('cq.vbs')
    os._exit(0)
# 歌单启用


def gdqy():
    selected_folder = folder_listbox323.get(tk.ACTIVE)
    if selected_folder:
        # print(selected_folder)
        current_dir = os.getcwd()
        combined_path = os.path.join(current_dir, 'g1')
        datam1 = os.path.join(script_dir, 'data')
        file_path1 = os.path.join(datam1, 'm1.txt')
        datam2 = os.path.join(script_dir, 'data')
        file_path2 = os.path.join(datam2, 'm2.txt')
        if selected_folder == combined_path:
            with open("m1.txt", "w") as file:
                file.write("1")
            with open("m2.txt", "w") as file:
                file.write(selected_folder)
        else:
            with open("m1.txt", "w") as file:
                file.write("2")
            with open("m2.txt", "w") as file:
                file.write(selected_folder)

# 模式启用


def msqy():
    selected_folder2 = folder_listbox322.get(tk.ACTIVE)
    if selected_folder2:
        # print(selected_folder)
        current_dir2 = os.getcwd()
        combined_path2 = os.path.join(current_dir2, 'a1')
        datam5 = os.path.join(script_dir, 'data')
        file_path5 = os.path.join(datam5, 'm5.txt')
        datam6 = os.path.join(script_dir, 'data')
        file_path6 = os.path.join(datam6, 'm6.txt')
        if selected_folder2 == combined_path2:
            with open("m5.txt", "w") as file:
                file.write("1")
            with open("m6.txt", "w") as file:
                file.write(selected_folder2)
        else:
            with open("m5.txt", "w") as file:
                file.write("2")
            with open("m6.txt", "w") as file:
                file.write(selected_folder2)


def m3_2():
    datam3 = os.path.join(script_dir, 'data')
    file_path3 = os.path.join(datam3, 'm3.txt')
    with open(file_path3, "w") as file:
        file.write('2')


def m3_1():
    datam3 = os.path.join(script_dir, 'data')
    file_path3 = os.path.join(datam3, 'm3.txt')
    with open(file_path3, "w") as file:
        file.write('1')


def go323():
    root32.withdraw()
    root323.deiconify()


def go322():
    root32.withdraw()
    root322.deiconify()


#bt34
# 33-to_do_list
#c311
def c313():
    root33.deiconify()

def get_tasks_33():
    try:
        if os.path.exists(data_file_33):
            with open(data_file_33, "r", encoding="utf-8") as f_33:
                return json.load(f_33)
    except:
        return []
    return []


def save_tasks_33(tasks_33):
    try:
        with open(data_file_33, "w", encoding="utf-8") as f_33:
            json.dump(tasks_33, f_33, ensure_ascii=False, indent=2)
    except:
        messagebox.showerror("错误", "保存失败!")


def get_filtered_tasks_33(tasks_33):
    filter_type_33 = filter_var_33.get()
    if filter_type_33 == "active":
        return [t for t in tasks_33 if not t["completed"]]
    if filter_type_33 == "completed":
        return [t for t in tasks_33 if t["completed"]]
    return tasks_33


def update_display_33():
    tasks_33 = get_tasks_33()
    display_tasks_33 = get_filtered_tasks_33(tasks_33)

    # 批量更新列表
    task_listbox_33.delete(0, tk.END)
    task_listbox_33.insert(
        0, *[f"✓ {t['text']}" if t["completed"] else t["text"] for t in display_tasks_33])

    # 批量设置颜色
    for i, task_33 in enumerate(display_tasks_33):
        if task_33["completed"]:
            task_listbox_33.itemconfig(i, fg="gray")

    # 更新统计（避免重复计算）
    total_33 = len(tasks_33)
    completed_33 = len([t for t in tasks_33 if t["completed"]])
    stats_label_33.config(
        text=f"总任务: {total_33} | 未完成: {total_33-completed_33} | 已完成: {completed_33}")


def add_task_33(event_33=None):
    task_text_33 = task_entry_33.get().strip()
    if not task_text_33:
        messagebox.showwarning("警告", "任务内容不能为空!")
        return

    tasks_33 = get_tasks_33()
    tasks_33.append({
        "id": datetime.datetime.now().strftime("%Y%m%d%H%M%S%f"),
        "text": task_text_33,
        "completed": False,
        "created_at": datetime.datetime.now().isoformat()
    })
    save_tasks_33(tasks_33)
    task_entry_33.delete(0, tk.END)
    update_display_33()


def modify_task_33(completed_33=None):
    selected_33 = task_listbox_33.curselection()
    if not selected_33:
        return

    tasks_33 = get_tasks_33()
    display_tasks_33 = get_filtered_tasks_33(tasks_33)
    idx_33 = selected_33[0]

    if 0 <= idx_33 < len(display_tasks_33):
        task_id_33 = display_tasks_33[idx_33]["id"]
        for t in tasks_33:
            if t["id"] == task_id_33:
                t["completed"] = not t["completed"] if completed_33 is None else completed_33
                break
        save_tasks_33(tasks_33)
        update_display_33()


def delete_task_33():
    selected_33 = task_listbox_33.curselection()
    if not selected_33 or not messagebox.askyesno("确认", "确定删除所选任务吗?"):
        return

    tasks_33 = get_tasks_33()
    display_tasks_33 = get_filtered_tasks_33(tasks_33)
    idx_33 = selected_33[0]

    if 0 <= idx_33 < len(display_tasks_33):
        task_id_33 = display_tasks_33[idx_33]["id"]
        save_tasks_33([t for t in tasks_33 if t["id"] != task_id_33])
        update_display_33()


def clear_completed_33():
    tasks_33 = get_tasks_33()
    completed_count_33 = len([t for t in tasks_33 if t["completed"]])
    if completed_count_33 > 0 and messagebox.askyesno("确认", f"确定删除{completed_count_33}个已完成任务?"):
        save_tasks_33([t for t in tasks_33 if not t["completed"]])
        update_display_33()

#窗口关闭事件处理
def asd():
    root2.withdraw()
    root3.withdraw()

def asd3():
    root2.withdraw()
    root3.withdraw()
    root31.withdraw()
    root33.withdraw()

def asd321():
    root321.destroy()

def asd32():
    root321.destroy()
    root32.withdraw()

def exit1():
    os._exit(0)

#Bt35-动图的实现
'''
def on_right_click(event):
    """右键点击GIF时打印'1'"""
    print('1')
'''


def reset_idle_timer():
    """重置无操作计时器"""
    global idle_timer, last_activity_time
    last_activity_time = root.tk.call('clock', 'milliseconds')
    if idle_timer:
        root.after_cancel(idle_timer)
    idle_timer = root.after(10000, switch_to_qqq)  # 10秒无操作

def preload_all_gifs():
    """程序启动时预加载所有GIF文件"""
    global frames_000, frames_www, frames_qqq
    print("开始预加载所有GIF文件...")
    # 获取当前脚本所在目录
    f000_dir = os.path.dirname(os.path.abspath(__file__))
    f000_path = os.path.join(f000_dir, "img", "000.gif")
    fwww_dir = os.path.dirname(os.path.abspath(__file__))
    fwww_path = os.path.join(fwww_dir, "img", "WWW.gif")
    fqqq_dir = os.path.dirname(os.path.abspath(__file__))
    fqqq_path = os.path.join(fqqq_dir, "img", "QQQ.gif")
    frames_000 = load_gif_frames(f000_path)
    frames_www = load_gif_frames(fwww_path)
    frames_qqq = load_gif_frames(fqqq_path)
    print("所有GIF文件预加载完成")


def load_gif_frames(gif_path):
    """加载指定GIF的所有帧并返回帧列表"""
    frames = []
    try:
        # 检查文件是否存在
        if not os.path.exists(gif_path):
            print(f"文件不存在: {gif_path}")
            return frames

        gif = Image.open(gif_path)
        total_frames = gif.n_frames

        # 计算等比缩小后的尺寸（原来的75%）
        original_width, original_height = gif.size
        new_width = int(original_width * 0.75)
        new_height = int(original_height * 0.75)

        # 预加载所有帧
        for i in range(total_frames):
            gif.seek(i)
            frame = gif.convert('RGBA')
            resized_frame = frame.resize((new_width, new_height), Image.BOX)
            transparent_frame = Image.new(
                'RGBA', resized_frame.size, (255, 255, 255, 0))
            transparent_frame.paste(resized_frame, (0, 0), resized_frame)
            frames.append(ImageTk.PhotoImage(transparent_frame))

        print(f"已加载 {gif_path}, 帧数: {total_frames}")
        return frames

    except Exception as e:
        print(f"加载GIF失败: {e}")
        return frames


def switch_to_qqq():
    """切换到QQQ.gif"""
    global current_gif_mode, current_frame_0
    if current_gif_mode != "qqq" and frames_qqq:
        current_gif_mode = "qqq"
        current_frame_0 = 0
        print("已切换到QQQ.gif（无操作状态）")
        # 在QQQ模式下也要设置空闲计时器，以便继续检测无操作
        reset_idle_timer()  # 添加这行


def switch_to_www():
    """切换到WWW.gif"""
    global current_gif_mode, current_frame_0, www_played
    if current_gif_mode != "www" and frames_www:
        current_gif_mode = "www"
        current_frame_0 = 0
        www_played = True
        print("切换到WWW.gif")
        if idle_timer:
            root.after_cancel(idle_timer)


def switch_to_000():
    """切换回000.gif"""
    global current_gif_mode, current_frame_0
    if current_gif_mode != "000" and frames_000:
        current_gif_mode = "000"
        current_frame_0 = 0
        print("切换回000.gif")
        reset_idle_timer()  # 添加这行：切换回000后重新开始空闲检测


def get_current_frames():
    """获取当前模式对应的帧列表"""
    if current_gif_mode == "000":
        return frames_000
    elif current_gif_mode == "www":
        return frames_www
    elif current_gif_mode == "qqq":
        return frames_qqq
    return frames_000  # 默认返回000.gif的帧


def start_move(event):
    global x_0, y_0
    x_0 = event.x
    y_0 = event.y
    reset_idle_timer()  # 添加这行：重置空闲计时器
    # 添加这行：如果当前是QQQ模式，立即切换回000
    if current_gif_mode == "qqq":
        switch_to_000()

def on_move(event):
    root = event.widget.master  # 获取根窗口
    new_x = root.winfo_x() + event.x - x_0
    new_y = root.winfo_y() + event.y - y_0
    root.geometry(f"+{new_x}+{new_y}")
    reset_idle_timer()  # 添加这行：重置空闲计时器
    # 添加这行：如果当前是QQQ模式，立即切换回000
    if current_gif_mode == "qqq":
        switch_to_000()


'''
def close_window(event):
    root = event.widget.master  # 获取根窗口
    root.quit()
'''


def animate():
    """动画循环"""
    global current_frame_0, loop_count_0, www_played, current_gif_mode

    # 获取当前GIF的帧列表
    current_frames = get_current_frames()

    # 更新显示的帧
    if current_frames and current_frame_0 < len(current_frames):
        label.configure(image=current_frames[current_frame_0])

    # 检查WWW.gif是否播放完毕
    if current_gif_mode == "www" and www_played and current_frames:
        if current_frame_0 == len(current_frames) - 1:  # 播放到最后一帧
            print("WWW.gif播放完毕，切换回000.gif")
            switch_to_000()
            www_played = False

    # 前进到下一帧
    if current_frames:
        current_frame_0 = (current_frame_0 + 1) % len(current_frames)

    # 设置下一帧的延迟
    if current_gif_mode == "000" and current_frames and current_frame_0 == 1:
        loop_count_0 += 1
        print(f"完成第 {loop_count_0} 轮，等待3秒...")
        root.after(3000, animate)  # 等待3秒
    elif current_gif_mode == "qqq" and current_frames and current_frame_0 == 1:
        # 添加QQQ.gif的循环逻辑，不需要3秒等待
        loop_count_0 += 1
        print(f"QQQ.gif 第 {loop_count_0} 轮")
        root.after(42, animate)  # 标准帧速率
    else:
        root.after(42, animate)  # 标准帧速率


root = tk.Tk()
counter = 0
root.resizable(False, False)  # 禁止调整大小
root.overrideredirect(True)  # 去掉标题栏和边框
root.attributes('-alpha', 1)  # 设置整个窗口的透明度
root.lift()  #提升窗口到顶层
root.attributes('-topmost', True)  # 设置窗口置顶
#Bt35
root.attributes('-transparentcolor', 'white')
root.config(bg='white')
# 预加载所有GIF文件
preload_all_gifs()
'''
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
'''
'''
a1 = (tk.Button(root, image=photo, highlightthickness=0, bd=0))
a1.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
root.bind('<Button>', c1)  # 绑定按钮的鼠标点击事件
# root.wm_attributes('-transparentcolor', 'white')
#拖拽功能的实现
root.bind("<Button-1>", start_drag)
root.bind("<B1-Motion>", drag)
'''
# 加载GIF
'''
gif = Image.open('ala.gif')
total_frames = gif.n_frames
print(f"总帧数: {total_frames}")
# 计算等比缩小后的尺寸（原来的1/2）
original_width, original_height = gif.size
new_width = int(original_width * 0.75)
new_height = int(original_height * 0.75)
print(f"原始尺寸: {original_width}x{original_height}")
print(f"缩小后尺寸: {new_width}x{new_height}")
# 预加载所有帧
'''
'''
for i in range(total_frames):
    gif.seek(i)
    frame = gif.convert('RGBA')
    # 将帧等比缩小至原来的1/2
    resized_frame = frame.resize((new_width, new_height), Image.BOX)
    # 创建白色背景的透明图像
    transparent_frame = Image.new('RGBA', resized_frame.size, (255, 255, 255, 0))
    transparent_frame.paste(resized_frame, (0, 0), resized_frame)
    frames_0.append(ImageTk.PhotoImage(transparent_frame))
'''
# 创建标签显示GIF
label = tk.Label(root, bg='white', bd=0)
label.pack()

# 绑定事件
label.bind('<Button-1>', start_move)      # 左键开始移动
label.bind('<B1-Motion>', on_move)        # 左键拖动移动
label.bind('<Button-3>', c1)  # 右键点击打印'1'
#label.bind('<Double-Button-1>', close_window)  # 双击关闭

# 设置初始位置并开始动画和空闲检测
root.geometry("+500+300")
reset_idle_timer()  # 启动空闲检测
animate()


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
# 获取当前脚本所在目录-25-12-13-Bt38
current_dir = os.path.dirname(os.path.abspath(__file__))
exit_img_path = os.path.join(current_dir, "img", "exit.png")
exit1_img_path = os.path.join(current_dir, "img", "exit_1.png")
#images["exit"] = ImageTk.PhotoImage(Image.open("./img/exit.png"))
#images["exit1"] = ImageTk.PhotoImage(Image.open("./img/exit_1.png"))
images["exit"] = ImageTk.PhotoImage(Image.open(exit_img_path))
images["exit1"] = ImageTk.PhotoImage(Image.open(exit1_img_path))
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

'''
#Bt38

# 修改load_img_compact_box函数：
def load_img_compact_box():
    """简洁版本的图片加载"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    img_dir = os.path.join(base_dir, "img")
    
    # 图片配置列表
    image_configs = [
        ("p21", "aboxs1.png"),
        ("p211", "aboxs1_1.png"),
        ("p22", "aboxs2.png"),
        ("p221", "aboxs2_1.png"),
        ("p23", "aboxs3.png"),
        ("p231", "aboxs3_1.png"),
        ("p24", "aboxs4.png"),
        ("p241", "aboxs4_1.png")
    ]
    
    # 注意：不要创建新的字典，更新全局images
    for key, filename in image_configs:
        img_path = os.path.join(img_dir, filename)
        if os.path.exists(img_path):
            images[key] = ImageTk.PhotoImage(Image.open(img_path))
        else:
            print(f"错误: {filename} 不存在")
            images[key] = None
    
    return images  # 返回更新后的字典

# 调用函数（它会更新现有的images字典）
load_img_compact_box()
'''
images["p21"] = ImageTk.PhotoImage(Image.open("./img/aboxs1.png"))
images["p211"] = ImageTk.PhotoImage(Image.open("./img/aboxs1_1.png"))
images["p22"] = ImageTk.PhotoImage(Image.open("./img/aboxs2.png"))
images["p221"] = ImageTk.PhotoImage(Image.open("./img/aboxs2_1.png"))
images["p23"] = ImageTk.PhotoImage(Image.open("./img/aboxs3.png"))
images["p231"] = ImageTk.PhotoImage(Image.open("./img/aboxs3_1.png"))
images["p24"] = ImageTk.PhotoImage(Image.open("./img/aboxs4.png"))
images["p241"] = ImageTk.PhotoImage(Image.open("./img/aboxs4_1.png"))
'''
b21 = tk.Button(root2, image=images["p21"],
                highlightthickness=0, bd=0, command=c31)
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
root3 = tk.Toplevel(root2)
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
                highlightthickness=0, bd=0, bg='#4682B4', pady=6,command=c311).pack(pady=7)
b32 = tk.Button(root3, text='随心记', font=('', 9),fg='#dfdfdf',
                highlightthickness=0, bd=0, bg='#4682B4', pady=6).pack(pady=7)
b33 = tk.Button(root3, text='待办', font=('', 9),fg='#dfdfdf',
                highlightthickness=0, bd=0, bg='#4682B4', pady=6,command=c313).pack(pady=7)
b34 = tk.Button(root3, text='时间顺序排序命名文件', font=('', 9),fg='#dfdfdf',
                highlightthickness=0, bd=0, bg='#4682B4', pady=6).pack(pady=7)
root3.withdraw()
#25-12-14-Bt38
# 在root3创建后添加以下代码（大约在创建b34按钮之后）

# 添加ABSG按钮（如果可用）
if ABSG_AVAILABLE:
    try:
        show_absg_func = create_absg_interface(root)  # 传入主窗口作为父窗口
        
        b35 = tk.Button(root3, text='成就故事', font=('', 9), fg='#dfdfdf',
                       highlightthickness=0, bd=0, bg='#4682B4', 
                       pady=6, command=show_absg_func)
        b35.pack(pady=7)
        print("ABSG按钮已添加到界面")
    except Exception as e:
        print(f"初始化ABSG功能失败: {e}")
        import traceback
        traceback.print_exc()
    b35.pack(pady=7)
#------root31-取色器
root31 = tk.Toplevel(root3)
root31.resizable(False, False)  # 禁止调整大小
root31.attributes('-alpha', 1)  # 设置整个窗口的透明度
# root.attributes('-topmost', True)  # 设置窗口置顶----------2025.6.19
root31.lift()  # 提升窗口到顶层
root31.configure(bg='white')
root31.geometry("400x500")
root31.title('ABoxs 工具-取色器')
# root.wm_attributes('-transparentcolor', 'black')
root31.protocol("WM_DELETE_WINDOW", asd3)
root31.withdraw()
# 31控制按钮框架
control_frame = tk.Frame(root31)
control_frame.pack(pady=10)

# 31开始/停止按钮
# b3t1，指button3,tool1
b3t11 = tk.Button(control_frame, text="开始",
                  highlightthickness=0, bd=0, command=start_capture)
b3t11.pack(side=tk.LEFT, padx=20)
b3t12 = tk.Button(control_frame, text="停止",
                  highlightthickness=0, bd=0, command=stop_capture)
b3t12.pack(side=tk.LEFT, padx=20)
# 31状态标签
status_label = tk.Label(control_frame, text="状态：未开始")
status_label.pack(side=tk.LEFT, padx=20)
# 31取色结果列表
result_frame = tk.Frame(root31,bg="white")
result_frame.pack(pady=10, fill=tk.BOTH, expand=True)
tk.Label(result_frame, text="取色记录:",bg="white").pack(anchor=tk.W)
result_list = tk.Listbox(result_frame, height=8)
result_list.pack(fill=tk.BOTH, expand=True)
# 31启动按键检测循环（替代<KeyPress-e>绑定）
check_key_press()
# ------
# 输入框区域
input_frame = tk.Frame(root31, padx=10, pady=10)
input_frame.pack(fill="x")

# 输入框标签
tk.Label(input_frame, text="输入16进制颜色（如#FF0088）：").grid(
    row=0, column=0, sticky="w")

# 输入框（绑定键盘释放事件）
entry = tk.Entry(input_frame, width=12)
entry.grid(row=1, column=0, sticky="w")
entry.bind("<KeyRelease>", update_color)  # 输入时实时更新

# 状态提示标签
status_label2 = tk.Label(input_frame, text="", fg="red")
status_label2.grid(row=1, column=1, padx=10, sticky="w")

# 颜色显示按钮
color_btn = tk.Button(root31, text="颜色预览", width=20, height=2)
color_btn.pack(pady=5)
color_btn.config(bg="#f0f0f0", fg="black")  # 初始默认色和黑色文字

# ------root32-#c32-弹窗及弹窗设置
# 设置
if root32 is None:
    print("第一次创建root32...")
    root32 = tk.Toplevel(root)
    #create_root2()
    #root2.deiconify()  # 显示窗口
    #return
#root32 = tk.Toplevel(root)
# 弹窗
root321 = tk.Toplevel(root32)
root322 = tk.Toplevel(root32)
root323 = tk.Toplevel(root32)


root32.protocol("WM_DELETE_WINDOW", asd32)
root321.protocol("WM_DELETE_WINDOW", asd321)
root322.protocol("WM_DELETE_WINDOW", asd32)
root323.protocol("WM_DELETE_WINDOW", asd32)
root32.withdraw()
root322.withdraw()
root323.withdraw()
# root.protocol("WM_DELETE_WINDOW", hide_window)
# 根据时间范围输出相应的信息
if 6 <= hour < 12:
    b = "早上好,又是元气满满的一天:)"
elif 12 <= hour < 18:
    b = "下午好"
elif 18 <= hour < 22:
    b = "晚上好,要注意休息:)"
else:
    b = "要注意休息:)"
a = ' '+b
root321.title('ABoxs1.0'+a)

# ----------------
# root.withdraw()
# ----------------
# root2.title('须知')
# messagebox.showinfo('ABoxs', '本程序由bicart制作')
screen_width321 = root321.winfo_screenwidth()
screen_height321 = root321.winfo_screenheight()
window_width321 = 413
window_height321 = 413
window_x_321 = screen_width321 - window_width321 - 20  # 在右边留出一定的边距
window_y_321 = screen_height321 - window_height321 - 100  # 在下边留出一定的边距
root321.geometry(
    f"{window_width321}x{window_height321}+{window_x_321}+{window_y_321}")
root321.overrideredirect(False)

# m3-选择弹窗背景图片
datam3 = os.path.join(script_dir, 'data')
file_path3 = os.path.join(datam3, 'm3.txt')
with open(file_path3, "r") as file:
    content3 = file.read()
#images["p3211"] = ImageTk.PhotoImage(Image.open("./img/xinkong413.png"))
#images["p3212"] = ImageTk.PhotoImage(Image.open("./img/qljs409.png"))
# 根据文件内容进行赋值
'''
if content3 == "1":
    #image321 = Image.open("./img/xinkong413.png")
    l3t211 = tk.Label(root321, image=images["p3211"])
elif content3 == "2":
    #image321 = Image.open("./img/qljs409.png")
    l3t211 = tk.Label(root321, image=images["p3212"])
# image = Image.open("xinkong413.png")
'''
img321_current_dir = os.path.dirname(os.path.abspath(__file__))
img321_path = os.path.join(img321_current_dir, "img", "xinkong413.png")
image321 = Image.open(img321_path)
images["p3211"] = ImageTk.PhotoImage(image321)
l3t211 = tk.Label(root321, image=images["p3211"])
l3t211.pack()
# 获取脚本所在的目录
# script_dir = os.path.dirname(os.path.abspath(__file__))
# 获取脚本所在目录（兼容打包后场景）
# 获取a1文件夹路径（适配Nuitka打包）
if hasattr(sys, 'frozen') and sys.frozen == 'nuitka':
    # 打包后：exe所在目录
    base_dir = os.path.dirname(sys.executable)
else:
    # 未打包：脚本所在目录
    base_dir = os.path.dirname(os.path.abspath(__file__))
folder_path321 = os.path.join(base_dir, 'a1')

# 读取文件（精简版，无try块）
file_names321 = os.listdir(folder_path321)
selected_file321 = random.choice(file_names321)
file_path321 = os.path.join(folder_path321, selected_file321)
with open(file_path321, 'r', encoding='utf-8') as file:
    t321 = file.read()
# print(f"成功读取文件：{selected_file}")
l3t212 = tk.Label(root321, font=('', 10, 'bold'), text=t321,
                  fg='#4682B4', bg='#F3FCFC', highlightthickness=0)
l3t212.config(fg='#4682B4', bg='#F3FCFC')
l3t212.place(relx=0.5, rely=0.45, anchor=tk.CENTER)
# label.configure(background='SystemTransparent')
b3t211 = tk.Button(root321, text='更多模式？去设置', bg='#B0C4DE',fg='white',command=go32)
b3t211.place(relx=0.5, rely=0.84, anchor=tk.CENTER)
# -------root2
root32.geometry("500x600")
root32.configure(bg='#99B9C8')
# root2.configure(bg='black')
l3t221 = tk.Label(root32, font=('Arial', 20, 'bold'),
                  text='ABoxs', fg='#4682B4', bg='#99B9C8')
l3t221.pack()
l3t221.config(fg='#4682B4')
l3t222 = tk.Label(root32, font=('', 13, 'bold'),
                  text='bicart', fg='#4682B4', bg='#99B9C8')
l3t222.pack()
l3t222.config(fg='#4682B4')
l3t223 = tk.Label(root32, font=('12345', 18, 'bold'),
                  text='模式', bg='#99B9C8', fg='#4682B4')
l3t223.pack()

var = tk.IntVar()
o321 = tk.Radiobutton(root32, text="诗词名著(默认)-a1", variable=var,
                      value=1, bg='#99B9C8', fg='#4682B4')
o321.pack()
o322 = tk.Radiobutton(root32, text="心灵鸡汤-a2", variable=var,
                      value=2, bg='#99B9C8', fg='#4682B4')
o322.pack()
o323 = tk.Radiobutton(root32, text="名人名言-a3", variable=var,
                      value=3, bg='#99B9C8', fg='#4682B4')
o323.pack()
l3t224 = tk.Label(root32, font=('', 10, 'bold'),
                  text='点了也没有用的。要去自定义模式中选择启用。', bg='#99B9C8', fg='#4682B4')
l3t224.pack()
datam5 = os.path.join(script_dir, 'data')
# 自动创建data文件夹（若不存在）
# os.makedirs(data_dir, exist_ok=True)
# 最终m5.txt的路径（data文件夹内）
# m5用来判断默认模式有没有启用
file_path5 = os.path.join(datam5, 'm5.txt')
# 打开文本文件并读取内容
with open(file_path5, "r") as file:
    content_m5 = file.read()
# 根据文件内容进行赋值
if content_m5 == "1":
    m5 = '已启用'
elif content_m5 == "2":
    m5 = '未启用'
else:
    m5 = None
b3t221 = tk.Button(root32, text='默认'+'('+m5+')',
                   font=("", 10, 'underline'))
b3t221.pack()
b3t221.config(fg='#F0FFFF', bg='#4682B4', activeforeground="#4682B4")
b3t222 = tk.Button(root32, text='自定义模式', command=go322, fg='#99B9C8',
                   bg='#4682B4', font=("", 10, 'underline'))
b3t222.pack()
b3t222.config(fg='#99B9C8', bg='#4682B4', activeforeground="#4682B4")
l3t225 = tk.Label(root32, font=('', 18, 'bold'),
                  text='歌单', fg='#4682B4', bg='#99B9C8')
l3t225.pack()
# -------m1
b3t223 = tk.Button(root32, text='自定义歌单', command=go323, fg='#99B9C8',
                   bg='#4682B4', font=("", 10, 'underline'))
b3t223.pack()
b3t223.config(fg='#99B9C8', bg='#4682B4', activeforeground="#4682B4")
l3t226 = tk.Label(root32, font=('', 18, 'bold'),
                  text='联动', fg='#4682B4', bg='#99B9C8')
l3t226.pack()
b3t224 = tk.Button(root32, text='默认', command=m3_1, fg='#99B9C8',
                   bg='#4682B4', font=("", 10, 'underline'))
b3t224.pack()
b3t224.config(fg='#99B9C8', bg='#4682B4', activeforeground="#4682B4")
b3t225 = tk.Button(root32, text='千里江山图', command=m3_2, fg='#99B9C8',
                   bg='#4682B4', font=("", 10, 'underline'), activeforeground="#4682B4")
b3t225.pack()
b3t225.config(fg='#99B9C8', bg='#4682B4')
# -------root2
# -------root3
root323.title("选择文件夹")
# root3.geometry("300x300")

folder_listbox323 = tk.Listbox(root323)
folder_listbox323.pack(fill=tk.BOTH, expand=1)

path323 = os.getcwd()  # 获取当前目录
for folder in os.listdir(path323):
    if folder.startswith("g") and os.path.isdir(os.path.join(path323, folder)):
        folder_listbox323.insert(tk.END, os.path.join(path323, folder))
l3t241 = tk.Label(root323, font=('12345', 10, 'bold'),
                  text='"g1"文件夹是默认歌单，请勿修改。')
l3t241.pack()
b3t241 = tk.Button(root323, text="点击创建新的歌单文件夹", command=newgd)
b3t241.pack()
select_button32_1 = tk.Button(
    root323, text="打开选中的文件夹", command=open_selected_folder)
select_button32_1.pack()
datam2 = os.path.join(script_dir, 'data')
file_path2 = os.path.join(datam2, 'm2.txt')
with open(file_path2, "r") as file:
    content_m2 = file.read()
l3t242 = tk.Label(root323, font=('', 10, 'bold'),
                  text='当前歌单文件夹：'+content_m2)
l3t242.pack()
b3t242 = tk.Button(root323, text="启用选中的文件夹作为歌单文件夹", command=gdqy)
b3t242.pack()
# -------root3
# -------root5-root322?
folder_listbox322 = tk.Listbox(root322)
folder_listbox322.pack(fill=tk.BOTH, expand=1)

path322 = os.getcwd()  # 获取当前目录
for folder2 in os.listdir(path322):
    if folder2.startswith("a") and os.path.isdir(os.path.join(path322, folder2)):
        folder_listbox322.insert(tk.END, os.path.join(path322, folder2))
l3t231 = tk.Label(root322, font=('12345', 10, 'bold'),
                  text='"a1"、"a2"、"a3"文件夹都是预置模式，请勿修改。')
l3t231.pack()
b3t231 = tk.Button(root322, text="点击创建新的模式文件夹", command=newms)
b3t231.pack()
select_button32_2 = tk.Button(
    root322, text="打开选中的文件夹", command=open_selected_folder2)
select_button32_2.pack()
datam6 = os.path.join(script_dir, 'data')
file_path6 = os.path.join(datam6, 'm6.txt')
with open(file_path6, "r") as file:
    content_m6 = file.read()
l3t232 = tk.Label(root322, font=('12345', 10, 'bold'),
                  text='当前模式文件夹：'+content_m6)
l3t232.pack()
b3t232 = tk.Button(root322, text="启用选中的文件夹作为模式文件夹", command=msqy)
b3t232.pack()

#-----------------------------------------------------------------------------------------------
#root33
#to-do-list
#c313
# 界面初始化
root33 = tk.Toplevel(root32)
root33.title("ABoxs 待办")
root33.geometry("700x700")
root33.option_add("*Font", ("SimHei", 12))
root33.withdraw()
root33.protocol("WM_DELETE_WINDOW", asd3)
root33.lift() 
filter_var_33 = tk.StringVar(value="all")
# 批量创建界面框架
frames_33 = [tk.Frame(root33, padx=10, pady=10) for _ in range(4)]
frames_33[0].pack(fill=tk.X)
frames_33[1].pack(fill=tk.X)
frames_33[2].pack(fill=tk.BOTH, expand=True)
frames_33[3].pack(fill=tk.X)

# 输入区域
tk.Label(frames_33[0], text="新任务:").pack(side=tk.LEFT)
task_entry_33 = tk.Entry(frames_33[0], width=40)
task_entry_33.pack(side=tk.LEFT, fill=tk.X, expand=True)
tk.Button(frames_33[0], text="添加", command=add_task_33).pack(side=tk.RIGHT)

# 过滤区域
tk.Label(frames_33[1], text="显示:").pack(side=tk.LEFT)
for text, value in [("全部", "all"), ("未完成", "active"), ("已完成", "completed")]:
    tk.Radiobutton(frames_33[1], text=text, variable=filter_var_33,
                   value=value, command=update_display_33).pack(side=tk.LEFT)
tk.Button(frames_33[1], text="清除已完成",
          command=clear_completed_33).pack(side=tk.RIGHT)

# 任务列表
scrollbar_33 = tk.Scrollbar(frames_33[2])
scrollbar_33.pack(side=tk.RIGHT, fill=tk.Y)
task_listbox_33 = tk.Listbox(
    frames_33[2], width=50, height=20, selectmode=tk.SINGLE, yscrollcommand=scrollbar_33.set)
task_listbox_33.pack(fill=tk.BOTH, expand=True)
scrollbar_33.config(command=task_listbox_33.yview)

# 操作按钮
for text, cmd in [("删除所选", delete_task_33), ("标记完成", lambda: modify_task_33(True)), ("标记未完成", lambda: modify_task_33(False))]:
    tk.Button(frames_33[3], text=text, command=cmd).pack(side=tk.LEFT)
stats_label_33 = tk.Label(frames_33[3], text="")
stats_label_33.pack(side=tk.RIGHT)

# 事件绑定
task_entry_33.bind("<Return>", add_task_33)
task_listbox_33.bind("<Double-1>", lambda e: modify_task_33())

# 初始加载
update_display_33()



#-----
#root2.withdraw()
#root_32.deiconify()


# 放在代码最底部
# 动态绑定所有按钮的事件（假设按钮和图片键存在对应关系）
buttons_info = [
    (b21, "p21", "p211"),   # (按钮对象, 正常图片键, 悬停图片键)
    (b22, "p22", "p221"),
    (b23, "p23", "p231"),
    (b24, "p24", "p241"),
    (b25, "exit", "exit1"),
]
#25-12-13-Bt38
for btn, normal_key, hover_key in buttons_info:
    enter_func, leave_func = create_hover_effect_safe(btn, normal_key, hover_key)
    btn.bind("<Enter>", enter_func)
    btn.bind("<Leave>", leave_func)


root.mainloop()
root32.mainloop()
