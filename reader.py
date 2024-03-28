import redis
import subprocess
import time


r = redis.StrictRedis(host='106.55.181.114', port=16379, db=0,password='dffg12dghj')
voice = "zh-CN-XiaoyiNeural"   
while True:
     # 监听队列，并设置超时时间（单位：秒）
    result = r.blpop('text_queue', timeout=1)
    if result is not None:
        key, message = result
        text = message.decode('utf-8')
        if text.strip():
            print("开始朗读："+text)
            command = ["edge-playback", "--text", text, "--voice", voice]
            subprocess.run(command)
        else:
            print("文本为空，跳过")


    # 在处理完队列中的消息后，可以进行其他操作
    # ...

    time.sleep(0.1)  # 降低循环速率，以免对系统造成过大压力