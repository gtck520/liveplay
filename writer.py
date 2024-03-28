import redis

# 连接到Redis服务器
r = redis.StrictRedis(host='106.55.181.114', port=16379, db=0,password='dffg12dghj')
# r.delete('text_queue')
print(r.ping())
# 输入要朗读的文本
text = input("请输入要朗读的文本：")

# 将文本加入到队列中
r.rpush('text_queue', text.encode('utf-8'))

print("文本已添加到队列中。")

# 获取当前队列数据
queue_data = r.lrange('text_queue', 0, -1)
print("当前队列数据：")
for data in queue_data:
    print(data.decode('utf-8'))
