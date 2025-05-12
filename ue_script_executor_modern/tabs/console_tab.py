from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QGridLayout, QPushButton, QLabel
from ue_script_executor_modern.config import COLORS
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

class ConsoleTab(QWidget):
    def __init__(self, parent=None, log_msg=None):
        super().__init__(parent)
        self.log_msg = log_msg
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        # 控制台命令分组
        console_group = QGroupBox("常用控制台命令")
        console_group.setStyleSheet(f"border: 1px solid {COLORS['border']}; border-radius: 8px; background-color: {COLORS['panel']};")
        console_group_layout = QVBoxLayout(console_group)
        console_group_layout.setContentsMargins(10, 10, 10, 10)
        commands = [
            ("显示帧率 (FPS: stat fps)", "stat fps", "在左上角显示当前帧率"),
            ("显示三角面数 (stat RHI)", "stat RHI", "显示显卡渲染统计信息"),
            ("显示内存 (stat memory)", "stat memory", "显示内存使用情况"),
            ("显示DrawCall (stat scenerendering)", "stat scenerendering", "显示场景渲染统计"),
            ("显示网格体信息 (stat staticmesh)", "stat staticmesh", "显示静态网格体统计"),
            ("显示蓝图性能 (stat blueprint)", "stat blueprint", "显示蓝图脚本性能统计"),
            ("显示物理信息 (stat physics)", "stat physics", "显示物理系统统计"),
            ("隐藏所有统计 (stat none)", "stat none", "关闭所有统计信息显示")
        ]
        grid = QGridLayout()
        grid.setSpacing(10)
        for i, (label, cmd, desc) in enumerate(commands):
            row, col = i // 2, i % 2
            btn = QPushButton(label)
            btn.setMinimumHeight(36)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {COLORS['card']};
                    color: {COLORS['text']};
                    border: 1px solid {COLORS['border']};
                    border-radius: 4px;
                    font-size: 14px;
                    font-weight: bold;
                    padding: 8px 0;
                }}
                QPushButton:hover {{
                    background-color: {COLORS['panel']};
                    color: {COLORS['text']};
                }}
                QPushButton:pressed {{
                    background-color: #23232b;
                    color: {COLORS['text']};
                }}
            """)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setToolTip(desc)
            btn.clicked.connect(lambda checked=False, c=cmd: self.copy_command(c))
            grid.addWidget(btn, row, col)
        console_group_layout.addLayout(grid)
        layout.addWidget(console_group)
        # 说明
        info_label = QLabel("点击按钮可复制常用控制台命令，粘贴到UE控制台或脚本中即可使用。")
        info_label.setStyleSheet(f"color: {COLORS['text']}; background-color: {COLORS['card']}; padding: 10px; border-radius: 5px; font-style: italic;")
        info_label.setWordWrap(True)
        layout.addWidget(info_label)
    def copy_command(self, cmd):
        QApplication.clipboard().setText(cmd)
        if self.log_msg:
            self.log_msg(f"已复制命令: {cmd}") 