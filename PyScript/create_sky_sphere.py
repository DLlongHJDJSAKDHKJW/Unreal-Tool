import unreal
asset = unreal.EditorAssetLibrary.load_asset('/Engine/EngineSky/BP_Sky_Sphere.BP_Sky_Sphere')
if asset:
    unreal.EditorLevelLibrary.spawn_actor_from_object(asset, [0,0,0])
    unreal.log('已创建天空球蓝图')
else:
    unreal.log_error('未找到BP_Sky_Sphere蓝图') 