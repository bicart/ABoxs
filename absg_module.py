#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件名：absg_module.py

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
import json
import os
import sys

def create_absg_interface(main_root):
    """创建ABSG接口函数"""

    absg_root = None  # 存储窗口引用

    def show_absg():
        nonlocal absg_root
        if absg_root is None or not absg_root.winfo_exists():
            create_window()
        else:
            absg_root.deiconify()
            absg_root.lift()

    def create_window():
        nonlocal absg_root
        absg_root = tk.Toplevel(main_root)
        absg_root.title("ABoxs-Story&Game")
        absg_root.geometry("700x350")

        # 获取当前目录（适配打包环境）
        if getattr(sys, 'frozen', False):
            # 打包后
            base_dir = sys._MEIPASS
        else:
            # 开发环境
            base_dir = os.path.dirname(os.path.abspath(__file__))

        # ABSG界面代码...
        c1 = tk.Canvas(absg_root, bg="#502f5c")
        h_scrollbar = tk.Scrollbar(
            absg_root, orient="horizontal", command=c1.xview)
        c1.configure(xscrollcommand=h_scrollbar.set)

        content_frame = tk.Frame(c1, bg="#502f5c")
        c1.create_window((0, 0), window=content_frame, anchor="nw")

        content_frame.bind("<Configure>", lambda e: c1.configure(
            scrollregion=c1.bbox("all")))
        c1.bind("<Configure>", lambda e: c1.itemconfig(1, height=e.height))

        c1.pack(side="top", fill="both", expand=True)
        h_scrollbar.pack(side="bottom", fill="x")
        content_frame.configure(width=2300, height=80)

        # 尝试加载配置 - 修正：从data目录加载config2.json
        try:
            # 主要尝试从data目录加载
            config_path = os.path.join(base_dir, "data", "config2.json")
            
            # 如果data目录没有，尝试从当前目录加载（向后兼容）
            if not os.path.exists(config_path):
                config_path = os.path.join(base_dir, "config2.json")
            
            if os.path.exists(config_path):
                print(f"加载ABSG配置文件: {config_path}")
                config = json.load(open(config_path, 'r', encoding='utf-8'))
                labels_config = config["labels"]
                settings = config["settings"]

                for i, label_config in enumerate(labels_config):
                    label_id = label_config["id"]
                    value = label_config["value"]
                    label_name = label_config["name"]

                    suffix = settings["image_suffix_b"] if value == 1 else settings["image_suffix_a"]
                    img_filename = f"{settings['image_prefix']}{label_id}{suffix}.{settings['image_extension']}"
                    
                    # 尝试从img目录加载图片
                    img_path = os.path.join(base_dir, "img", img_filename)
                    
                    # 如果img目录没有，尝试从data/img目录（备用）
                    if not os.path.exists(img_path) and os.path.exists(os.path.join(base_dir, "data", "img")):
                        img_path = os.path.join(base_dir, "data", "img", img_filename)

                    if os.path.exists(img_path):
                        try:
                            image = Image.open(img_path)
                            photo = ImageTk.PhotoImage(image)
                            label = tk.Label(
                                content_frame, image=photo, bg="#502f5c")
                            label.image = photo  # 保持引用
                            label.grid(row=0, column=i, padx=18, pady=(124, 0))

                            name_label = tk.Label(content_frame, text=label_name,
                                                font=("Arial", 12), bg="#502f5c", fg='white')
                            name_label.grid(row=1, column=i, padx=10)
                        except Exception as img_error:
                            print(f"加载图片失败 {img_path}: {img_error}")
                            # 显示文字替代
                            placeholder = tk.Label(content_frame, text=f"[{label_name}]",
                                                 font=("Arial", 12), bg="#502f5c", fg='white')
                            placeholder.grid(row=0, column=i, padx=18, pady=(124, 0))
                            
                            name_label = tk.Label(content_frame, text=label_name,
                                                font=("Arial", 12), bg="#502f5c", fg='white')
                            name_label.grid(row=1, column=i, padx=10)
                    else:
                        # 图片不存在，显示文字替代
                        print(f"图片不存在: {img_path}")
                        placeholder = tk.Label(content_frame, text=f"[{label_name}]",
                                             font=("Arial", 12), bg="#502f5c", fg='white')
                        placeholder.grid(row=0, column=i, padx=18, pady=(124, 0))
                        
                        name_label = tk.Label(content_frame, text=label_name,
                                            font=("Arial", 12), bg="#502f5c", fg='white')
                        name_label.grid(row=1, column=i, padx=10)
            else:
                # 配置文件不存在
                print(f"配置文件不存在: {config_path}")
                error_label = tk.Label(content_frame, 
                                     text="ABSG需要配置文件: data/config2.json",
                                     font=("Arial", 14), bg="#502f5c", fg='yellow')
                error_label.pack(pady=50)
                
        except json.JSONDecodeError as e:
            print(f"配置文件格式错误: {e}")
            error_label = tk.Label(content_frame, text="配置文件格式错误",
                                 font=("Arial", 14), bg="#502f5c", fg='red')
            error_label.pack(pady=50)
        except Exception as e:
            print(f"ABSG加载失败: {e}")
            import traceback
            traceback.print_exc()
            error_label = tk.Label(content_frame, text=f"系统错误: {str(e)}",
                                 font=("Arial", 12), bg="#502f5c", fg='white')
            error_label.pack(pady=50)

    return show_absg