import unreal
import time

# 基础关卡路径和名称
base_path = '/Game/BlankLevel'
asset_registry = unreal.AssetRegistryHelpers.get_asset_registry()

# 检查是否存在同名关卡，自动递增后缀
level_path = base_path
index = 1
while asset_registry.get_asset_by_object_path(level_path + '.umap').is_valid() or unreal.EditorAssetLibrary.does_asset_exist(level_path + '.umap'):
    level_path = f'{base_path}_{index}'
    index += 1

# 再用AssetLibrary做一次检测
if unreal.EditorAssetLibrary.does_asset_exist(level_path + '.umap'):
    unreal.log_warning(f'关卡 {level_path} 已存在，未创建新关卡')
else:
    unreal.EditorLevelLibrary.new_level(level_path)
    # 创建后再次检测
    time.sleep(0.5)  # 等待UE刷新
    if unreal.EditorAssetLibrary.does_asset_exist(level_path + '.umap'):
        unreal.log(f'已创建空白关卡 {level_path}')
    else:
        unreal.log_error(f'关卡 {level_path} 创建失败，请检查目标路径是否被占用') 