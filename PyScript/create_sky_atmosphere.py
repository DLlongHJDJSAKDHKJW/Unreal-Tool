import unreal
actor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.SkyAtmosphere, [0,0,0])
unreal.log('已创建天空大气（SkyAtmosphere）') 