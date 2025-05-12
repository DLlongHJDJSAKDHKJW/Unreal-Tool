# 颜色与样式配置
COLORS = {
    "primary": "#ffffff",      # 主色改为白色
    "secondary": "#7d3c98",    # 深紫色
    "success": "#2ecc71",      # 鲜绿色
    "warning": "#f39c12",      # 橙色
    "danger": "#e74c3c",       # 红色
    "dark": "#1e1e2e",         # 深紫蓝背景
    "light": "#d1c4e9",        # 浅紫色
    "background": "#282a36",   # 暗色背景
    "panel": "#2f3144",        # 面板背景
    "card": "#373951",         # 卡片背景
    "white": "#ffffff",        # 白色
    "text": "#e2e2f0",         # 文本颜色
    "black": "#191927",        # 深色
    "border": "#4a4d73"        # 边框颜色
}

STYLESHEET = f"""
QMainWindow {{
    background-color: {COLORS["background"]};
}}
QWidget {{
    font-family: 'Segoe UI', Arial, sans-serif;
}}
QLabel {{
    color: {COLORS["text"]};
    font-size: 13px;
}}
QTabWidget::pane {{
    border: 1px solid {COLORS["border"]};
    border-radius: 4px;
    background-color: {COLORS["panel"]};
}}
QTabBar::tab {{
    background-color: {COLORS["panel"]};
    color: {COLORS["text"]};
    border: 1px solid {COLORS["border"]};
    border-bottom-color: {COLORS["panel"]};
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
    min-width: 100px;
    padding: 8px;
    font-size: 13px;
}}
QTabBar::tab:selected {{
    background-color: {COLORS["card"]};
    border-bottom-color: {COLORS["card"]};
    color: {COLORS["primary"]};
    font-weight: bold;
}}
QTabBar::tab:hover {{
    background-color: {COLORS["card"]};
}}
QPushButton {{
    background-color: {COLORS["primary"]};
    color: {COLORS["white"]};
    border: none;
    border-radius: 4px;
    padding: 8px 16px;
    font-size: 13px;
    font-weight: bold;
}}
QPushButton:hover {{
    background-color: {COLORS["secondary"]};
    border: 1px solid {COLORS["light"]};
}}
QPushButton:pressed {{
    background-color: #4a2b88;
    padding-top: 9px;
    padding-left: 17px;
}}
QPushButton:focus {{
    border: 1px solid {COLORS["light"]};
}}
QPushButton#success {{
    background-color: {COLORS["success"]};
}}
QPushButton#success:hover {{
    background-color: #27ae60;
    border: 1px solid #a5d6a7;
}}
QPushButton#success:pressed {{
    background-color: #1e8449;
    padding-top: 9px;
    padding-left: 17px;
}}
QPushButton#danger {{
    background-color: {COLORS["danger"]};
}}
QPushButton#danger:hover {{
    background-color: #c0392b;
    border: 1px solid #ffcdd2;
}}
QPushButton#danger:pressed {{
    background-color: #a93226;
    padding-top: 9px;
    padding-left: 17px;
}}
QPushButton#warning {{
    background-color: {COLORS["warning"]};
}}
QPushButton#warning:hover {{
    background-color: #d35400;
    border: 1px solid #ffe0b2;
}}
QPushButton#warning:pressed {{
    background-color: #ba4a00;
    padding-top: 9px;
    padding-left: 17px;
}}
QPushButton:disabled {{
    background-color: #555566;
    color: #aaaaaa;
}}
QTextEdit, QLineEdit, QComboBox {{
    border: 1px solid {COLORS["border"]};
    border-radius: 4px;
    padding: 8px;
    background-color: {COLORS["card"]};
    color: {COLORS["text"]};
}}
QTextEdit:focus, QLineEdit:focus, QComboBox:focus {{
    border: 1px solid {COLORS["primary"]};
}}
QStatusBar {{
    background-color: {COLORS["dark"]};
    color: {COLORS["white"]};
    font-size: 13px;
    padding: 4px;
}}
QGroupBox {{
    border: 1px solid {COLORS["border"]};
    border-radius: 8px;
    margin-top: 16px;
    padding: 10px;
    font-weight: bold;
    background-color: {COLORS["panel"]};
    color: {COLORS["text"]};
}}
QGroupBox::title {{
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0 6px;
    color: {COLORS["white"]};
}}
QToolBar {{
    background-color: {COLORS["primary"]};
    border: none;
    spacing: 3px;
    padding: 3px;
}}
QToolButton {{
    background-color: transparent;
    border: none;
    border-radius: 4px;
    padding: 8px;
    color: {COLORS["white"]};
    font-weight: bold;
}}
QToolButton:hover {{
    background-color: {COLORS["secondary"]};
}}
QCheckBox {{
    color: {COLORS["text"]};
}}
QCheckBox::indicator:checked {{
    background-color: {COLORS["primary"]};
    border: 2px solid {COLORS["primary"]};
    width: 14px;
    height: 14px;
}}
""" 