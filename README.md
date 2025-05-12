# 虚幻引擎Python执行器

这是一个现代化的桌面应用，允许用户从桌面应用向运行中的虚幻引擎发送Python代码，并查看执行结果。该工具特别适合开发者在不重启引擎的情况下快速执行和测试Python脚本。

## 功能特点

- **即时执行** - 无需重启UE即可执行Python脚本
- **现代化界面** - 美观直观的用户界面
- **多标签设计** - 主页、蓝图工具、动画工具等功能分类清晰
- **代码编辑器** - 内置语法高亮和代码编辑功能
- **预设脚本** - 内置多种常用脚本模板
- **连接管理** - 支持多端口连接到虚幻引擎

## 安装与使用

### 环境要求

- Python 3.7或更高版本
- PyQt5
- 虚幻引擎4.26或更高版本（已启用Python支持）

### 快速开始

1. 克隆仓库到本地：
   ```
   git clone https://github.com/你的用户名/虚幻引擎Python执行器.git
   ```

2. 安装依赖：
   ```
   pip install PyQt5
   ```

3. 启动应用：
   ```
   python main.py
   ```

### 在虚幻引擎中设置

1. 确保你的虚幻项目已启用Python支持
2. 添加以下Python脚本到项目的启动脚本或手动在Python控制台执行：
   ```python
   # 这段代码将在虚幻引擎中启动监听服务
   import socket
   import unreal
   import threading
   
   def socket_server():
       sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
       sock.bind(('localhost', 9876))
       sock.listen(1)
       unreal.log("Python执行器服务已启动，监听端口9876")
       
       while True:
           conn, addr = sock.accept()
           data = conn.recv(65536).decode('utf-8')
           if data:
               try:
                   unreal.log("执行Python代码...")
                   exec(data)
                   conn.send("执行成功".encode('utf-8'))
               except Exception as e:
                   error_msg = str(e)
                   unreal.log_error(f"执行错误: {error_msg}")
                   conn.send(f"执行错误: {error_msg}".encode('utf-8'))
           conn.close()
   
   thread = threading.Thread(target=socket_server)
   thread.daemon = True
   thread.start()
   ```

## 使用技巧

- **蓝图工具**: 可以快速生成蓝图和蓝图函数，如冒泡排序算法
- **动画工具**: 辅助处理骨骼动画和动画序列
- **常用工具**: 提供一系列常用操作的快捷访问

## 开发者笔记

### 虚幻引擎Python脚本注意事项

在使用本工具向虚幻引擎发送Python脚本时，请遵循以下规则以避免执行问题：

1. **避免使用嵌套函数**
2. **避免使用递归函数**
3. **避免依赖函数间调用**
4. **使用扁平化代码结构**
5. **优先使用迭代而非递归**

完整的最佳实践和问题排查请参考本文档后半部分。

## 工作原理

此方法基于"热文件"监视机制，非常简单：

1. 在UE中运行一个监视脚本，它会持续检查特定文件
2. 使用桌面工具编写Python代码并保存到该文件
3. 当文件被保存，UE中的监视器自动执行脚本

## 使用步骤

### 一次性设置 (在UE中)

1. 启动虚幻引擎
2. 打开Python控制台 (窗口 → 开发者工具 → Python控制台)
3. 将`UEScriptWatcher.py`的内容复制粘贴到控制台中，按回车执行
4. 你会在输出日志中看到"脚本监视器已启动"

### 每次使用 (在桌面上)

1. 运行桌面工具：
   ```
   py -3 simple_ue_script_executor.py
   ```

2. 在编辑器中写入或从文件加载Python代码

3. 点击"保存并执行"按钮

4. 虚幻引擎会自动执行你的代码

## 文件说明

- `UEScriptWatcher.py`: 在UE中运行的监视脚本
- `simple_ue_script_executor.py`: 桌面编辑工具
- 执行文件保存在: `C:\Users\你的用户名\UEScripts\execute_me.py`

## 优点

- **无需重启UE** - 随时执行Python代码
- **极度简单** - 无需插件、无需网络连接
- **无需特殊设置** - 除了复制粘贴监视脚本
- **即写即用** - 修改代码后立即执行

## 可能的问题

如果脚本没有自动执行，检查:
1. 确认监视脚本在UE中正在运行
2. 检查输出日志是否有监视器的信息
3. 尝试重新保存脚本

## 高级用途

你可以:
- 设置自动启动监视脚本
- 修改监视的文件路径
- 使用多个监视文件实现高级功能 

# 虚幻引擎Python脚本执行问题排查与解决方案

## 问题概述

在开发虚幻引擎的Python脚本执行工具过程中，我们遇到了一系列与Python函数作用域和执行环境相关的问题。这些问题主要出现在通过网络发送并在虚幻引擎中执行复杂结构Python脚本时。本文档总结了这些问题及其解决方案，以便日后快速应对类似情况。

## 问题症状

在执行包含函数定义和调用的Python脚本时，虚幻引擎日志中出现以下错误：

```python
LogPython: Error: 处理 NewBlueprint_C_1 时发生错误: name 'process_component' is not defined
LogPython: Error: 处理 NewBlueprint_C_1 时发生错误: name 'processed_components' is not defined
LogPython: Error: 处理 NewBlueprint_C_1 时发生错误: name 'spawn_model' is not defined
```

## 原因分析

### 虚幻引擎Python执行环境的特殊性

1. 虚幻引擎的Python执行环境与标准Python解释器有所不同
2. 通过网络传输执行的代码片段中，全局与局部命名空间的处理方式特殊
3. 函数作用域和变量访问规则可能被修改或限制

### 具体技术问题

1. **函数作用域问题**：递归和嵌套函数在UE的Python环境中可能导致作用域污染
2. **全局变量访问**：即使使用`global`关键字，函数内部也可能无法正确访问全局变量
3. **命名空间隔离**：通过socket传输的Python代码执行时，全局命名空间可能被重置或隔离

## 尝试解决方案

### 方案1：使用global关键字

```python
def process_component(component):
    global processed_components
    # 函数体...
```

**结果**：部分情况下仍然出现变量未定义错误

### 方案2：调整函数定义顺序

```python
def spawn_model(...): ...
def process_component(...): ...

# 主代码
```

**结果**：函数仍然无法被正确调用

### 方案3：使用非递归方法

```python
def get_all_components(root_component):
    result = []
    to_process = [root_component]
    # 使用队列迭代而非递归
```

**结果**：仍然存在函数调用问题

## 最终解决方案：代码内联

完全避免任何函数定义和调用，将所有逻辑直接内联到主代码流中：

```python
# 直接在主代码流中实现所有逻辑
all_components = []
to_process = [actor.root_component]

while to_process:
    current = to_process.pop(0)
    if current:
        all_components.append(current)
        children = current.get_children_components(False)
        to_process.extend(children)

# 处理每个组件时直接内联逻辑，不调用函数
for component in all_components:
    if isinstance(component, unreal.StaticMeshComponent):
        static_mesh = component.static_mesh
        if static_mesh:
            # 直接内联获取变换和生成Actor的代码
            world_location = component.get_world_location()
            # ... 其他代码 ...
```

## 最佳实践总结

### 代码结构建议

1. **避免函数调用**：在虚幻引擎执行的Python脚本中，尽量避免复杂的函数调用结构
2. **避免递归**：用迭代替代递归，使用队列或栈来管理处理项
3. **扁平化代码**：将复杂的嵌套代码结构扁平化
4. **接受代码冗余**：在此场景下，代码冗余比复杂的函数调用结构更可靠

### 调试与错误处理

1. **充分日志记录**：
   ```python
   unreal.log(f"找到 {len(all_components)} 个组件")
   unreal.log_error(f"处理 {actor.get_name()} 时发生错误: {str(e)}")
   ```

2. **异常捕获**：
   ```python
   try:
       # 操作代码
   except Exception as e:
       unreal.log_error(f"执行错误: {str(e)}")
       unreal.log_error(traceback.format_exc())
   ```

## 适用场景

此解决方案特别适用于：

1. 在虚幻引擎中通过远程脚本执行复杂操作
2. 需要处理层次结构数据（如组件树）的脚本
3. 需要在不同对象间共享数据的脚本

## 未来优化建议

1. 考虑使用虚幻引擎的Python模块系统
2. 将复杂逻辑封装到插件中，而非通过远程执行脚本
3. 使用虚幻引擎的异步任务系统处理复杂操作

## 示例应用：蓝图分解功能

我们成功应用上述方法实现了蓝图分解功能，该功能可以将选中的蓝图中的静态网格和骨骼网格提取为独立Actor。通过采用内联代码的方式，避免了函数调用问题，实现了功能的稳定运行。 