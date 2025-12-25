# update_ships_simple.py
import json
import os
from pathlib import Path
import urllib.request
import re

def update_ships_json():
    """简单的 ships.json 更新函数"""
    base_path = "renderer/versions"
    # 获取所有版本文件夹
    version_folders = get_all_version_folders(base_path)

    if not version_folders:
        print(f"在 {base_path} 下没有找到版本文件夹")
        return

    print(f"找到的版本文件夹: {version_folders}")

    # 排序并获取最大值
    max_version_str, max_version_parts = sort_and_get_max_version(version_folders)
    print(f"\n最大版本: {max_version_str}")

    # 1. 查找 ships.json
    possible_paths = [
        Path("".join([base_path,'/',max_version_str,'/resources/ships.json'])),
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
    api_url = "https://v3-api.wows.shinoaki.com/public/wows/encyclopedia/wowsMinimapRenderer/ship/transform?server=asia"
    print(f"发送到: {api_url}")

    try:
        json_data = json.dumps(data).encode('utf-8')
        headers = {'Content-Type': 'application/json'}

        req = urllib.request.Request(api_url, data=json_data, headers=headers, method='POST')
        response = urllib.request.urlopen(req)

        result = json.loads(response.read().decode('utf-8'))['data']
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

class Version:
    """自定义版本类，支持 x_y_z 格式的比较"""
    def __init__(self, version_str):
        self.version_str = version_str
        # 将字符串分割成数字列表
        self.parts = tuple(map(int, version_str.split('_')))

    def __lt__(self, other):
        return self.parts < other.parts

    def __eq__(self, other):
        return self.parts == other.parts

    def __repr__(self):
        return f"Version('{self.version_str}')"

def get_all_version_folders(base_path):
    """
    获取base_path下所有符合版本格式的文件夹
    格式要求: 数字_数字_数字 (如 13_5_0)
    """
    versions_dir = Path(base_path)

    if not versions_dir.exists():
        print(f"路径不存在: {base_path}")
        return []

    version_folders = []
    pattern = re.compile(r'^\d+(_\d+)*$')  # 匹配数字_数字_数字格式

    for item in versions_dir.iterdir():
        if item.is_dir() and pattern.match(item.name):
            version_folders.append(item.name)

    return version_folders

def sort_and_get_max_version(version_strings):
    """对版本字符串进行排序并获取最大值"""
    if not version_strings:
        return None

    # 创建Version对象列表
    versions = [Version(v) for v in version_strings]

    # 排序（从小到大）
    sorted_versions = sorted(versions)

    # 获取最大值（最后一个）
    max_version = sorted_versions[-1]

    return max_version.version_str, max_version.parts
