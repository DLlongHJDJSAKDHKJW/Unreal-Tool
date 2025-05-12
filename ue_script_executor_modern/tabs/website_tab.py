from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QGridLayout, QPushButton, QLabel, QHBoxLayout, QLineEdit
from ue_script_executor_modern.config import COLORS
import webbrowser
from PyQt5.QtCore import Qt

class WebsiteTab(QWidget):
    def __init__(self, parent=None, log_msg=None):
        super().__init__(parent)
        self.log_msg = log_msg
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        # 常用网站组
        website_group = QGroupBox("常用资源网站")
        website_group.setStyleSheet(f"border: 1px solid {COLORS['border']}; border-radius: 8px; background-color: {COLORS['panel']};")
        website_group_layout = QVBoxLayout(website_group)
        website_group_layout.setContentsMargins(10, 10, 10, 10)
        websites = [
            ("虚幻引擎官网", "https://www.unrealengine.com"),
            ("虚幻引擎文档", "https://docs.unrealengine.com"),
            ("虚幻引擎市场", "https://www.unrealengine.com/marketplace"),
            ("虚幻引擎论坛", "https://forums.unrealengine.com"),
            ("虚幻引擎问答", "https://answers.unrealengine.com"),
            ("GitHub", "https://github.com"),
            ("ArtStation", "https://www.artstation.com"),
            ("Sketchfab", "https://sketchfab.com")
        ]
        website_grid = QGridLayout()
        website_grid.setSpacing(10)
        for i, (name, url) in enumerate(websites):
            row, col = i // 2, i % 2
            web_btn = QPushButton(name)
            web_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {COLORS['card']};
                    color: {COLORS['text']};
                    border: 1px solid {COLORS['border']};
                    border-radius: 4px;
                    padding: 15px;
                    text-align: left;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background-color: {COLORS['primary']};
                    color: {COLORS['black']};
                }}
            """)
            web_btn.setCursor(Qt.PointingHandCursor)
            web_btn.clicked.connect(lambda checked=False, u=url: self.open_website(u))
            website_grid.addWidget(web_btn, row, col)
        website_group_layout.addLayout(website_grid)
        layout.addWidget(website_group)
        # 自定义链接
        custom_group = QGroupBox("添加自定义链接")
        custom_group.setStyleSheet(f"border: 1px solid {COLORS['border']}; border-radius: 8px; background-color: {COLORS['panel']};")
        custom_layout = QVBoxLayout(custom_group)
        custom_layout.setContentsMargins(10, 10, 10, 10)
        name_layout = QHBoxLayout()
        name_label = QLabel("网站名称:")
        name_label.setMinimumWidth(80)
        name_label.setStyleSheet("font-weight: bold;")
        name_layout.addWidget(name_label)
        self.website_name_edit = QLineEdit()
        self.website_name_edit.setPlaceholderText("输入网站名称")
        self.website_name_edit.setStyleSheet(f"border: 1px solid {COLORS['border']}; border-radius: 6px; padding: 8px; background-color: {COLORS['card']};")
        name_layout.addWidget(self.website_name_edit)
        custom_layout.addLayout(name_layout)
        url_layout = QHBoxLayout()
        url_label = QLabel("网站URL:")
        url_label.setMinimumWidth(80)
        url_label.setStyleSheet("font-weight: bold;")
        url_layout.addWidget(url_label)
        self.website_url_edit = QLineEdit()
        self.website_url_edit.setPlaceholderText("输入网站URL (例如: https://www.example.com)")
        self.website_url_edit.setStyleSheet(f"border: 1px solid {COLORS['border']}; border-radius: 6px; padding: 8px; background-color: {COLORS['card']};")
        url_layout.addWidget(self.website_url_edit)
        custom_layout.addLayout(url_layout)
        add_layout = QHBoxLayout()
        add_layout.addStretch()
        add_website_btn = QPushButton("添加网站")
        add_website_btn.setStyleSheet(f"background-color: {COLORS['success']}; color: white; border: none; border-radius: 4px; padding: 10px 20px; font-size: 14px; font-weight: bold;")
        add_website_btn.setCursor(Qt.PointingHandCursor)
        add_website_btn.clicked.connect(self.add_custom_website)
        add_layout.addWidget(add_website_btn)
        custom_layout.addLayout(add_layout)
        layout.addWidget(custom_group)
    def open_website(self, url):
        try:
            webbrowser.open(url)
            if self.log_msg:
                self.log_msg(f"已打开网站: {url}")
        except Exception as e:
            if self.log_msg:
                self.log_msg(f"打开网站失败: {e}", level="error")
    def add_custom_website(self):
        name = self.website_name_edit.text().strip()
        url = self.website_url_edit.text().strip()
        if not name or not url:
            if self.log_msg:
                self.log_msg("请输入网站名称和URL", level="warning")
            return
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
        try:
            webbrowser.open(url)
            self.website_name_edit.clear()
            self.website_url_edit.clear()
            if self.log_msg:
                self.log_msg(f"已添加并打开网站: {name}")
        except Exception as e:
            if self.log_msg:
                self.log_msg(f"打开网站失败: {e}", level="error") 