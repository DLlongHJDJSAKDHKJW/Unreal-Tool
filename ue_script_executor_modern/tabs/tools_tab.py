from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QGridLayout, QPushButton, QLabel
from ue_script_executor_modern.config import COLORS
from PyQt5.QtCore import Qt

class ToolsTab(QWidget):
    def __init__(self, parent=None, log_msg=None, send_to_ue=None):
        super().__init__(parent)
        self.log_msg = log_msg  # 日志方法由主窗口传入
        self.send_to_ue = send_to_ue  # 脚本发送方法由主窗口传入
        self.language_toggle_state = 'en'
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        tools_group = QGroupBox("常用工具")
        tools_group.setStyleSheet(f"border: 1px solid {COLORS['border']}; border-radius: 8px; background-color: {COLORS['panel']};")
        tools_group_layout = QVBoxLayout(tools_group)
        tools_group_layout.setContentsMargins(10, 10, 10, 10)
        tools_group_layout.setSpacing(10)
        buttons_layout = QGridLayout()
        buttons_layout.setSpacing(12)
        # 分解蓝图
        btn_decompose = QPushButton("分解蓝图")
        btn_decompose.setMinimumHeight(40)
        btn_decompose.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['card']};
                color: {COLORS['text']};
                border: 1px solid {COLORS['border']};
                border-radius: 4px;
                font-size: 14px;
                font-weight: bold;
                padding: 10px 0;
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
        btn_decompose.clicked.connect(self.extract_blueprint_models)
        buttons_layout.addWidget(btn_decompose, 0, 0)
        # 切换英文
        self.lang_btn = QPushButton('切换英文')
        self.lang_btn.setMinimumHeight(40)
        self.lang_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['card']};
                color: {COLORS['text']};
                border: 1px solid {COLORS['border']};
                border-radius: 4px;
                font-size: 14px;
                font-weight: bold;
                padding: 10px 0;
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
        self.lang_btn.setCursor(Qt.PointingHandCursor)
        self.lang_btn.clicked.connect(self.toggle_language)
        buttons_layout.addWidget(self.lang_btn, 0, 1)
        # 新增功能按钮
        btn_blank_level = QPushButton("创建空白关卡")
        btn_blank_level.setMinimumHeight(40)
        btn_blank_level.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['card']};
                color: {COLORS['text']};
                border: 1px solid {COLORS['border']};
                border-radius: 4px;
                font-size: 14px;
                font-weight: bold;
                padding: 10px 0;
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
        btn_blank_level.clicked.connect(self.create_blank_level)
        buttons_layout.addWidget(btn_blank_level, 1, 0)
        btn_directional_light = QPushButton("创建平行光")
        btn_directional_light.setMinimumHeight(40)
        btn_directional_light.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['card']};
                color: {COLORS['text']};
                border: 1px solid {COLORS['border']};
                border-radius: 4px;
                font-size: 14px;
                font-weight: bold;
                padding: 10px 0;
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
        btn_directional_light.clicked.connect(self.create_directional_light)
        buttons_layout.addWidget(btn_directional_light, 1, 1)
        btn_height_fog = QPushButton("创建高度雾")
        btn_height_fog.setMinimumHeight(40)
        btn_height_fog.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['card']};
                color: {COLORS['text']};
                border: 1px solid {COLORS['border']};
                border-radius: 4px;
                font-size: 14px;
                font-weight: bold;
                padding: 10px 0;
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
        btn_height_fog.clicked.connect(self.create_height_fog)
        buttons_layout.addWidget(btn_height_fog, 2, 0)
        btn_sky_atmosphere = QPushButton("创建天空大气")
        btn_sky_atmosphere.setMinimumHeight(40)
        btn_sky_atmosphere.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['card']};
                color: {COLORS['text']};
                border: 1px solid {COLORS['border']};
                border-radius: 4px;
                font-size: 14px;
                font-weight: bold;
                padding: 10px 0;
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
        btn_sky_atmosphere.clicked.connect(self.create_sky_atmosphere)
        buttons_layout.addWidget(btn_sky_atmosphere, 2, 1)
        btn_sky_light = QPushButton("创建天光")
        btn_sky_light.setMinimumHeight(40)
        btn_sky_light.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['card']};
                color: {COLORS['text']};
                border: 1px solid {COLORS['border']};
                border-radius: 4px;
                font-size: 14px;
                font-weight: bold;
                padding: 10px 0;
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
        btn_sky_light.clicked.connect(self.create_sky_light)
        buttons_layout.addWidget(btn_sky_light, 3, 0)
        btn_sky_sphere = QPushButton("创建天空球")
        btn_sky_sphere.setMinimumHeight(40)
        btn_sky_sphere.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['card']};
                color: {COLORS['text']};
                border: 1px solid {COLORS['border']};
                border-radius: 4px;
                font-size: 14px;
                font-weight: bold;
                padding: 10px 0;
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
        btn_sky_sphere.clicked.connect(self.create_sky_sphere)
        buttons_layout.addWidget(btn_sky_sphere, 3, 1)
        btn_floor = QPushButton("创建地面")
        btn_floor.setMinimumHeight(40)
        btn_floor.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['card']};
                color: {COLORS['text']};
                border: 1px solid {COLORS['border']};
                border-radius: 4px;
                font-size: 14px;
                font-weight: bold;
                padding: 10px 0;
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
        btn_floor.clicked.connect(self.create_floor)
        buttons_layout.addWidget(btn_floor, 4, 0)
        tools_group_layout.addLayout(buttons_layout)
        layout.addWidget(tools_group)
        info_label = QLabel("提示：点击按钮执行相应的工具功能。某些操作可能需要先在UE中选择相关资产。")
        info_label.setStyleSheet(f"color: {COLORS['text']}; background-color: {COLORS['card']}; padding: 10px; border-radius: 5px; font-style: italic;")
        info_label.setWordWrap(True)
        layout.addWidget(info_label)

    def extract_blueprint_models(self):
        if self.log_msg:
            self.log_msg("此功能尚未实现", level="warning")

    def toggle_language(self):
        import os
        if self.language_toggle_state == 'en':
            script_path = os.path.join('PyScript', 'switch_to_english.py')
            try:
                with open(script_path, 'r', encoding='utf-8') as f:
                    code = f.read()
                if self.send_to_ue:
                    self.send_to_ue(code)
                self.lang_btn.setText('切换中文')
                self.language_toggle_state = 'zh'
                if self.log_msg:
                    self.log_msg('已发送切换为英文脚本')
            except Exception as e:
                if self.log_msg:
                    self.log_msg(f'切换英文脚本发送失败: {e}', level='error')
        else:
            script_path = os.path.join('PyScript', 'switch_to_chinese.py')
            try:
                with open(script_path, 'r', encoding='utf-8') as f:
                    code = f.read()
                if self.send_to_ue:
                    self.send_to_ue(code)
                self.lang_btn.setText('切换英文')
                self.language_toggle_state = 'en'
                if self.log_msg:
                    self.log_msg('已发送切换为中文脚本')
            except Exception as e:
                if self.log_msg:
                    self.log_msg(f'切换中文脚本发送失败: {e}', level='error')

    def create_blank_level(self):
        import os
        script_path = os.path.join('PyScript', 'create_blank_level.py')
        try:
            with open(script_path, 'r', encoding='utf-8') as f:
                code = f.read()
            if self.send_to_ue:
                self.send_to_ue(code)
            if self.log_msg:
                self.log_msg('已发送创建空白关卡脚本')
        except Exception as e:
            if self.log_msg:
                self.log_msg(f'创建空白关卡脚本发送失败: {e}', level='error')

    def create_directional_light(self):
        import os
        script_path = os.path.join('PyScript', 'create_directional_light.py')
        try:
            with open(script_path, 'r', encoding='utf-8') as f:
                code = f.read()
            if self.send_to_ue:
                self.send_to_ue(code)
            if self.log_msg:
                self.log_msg('已发送创建平行光脚本')
        except Exception as e:
            if self.log_msg:
                self.log_msg(f'创建平行光脚本发送失败: {e}', level='error')

    def create_height_fog(self):
        import os
        script_path = os.path.join('PyScript', 'create_height_fog.py')
        try:
            with open(script_path, 'r', encoding='utf-8') as f:
                code = f.read()
            if self.send_to_ue:
                self.send_to_ue(code)
            if self.log_msg:
                self.log_msg('已发送创建高度雾脚本')
        except Exception as e:
            if self.log_msg:
                self.log_msg(f'创建高度雾脚本发送失败: {e}', level='error')

    def create_sky_atmosphere(self):
        import os
        script_path = os.path.join('PyScript', 'create_sky_atmosphere.py')
        try:
            with open(script_path, 'r', encoding='utf-8') as f:
                code = f.read()
            if self.send_to_ue:
                self.send_to_ue(code)
            if self.log_msg:
                self.log_msg('已发送创建天空大气脚本')
        except Exception as e:
            if self.log_msg:
                self.log_msg(f'创建天空大气脚本发送失败: {e}', level='error')

    def create_sky_light(self):
        import os
        script_path = os.path.join('PyScript', 'create_sky_light.py')
        try:
            with open(script_path, 'r', encoding='utf-8') as f:
                code = f.read()
            if self.send_to_ue:
                self.send_to_ue(code)
            if self.log_msg:
                self.log_msg('已发送创建天光脚本')
        except Exception as e:
            if self.log_msg:
                self.log_msg(f'创建天光脚本发送失败: {e}', level='error')

    def create_sky_sphere(self):
        import os
        script_path = os.path.join('PyScript', 'create_sky_sphere.py')
        try:
            with open(script_path, 'r', encoding='utf-8') as f:
                code = f.read()
            if self.send_to_ue:
                self.send_to_ue(code)
            if self.log_msg:
                self.log_msg('已发送创建天空球脚本')
        except Exception as e:
            if self.log_msg:
                self.log_msg(f'创建天空球脚本发送失败: {e}', level='error')

    def create_floor(self):
        import os
        script_path = os.path.join('PyScript', 'create_floor.py')
        try:
            with open(script_path, 'r', encoding='utf-8') as f:
                code = f.read()
            if self.send_to_ue:
                self.send_to_ue(code)
            if self.log_msg:
                self.log_msg('已发送创建地面脚本')
        except Exception as e:
            if self.log_msg:
                self.log_msg(f'创建地面脚本发送失败: {e}', level='error') 