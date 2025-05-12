import unreal

def extract_models_from_component(component, processed_components):
    """
    递归地从组件中提取模型，并保持正确的缩放。
    """
    if component in processed_components:
        return
    processed_components.add(component)

    def spawn_model(mesh, component):
        """
        生成模型并保持正确的缩放和变换
        """
        # 获取世界变换
        world_location = component.get_world_location()
        world_rotation = component.get_world_rotation()
        
        # 获取完整的世界缩放
        parent_component = component.get_attach_parent()
        cumulative_scale = component.relative_scale3d
        
        # 递归计算累积缩放
        while parent_component:
            cumulative_scale = cumulative_scale * parent_component.relative_scale3d
            parent_component = parent_component.get_attach_parent()
        
        # 生成Actor
        new_actor = unreal.EditorLevelLibrary.spawn_actor_from_object(
            mesh, world_location, world_rotation
        )
        
        # 设置缩放
        if new_actor and new_actor.root_component:
            new_actor.root_component.set_editor_property('relative_scale3d', cumulative_scale)
        
        return new_actor

    # 检查静态网格体组件
    if isinstance(component, unreal.StaticMeshComponent):
        static_mesh = component.static_mesh
        if static_mesh:
            new_actor = spawn_model(static_mesh, component)
            if new_actor:
                unreal.log(f"已添加静态网格模型: {static_mesh.get_name()} 到场景中")
    
    # 检查骨骼网格体组件
    elif isinstance(component, unreal.SkeletalMeshComponent):
        skeletal_mesh = component.skeletal_mesh
        if skeletal_mesh:
            new_actor = spawn_model(skeletal_mesh, component)
            if new_actor:
                unreal.log(f"已添加骨骼模型: {skeletal_mesh.get_name()} 到场景中")

    # 递归处理所有子组件
    for child_component in component.get_children_components(False):
        extract_models_from_component(child_component, processed_components)

def extract_models_from_blueprint(actor):
    try:
        processed_components = set()
        extract_models_from_component(actor.root_component, processed_components)
    except Exception as e:
        unreal.log_error(f"处理 {actor.get_name()} 时发生错误: {str(e)}")

# 主脚本
try:
    # 获取编辑器选中的场景Actor
    editor_subsystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    selected_actors = editor_subsystem.get_selected_level_actors()
    
    if len(selected_actors) == 0:
        unreal.log_warning("没有选中任何场景Actor")
    else:
        for actor in selected_actors:
            unreal.log(f"正在处理场景中的Actor: {actor.get_name()}")
            extract_models_from_blueprint(actor)
            
except Exception as e:
    unreal.log_error(f"脚本执行错误: {str(e)}")
