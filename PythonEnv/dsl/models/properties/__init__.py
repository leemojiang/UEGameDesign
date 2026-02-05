# 所有组件的properties文件 在这里注册和定义.

# models/properties/__init__.py
import os
import importlib

# 当前目录
package_dir = os.path.dirname(__file__)

for filename in os.listdir(package_dir):
    if filename.endswith(".py") and filename not in ("__init__.py",):
        module_name = filename[:-3]  # 去掉 .py
        importlib.import_module(f"{__name__}.{module_name}")

print("Component Properties Auto Registered")