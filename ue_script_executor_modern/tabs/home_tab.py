from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QHBoxLayout, QPushButton, QLabel, QLineEdit, QTextEdit
from ue_script_executor_modern.config import COLORS
from PyQt5.QtCore import Qt, pyqtSignal

class HomeTab(QWidget):
    testConnectionRequested = pyqtSignal()
    runTestCodeRequested = pyqtSignal()
    shutdownServerRequested = pyqtSignal()
    copyExecutorScriptRequested = pyqtSignal()
    def __init__(self, parent=None, log_msg=None, send_to_ue=None):
        super().__init__(parent)
        self.log_msg = log_msg
        self.send_to_ue = send_to_ue
        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(6)
        # 连接设置分组
        connection_group = QGroupBox("连接设置")
        connection_group.setStyleSheet(f"border: 1px solid {COLORS['border']}; border-radius: 8px; background-color: {COLORS['panel']};")
        group_layout = QVBoxLayout(connection_group)
        group_layout.setContentsMargins(4, 4, 4, 4)
        group_layout.setSpacing(4)
        row1 = QHBoxLayout()
        row1.setSpacing(8)
        self.port_display = QLabel("端口: 未连接")
        self.port_display.setStyleSheet("font-weight: bold; color: #e2e2f0; font-size: 15px; padding: 5px;")
        row1.insertWidget(0, self.port_display)
        port_label = QLabel("端口:")
        port_label.setStyleSheet("font-size: 17px; font-weight: bold; color: #e2e2f0;")
        self.port_input = QLineEdit()
        self.port_input.setText("9876")
        self.port_input.setFixedWidth(70)
        self.port_input.setStyleSheet("font-size: 17px; font-weight: bold; color: #e2e2f0; padding: 4px 8px; border-radius: 6px;")
        row1.insertWidget(1, port_label)
        row1.insertWidget(2, self.port_input)
        copy_button = QPushButton("复制执行器脚本")
        copy_button.setMinimumHeight(44)
        copy_button.setMinimumWidth(140)
        copy_button.setStyleSheet(f"background-color: {COLORS['card']}; color: {COLORS['text']}; border-radius: 4px; font-weight: bold;")
        copy_button.clicked.connect(self.copyExecutorScriptRequested.emit)
        row1.addWidget(self.port_display)
        row1.addStretch(1)
        row1.addWidget(copy_button)
        group_layout.addLayout(row1)
        # 清理多余按钮，只保留一组
        row2 = QHBoxLayout()
        row2.setSpacing(12)
        btn_connect = QPushButton("连接虚幻")
        btn_connect.setMinimumHeight(40)
        btn_connect.setMinimumWidth(80)
        btn_connect.setStyleSheet(f"QPushButton {{background-color: {COLORS['card']}; color: {COLORS['text']}; border-radius: 4px; font-weight: bold;}} QPushButton:hover {{background-color: #44485a; color: #fff;}} QPushButton:pressed {{background-color: #23232b; color: #fff;}}")
        btn_connect.clicked.connect(self.testConnectionRequested.emit)
        self.connect_btn = btn_connect
        row2.addWidget(btn_connect)
        btn_run = QPushButton("运行测试")
        btn_run.setMinimumHeight(40)
        btn_run.setMinimumWidth(80)
        btn_run.setStyleSheet(f"QPushButton {{background-color: {COLORS['card']}; color: {COLORS['text']}; border-radius: 4px; font-weight: bold;}} QPushButton:hover {{background-color: #44485a; color: #fff;}} QPushButton:pressed {{background-color: #23232b; color: #fff;}}")
        btn_run.clicked.connect(self.runTestCodeRequested.emit)
        row2.addWidget(btn_run)
        btn_shutdown = QPushButton("退出服务器")
        btn_shutdown.setMinimumHeight(40)
        btn_shutdown.setMinimumWidth(80)
        btn_shutdown.setStyleSheet(f"QPushButton {{background-color: {COLORS['card']}; color: {COLORS['text']}; border-radius: 4px; font-weight: bold;}} QPushButton:hover {{background-color: #44485a; color: #fff;}} QPushButton:pressed {{background-color: #23232b; color: #fff;}}")
        btn_shutdown.clicked.connect(self.shutdownServerRequested.emit)
        row2.addWidget(btn_shutdown)
        group_layout.addLayout(row2)
        # 授权码系统分组
        auth_group = QGroupBox("授权码系统")
        auth_group.setStyleSheet(f"border: 1px solid {COLORS['border']}; border-radius: 8px; background-color: {COLORS['panel']};")
        auth_layout = QHBoxLayout(auth_group)
        auth_layout.setContentsMargins(6, 6, 6, 6)
        auth_layout.setSpacing(6)
        self.auth_input = QLineEdit()
        self.auth_input.setPlaceholderText("请输入授权码")
        self.auth_input.setMinimumWidth(120)
        self.auth_input.setMaximumWidth(160)
        self.auth_input.setStyleSheet("font-size:14px;padding:6px 8px;border-radius:6px;")
        auth_btn = QPushButton("验证/复制")
        auth_btn.setMinimumWidth(70)
        auth_btn.setStyleSheet(f"background-color: {COLORS['card']}; color: {COLORS['text']}; border-radius: 4px; font-weight: bold;")
        auth_btn.clicked.connect(lambda: self.log_msg("授权码已处理（示例）"))
        self.auth_display = QLabel("未验证")
        self.auth_display.setStyleSheet("font-size:14px;font-weight:bold;padding:0 8px;")
        auth_layout.addWidget(QLabel("授权码:"))
        auth_layout.addWidget(self.auth_input)
        auth_layout.addWidget(auth_btn)
        auth_layout.addWidget(self.auth_display)
        group_layout.addWidget(auth_group)
        layout.addWidget(connection_group)
        # 一键清理/重置分组
        clean_group = QGroupBox("一键清理/重置")
        clean_group.setStyleSheet(f"border: 1px solid {COLORS['border']}; border-radius: 8px; background-color: {COLORS['panel']};")
        clean_layout = QHBoxLayout(clean_group)
        clean_layout.setContentsMargins(6, 4, 6, 4)
        clean_layout.setSpacing(6)
        btn_clear_log = QPushButton("清空日志")
        btn_clear_log.setMinimumHeight(40)
        btn_clear_log.setStyleSheet(f"background-color: {COLORS['card']}; color: {COLORS['text']}; border-radius: 4px; font-weight: bold;")
        btn_clear_log.clicked.connect(lambda: self.home_log.clear())
        btn_reset = QPushButton("重置界面")
        btn_reset.setMinimumHeight(40)
        btn_reset.setStyleSheet(f"background-color: {COLORS['card']}; color: {COLORS['text']}; border-radius: 4px; font-weight: bold;")
        btn_reset.clicked.connect(lambda: self.log_msg("界面已重置（示例）"))
        clean_layout.addWidget(btn_clear_log)
        clean_layout.addWidget(btn_reset)
        layout.addWidget(clean_group)
        # 版本信息与更新检测分组
        version_group = QGroupBox("版本信息与更新检测")
        version_group.setStyleSheet(f"border: 1px solid {COLORS['border']}; border-radius: 8px; background-color: {COLORS['panel']};")
        version_layout = QHBoxLayout(version_group)
        version_layout.setContentsMargins(6, 4, 6, 4)
        version_layout.setSpacing(6)
        version_label = QLabel("当前版本: v2.3")
        version_label.setStyleSheet("font-size:13px;color:#CCCCCC;")
        btn_check_update = QPushButton("检查更新")
        btn_check_update.setMinimumHeight(40)
        btn_check_update.setStyleSheet(f"background-color: {COLORS['card']}; color: {COLORS['text']}; border-radius: 4px; font-weight: bold;")
        btn_check_update.clicked.connect(lambda: self.log_msg("已是最新版本（示例）"))
        version_layout.addWidget(version_label)
        version_layout.addWidget(btn_check_update)
        layout.addWidget(version_group)
        # 日志区
        log_group = QGroupBox("操作日志")
        log_group.setStyleSheet(f"border: 1px solid {COLORS['border']}; border-radius: 8px; background-color: {COLORS['panel']};")
        log_layout = QVBoxLayout(log_group)
        log_layout.setContentsMargins(6, 4, 6, 4)
        log_layout.setSpacing(4)
        self.home_log = QTextEdit()
        self.home_log.setReadOnly(True)
        self.home_log.setMinimumHeight(60)
        self.home_log.setMaximumHeight(180)
        self.home_log.setStyleSheet(f"background-color:{COLORS['panel']};color:{COLORS['text']};border-radius:6px;font-size:13px;padding:4px 10px;")
        log_layout.addWidget(self.home_log)
        layout.addWidget(log_group)
        # 使用说明
        desc = QLabel(
            "<b>使用说明：</b><br>"
            "1. 启动虚幻引擎并确保已启用Python插件。<br>"
            "2. 点击\"复制执行器脚本\"，在UE的Python控制台粘贴并执行。<br>"
            "3. 回到本工具，点击\"测试连接\"确保通信正常。<br>"
            "4. 你可以在下方各功能页中批量执行脚本、管理资产、快速调试。<br>"
            "5. 授权码系统可用于高级功能解锁或团队协作授权。<br>"
        )
        desc.setWordWrap(True)
        desc.setStyleSheet("color: #CCCCCC; font-size: 12px; margin-top: 4px;")
        layout.addStretch(1)
        layout.addWidget(desc)
        # 优化所有按钮交互样式
        btn_style = f"""
            QPushButton {{
                background-color: {COLORS['card']};
                color: {COLORS['text']};
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
                padding: 8px 0;
                border: 1px solid {COLORS['border']};
                box-shadow: 0 2px 8px #00000022;
            }}
            QPushButton:hover {{
                background-color: #44485a;
                color: #fff;
            }}
            QPushButton:pressed {{
                background-color: #23232b;
                color: #fff;
            }}
        """
        copy_button.setStyleSheet(btn_style)
        btn_clear_log.setStyleSheet(btn_style)
        btn_reset.setStyleSheet(btn_style)
        btn_check_update.setStyleSheet(btn_style)
        # 记录所有功能按钮
        self.copy_button = copy_button
        self.auth_btn = auth_btn
        self.btn_check_update = btn_check_update
        self.all_buttons = [btn_connect, btn_run, btn_shutdown, btn_clear_log, btn_reset, btn_check_update, copy_button, auth_btn]
        # 连接状态控制
        self.connected = False

    def copy_executor_script(self):
        from PyQt5.QtWidgets import QApplication
        script = (
            "import unreal\n"
            "# 这里是你的执行器脚本内容，可以替换为实际内容\n"
            "unreal.log('执行器脚本已复制')\n"
        )
        clipboard = QApplication.clipboard()
        clipboard.setText(script)
        if self.log_msg:
            self.log_msg("已复制执行器脚本到剪贴板")

    def get_port(self):
        try:
            return int(self.port_input.text())
        except Exception:
            return 9877

    def set_connected(self, connected):
        self.connected = connected
        # 只允许这些按钮始终可用
        allow = [self.copy_button, self.auth_input, self.auth_btn, self.btn_check_update, self.connect_btn]
        for btn in self.all_buttons:
            if btn in allow:
                btn.setEnabled(True)
            else:
                btn.setEnabled(connected)
        # 再次确保连接虚幻按钮始终可用
        if hasattr(self, 'connect_btn'):
            self.connect_btn.setEnabled(True) 