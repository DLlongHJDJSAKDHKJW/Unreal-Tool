import unreal
unreal.SystemLibrary.execute_console_command(
    unreal.EditorLevelLibrary.get_editor_world(),
    "culture=zh-Hans"
)
unreal.log('已切换为中文界面') 