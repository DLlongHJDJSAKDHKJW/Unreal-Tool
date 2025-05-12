import unreal
unreal.SystemLibrary.execute_console_command(
    unreal.EditorLevelLibrary.get_editor_world(),
    "culture=en"
)
unreal.log('已切换为英文界面') 