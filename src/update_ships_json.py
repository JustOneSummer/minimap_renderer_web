# update_ships_simple.py
import json
import os
from pathlib import Path
import urllib.request

def update_ships_json():
    """简单的 ships.json 更新函数"""

    # 1. 查找 ships.json
    possible_paths = [
        Path("renderer/resources/ships.json"),
        ]

    source_path = None
    for path in possible_paths:
        if path.exists():
            source_path = path
            print(f"找到文件: {source_path}")
            break

    if not source_path:
        print("未找到 ships.json 文件")
        return False

    # 2. 读取文件
    try:
        with open(source_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"成功读取 JSON，包含 {len(data)} 个条目")
    except:
        print("UTF-8 读取失败，尝试 GBK")
        with open(source_path, 'r', encoding='gbk') as f:
            data = json.load(f)

    # 3. 发送到 API
    api_url = "https://v3-api.wows.shinoaki.com/public/wows/encyclopedia/wowsMinimapRenderer/ship/transform"
    print(f"发送到: {api_url}")

    try:
        json_data = json.dumps(data).encode('utf-8')
        headers = {'Content-Type': 'application/json'}

        req = urllib.request.Request(api_url, data=json_data, headers=headers, method='POST')
        response = urllib.request.urlopen(req)

        result = json.loads(response.read().decode('utf-8'))
        print(f"API 响应成功")

    except Exception as e:
        print(f"API 请求失败: {e}")
        return False

    # 4. 保存到根目录
    output_path = Path("ships.json")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"保存到: {output_path.absolute()}")
    return True