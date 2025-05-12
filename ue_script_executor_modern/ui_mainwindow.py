import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QWidget, QTabWidget, QHBoxLayout, QLabel, QPushButton, QMessageBox
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QPixmap
from ue_script_executor_modern.config import COLORS, STYLESHEET
from ue_script_executor_modern.tabs.tools_tab import ToolsTab
from ue_script_executor_modern.tabs.blueprint_tab import BlueprintTab
from ue_script_executor_modern.tabs.material_tab import MaterialTab
from ue_script_executor_modern.tabs.website_tab import WebsiteTab
from ue_script_executor_modern.tabs.console_tab import ConsoleTab
from ue_script_executor_modern.tabs.home_tab import HomeTab
from PyQt5.QtSvg import QSvgRenderer
from PyQt5.QtGui import QPainter

class ModernUEScriptExecutor(QMainWindow):
    def send_to_ue(self, code):
        import socket
        port = 9877
        if hasattr(self, 'home_tab') and hasattr(self.home_tab, 'get_port'):
            port = self.home_tab.get_port()
        print(f"[DEBUG] 即将发送到UE端口{port}: {code[:60]}...")
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(2)
                s.connect(('localhost', port))
                s.sendall(code.encode('utf-8'))
            print("[DEBUG] 命令已通过socket发送")
            if hasattr(self, 'log_msg') and self.log_msg:
                self.log_msg(f"命令已发送到UE端口{port}")
        except Exception as e:
            print(f"[DEBUG] 发送失败: {e}")
            if hasattr(self, 'log_msg') and self.log_msg:
                self.log_msg(f"发送失败: 无法连接到UE执行器: {e}")

    def __init__(self):
        super().__init__()
        self.setWindowTitle("虚幻引擎Python执行器")
        self.setStyleSheet(STYLESHEET)
        self.resize(500, 700)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setStyleSheet("QMainWindow { border-radius: 12px; background: transparent; }")
        central_widget = QWidget()
        central_widget.setStyleSheet("background-color: #282a36; border-radius: 12px;")
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        self.create_title_bar(main_layout)  # 先添加标题栏
        # 日志方法和脚本发送方法占位
        def log_msg(msg, level="info"):
            print(f"[{level}] {msg}")
        # 创建TabWidget
        self.tab_widget = QTabWidget()
        self.home_tab = HomeTab(log_msg=log_msg, send_to_ue=self.send_to_ue)
        self.home_tab.testConnectionRequested.connect(self.test_connection)
        self.home_tab.runTestCodeRequested.connect(self.run_test_code)
        self.home_tab.shutdownServerRequested.connect(self.shutdown_server)
        self.home_tab.copyExecutorScriptRequested.connect(self.copy_executor_script)
        self.tab_widget.addTab(self.home_tab, "主页")
        self.tab_widget.addTab(ToolsTab(log_msg=log_msg, send_to_ue=self.send_to_ue), "工具")
        self.tab_widget.addTab(BlueprintTab(log_msg=log_msg), "蓝图")
        self.tab_widget.addTab(MaterialTab(log_msg=log_msg), "材质")
        self.tab_widget.addTab(WebsiteTab(log_msg=log_msg), "网站")
        self.tab_widget.addTab(ConsoleTab(log_msg=log_msg), "控制台命令")
        main_layout.addWidget(self.tab_widget)
        # 优化TabWidget样式
        tab_style = """
        QTabWidget::pane {
            border: 1px solid #4a4d73;
            background-color: #282a36;
            margin-left: 4px;
            margin-right: 4px;
            margin-bottom: 0px;
        }
        QTabBar::tab {
            background-color: #2f3144;
            color: #e2e2f0;
            border: 1px solid #4a4d73;
            border-bottom: none;
            border-top-left-radius: 8px;
            border-top-right-radius: 8px;
            min-width: 60px;
            padding: 8px 18px;
            font-size: 14px;
            margin-right: 2px;
        }
        QTabBar::tab:selected {
            background-color: #373951;
            color: #fff;
            font-weight: bold;
            border-bottom: 2px solid #f7c325;
        }
        QTabBar::tab:hover {
            background-color: #44485a;
            color: #fff;
        }
        """
        self.tab_widget.setStyleSheet(tab_style)

    def create_title_bar(self, parent_layout):
        title_bar = QWidget()
        title_bar.setFixedHeight(30)
        title_bar.setStyleSheet(f"background-color: {COLORS['background']}; border-top-left-radius: 18px; border-top-right-radius: 18px; border-bottom: 1px solid {COLORS['border']};")
        title_layout = QHBoxLayout(title_bar)
        title_layout.setContentsMargins(8, 0, 8, 0)
        title_layout.setSpacing(6)
        title_label = QLabel("虚幻引擎Python执行器")
        title_label.setStyleSheet(f"color: {COLORS['primary']}; font-weight: bold; font-size: 13px;")
        title_layout.addWidget(title_label)
        version_label = QLabel("v2.3")
        version_label.setStyleSheet(f"color: {COLORS['light']}; padding-top: 1px; font-size: 11px;")
        title_layout.addWidget(version_label)
        title_layout.addStretch()
        self.pin_button = QPushButton()
        self.pin_button.setFixedSize(24, 24)
        self.pin_button.setCheckable(True)
        self.pin_button.setChecked(False)
        self.pin_button.setToolTip("窗口置顶")
        self.pin_button.setStyleSheet(f"QPushButton {{background-color: transparent; border: none;}} QPushButton:checked {{background-color: transparent;}}");
        svg_pin_off = '''
        <svg width="20" height="20" viewBox="0 0 20 20">
          <path d="M10 2 L13 7 L17 8 L16 10 L12 9 L10 18 L8 9 L4 10 L3 8 L7 7 Z" fill="#e2e2f0" stroke="#e2e2f0" stroke-width="1.5"/>
        </svg>
        '''
        svg_pin_on = '''
        <svg width="20" height="20" viewBox="0 0 20 20">
          <path d="M10 2 L13 7 L17 8 L16 10 L12 9 L10 18 L8 9 L4 10 L3 8 L7 7 Z" fill="#f7c325" stroke="#f7c325" stroke-width="1.5"/>
        </svg>
        '''
        def svg_icon(svg):
            pixmap = QPixmap(16, 16)
            pixmap.fill(Qt.transparent)
            renderer = QSvgRenderer(bytearray(svg, encoding='utf-8'))
            painter = QPainter(pixmap)
            renderer.render(painter)
            painter.end()
            return QIcon(pixmap)
        self.pin_icon = svg_icon(svg_pin_off)
        self.pin_icon_on = svg_icon(svg_pin_on)
        self.pin_button.setIcon(self.pin_icon)
        self.pin_button.setIconSize(QSize(20, 20))
        self.pin_button.setText("")
        self.pin_button.clicked.connect(self.toggle_window_top_icon)
        title_layout.addWidget(self.pin_button)
        min_button = QPushButton("＿")
        min_button.setFixedSize(28, 26)
        min_button.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent; color: {COLORS['text']}; border: none; border-radius: 3px; font-weight: bold; font-size: 15px;
            }}
            QPushButton:hover {{
                background-color: #44485a;
            }}
        """)
        min_button.clicked.connect(self.showMinimized)
        min_button.setCursor(Qt.PointingHandCursor)
        max_button = QPushButton("◻")
        max_button.setFixedSize(28, 26)
        max_button.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent; color: {COLORS['text']}; border: none; border-radius: 3px; font-weight: bold; font-size: 15px;
            }}
            QPushButton:hover {{
                background-color: #44485a;
            }}
        """)
        max_button.clicked.connect(self.toggle_maximize)
        max_button.setCursor(Qt.PointingHandCursor)
        close_button = QPushButton("✕")
        close_button.setFixedSize(28, 26)
        close_button.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent; color: {COLORS['text']}; border: none; border-radius: 3px; font-weight: bold; font-size: 15px;
            }}
            QPushButton:hover {{
                background-color: #e05c5c; color: white;
            }}
        """)
        close_button.clicked.connect(self.close_application)
        close_button.setCursor(Qt.PointingHandCursor)
        title_layout.addWidget(min_button)
        title_layout.addWidget(max_button)
        title_layout.addWidget(close_button)
        parent_layout.addWidget(title_bar)
        title_bar.mousePressEvent = self.title_bar_mouse_press
        title_bar.mouseMoveEvent = self.title_bar_mouse_move
        title_bar.mouseDoubleClickEvent = self.title_bar_double_click

        def svg_icon(svg_str):
            pixmap = QPixmap(20, 20)
            pixmap.fill(Qt.transparent)
            renderer = QSvgRenderer(bytearray(svg_str, encoding='utf-8'))
            painter = QPainter(pixmap)
            renderer.render(painter)
            painter.end()
            return QIcon(pixmap)
        svg_min = '''
        <svg width="20" height="20" viewBox="0 0 20 20">
          <rect x="4" y="10" width="12" height="2" rx="1" fill="#e2e2f0"/>
        </svg>
        '''
        svg_max = '''
        <svg width="20" height="20" viewBox="0 0 20 20">
          <rect x="4" y="4" width="12" height="12" rx="2" fill="none" stroke="#e2e2f0" stroke-width="2"/>
        </svg>
        '''
        svg_close = '''
        <svg width="20" height="20" viewBox="0 0 20 20">
          <line x1="5" y1="5" x2="15" y2="15" stroke="#e2e2f0" stroke-width="2"/>
          <line x1="15" y1="5" x2="5" y2="15" stroke="#e2e2f0" stroke-width="2"/>
        </svg>
        '''
        min_button.setIcon(svg_icon(svg_min))
        max_button.setIcon(svg_icon(svg_max))
        close_button.setIcon(svg_icon(svg_close))
        min_button.setText("")
        max_button.setText("")
        close_button.setText("")

    def toggle_window_top_icon(self):
        """切换窗口置顶状态，并切换图标"""
        if self.pin_button.isChecked():
            self.setWindowFlag(Qt.WindowStaysOnTopHint, True)
            self.pin_button.setIcon(self.pin_icon_on)
        else:
            self.setWindowFlag(Qt.WindowStaysOnTopHint, False)
            self.pin_button.setIcon(self.pin_icon)
        self.show()

    def toggle_maximize(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def close_application(self):
        self.close()

    def title_bar_mouse_press(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_pos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def title_bar_mouse_move(self, event):
        if hasattr(self, '_drag_pos') and event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self._drag_pos)
            event.accept()

    def title_bar_double_click(self, event):
        self.toggle_maximize()

    def test_connection(self):
        test_code = 'unreal.log("UE执行器连接测试成功!")'
        import socket
        port = self.home_tab.get_port() if hasattr(self, 'home_tab') else 9876
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(2)
                s.connect(('localhost', port))
                s.sendall(test_code.encode('utf-8'))
            self.home_tab.port_display.setText(f"端口: 已连接")
            self.home_tab.port_display.setStyleSheet("font-weight: bold; color: #44DD44; font-size: 15px; padding: 5px;")
            self.home_tab.set_connected(True)
            if hasattr(self, 'log_msg') and self.log_msg:
                self.log_msg("已连接到虚幻引擎")
        except Exception as e:
            self.home_tab.port_display.setText(f"端口: 未连接")
            self.home_tab.port_display.setStyleSheet("font-weight: bold; color: #e74c3c; font-size: 15px; padding: 5px;")
            self.home_tab.set_connected(False)
            if hasattr(self, 'log_msg') and self.log_msg:
                self.log_msg(f"连接失败: {e}")

    def run_test_code(self):
        try:
            script_path = "PyScript/test_script.py"
            with open(script_path, "r", encoding="utf-8") as f:
                code = f.read()
            self.send_to_ue(code)
            if hasattr(self, 'log_msg') and self.log_msg:
                self.log_msg("已发送测试脚本内容到UE")
        except Exception as e:
            if hasattr(self, 'log_msg') and self.log_msg:
                self.log_msg(f"运行测试失败: {e}")

    def shutdown_server(self):
        try:
            self.send_to_ue("SHUTDOWN_SERVER")
            if hasattr(self, 'log_msg') and self.log_msg:
                self.log_msg("已发送退出服务器命令到UE")
            # 断开后端口状态变红色"端口: 已断开"
            if hasattr(self, 'home_tab'):
                self.home_tab.port_display.setText("端口: 已断开")
                self.home_tab.port_display.setStyleSheet("font-weight: bold; color: #e74c3c; font-size: 15px; padding: 5px;")
                self.home_tab.set_connected(False)
        except Exception as e:
            if hasattr(self, 'log_msg') and self.log_msg:
                self.log_msg(f"退出服务器失败: {e}")

    def copy_executor_script(self):
        from PyQt5.QtWidgets import QApplication
        try:
            with open("UESimpleExecutor.py", "r", encoding="utf-8") as f:
                script = f.read()
            clipboard = QApplication.clipboard()
            clipboard.setText(script)
            if hasattr(self, 'log_msg') and self.log_msg:
                self.log_msg("已复制执行器脚本到剪贴板")
        except Exception as e:
            if hasattr(self, 'log_msg') and self.log_msg:
                self.log_msg(f"复制失败: 无法读取UESimpleExecutor.py: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ModernUEScriptExecutor()
    window.show()
    sys.exit(app.exec_()) 