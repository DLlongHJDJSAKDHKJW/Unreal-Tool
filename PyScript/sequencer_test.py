import unreal

# 简化版的定序器关键帧后移脚本
unreal.log("开始执行关键帧后移")

# 获取当前定序器
seq = unreal.LevelSequenceEditorBlueprintLibrary.get_current_level_sequence()
if not seq:
    unreal.log("未找到定序器")
    exit()

# 获取选中的轨道
tracks = unreal.LevelSequenceEditorBlueprintLibrary.get_selected_tracks()
if not tracks:
    unreal.log("未选中轨道")
    exit()

count = 0  # 计数器

# 处理每个轨道
for track in tracks:
    track_name = track.get_display_name()
    unreal.log(f"处理轨道: {track_name}")
    
    # 检查是否是动画轨道
    is_anim = False
    try:
        if "Animation" in track_name:
            is_anim = True
        # 还可以添加其他判断条件
    except:
        pass
    
    # 获取区段
    sections = track.get_sections()
    for section in sections:
        try:
            # 处理动画片段
            if is_anim:
                try:
                    # 获取起始帧
                    start_frame = section.get_start_frame().frame_number.value
                    # 设置新起始帧
                    section.set_start_frame(unreal.FrameNumber(start_frame + 5))
                    count += 1
                    unreal.log(f"已移动动画片段: {start_frame} -> {start_frame+5}")
                except:
                    # 尝试使用set_range
                    try:
                        range_obj = section.get_range()
                        start_val = range_obj.get_lower_bound_value()
                        end_val = range_obj.get_upper_bound_value()
                        section.set_range(
                            unreal.FrameNumber(start_val + 5),
                            unreal.FrameNumber(end_val + 5)
                        )
                        count += 1
                        unreal.log("已通过范围移动动画片段")
                    except:
                        pass
                continue
            
            # 处理普通轨道
            channels = []
            try:
                # 尝试获取通道
                if hasattr(section, 'get_all_channels'):
                    channels = section.get_all_channels()
                elif hasattr(section, 'get_channels'):
                    channels = section.get_channels()
            except:
                continue
            
            # 处理每个通道
            for channel in channels:
                if not channel:
                    continue
                
                # 获取关键帧
                keys = channel.get_keys()
                if not keys:
                    continue
                
                # 保存关键帧数据
                key_data = []
                for key in keys:
                    try:
                        time_obj = key.get_time()
                        # 获取帧号
                        frame_num = 0
                        if hasattr(time_obj, 'frame_number'):
                            frame_num = time_obj.frame_number.value
                        elif hasattr(time_obj, 'value'):
                            frame_num = time_obj.value
                        
                        value = key.get_value()
                        key_data.append((frame_num, value))
                    except:
                        continue
                
                # 删除关键帧
                for key in keys:
                    try:
                        channel.remove_key(key)
                    except:
                        pass
                
                # 添加新关键帧
                for frame_num, value in key_data:
                    try:
                        new_frame = unreal.FrameNumber(frame_num + 5)
                        channel.add_key(new_frame, value)
                        count += 1
                    except:
                        pass
        except:
            continue

# 输出结果
unreal.log(f"已成功移动 {count} 个关键帧") 