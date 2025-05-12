import unreal
actor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.ExponentialHeightFog, [0,0,0])
unreal.log('已创建高度雾') 