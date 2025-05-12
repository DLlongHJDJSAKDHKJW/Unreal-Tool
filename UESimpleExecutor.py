"""
UESimpleExecutor.py - 虚幻引擎Python脚本执行器
--------------------------------------------
这个脚本提供了一个简单可靠的方式在虚幻引擎中执行Python代码，
确保所有代码都在主线程上执行，解决常见的线程问题。

主要功能:
1. 在主线程上执行Python代码
2. 执行Python脚本文件
3. 通过Socket接收并执行远程代码
4. 提供详细的错误报告
"""

import unreal
import socket
import threading
import time
import os
import random
import queue
import sys
import traceback
from datetime import datetime

# ======================================================
# 配置参数
# ======================================================
VERSION = "2.3"
DEFAULT_PORT = 9876        # 默认起始端口
MAX_PORT_TRIES = 20        # 最大尝试端口数
MAX_QUEUE_SIZE = 100       # 命令队列最大长度
EXECUTION_TIMEOUT = 30     # 执行超时时间(秒)
DEBUG_MODE = False         # 调试模式(输出更多日志)
QUIET_MODE = True          # 安静模式(只显示必要信息)

# ======================================================
# 全局变量
# ======================================================
command_queue = queue.Queue(MAX_QUEUE_SIZE)  # 线程安全的命令队列
TICK_HANDLE = None         # Slate回调句柄
last_execution_time = 0    # 上次执行时间戳
execution_count = 0        # 执行计数器
server_socket = None       # 服务器套接字
server_thread = None       # 服务器线程
is_running = True          # 运行状态

# ======================================================
# 辅助函数
# ======================================================
def log_info(message, force=False):
    """输出信息日志"""
    if force or not QUIET_MODE:
        unreal.log(f"[UEExecutor] {message}")

def log_error(message):
    """输出错误日志"""
    unreal.log_error(f"[UEExecutor] {message}")

def log_warning(message):
    """输出警告日志"""
    unreal.log_warning(f"[UEExecutor] {message}")

def log_debug(message):
    """调试日志，仅在DEBUG_MODE=True时输出"""
    if DEBUG_MODE:
        unreal.log(f"[UEExecutor:DEBUG] {message}")

def get_timestamp():
    """获取当前时间戳(毫秒)"""
    return int(time.time() * 1000)

def format_traceback(e):
    """格式化异常堆栈信息"""
    exc_type, exc_value, exc_traceback = sys.exc_info()
    tb_lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
    return "".join(tb_lines)

def find_available_port(start_port=DEFAULT_PORT, max_tries=MAX_PORT_TRIES):
    """尝试找到一个可用的端口"""
    for offset in range(max_tries):
        port = start_port + offset
        try:
            # 尝试绑定端口以检查是否可用
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('localhost', port))
                log_info(f"找到可用端口: {port}", force=True)
                return port
        except OSError:
            log_debug(f"端口 {port} 已被占用，尝试下一个...")
    
    # 如果所有端口都不可用，使用随机端口
    random_port = random.randint(10000, 65000)
    log_warning(f"所有尝试的端口都被占用，使用随机端口: {random_port}")
    return random_port

# ======================================================
# 核心执行功能
# ======================================================
def on_tick(delta_seconds):
    """每一帧检查队列并执行代码"""
    global command_queue, execution_count, last_execution_time, is_running
    
    # 如果服务已停止，不再处理队列
    if not is_running:
        return False
    
    try:
        # 非阻塞地获取队列中的命令
        if not command_queue.empty():
            code = command_queue.get_nowait()
            execution_id = execution_count + 1
            execution_count = execution_id
            
            start_time = get_timestamp()
            last_execution_time = start_time
            
            log_info(f"------ 开始执行代码 #{execution_id} ------")
            success = True
            
            try:
                # 在独立的locals环境中执行代码，但使用全局globals
                local_vars = {}
                exec(code, globals(), local_vars)
            except Exception as e:
                success = False
                log_error(f"执行出错 #{execution_id}: {type(e).__name__}: {str(e)}")
                log_error(format_traceback(e))
            finally:
                end_time = get_timestamp()
                execution_time = end_time - start_time
                
                if success:
                    log_info(f"------ 执行完成 #{execution_id} (耗时: {execution_time}ms) ------")
                else:
                    log_error(f"------ 执行失败 #{execution_id} (耗时: {execution_time}ms) ------")
                
                command_queue.task_done()
    except Exception as e:
        log_error(f"队列处理出错: {str(e)}")
    
    # 返回True表示继续执行回调
    return True

def execute_in_main_thread(code_str):
    """将代码放入队列，等待主线程执行"""
    global command_queue, is_running
    
    if not is_running:
        log_warning("服务已停止，无法执行代码")
        return False
    
    try:
        # 检查队列是否已满
        if command_queue.full():
            log_warning("命令队列已满，请稍后再试")
            return False
            
        command_queue.put(code_str)
        log_info(f"代码已加入队列，等待主线程执行 (队列长度: {command_queue.qsize()})")
        return True
    except Exception as e:
        log_error(f"加入队列失败: {str(e)}")
        return False

def execute_file(file_path):
    """执行Python文件的内容"""
    if not is_running:
        log_warning("服务已停止，无法执行文件")
        return False
        
    try:
        if not os.path.exists(file_path):
            log_error(f"文件不存在: {file_path}")
            return False
            
        file_size = os.path.getsize(file_path) / 1024  # KB
        log_info(f"读取文件: {file_path} ({file_size:.1f} KB)")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
            
        file_name = os.path.basename(file_path)
        log_info(f"执行文件: {file_name}")
        
        # 添加文件路径作为注释，方便调试
        wrapped_code = f"""# 执行文件: {file_path}
# 时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{code}
"""
        return execute_in_main_thread(wrapped_code)
    except Exception as e:
        log_error(f"文件执行出错: {str(e)}")
        log_error(format_traceback(e))
        return False

def direct_execute(code_str):
    """执行代码字符串"""
    return execute_in_main_thread(code_str)

# ======================================================
# 服务器功能
# ======================================================
def start_server():
    """启动Socket服务器接收代码"""
    global server_socket, server_thread, is_running
    
    try:
        # 查找可用端口
        port = find_available_port()
        
        # 创建服务器套接字
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(('localhost', port))
        server_socket.listen(5)
        server_socket.settimeout(1)  # 设置超时，以便能够响应停止命令
        
        log_info(f"Socket服务器已启动，端口: {port}", force=True)
        
        def server_loop():
            """处理客户端连接的线程函数"""
            global is_running
            
            while is_running:
                try:
                    client, addr = server_socket.accept()
                    client.settimeout(5)
                    log_info(f"[DEBUG] 收到连接: {addr}", force=True)
                    unreal.log(f"[DEBUG] 收到连接: {addr}")
                    client_thread = threading.Thread(
                        target=handle_client, 
                        args=(client, addr)
                    )
                    client_thread.daemon = True
                    client_thread.start()
                except socket.timeout:
                    continue
                except Exception as e:
                    if is_running:
                        log_error(f"接受连接出错: {str(e)}")
                    time.sleep(0.5)
            
            log_info("服务器线程已退出")
        
        def handle_client(client_socket, addr):
            """处理单个客户端的请求"""
            try:
                data = client_socket.recv(4096)
                if data:
                    code = data.decode('utf-8')
                    log_info(f"[DEBUG] 收到来自 {addr} 的代码 ({len(code)} 字节)", force=True)
                    unreal.log(f"[DEBUG] 收到代码内容: {code[:80]}")
                    # 自动修正：识别SHUTDOWN_SERVER命令
                    if code.strip() == "SHUTDOWN_SERVER":
                        log_info("收到SHUTDOWN_SERVER命令，准备关闭服务器", force=True)
                        shutdown_server()
                    else:
                        execute_in_main_thread(code)
                    try:
                        client_socket.sendall(b"OK")
                    except:
                        pass
            except Exception as e:
                log_error(f"处理客户端 {addr} 出错: {str(e)}")
            finally:
                client_socket.close()
        
        # 启动服务器线程
        is_running = True
        server_thread = threading.Thread(target=server_loop)
        server_thread.daemon = True
        server_thread.start()
        
        # 返回成功状态和使用的端口
        return True, port
    except Exception as e:
        log_error(f"启动服务器出错: {str(e)}")
        log_error(format_traceback(e))
        return False, None

def shutdown_server():
    """关闭服务器并清理资源 - 安全版本，避免引起UE崩溃"""
    global is_running
    
    log_info("正在安全关闭服务器...", force=True)
    
    # 设置停止标志，但不立即关闭任何资源
    is_running = False
    
    # 仅从unreal模块中移除端口信息
    if hasattr(unreal, 'simple_executor_port'):
        try:
            port = unreal.simple_executor_port
            delattr(unreal, 'simple_executor_port')
            log_info(f"服务器端口 {port} 已释放", force=True)
        except:
            pass
    
    log_info("服务器已标记为关闭状态", force=True)
    log_info("请重新启动UE以完全释放资源", force=True)
    return True

# ======================================================
# 主线程执行管理
# ======================================================
def start_main_thread_executor():
    """设置主线程执行回调"""
    global TICK_HANDLE
    
    try:
        if TICK_HANDLE is not None:
            unreal.unregister_slate_post_tick_callback(TICK_HANDLE)
            TICK_HANDLE = None
        
        TICK_HANDLE = unreal.register_slate_post_tick_callback(on_tick)
        log_info("主线程执行器已启动", force=True)
        return TICK_HANDLE is not None
    except Exception as e:
        log_error(f"启动主线程执行器失败: {str(e)}")
        return False

def cleanup():
    """清理资源"""
    global TICK_HANDLE, command_queue
    
    try:
        if TICK_HANDLE is not None:
            unreal.unregister_slate_post_tick_callback(TICK_HANDLE)
            TICK_HANDLE = None
        
        # 清空命令队列
        while not command_queue.empty():
            try:
                command_queue.get_nowait()
                command_queue.task_done()
            except:
                pass
                
        log_info("资源已清理")
        return True
    except Exception as e:
        log_error(f"清理资源出错: {str(e)}")
        return False

def get_status():
    """获取执行器状态信息"""
    status = {
        "version": VERSION,
        "active": TICK_HANDLE is not None and is_running,
        "queue_size": command_queue.qsize() if command_queue else 0,
        "execution_count": execution_count,
        "last_execution": last_execution_time
    }
    
    return status

# ======================================================
# 实用工具函数
# ======================================================
def run_ue_command(command):
    """执行UE编辑器命令"""
    try:
        return unreal.EditorLevelLibrary.execute_console_command(command)
    except Exception as e:
        log_error(f"执行控制台命令出错: {str(e)}")
        return False

def get_selected_actors():
    """获取当前选中的Actor列表"""
    try:
        return unreal.EditorLevelLibrary.get_selected_level_actors()
    except Exception as e:
        log_error(f"获取选中Actor失败: {str(e)}")
        return []

def create_actor(actor_class, location=None, rotation=None):
    """在场景中创建一个Actor"""
    try:
        if location is None:
            location = unreal.Vector(0, 0, 0)
        if rotation is None:
            rotation = unreal.Rotator(0, 0, 0)
            
        return unreal.EditorLevelLibrary.spawn_actor_from_class(
            actor_class, 
            location, 
            rotation
        )
    except Exception as e:
        log_error(f"创建Actor失败: {str(e)}")
        return None

def run_test_code():
    """运行测试代码"""
    test_code = """
# 测试代码
unreal.log("[测试] 测试代码执行成功!")
"""
    direct_execute(test_code)
    log_info("测试代码已执行")

# ======================================================
# 注册函数到unreal模块
# ======================================================
# 基本功能
unreal.simple_execute = direct_execute
unreal.execute_file = execute_file
unreal.execute_in_main_thread = execute_in_main_thread
unreal.restart_executor = start_main_thread_executor
unreal.cleanup_executor = cleanup
unreal.get_executor_status = get_status
unreal.run_test = run_test_code
unreal.shutdown_server = shutdown_server

# 实用工具
unreal.run_command = run_ue_command
unreal.get_selected = get_selected_actors
unreal.create_actor = create_actor

# 设置调试级别
def set_debug(enabled=True):
    """启用或禁用调试模式"""
    global DEBUG_MODE
    DEBUG_MODE = enabled
    log_info(f"调试模式: {'启用' if enabled else '禁用'}")
    return DEBUG_MODE

def set_quiet(enabled=True):
    """启用或禁用安静模式"""
    global QUIET_MODE
    QUIET_MODE = enabled
    log_info(f"安静模式: {'启用' if enabled else '禁用'}", force=True)
    return QUIET_MODE

unreal.set_debug = set_debug
unreal.set_quiet = set_quiet

# ======================================================
# 初始化
# ======================================================
# 清理之前可能已存在的属性
if hasattr(unreal, 'simple_executor_port'):
    delattr(unreal, 'simple_executor_port')

# 首先启动主线程执行器
if start_main_thread_executor():
    # 然后启动Socket服务器
    server_status, port = start_server()
    
    if server_status:
        # 存储端口号以便桌面工具查询
        unreal.simple_executor_port = port
        
        # 打印极简启动信息
        log_info(f"极简Python执行器 v{VERSION} 已启动", force=True)
        
        # 不自动执行测试代码，用户可以通过unreal.run_test()手动执行
    else:
        log_error("服务器启动失败，功能可能不完整")
else:
    log_error("主线程执行器启动失败") 