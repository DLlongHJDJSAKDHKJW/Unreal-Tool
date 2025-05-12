import unreal
import traceback

unreal.log("[定序器测试] 开始执行")
try:
    seq = unreal.LevelSequenceEditorBlueprintLibrary.get_current_level_sequence()
    if not seq:
        unreal.log_warning("未找到当前打开的定序器")
    else:
        seq_name = seq.get_name()
        unreal.log(f"当前定序器名称: {seq_name}")
        selected_tracks = unreal.LevelSequenceEditorBlueprintLibrary.get_selected_tracks()
        if not selected_tracks:
            unreal.log_warning("未选中任何轨道")
        else:
            unreal.log(f"选中的轨道数量: {len(selected_tracks)}")
            found = False
            
            # 遍历所有选中的轨道
            for track in selected_tracks:
                track_name = track.get_display_name()
                unreal.log(f"处理轨道: {track_name}")
                sections = track.get_sections()
                
                for section in sections:
                    # 获取Transform Section的所有通道
                    transform_section = unreal.MovieScene3DTransformSection.cast(section)
                    if transform_section:
                        # 获取所有通道
                        channels = transform_section.get_all_channels()
                        unreal.log(f"找到 {len(channels)} 个通道")
                        
                        for channel in channels:
                            if channel:
                                keys = channel.get_keys()
                                if keys:
                                    found = True
                                    unreal.log(f"通道: {channel.get_name()}，关键帧数量: {len(keys)}")
                                    
                                    # 记录所有关键帧的时间和值
                                    key_data = []
                                    for k in keys:
                                        time = k.get_time()
                                        value = k.get_value()
                                        key_data.append((time, value))
                                    
                                    # 删除所有关键帧
                                    for k in keys:
                                        channel.remove_key(k)
                                    
                                    # 添加新的关键帧（时间+5帧）
                                    for time, value in key_data:
                                        new_time = unreal.FrameNumber(time.frame_number.value + 5)
                                        channel.add_key(new_time, value)
                                    
                                    unreal.log(f"通道 {channel.get_name()} 的关键帧已整体后移5帧")
            if not found:
                unreal.log_warning("选中的轨道下没有可操作的区段或关键帧")
except Exception as e:
    unreal.log_error(f"定序器测试脚本出错: {str(e)}")
    unreal.log_error(traceback.format_exc()) 