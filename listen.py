from flask import Flask, request
from datetime import datetime
import redis
app = Flask(__name__)
r = redis.StrictRedis(host='106.55.181.114', port=16379, db=0,password='dffg12dghj')
last_processed_time = None
last_nickname = None
time_window = 1  # 时间窗口为 5 秒
@app.route('/forward', methods=['POST'])
def handle_forward_request():
    if request.method == 'POST':
        global last_nickname
        global last_processed_time
        current_time = datetime.now()
        data = request.get_json()  # 获取 POST 请求的 JSON 数据
        if "events" in data and len(data["events"]) > 0 and "content" in data["events"][0]:
            content = data["events"][0]["content"]
        else:
        	content = ""
        nickname=data["events"][0]["nickname"]
        decoded_type=data["events"][0]["decoded_type"]
        if last_nickname==nickname and last_processed_time is not None and (current_time - last_processed_time).seconds < time_window:
            return '重复请求，已忽略'
        key="来了"
        last_processed_time = current_time
        last_nickname = nickname
        if key in content:
            # 将文本加入到队列中
            text = "哟，欢迎"+nickname+"来到直播间"
            r.rpush('text_queue', text.encode('utf-8'))
        elif decoded_type=="like":
            text = "哇，感谢"+nickname+"的大力点赞"
            r.rpush('text_queue', text.encode('utf-8'))
        elif decoded_type=="combogift" or decoded_type=="gift":
            if "爱心" in content:
                text = "嘿，感谢"+nickname+"送的爱心，爱你哟"
            else:
                text = "哇，感谢"+nickname+"送的礼物，爱你哟"
            r.rpush('text_queue', text.encode('utf-8'))
        else:
            print("字符串中不包含指定的子字符串")
        # 在这里处理接收到的数据
        # 示例：打印接收到的数据
        print(data)
        # 返回响应
        return 'POST 请求已接收'

if __name__ == '__main__':
    app.run(port=8000)  # 指定端口号为 8000
