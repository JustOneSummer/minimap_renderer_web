# patches.py
import functools
import json
import update_ships_json

def patch_class_method(cls_name, method_name):
    """
    装饰器工厂：用于修补类方法
    """
    def decorator(new_method):
        # 延迟导入，避免循环依赖
        import importlib

        def apply_patch():
            try:
                print("补丁模块已加载，开始应用补丁...")
                if update_ships_json.update_ships_json():
                    print("ships.json ✅ 更新成功")
                else:
                    print("ships.json ❌ 更新失败")
                # 导入目标模块
                module = importlib.import_module('renderer.resman')
                target_class = getattr(module, cls_name)

                # 保存原始方法
                original_method = getattr(target_class, method_name)

                # 包装新方法
                @functools.wraps(original_method)
                def wrapper(self, *args, **kwargs):
                    # 调用新方法，但新方法可以通过 self._original_method 访问原始方法
                    return new_method(self, original_method, *args, **kwargs)

                # 设置包装器
                setattr(target_class, method_name, wrapper)

                # 将原始方法保存在包装器中（可选）
                wrapper._original_method = original_method

                print(f"✅ 已修补 {cls_name}.{method_name}")
                return True

            except Exception as e:
                print(f"❌ 修补失败 {cls_name}.{method_name}: {e}")
                import traceback
                traceback.print_exc()
                return False

        # 立即应用补丁
        apply_patch()
        return new_method

    return decorator

# 定义具体的补丁
@patch_class_method('ResourceManager', 'load_font')
def patched_load_font(self, original_method, filename, path=None, size=12):
    # 调用原始方法
    return original_method(self, "warhelios_bold_zh.ttf", path, size)

@patch_class_method('ResourceManager', 'load_json')
def patched_load_json(self, original_method, filename, path=None):
    if filename == "ships.json":
        key = f"ships.json"
        if cached := self._cache.get(key, None):
            return cached
        ships_path = "ships.json"
        with open(ships_path,'r', encoding='utf-8') as tr:
            data = json.load(tr, object_hook=self.key_converter)
            self._cache[key] = data
            return data
    # 调用原始方法
    return original_method(self, filename, path)

