# 坦克游戏设计
我在使用UE5设计一款3D坦克游戏,请根据以下的需求帮我设计一下我的类型和项目架构.

1.使用UE5惯用的命名规范,比如蓝图类型命名为"BP_XXX",接口命名成"IBP_XXX".每一个类型对应一个单独的文件,文件名和类名相同.请规划项目的目录结构,将文件放到对应的路径里面.

2.请使用PlantUML进行描述,并按照如下规则进行设计:

对于继承UE内置类型的class,使用<<>> Stereotype进行标记 比如:
```
    class ArmorComponent <<component>>
    class HealthComponent <<component>>
```

对于数据类型使用 <<config>> 进行标记,并以Data作为类名结尾命名:
```
    class MyWeaponData <<config>>
```

对于Interface,使用interface关键字:
```
    interface IDamageable {
    +ApplyDamage()
    }
```

对于事件系统,Event Dispatcher使用 <<delegate>> 进行标记, 回调函数(handler)的入口点使用<<event>>进行标记,确保delegate使用"OnXXX()"形式命名,handler使用"OnXXXHandler()"命名.
```
    class ArmorComponent {
        <<delegate>> OnHit(hit: HitResult)
        +ProcessHit(hit: HitResult)
    }
    
    class WeaponSystem {
        <<event>> OnHitHandler(hit: HitResult)
    }
    
    WeaponSystem ..> ArmorComponent : binds OnHit
```

3. 请将整体规划,包括具体类型的代码,相应的数据结构代码,文件命名和路径,写入到Index.md文件里面,PlantUML写入到design.puml文件里面.

4. 对这个游戏我目前设想: 对于所有能发射的武器,定义GenericFireArm类型,需要有Projectile发射物.至于后坐力,弹药,散布,瞄准镜,都是对应的模块.被攻击的目标有Armor模块.整体的操作对象是Tank,需要设计它和Controller的关系.我还希望坦克可以做到更复杂的受到攻击效果,比如不同的模块,像是起火,发动机,不能行动之类的问题.

