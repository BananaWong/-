import tkinter as tk
from tkinter import filedialog
import cv2
import os
import webbrowser
import numpy as np

def remove_background(input_image_path, output_image_path):
    # 读取图片
    img = cv2.imread(input_image_path)
    if img is None:
        raise ValueError(f"无法加载图像: {input_image_path}")

    # 转换为灰度图像
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 创建一个与原图像相同大小的全黑背景
    background = np.zeros_like(img)

    # 创建掩码，将非黑色区域设置为白色
    _, mask = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)

    # 将掩码转换为BGR格式
    mask_bgr = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

    # 使用掩码将灰度图像放置在黑色背景上
    gray_bgr = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    result = cv2.bitwise_and(gray_bgr, mask_bgr)
    result = cv2.bitwise_or(result, background)

    # 保存处理后的图像为 BMP 格式
    cv2.imwrite(output_image_path, result)

def select_image():
    file_path = filedialog.askopenfilename()
    input_path_label.config(text=file_path)
    return file_path

def process_image():
    try:
        input_path = input_path_label.cget("text")
        output_path = 'output.bmp'  # 将文件保存为 BMP 格式
        remove_background(input_path, output_path)
        output_path_label.config(text=output_path)

        # 获取 output.bmp 的绝对路径
        abs_output_path = os.path.abspath(output_path)
        # 使用默认图片查看器打开图片
        webbrowser.open(abs_output_path)
    except ValueError as e:
        output_path_label.config(text=f"错误: {e}")

def open_remove_bg():
    # 打开 remove.bg 网站
    webbrowser.open("https://www.remove.bg")

root = tk.Tk()
root.title("图像处理工具")

# 选择图像按钮
select_button = tk.Button(root, text="选择图像", command=select_image)
select_button.pack()

# 显示选择的图像路径
input_path_label = tk.Label(root, text="")
input_path_label.pack()

# 处理图像按钮
process_button = tk.Button(root, text="处理图像", command=process_image)
process_button.pack()

# 新增打开 remove.bg 的按钮
remove_bg_button = tk.Button(root, text="打开 remove.bg", command=open_remove_bg)
remove_bg_button.pack()

# 显示处理后的图像路径
output_path_label = tk.Label(root, text="")
output_path_label.pack()

root.mainloop()
