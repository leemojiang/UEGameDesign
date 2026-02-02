#清理变量并导入UE加载package的环境变量.

for name in list(globals().keys()):
    if name not in ["__builtins__", "__name__", "__doc__"]:
        del globals()[name]
import sys
# 清理模块缓存
for key in list(sys.modules.keys()):
    if key.startswith("dsl."): 
        del sys.modules[key]


import sys
env = "C:\\Users\\LEEL\\Desktop\\UEGameDesign\\PythonEnv\\.venv\\Lib\\site-packages"
if env not in sys.path:
    print("Adding new env to sys.path: ", env)
    sys.path.extend([ env])

env = "C:\\Users\\LEEL\\Desktop\\UEGameDesign\\PythonEnv\\"
if env not in sys.path:
    print("Adding new env to sys.path: ", env)
    sys.path.extend([ env])

import unreal
print("Unreal Engine Python Environment Initialized.")