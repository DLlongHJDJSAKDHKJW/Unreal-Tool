from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QGridLayout, QPushButton, QLabel, QHBoxLayout, QSpinBox
from ue_script_executor_modern.config import COLORS
from PyQt5.QtCore import Qt

class ToolsTab(QWidget):
    def __init__(self, parent=None, log_msg=None, send_to_ue=None):
        super().__init__(parent)
        self.log_msg = log_msg  # 日志方法由主窗口传入
        self.send_to_ue = send_to_ue  # 脚本发送方法由主窗口传入
        self.language_toggle_state = 'en'
        
        # 主布局
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(15)
        
        # 创建按钮样式
        self.button_style = f"""
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
        """
        
        # 创建常用功能区域
        common_group = QGroupBox("常用功能")
        common_group.setStyleSheet(f"""
            QGroupBox {{
                font-size: 16px;
                font-weight: bold;
                color: {COLORS['text']};
                border: 1px solid {COLORS['border']};
                border-radius: 6px;
                margin-top: 10px;
                padding-top: 10px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }}
        """)
        common_layout = QGridLayout(common_group)
        common_layout.setSpacing(12)
        
        # 常用功能按钮
        common_buttons = []
        
        btn_decompose = self.create_button("分解蓝图")
        btn_decompose.clicked.connect(self.extract_blueprint_models)
        common_buttons.append(btn_decompose)
        
        self.lang_btn = self.create_button('切换英文')
        self.lang_btn.setCursor(Qt.PointingHandCursor)
        self.lang_btn.clicked.connect(self.toggle_language)
        common_buttons.append(self.lang_btn)
        
        btn_blank_level = self.create_button("创建空白关卡")
        btn_blank_level.clicked.connect(self.create_blank_level)
        common_buttons.append(btn_blank_level)
        
        btn_directional_light = self.create_button("创建平行光")
        btn_directional_light.clicked.connect(self.create_directional_light)
        common_buttons.append(btn_directional_light)
        
        btn_height_fog = self.create_button("创建高度雾")
        btn_height_fog.clicked.connect(self.create_height_fog)
        common_buttons.append(btn_height_fog)
        
        btn_sky_atmosphere = self.create_button("创建天空大气")
        btn_sky_atmosphere.clicked.connect(self.create_sky_atmosphere)
        common_buttons.append(btn_sky_atmosphere)
        
        btn_sky_light = self.create_button("创建天光")
        btn_sky_light.clicked.connect(self.create_sky_light)
        common_buttons.append(btn_sky_light)
        
        btn_sky_sphere = self.create_button("创建天空球")
        btn_sky_sphere.clicked.connect(self.create_sky_sphere)
        common_buttons.append(btn_sky_sphere)
        
        btn_floor = self.create_button("创建地面")
        btn_floor.clicked.connect(self.create_floor)
        common_buttons.append(btn_floor)
        
        # 将常用功能按钮添加到网格布局，每行5个
        for idx, btn in enumerate(common_buttons):
            row = idx // 5
            col = idx % 5
            common_layout.addWidget(btn, row, col)
        
        # 创建定序器功能区域
        sequencer_group = QGroupBox("定序器功能")
        sequencer_group.setStyleSheet(f"""
            QGroupBox {{
                font-size: 16px;
                font-weight: bold;
                color: {COLORS['text']};
                border: 1px solid {COLORS['border']};
                border-radius: 6px;
                margin-top: 10px;
                padding-top: 10px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }}
        """)
        
        # 使用网格布局，确保每行5个按钮
        sequencer_layout = QGridLayout(sequencer_group)
        sequencer_layout.setSpacing(12)
        
        # 创建轨道移动控制区域
        track_move_widget = QWidget()
        track_move_layout = QHBoxLayout(track_move_widget)
        track_move_layout.setContentsMargins(0, 0, 0, 0)
        
        # 帧数输入框
        frames_label = QLabel("帧数:")
        frames_label.setStyleSheet(f"color: {COLORS['text']}; font-size: 14px;")
        track_move_layout.addWidget(frames_label)
        
        self.frames_input = QSpinBox()
        self.frames_input.setMinimum(1)
        self.frames_input.setMaximum(100)
        self.frames_input.setValue(5)  # 默认值为5
        self.frames_input.setStyleSheet(f"""
            QSpinBox {{
                background-color: {COLORS['card']};
                color: {COLORS['text']};
                border: 1px solid {COLORS['border']};
                border-radius: 4px;
                padding: 5px;
                min-width: 50px;
                font-size: 14px;
            }}
            QSpinBox::up-button, QSpinBox::down-button {{
                background-color: {COLORS['panel']};
                border: 1px solid {COLORS['border']};
            }}
        """)
        track_move_layout.addWidget(self.frames_input)
        
        # 轨道移动按钮
        btn_track_move = self.create_button("轨道移动")
        btn_track_move.clicked.connect(self.run_sequencer_move)
        track_move_layout.addWidget(btn_track_move)
        
        # 将轨道移动控件添加到网格的第一个位置
        sequencer_layout.addWidget(track_move_widget, 0, 0, 1, 2)  # 跨两列
        
        # 添加分组到主布局
        layout.addWidget(common_group)
        layout.addWidget(sequencer_group)
        
        # 添加弹性空间
        layout.addStretch()
    
    def create_button(self, text):
        """创建统一样式的按钮"""
        btn = QPushButton(text)
        btn.setMinimumHeight(40)
        btn.setStyleSheet(self.button_style)
        return btn

    def extract_blueprint_models(self):
        import os
        script_path = os.path.join('PyScript', 'extract_blueprint_models.py')
        try:
            with open(script_path, 'r', encoding='utf-8') as f:
                code = f.read()
            if self.send_to_ue:
                self.send_to_ue(code)
            if self.log_msg:
                self.log_msg('已发送蓝图分解脚本')
        except Exception as e:
            if self.log_msg:
                self.log_msg(f'蓝图分解脚本发送失败: {e}', level='error')

    def toggle_language(self):
        import os
        if self.language_toggle_state == 'en':
            # 切换为中文
            script_path = os.path.join('PyScript', 'switch_to_chinese.py')
            self.lang_btn.setText('切换英文')
            self.language_toggle_state = 'zh'
        else:
            # 切换为英文
            script_path = os.path.join('PyScript', 'switch_to_english.py')
            self.lang_btn.setText('切换中文')
            self.language_toggle_state = 'en'
        
        try:
            with open(script_path, 'r', encoding='utf-8') as f:
                code = f.read()
            if self.send_to_ue:
                self.send_to_ue(code)
            if self.log_msg:
                if self.language_toggle_state == 'en':
                    self.log_msg('已发送切换为英文脚本')
                else:
                    self.log_msg('已发送切换为中文脚本')
        except Exception as e:
            if self.log_msg:
                self.log_msg(f'语言切换脚本发送失败: {e}', level='error')

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

    def run_sequencer_test(self):
        """旧方法保留兼容性"""
        self.run_sequencer_move()

    def run_sequencer_move(self):
        """运行轨道移动脚本，使用自定义帧数"""
        import os
        script_path = os.path.join('PyScript', 'sequencer_test.py')
        try:
            with open(script_path, 'r', encoding='utf-8') as f:
                script_content = f.read()
                
            # 获取用户设置的帧数
            frames = self.frames_input.value()
            
            # 替换脚本中的帧数值
            modified_script = script_content.replace("frame_number + 5", f"frame_number + {frames}")
            
            if self.send_to_ue:
                self.send_to_ue(modified_script)
            if self.log_msg:
                self.log_msg(f'已发送轨道移动脚本(移动{frames}帧)')
        except Exception as e:
            if self.log_msg:
                self.log_msg(f'轨道移动脚本发送失败: {e}', level='error') 