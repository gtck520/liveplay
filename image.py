import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import glob
import time
import threading
import queue
import redis


class ImageHandler:
    def __init__(self, image_label, update_queue):
        self.image_label = image_label
        self.update_queue = update_queue
        self.last_modified = 0
        self.lock = threading.Lock()
        self.redis_conn = redis.StrictRedis(host='106.55.181.114', port=16379, db=0, password='dffg12dghj')
        self.waiting_queue = "makeword"  # 待生成中的图片队列名
        self.generating_queue = "generating_images"  # 生成中的图片队列名

    def update_image(self):
        # 使用原始字符串定义的路径
        folder_path = r"F:\konger\ComfyUI-aki-v1.2\output"
        
        # 使用glob.glob获取文件列表
        pattern = os.path.join(folder_path, "*.jpg")
        jpg_filenames = glob.glob(pattern)
        jpeg_filenames = glob.glob(pattern.replace('.jpg', '.jpeg'))
        png_filenames = glob.glob(pattern.replace('.jpg', '.png'))
        
        # 合并文件列表并去重
        filenames = list(set(jpg_filenames + jpeg_filenames + png_filenames))
        # 规范化所有文件名
        filenames = [os.path.normpath(f) for f in filenames]  
        # 确保文件存在
        valid_filenames = [f for f in filenames if os.path.exists(f)]
        
        if valid_filenames:
            # 使用os.path.getmtime获取最新文件的修改时间
            newest_image = max(valid_filenames, key=os.path.getmtime)
            modified_time = os.path.getmtime(newest_image)
            
            if modified_time > self.last_modified:
                self.last_modified = modified_time
                print(f"图像1: {newest_image}")
                try:
                    # 尝试打开图片
                    with Image.open(newest_image) as image:
                        width, height = image.size
                        aspect_ratio = min(1.0 * self.image_label.winfo_width() / width, 1.0 * self.image_label.winfo_height() / height)
                        new_width = int(width * aspect_ratio)
                        new_height = int(height * aspect_ratio)
                        image = image.resize((new_width, new_height))
                        photo = ImageTk.PhotoImage(image)
                        
                        with self.lock:
                            self.update_queue.put(photo)
                except Image.UnidentifiedImageError as e:
                    print(f"无法识别图像文件: {newest_image}")
                except IOError as e:
                    print(f"无法打开图像文件: {newest_image}")
    def get_waiting_images(self):
        waiting_images = self.redis_conn.lrange(self.waiting_queue, 0, -1)
        return ", ".join([image.decode() for image in waiting_images])

    def get_generating_images(self):
        generating_images = self.redis_conn.lrange(self.generating_queue, 0, -1)
        return ", ".join([image.decode() for image in generating_images])



def update_image_in_main_thread(image_label, update_queue):
    try:
        photo = update_queue.get(block=False)
        image_label.configure(image=photo)
        image_label.image = photo
    except queue.Empty:
        pass
    # 每隔200毫秒检查一次
    image_label.after(200, lambda: update_image_in_main_thread(image_label, update_queue))

def display_subtitle(subtitle_label):
    if not update_queue.empty():
        new_text = update_queue.get()
        subtitle_label.configure(text=new_text)

    subtitle_label.place(relx=0.5, rely=0, anchor="n")
    subtitle_label.after(5000, hide_subtitle, subtitle_label)

def hide_subtitle(subtitle_label):
    subtitle_label.configure(text="")
    subtitle_label.after(5000, display_subtitle, subtitle_label)

def toggle_subtitle(subtitle_label, image_handler):
    # 切换字幕的显示和隐藏
    current_text = subtitle_label.cget("text")
    # print(current_text)
    if current_text == "":
        # 如果当前文本是隐藏文本，则显示新的文本
        waiting_images = image_handler.get_waiting_images()
        generating_images = image_handler.get_generating_images()
        new_text ="正在生成的图片：%s\n等待生成的图片：%s" % (generating_images, waiting_images)
    else:
        # 如果当前文本是显示文本，则隐藏
        new_text = ""

    # 更新标签文本
    subtitle_label.configure(text=new_text)
    # 5秒后再次调用toggle_subtitle函数
    subtitle_label.after(5000, toggle_subtitle, subtitle_label, image_handler)

def check_for_image_update(image_handler, subtitle_label, window):
    subtitle_thread = threading.Thread(target=display_subtitle, args=(subtitle_label,))
    subtitle_thread.start()
    toggle_subtitle(subtitle_label, image_handler)
    while True:
        image_handler.update_image()        
        # 启动字幕切换循环
        
 
# 创建主窗口
root = tk.Tk()
root.title("图片浏览")
root.geometry("512x768")

# 创建标签用于显示图片
image_label = tk.Label(root)
image_label.pack(fill='both', expand=True)

# 文本标签用于显示字幕
subtitle_label = tk.Label(root, text="", fg="black", font=("Arial", 14))
subtitle_label.pack()

# 延迟一段时间，确保窗口显示出来
root.update_idletasks()

# 创建图片处理对象和消息队列
update_queue = queue.Queue()
image_handler = ImageHandler(image_label, update_queue)

# messagebox.showinfo("提醒", "请将图片文件放置在指定的文件夹中，然后启动程序。")

# 启动守护线程和定时器
update_thread = threading.Thread(target=check_for_image_update, args=(image_handler,subtitle_label,root), daemon=True)
update_thread.start()
update_image_in_main_thread(image_label, update_queue)

# 启动主事件循环
root.mainloop()
