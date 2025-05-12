import unreal
rotator = unreal.Rotator(-46, 0, 0)
actor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.DirectionalLight, [0,0,0], rotator)
unreal.log('已创建平行光，旋转为Pitch=-46, Yaw=0, Roll=0') 