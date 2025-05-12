import unreal
actor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.SkyLight, [0,0,0])
unreal.log('已创建天光（SkyLight）') 