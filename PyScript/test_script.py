import unreal
from datetime import datetime

# 打印基本信息
def test_basic():
    try:
        # 只输出最基本信息，确保一定能执行成功
        unreal.log("="*50)
        unreal.log("测试脚本执行中...")
        unreal.log(f"当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # 只使用一定存在的API - project_dir()
        try:
            unreal.log(f"项目目录: {unreal.Paths.project_dir()}")
        except:
            unreal.log("无法获取项目目录")
        
        # 安全获取引擎版本
        try:
            unreal.log(f"引擎版本: {unreal.get_engine_version()}")
        except:
            unreal.log("无法获取引擎版本")
        
        unreal.log("基本测试完成")
        unreal.log("="*50)
    except Exception as e:
        unreal.log_error(f"执行出错: {str(e)}")

# 直接调用最简单的测试，不使用任何线程或回调机制
test_basic()
