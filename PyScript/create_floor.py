import unreal
# 资产路径（引擎内容）
floor_path = '/Engine/MapTemplates/SM_Template_Map_Floor.SM_Template_Map_Floor'
asset = unreal.EditorAssetLibrary.load_asset(floor_path)
if asset:
    actor = unreal.EditorLevelLibrary.spawn_actor_from_object(asset, [0,0,0])
    unreal.log('已创建地面（SM_Template_Map_Floor）')
else:
    unreal.log_error('未找到SM_Template_Map_Floor静态网格体，请确保引擎内容已显示') 