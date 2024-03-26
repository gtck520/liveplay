import redis
import subprocess


r = redis.StrictRedis(host='106.55.181.114', port=16379, db=0,password='123456')
    
while True:
    key, message = r.blpop('text_queue')
    text = message.decode('utf-8')
    import subprocess
    voice = "zh-CN-YunxiNeural"

    if text.strip():  # 检查文本是否为空（删除前后的空白字符后）
        print("开始朗读"+text)
        command = ["edge-playback", "--text", text, "--voice", voice]
        subprocess.run(command)
    else:
        print("文本为空跳过")
