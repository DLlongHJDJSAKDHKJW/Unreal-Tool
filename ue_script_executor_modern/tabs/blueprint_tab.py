from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QGridLayout, QPushButton, QLabel
from ue_script_executor_modern.config import COLORS
from PyQt5.QtCore import Qt

class BlueprintTab(QWidget):
    def __init__(self, parent=None, log_msg=None):
        super().__init__(parent)
        self.log_msg = log_msg
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        # 蓝图分组
        bp_group = QGroupBox("蓝图")
        bp_group.setStyleSheet(f"border: 1px solid {COLORS['border']}; border-radius: 8px; background-color: {COLORS['panel']};")
        bp_layout = QGridLayout(bp_group)
        bp_layout.setContentsMargins(10, 10, 10, 10)
        bp_layout.setSpacing(10)
        # 蓝图按钮 - 冒泡排序
        btn = QPushButton("冒泡排序")
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
        btn.clicked.connect(self.copy_bubble_sort_usage)
        bp_layout.addWidget(btn, 0, 0)
        # 蓝图函数分组
        bp_func_group = QGroupBox("蓝图函数")
        bp_func_group.setStyleSheet(f"border: 1px solid {COLORS['border']}; border-radius: 8px; background-color: {COLORS['panel']};")
        bp_func_layout = QGridLayout(bp_func_group)
        bp_func_layout.setContentsMargins(10, 10, 10, 10)
        bp_func_layout.setSpacing(10)
        btn_func = QPushButton("冒泡排序")
        btn_func.setMinimumHeight(36)
        btn_func.setStyleSheet(btn.styleSheet())
        btn_func.setCursor(Qt.PointingHandCursor)
        btn_func.clicked.connect(self.copy_bubble_sort_function)
        bp_func_layout.addWidget(btn_func, 0, 0)
        # 提示
        tip_label = QLabel("点击按钮将相应蓝图代码复制到剪贴板")
        tip_label.setStyleSheet("color: #AAAAAA; font-size: 12px;")
        tip_label.setAlignment(Qt.AlignCenter)
        # 组装
        layout.addWidget(bp_group)
        layout.addWidget(bp_func_group)
        layout.addWidget(tip_label)
        layout.addStretch(1)
    def copy_bubble_sort_usage(self):
        try:
            with open("JsonFile/冒泡排序用法.json", "r", encoding="utf-8") as f:
                content = f.read()
            from PyQt5.QtWidgets import QApplication
            QApplication.clipboard().setText(content)
            if self.log_msg:
                self.log_msg("冒泡排序用法已复制到剪贴板")
        except Exception as e:
            if self.log_msg:
                self.log_msg(f"复制冒泡排序用法失败: {e}", level="error")
    def copy_bubble_sort_function(self):
        try:
            with open("JsonFile/冒泡排序.json", "r", encoding="utf-8") as f:
                content = f.read()
            from PyQt5.QtWidgets import QApplication
            QApplication.clipboard().setText(content)
            if self.log_msg:
                self.log_msg("冒泡排序函数已复制到剪贴板")
        except Exception as e:
            if self.log_msg:
                self.log_msg(f"复制冒泡排序函数失败: {e}", level="error") 