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
但是UE的unreal包是在运行时注入的,所以即使有python环境也无法使用unreal包.解决办法是在python运行时把动依赖路径动态注入进去

```python
import sys 
env = "C:\\Users\\LEEL\\Desktop\\UEGameDesign\\PythonEnv\\.venv\\Lib\\site-packages"
if env not in sys.path:
    sys.path.extend([env])
```