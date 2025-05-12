# 虚幻引擎定序器关键帧操作指南

## 1. 整体移动轨道关键帧

### 功能描述
将选中轨道的所有关键帧整体向后移动5帧。

### 使用方法
1. 在定序器中选中一个Transform轨道
2. 点击"定序器测试"按钮
3. 该轨道下的所有关键帧将向后移动5帧

### 代码实现
```python
import unreal
import traceback

unreal.log("[定序器测试] 开始执行")
try:
    # 获取当前打开的定序器
    seq = unreal.LevelSequenceEditorBlueprintLibrary.get_current_level_sequence()
    if not seq:
        unreal.log_warning("未找到当前打开的定序器")
    else:
        seq_name = seq.get_name()
        unreal.log(f"当前定序器名称: {seq_name}")
        
        # 获取选中的轨道
        selected_tracks = unreal.LevelSequenceEditorBlueprintLibrary.get_selected_tracks()
        if not selected_tracks:
            unreal.log_warning("未选中任何轨道")
        else:
            track = selected_tracks[0]
            track_name = track.get_display_name()
            unreal.log(f"选中轨道名称: {track_name}")
            
            # 获取轨道下的所有区段
            sections = track.get_sections()
            found = False
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
                unreal.log_warning("选中轨道下没有可操作的区段或关键帧")
except Exception as e:
    unreal.log_error(f"定序器测试脚本出错: {str(e)}")
    unreal.log_error(traceback.format_exc())
```

### 关键API说明
1. `get_current_level_sequence()` - 获取当前打开的定序器
2. `get_selected_tracks()` - 获取选中的轨道
3. `get_sections()` - 获取轨道下的所有区段
4. `get_all_channels()` - 获取区段下的所有通道
5. `get_keys()` - 获取通道下的所有关键帧
6. `get_time()` - 获取关键帧的时间
7. `get_value()` - 获取关键帧的值
8. `remove_key()` - 删除单个关键帧
9. `add_key()` - 添加新的关键帧

### 注意事项
1. 只能操作Transform类型的轨道
2. 需要先选中轨道才能执行操作
3. 所有关键帧都会移动，不能选择性移动
4. 移动距离固定为5帧

## 2. 选择性移动关键帧

### 功能描述
只移动选中的关键帧，未选中的关键帧保持不变。

### 使用方法
1. 在定序器中选择要移动的关键帧
2. 点击"定序器测试"按钮
3. 只有选中的关键帧会向后移动5帧

### 代码实现
```python
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
        
        # 获取所有选中的关键帧
        selected_keys = unreal.LevelSequenceEditorBlueprintLibrary.get_selected_keys()
        if not selected_keys:
            unreal.log_warning("未选中任何关键帧")
        else:
            unreal.log(f"选中的关键帧数量: {len(selected_keys)}")
            
            # 按通道分组选中的关键帧
            channel_keys = {}
            for key in selected_keys:
                channel = key.get_owner()
                if channel:
                    if channel not in channel_keys:
                        channel_keys[channel] = []
                    channel_keys[channel].append(key)
            
            # 处理每个通道的选中关键帧
            for channel, keys in channel_keys.items():
                unreal.log(f"处理通道: {channel.get_name()}，选中关键帧数量: {len(keys)}")
                
                # 记录选中关键帧的时间和值
                key_data = []
                for k in keys:
                    time = k.get_time()
                    value = k.get_value()
                    key_data.append((time, value))
                
                # 删除选中的关键帧
                for k in keys:
                    channel.remove_key(k)
                
                # 添加新的关键帧（时间+5帧）
                for time, value in key_data:
                    new_time = unreal.FrameNumber(time.frame_number.value + 5)
                    channel.add_key(new_time, value)
                
                unreal.log(f"通道 {channel.get_name()} 的选中关键帧已后移5帧")
except Exception as e:
    unreal.log_error(f"定序器测试脚本出错: {str(e)}")
    unreal.log_error(traceback.format_exc())
```

### 关键API说明
1. `get_current_level_sequence()` - 获取当前打开的定序器
2. `get_selected_keys()` - 获取所有选中的关键帧
3. `get_owner()` - 获取关键帧所属的通道
4. `get_time()` - 获取关键帧的时间
5. `get_value()` - 获取关键帧的值
6. `remove_key()` - 删除单个关键帧
7. `add_key()` - 添加新的关键帧

### 注意事项
1. 不需要选中轨道，只需要选中关键帧
2. 可以同时选择多个通道的关键帧
3. 移动距离固定为5帧
4. 未选中的关键帧保持不变 