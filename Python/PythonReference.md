下面给你一份**可直接使用、结构清晰、带示例代码的 UE Python API Reference（实战版）**，专门针对你关心的：

- 如何用 Python **动态创建 Blueprint**
- 如何 **动态添加 Component**
- 如何 **给 Blueprint 或 Component 设置属性**
- 如何处理 **UE 类型（Struct、Curve、Object、Array、Map）**

这份参考是我根据你当前的载具系统需求特别整理的，风格偏“工程实战”，你可以直接拿去做 YAML→UE 自动生成器。

---

# 📘 UE Python API Reference（实战版）

---

# 1. 创建 Blueprint（Class Blueprint）

```python
import unreal

def create_blueprint(bp_name, parent_class, folder="/Game/Generated"):
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()

    factory = unreal.BlueprintFactory()
    factory.set_editor_property("ParentClass", parent_class)

    bp = asset_tools.create_asset(
        bp_name,
        folder,
        unreal.Blueprint,
        factory
    )
    return bp
```

使用：

```python
bp = create_blueprint("BP_Tank", unreal.Pawn)
```

---

# 2. 获取 Blueprint 的 CDO（默认对象）

Blueprint 的属性必须通过 CDO 设置：

```python
bp_generated_class = bp.generated_class
cdo = bp_generated_class.get_default_object()
```

---

# 3. 动态添加 Component（核心）

UE Python 允许你向 Blueprint 添加组件：

```python
def add_component_to_bp(bp, component_class, name):
    bp_scs = bp.simple_construction_script
    new_node = bp_scs.create_node(component_class, name)
    return new_node
```

示例：

```python
mesh_node = add_component_to_bp(bp, unreal.StaticMeshComponent, "TankBody")
turret_node = add_component_to_bp(bp, unreal.StaticMeshComponent, "TankTurret")
```

---

# 4. 给 Component 设置属性

组件属性通过 SCS Node 的 `component_template` 设置：

```python
mesh_template = mesh_node.get_editor_property("component_template")

mesh_template.set_editor_property(
    "static_mesh",
    unreal.load_asset("/Game/Vehicles/Tank/Mesh.TankBody")
)
```

设置 Transform：

```python
mesh_node.set_editor_property("relative_location", unreal.Vector(0, 0, 0))
mesh_node.set_editor_property("relative_rotation", unreal.Rotator(0, 0, 0))
```

---

# 5. 给 Blueprint CDO 设置属性

例如设置移动速度：

```python
cdo.set_editor_property("max_speed", 40.0)
cdo.set_editor_property("acceleration", 12.0)
```

设置引用：

```python
cdo.set_editor_property(
    "vehicle_mesh",
    unreal.load_asset("/Game/Vehicles/Tank/Mesh.TankBody")
)
```

---

# 6. 设置 UE Struct（例如 FMyWeaponConfig）

假设你有一个 C++ Struct：

```cpp
USTRUCT(BlueprintType)
struct FWeaponConfig
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere)
    float Damage;

    UPROPERTY(EditAnywhere)
    float Reload;
};
```

Python 中这样创建 Struct：

```python
weapon_struct = unreal.WeaponConfig()
weapon_struct.damage = 120
weapon_struct.reload = 4.0

cdo.set_editor_property("main_gun", weapon_struct)
```

---

# 7. 设置数组（TArray）

```python
arr = []
arr.append(unreal.Vector(1, 2, 3))
arr.append(unreal.Vector(4, 5, 6))

cdo.set_editor_property("waypoints", arr)
```

---

# 8. 设置 Map（TMap）

```python
mp = {"MainGun": 120, "MG": 10}
cdo.set_editor_property("weapon_damage_map", mp)
```

---

# 9. 设置 Curve（例如 FRichCurve / UCurveFloat）

## 9.1 创建 CurveFloat 资源

```python
def create_curve_float(name, folder="/Game/Generated"):
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    factory = unreal.CurveFactory()
    return asset_tools.create_asset(name, folder, unreal.CurveFloat, factory)
```

## 9.2 修改 Curve 数据

```python
curve = create_curve_float("TankTorqueCurve")

curve_float = curve.get_editor_property("float_curve")

curve_float.add_key(0.0, 0.0)
curve_float.add_key(100.0, 500.0)
curve_float.add_key(200.0, 300.0)

curve.mark_package_dirty()
```

## 9.3 把 Curve 赋值给 Blueprint

```python
cdo.set_editor_property("torque_curve", curve)
```

---

# 10. 设置 FRichCurve（Struct 版）

如果你的属性是：

```cpp
UPROPERTY(EditAnywhere)
FRichCurve TorqueCurve;
```

Python：

```python
rich_curve = unreal.RichCurve()
rich_curve.add_key(0.0, 0.0)
rich_curve.add_key(100.0, 500.0)

cdo.set_editor_property("torque_curve", rich_curve)
```

---

# 11. 保存资源

```python
unreal.EditorAssetLibrary.save_asset(bp.get_path_name())
```

---

# 📦 最终示例：从 YAML 生成一个载具 Blueprint

```python
import unreal, yaml

config = yaml.safe_load(open("tank.yaml"))

bp = create_blueprint("BP_" + config["name"], unreal.Pawn)
bp_scs = bp.simple_construction_script
cdo = bp.generated_class.get_default_object()

# 添加 Mesh
body_node = add_component_to_bp(bp, unreal.StaticMeshComponent, "Body")
body_template = body_node.get_editor_property("component_template")
body_template.set_editor_property("static_mesh", unreal.load_asset(config["mesh"]))

# 设置移动参数
cdo.set_editor_property("max_speed", config["movement"]["max_speed"])
cdo.set_editor_property("acceleration", config["movement"]["acceleration"])

# 设置武器 Struct
weapon = unreal.WeaponConfig()
weapon.damage = config["weapons"]["main_gun"]["damage"]
weapon.reload = config["weapons"]["main_gun"]["reload"]
cdo.set_editor_property("main_gun", weapon)

# 保存
unreal.EditorAssetLibrary.save_asset(bp.get_path_name())
```

---

# 🎯 你现在拥有的能力

你已经可以：

- 用 Python 自动生成 Blueprint
- 动态添加组件
- 设置组件属性
- 设置 Blueprint 属性
- 设置 Struct / Array / Map
- 设置 Curve / RichCurve
- 完整实现 YAML → UE 自动生成器

这已经是专业团队在做的“数据驱动内容生成”流程。

---

如果你愿意，我可以继续帮你：

- 设计一套 **完整的载具 YAML Schema**
- 写一个 **可直接运行的 UE Python 生成器项目模板**
- 给你画一张 **UML 架构图**（你喜欢 UML）
- 帮你设计 **载具系统的 DataAsset 结构**

你想继续扩展哪一部分呢？