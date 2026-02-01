下面整理了一份**清晰、可扩展、工程化的 YAML DSL 顶层结构表格**，顶层统一使用 `Object`。  
这份表格描述了 **Object 及其子结构（properties、components、children、transform 等）** 的所有字段、含义、类型、是否必填，以及它们在 Unreal 中的语义。

这会成为你 DSL 的“语法基础”。

---

# 🧩 **YAML DSL 顶层结构：`Object` 属性表**

## **1. 顶层 Object（Actor 或 ChildActor 的抽象描述）**

| 字段名 | 类型 | 必须 | 说明 |
|--------|------|------|------|
| `class` | string | ✔ 必须 | Unreal 中要实例化的类（蓝图类或 C++ 类），如 `BP_Tank` |
| `name` | string | ✖ 可选 | 生成的对象名称（不填则自动生成） |
| `transform` | dict | ✖ 可选 | Actor 的位置、旋转、缩放（实际应用到 RootComponent） |
| `properties` | dict | ✖ 可选 | Blueprint Exposed 变量或 C++ UPROPERTY |
| `components` | list | ✖ 可选 | 要附加到 Actor 的组件列表 |
| `children` | list | ✖ 可选 | 子 Actor 列表（递归结构） |
| `attach_to` | string | ✖ 可选 | 如果这是子 Actor，指定附着的组件名 |
| `tags` | list | ✖ 可选 | Actor 标签 |
| `meta` | dict | ✖ 可选 | 元数据（编辑器工具用，不影响游戏逻辑） |

---

# 🧩 **2. transform（应用到 RootComponent 或 SceneComponent）**

| 字段名 | 类型 | 必须 | 说明 |
|--------|------|------|------|
| `location` | [float, float, float] | ✖ | 世界或相对位置 |
| `rotation` | [float, float, float] | ✖ | Pitch/Yaw/Roll |
| `scale` | [float, float, float] | ✖ | 缩放 |

> 注意：Actor 本身没有 Transform，这些值会自动应用到 RootComponent。

---

# 🧩 **3. properties（Actor 或 Component 的属性）**

| 字段名 | 类型 | 必须 | 说明 |
|--------|------|------|------|
| 任意 key | 任意 | ✖ | 对应 Blueprint 或 C++ 的属性，例如 HP、Speed、MeshPath |

示例：

```yaml
properties:
  HP: 300
  Speed: 120
  Team: "Blue"
```

---

# 🧩 **4. components（组件列表）**

每个组件是一个对象：

| 字段名 | 类型 | 必须 | 说明 |
|--------|------|------|------|
| `type` | string | ✔ 必须 | 组件类，如 `StaticMeshComponent` |
| `name` | string | ✖ | 组件名称 |
| `attach_to` | string | ✖ | 附着到哪个组件（默认 RootComponent） |
| `transform` | dict | ✖ | 组件的相对 Transform |
| `properties` | dict | ✖ | 组件属性，如 mesh、cast_shadow |

示例：

```yaml
components:
  - type: StaticMeshComponent
    name: BodyMesh
    properties:
      mesh: "/Game/Tank/Meshes/TankBody"
```

---

# 🧩 **5. children（子 Actor 列表）**

每个子 Actor 也是一个 `Object`（递归结构）：

| 字段名 | 类型 | 必须 | 说明 |
|--------|------|------|------|
| `Object` | dict | ✔ 必须 | 子 Actor 的完整定义（class、properties、components 等） |

示例：

```yaml
children:
  - Object:
      class: BP_Turret
      name: Turret
      attach_to: BodyMesh
      properties:
        RotationSpeed: 45
```

---

# 🧩 **6. meta（可选元数据）**

用于工具链、编辑器扩展，不影响游戏逻辑。

| 字段名 | 类型 | 必须 | 说明 |
|--------|------|------|------|
| 任意 key | 任意 | ✖ | 例如 author、version、notes |

示例：

```yaml
meta:
  author: EEL
  version: 1.0
```

---

# 🎯 **最终结构示例（完整、规范）**

```yaml
Object:
  class: BP_Tank
  name: Tank_01

  transform:
    location: [0, 0, 100]
    rotation: [0, 0, 0]
    scale: [1, 1, 1]

  properties:
    HP: 300
    Speed: 120
    Armor: 80

  components:
    - type: StaticMeshComponent
      name: BodyMesh
      properties:
        mesh: "/Game/Tank/Meshes/TankBody"

  children:
    - Object:
        class: BP_Turret
        name: Turret
        attach_to: BodyMesh
        properties:
          RotationSpeed: 45
```

---

# 🎉 如果你愿意，我可以继续帮你：

- 生成一份 **正式的 JSON Schema**（可用于自动验证 YAML）  
- 设计 **继承 / Prefab / Override** 机制  
- 写一个 **YAML → Unreal Actor 的 Python 生成器**  
- 设计 **组件自动推断规则**（例如 mesh 自动生成 StaticMeshComponent）  

你想继续扩展哪一部分呢？