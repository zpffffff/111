import json

# 读取 JSON 文件
with open("huizhou_traffic_2016.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# 打印前几条数据
print(json.dumps(data[:3], indent=4, ensure_ascii=False))
