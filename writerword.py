import tkinter as tk
import redis
import threading
import time

# 连接到 Redis 服务器
r = redis.StrictRedis(host='106.55.181.114', port=16379, db=0, password='dffg12dghj')

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("文字队列")
        
        # 输入框
        self.text_entry = tk.Entry(root)
        self.text_entry.pack()
        
        # 添加按钮
        self.add_button = tk.Button(root, text="添加到队列", command=self.add_to_queue)
        self.add_button.pack()
        
        # 显示队列数据的文本框
        self.queue_data_textbox = tk.Text(root)
        self.queue_data_textbox.pack()

        # 创建线程并启动
        self.input_thread = threading.Thread(target=self.process_input)
        self.queue_thread = threading.Thread(target=self.process_queue)
        self.input_thread.start()
        self.queue_thread.start()

    def add_to_queue(self):
        text = self.text_entry.get()
        
        if text.lower() != "exit":
            # 将文本加入到队列中
            r.rpush('makeword', text.encode('utf-8'))
            print("文本已添加到队列中。")
            
        self.text_entry.delete(0, tk.END)

    def process_input(self):
        while True:
            self.root.update()
            time.sleep(0.1)
            
    def process_queue(self):
        while True:
            # 获取当前队列数据
            queue_data = r.lrange('makeword', 0, -1)
            
            # 清空文本框
            self.queue_data_textbox.delete("1.0", tk.END)
            
            # 显示队列数据
            for data in queue_data:
                self.queue_data_textbox.insert(tk.END, data.decode('utf-8') + "\n")
            
            self.root.update()
            time.sleep(0.1)

# 创建主窗口
root = tk.Tk()
app = App(root)

# 启动主事件循环
root.mainloop()
