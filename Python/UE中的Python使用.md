## UE中Python环境在哪里?
    UE自带Python环境,
    如果想要安装第三方包,需要往这个环境里面安装"<UE安装目录>/Engine/Binaries/ThirdParty/Python3/Win64/Lib/site-packages/

## VSCode开启UE Python环境?
在Vscode中使用Unreal Engine Python插件.

Unreal Editor
启用这两个插件,并保持编辑器开启：

    Python Editor Script Plugin
    Editor Scripting Utilities
设置里打开:

    Enable Remote Execution


## 如何使用第三方Python包?

如果不想把UE官方的环境搞乱,可以先创建一个虚拟环境:
```bash
    uv venv --python E:\UE_5.7\Engine\Binaries\ThirdParty\Python3\Win64\python.exe --system-site-packages .venv 
    uv init --no-venv
```
但是UE的unreal包是在运行时注入的,所以即使有UE的python环境也无法使用unreal包.解决办法是在python运行时把动依赖路径动态注入进去

```python
import sys 
env = "C:\\Users\\LEEL\\Desktop\\UEGameDesign\\PythonEnv\\.venv\\Lib\\site-packages"
if env not in sys.path:
    sys.path.extend([env])
```

同样的可以把开发路径的也加入进去，这样就可以将正在开发的python代码写成模块并导入：

```python
env = "C:\\Users\\LEEL\\Desktop\\UEGameDesign\\PythonEnv\\"
if env not in sys.path:
    print("Adding new env to sys.path: ", env)
    sys.path.extend([ env])
```

## 清理变量以及导入？
UE的执行环境python环境还有一个问题，它的python环境始终是运行着的，无法像一般处理python脚本一样重启环境来清楚变量，或者重新加载python的模块或者包.这样的话有些模块修改后需要清除缓存并重新导入：

```python
# 清理变量
for name in list(globals().keys()):
    if name not in ["__builtins__", "__name__", "__doc__"]:
        del globals()[name]
import sys
# 清理模块缓存
for key in list(sys.modules.keys()):
    if key.startswith("dsl."): 
        del sys.modules[key]

```
