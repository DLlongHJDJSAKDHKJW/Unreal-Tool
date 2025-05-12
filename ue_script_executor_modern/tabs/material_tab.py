from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QGridLayout, QFrame, QLabel, QPushButton, QHBoxLayout, QLineEdit
from PyQt5.QtCore import Qt
from ue_script_executor_modern.config import COLORS

class MaterialTab(QWidget):
    def __init__(self, parent=None, log_msg=None):
        super().__init__(parent)
        self.log_msg = log_msg
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        # 材质预设组
        material_group = QGroupBox("材质预设")
        material_group.setStyleSheet(f"border: 1px solid {COLORS['border']}; border-radius: 8px; background-color: {COLORS['panel']};")
        material_group_layout = QVBoxLayout(material_group)
        material_group_layout.setContentsMargins(10, 10, 10, 10)
        material_grid = QGridLayout()
        material_grid.setSpacing(12)
        material_presets = [
            ("金属", "metallic.png"),
            ("木材", "wood.png"),
            ("布料", "fabric.png"),
            ("玻璃", "glass.png"),
            ("水面", "water.png"),
            ("皮革", "leather.png"),
            ("塑料", "plastic.png"),
            ("岩石", "stone.png")
        ]
        for i, (name, _) in enumerate(material_presets):
            row, col = i // 4, i % 4
            card = QFrame()
            card.setStyleSheet(f"""
                QFrame {{
                    background-color: {COLORS['card']};
                    border-radius: 8px;
                    border: 1px solid {COLORS['border']};
                }}
                QFrame:hover {{
                    border: 1px solid {COLORS['primary']};
                }}
            """)
            card_layout = QVBoxLayout(card)
            card_layout.setContentsMargins(10, 10, 10, 10)
            card_layout.setSpacing(8)
            image_placeholder = QLabel(f"[{name}预览]")
            image_placeholder.setAlignment(Qt.AlignCenter)
            image_placeholder.setMinimumHeight(60)
            image_placeholder.setStyleSheet(f"background-color: #3a3a3a; color: {COLORS['text']}; border-radius: 4px;")
            card_layout.addWidget(image_placeholder)
            name_label = QLabel(name)
            name_label.setAlignment(Qt.AlignCenter)
            name_label.setStyleSheet("font-weight: bold;")
            card_layout.addWidget(name_label)
            apply_btn = QPushButton("应用")
            apply_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {COLORS['primary']};
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 5px;
                }}
                QPushButton:hover {{
                    background-color: {COLORS['secondary']};
                }}
            """)
            apply_btn.setCursor(Qt.PointingHandCursor)
            apply_btn.clicked.connect(self.dummy_function)
            card_layout.addWidget(apply_btn)
            material_grid.addWidget(card, row, col)
        material_group_layout.addLayout(material_grid)
        layout.addWidget(material_group)
        # 材质参数调整
        params_group = QGroupBox("材质参数调整")
        params_group.setStyleSheet(f"border: 1px solid {COLORS['border']}; border-radius: 8px; background-color: {COLORS['panel']};")
        params_layout = QVBoxLayout(params_group)
        params_layout.setContentsMargins(10, 10, 10, 10)
        params = [
            ("Base Color", "RGB(255, 255, 255)"),
            ("Metallic", "0.0"),
            ("Roughness", "0.5"),
            ("Specular", "0.5"),
            ("Emissive", "RGB(0, 0, 0)")
        ]
        for param, value in params:
            param_layout = QHBoxLayout()
            param_label = QLabel(param)
            param_label.setMinimumWidth(100)
            param_label.setStyleSheet("font-weight: bold;")
            param_layout.addWidget(param_label)
            param_value = QLineEdit(value)
            param_value.setStyleSheet(f"border: 1px solid {COLORS['border']}; border-radius: 4px; padding: 5px; background-color: {COLORS['card']};")
            param_layout.addWidget(param_value)
            apply_param_btn = QPushButton("设置")
            apply_param_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {COLORS['primary']};
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 5px 10px;
                }}
                QPushButton:hover {{
                    background-color: {COLORS['secondary']};
                }}
            """)
            apply_param_btn.clicked.connect(self.dummy_function)
            param_layout.addWidget(apply_param_btn)
            params_layout.addLayout(param_layout)
        layout.addWidget(params_group)
    def dummy_function(self):
        if self.log_msg:
            self.log_msg("此功能尚未实现", level="warning") 