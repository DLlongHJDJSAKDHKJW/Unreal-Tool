import unreal
# 资产路径（引擎内容）
sky_bp_path = '/Engine/EngineSky/BP_Sky_Sphere.BP_Sky_Sphere'
asset = unreal.EditorAssetLibrary.load_asset(sky_bp_path)
if asset:
    actor = unreal.EditorLevelLibrary.spawn_actor_from_object(asset, [0,0,0])
    unreal.log('已创建天空球蓝图（BP_Sky_Sphere）')
else:
    unreal.log_error('未找到BP_Sky_Sphere蓝图，请确保引擎内容已显示') 