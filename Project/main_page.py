# main_page.py

import sys
import json
import os
from datetime import datetime

from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QSizePolicy, QStackedWidget,
    QStatusBar, QLabel, QFrame
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont

from styles import *
from Pages.home_page import HomePage
from Pages.production_page import ProductionPage
from Pages.tf_management_page import TFManagementPage
from Pages.production_data_page import ProductionDataPage
from plc_handler import PLCHandler


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Cutting Machine Control System")
        self.setStyleSheet(MAIN_WINDOW_STYLE)

        # UI References
        self.left_status = None
        self.plc_indicator = None
        self.plc_status_label = None
        self.plc_ip_label = None
        self.system_status = None
        self.datetime_label = None
        self.uptime_label = None

        # Main Layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.setup_top_bar(main_layout)
        self.setup_content_area(main_layout)
        self.setup_bottom_status_bar(main_layout)

        self.setup_timers()
        self.init_plc()

        self.activate_top_button("Home")

    # =========================================================
    # TOP BAR
    # =========================================================
    def setup_top_bar(self, main_layout):
        topbar = QFrame()
        topbar.setStyleSheet(TOPBAR_STYLE)
        topbar.setFixedHeight(80)

        topbar_layout = QHBoxLayout(topbar)
        topbar_layout.setContentsMargins(10, 5, 10, 5)

        self.stack = QStackedWidget()

        self.pages = {
            "Home": HomePage(),
            "Production": ProductionPage(self),
            "TF Management": TFManagementPage(),
            "Production Data": ProductionDataPage()
        }

        self.pages["Production Data"].set_production_page_reference(
            self.pages["Production"]
        )

        for page in self.pages.values():
            self.stack.addWidget(page)

        buttons_container = QWidget()
        buttons_layout = QHBoxLayout(buttons_container)
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        buttons_layout.setSpacing(5)

        self.top_buttons = {}

        for name in self.pages.keys():
            btn = QPushButton(name)
            btn.setFixedHeight(60)
            btn.setMinimumWidth(120)
            btn.setSizePolicy(
                QSizePolicy.Policy.Expanding,
                QSizePolicy.Policy.Expanding
            )

            btn.setStyleSheet(TOPBAR_BUTTON_STYLE)

            btn.clicked.connect(
                lambda checked, n=name: self.activate_top_button(n)
            )

            buttons_layout.addWidget(btn)
            self.top_buttons[name] = btn

        topbar_layout.addWidget(buttons_container)

        main_layout.addWidget(topbar)

    # =========================================================
    # CONTENT AREA
    # =========================================================
    def setup_content_area(self, main_layout):
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        # Sidebar
        sidebar = QFrame()
        sidebar.setStyleSheet(SIDEBAR_STYLE)
        sidebar.setFixedWidth(180)

        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(10, 10, 10, 10)
        sidebar_layout.setSpacing(10)

        self.sidebar_buttons = {}

        for name, color in SIDEBAR_BUTTON_COLORS.items():
            btn = QPushButton(name)

            btn.setMinimumHeight(50)

            btn.setSizePolicy(
                QSizePolicy.Policy.Expanding,
                QSizePolicy.Policy.Expanding
            )

            btn.setStyleSheet(
                SIDEBAR_BUTTON_STYLE.format(bg=color)
            )

            sidebar_layout.addWidget(btn)

            self.sidebar_buttons[name] = btn

        # Disable buttons initially
        for name, btn in self.sidebar_buttons.items():
            if name not in ["Restore", "Reset"]:
                btn.setEnabled(False)
                btn.setStyleSheet(
                    SIDEBAR_BUTTON_STYLE.format(bg="#A0A0A0")
                )

        # Enable controls
        def enable_all_buttons():
            for name, btn in self.sidebar_buttons.items():
                btn.setEnabled(True)
                btn.setStyleSheet(
                    SIDEBAR_BUTTON_STYLE.format(
                        bg=SIDEBAR_BUTTON_COLORS[name]
                    )
                )

            self.update_status_message(
                "All controls enabled",
                "success"
            )

        # Button Connections
        self.sidebar_buttons["Restore"].clicked.connect(enable_all_buttons)
        self.sidebar_buttons["Reset"].clicked.connect(enable_all_buttons)

        self.sidebar_buttons["Start"].clicked.connect(
            lambda: self.send_plc_command("START")
        )

        self.sidebar_buttons["Stop"].clicked.connect(
            lambda: self.send_plc_command("STOP")
        )

        self.sidebar_buttons["Production"].clicked.connect(
            lambda: self.activate_top_button("Production")
        )

        self.sidebar_buttons["Supply"].clicked.connect(
            lambda: self.update_status_message(
                "Supply mode activated",
                "info"
            )
        )

        content_layout.addWidget(sidebar, 0)
        content_layout.addWidget(self.stack, 1)

        main_layout.addLayout(content_layout)

    # =========================================================
    # STATUS BAR
    # =========================================================
    def setup_bottom_status_bar(self, main_layout):
        self.status_bar = QStatusBar()

        self.status_bar.setStyleSheet(STATUS_BAR_STYLE)
        self.status_bar.setFixedHeight(35)

        # Left Status
        self.left_status = QLabel("✅ System Ready")
        self.left_status.setStyleSheet(STATUS_LEFT_STYLE)

        self.status_bar.addWidget(self.left_status, 2)

        # PLC Section
        plc_container = QFrame()
        plc_container.setStyleSheet(PLC_CONTAINER_STYLE)

        plc_layout = QHBoxLayout(plc_container)
        plc_layout.setContentsMargins(10, 2, 10, 2)
        plc_layout.setSpacing(10)

        self.plc_indicator = QLabel("🔴")
        self.plc_indicator.setStyleSheet(PLC_INDICATOR_STYLE)

        self.plc_status_label = QLabel("PLC: DISCONNECTED")
        self.plc_status_label.setStyleSheet(
            PLC_STATUS_DISCONNECTED_STYLE
        )

        self.plc_ip_label = QLabel("")
        self.plc_ip_label.setStyleSheet(PLC_IP_STYLE)

        plc_layout.addWidget(self.plc_indicator)
        plc_layout.addWidget(self.plc_status_label)
        plc_layout.addWidget(self.plc_ip_label)
        plc_layout.addStretch()

        self.status_bar.addPermanentWidget(plc_container, 1)

        # Right Side
        right_container = QWidget()

        right_layout = QHBoxLayout(right_container)
        right_layout.setContentsMargins(0, 0, 10, 0)
        right_layout.setSpacing(15)

        self.system_status = QLabel("⏸️")
        self.system_status.setStyleSheet(SYSTEM_STATUS_STYLE)

        right_layout.addWidget(self.system_status)

        sep1 = QLabel("|")
        sep1.setStyleSheet(SEPARATOR_STYLE)

        right_layout.addWidget(sep1)

        self.datetime_label = QLabel("")
        self.datetime_label.setStyleSheet(DATETIME_STYLE)

        right_layout.addWidget(self.datetime_label)

        sep2 = QLabel("|")
        sep2.setStyleSheet(SEPARATOR_STYLE)

        right_layout.addWidget(sep2)

        self.uptime_label = QLabel("Uptime: 00:00:00")
        self.uptime_label.setStyleSheet(UPTIME_STYLE)

        right_layout.addWidget(self.uptime_label)

        self.status_bar.addPermanentWidget(right_container)

        main_layout.addWidget(self.status_bar)

    # =========================================================
    # TIMERS
    # =========================================================
    def setup_timers(self):
        self.datetime_timer = QTimer()
        self.datetime_timer.timeout.connect(self.update_datetime)
        self.datetime_timer.start(1000)

        self.start_time = datetime.now()

        self.uptime_timer = QTimer()
        self.uptime_timer.timeout.connect(self.update_uptime)
        self.uptime_timer.start(1000)

        self.status_clear_timer = QTimer()
        self.status_clear_timer.setSingleShot(True)

        self.update_datetime()
        self.update_uptime()

    # =========================================================
    # PLC
    # =========================================================
    def init_plc(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))

        config_path = os.path.join(
            current_dir,
            'plc_config.json'
        )

        try:
            with open(config_path, 'r') as f:
                config = json.load(f)

        except FileNotFoundError:
            config = {
                "plc_ip": "192.168.1.5",
                "port": 502,
                "polling_interval_ms": 200,
                "auto_connect": True
            }

            with open(config_path, 'w') as f:
                json.dump(config, f, indent=4)

        self.plc_ip_label.setText(
            f"📡 {config['plc_ip']}:{config['port']}"
        )

        self.plc = PLCHandler(
            config['plc_ip'],
            config['port']
        )

        self.plc.connection_status.connect(
            self.on_plc_connection
        )

        self.plc.data_updated.connect(
            self.on_plc_data
        )

        self.plc.connection_error.connect(
            self.on_plc_error
        )

        if config.get('auto_connect', True):

            self.update_status_message(
                f"Connecting to PLC at {config['plc_ip']}...",
                "info"
            )

            if self.plc.connect():

                self.plc.start_polling(
                    config.get('polling_interval_ms', 200)
                )

                self.update_status_message(
                    "PLC Connected Successfully",
                    "success"
                )

                self.pages["Home"].connect_to_plc(self.plc)

            else:
                self.update_status_message(
                    "PLC Connection Failed",
                    "error"
                )

    def send_plc_command(self, command):
        if hasattr(self, 'plc') and self.plc.connected:

            if self.plc.send_command(command):

                print(f"[PLC] Command sent: {command}")

                self.update_status_message(
                    f"Command '{command}' sent",
                    "success"
                )

            else:
                print(f"[PLC] Failed: {command}")

                self.update_status_message(
                    f"Failed to send '{command}'",
                    "error"
                )

        else:
            self.update_status_message(
                "PLC not connected",
                "warning"
            )

    # =========================================================
    # PLC CALLBACKS
    # =========================================================
    def on_plc_connection(self, connected):
        if connected:
            self.plc_indicator.setText("🟢")

            self.plc_status_label.setText(
                "PLC: CONNECTED"
            )

            self.plc_status_label.setStyleSheet(
                PLC_STATUS_CONNECTED_STYLE
            )

            self.update_status_message(
                "PLC Connected Successfully",
                "success"
            )

        else:
            self.plc_indicator.setText("🔴")

            self.plc_status_label.setText(
                "PLC: DISCONNECTED"
            )

            self.plc_status_label.setStyleSheet(
                PLC_STATUS_DISCONNECTED_STYLE
            )

            self.update_status_message(
                "PLC Disconnected",
                "error"
            )

    def on_plc_error(self, error_msg):
        self.update_status_message(
            f"PLC Error: {error_msg}",
            "error"
        )

    def on_plc_data(self, data):
        status = data.get('status', 'UNKNOWN')

        status_icons = {
            'RUNNING': ('🏭', 'Machine Running', "#A0D995"),
            'IDLE': ('⏸️', 'Machine Idle', "#FFD95A"),
            'ERROR': ('⚠️', 'Machine Error', "#D9534F"),
            'STOPPED': ('⏹️', 'Machine Stopped', "#FF8C42")
        }

        if status in status_icons:
            icon, tooltip, color = status_icons[status]

            self.system_status.setText(icon)

            self.system_status.setToolTip(tooltip)

            self.system_status.setStyleSheet(
                f"font-size: 16px; color: {color};"
            )

        if status == 'RUNNING':
            self.sidebar_buttons["Start"].setEnabled(False)
            self.sidebar_buttons["Stop"].setEnabled(True)

        elif status in ['STOPPED', 'IDLE']:
            self.sidebar_buttons["Start"].setEnabled(True)
            self.sidebar_buttons["Stop"].setEnabled(False)

        if status == 'ERROR':
            self.update_status_message(
                "Machine ERROR state",
                "error"
            )

    # =========================================================
    # STATUS MESSAGES
    # =========================================================
    def update_status_message(self, message, msg_type="info"):

        styles = {
            "success": STATUS_LEFT_SUCCESS_STYLE,
            "error": STATUS_LEFT_ERROR_STYLE,
            "warning": STATUS_LEFT_WARNING_STYLE,
            "info": STATUS_LEFT_INFO_STYLE
        }

        icons = {
            "success": "✅",
            "error": "❌",
            "warning": "⚠️",
            "info": "ℹ️"
        }

        self.left_status.setText(
            f"{icons.get(msg_type)} {message}"
        )

        self.left_status.setStyleSheet(
            styles.get(msg_type)
        )

        delay = STATUS_CLEAR_DELAYS.get(
            msg_type,
            3000
        )

        self.status_clear_timer.stop()

        QTimer.singleShot(
            delay,
            self.reset_status_message
        )

    def reset_status_message(self):
        self.left_status.setText("✅ System Ready")
        self.left_status.setStyleSheet(STATUS_LEFT_STYLE)

    # =========================================================
    # TIME FUNCTIONS
    # =========================================================
    def update_datetime(self):
        now = datetime.now()

        self.datetime_label.setText(
            now.strftime("%d-%m-%Y %H:%M:%S")
        )

    def update_uptime(self):
        elapsed = datetime.now() - self.start_time

        total_seconds = int(elapsed.total_seconds())

        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60

        self.uptime_label.setText(
            f"Uptime: {hours:02d}:{minutes:02d}:{seconds:02d}"
        )

    # =========================================================
    # PAGE NAVIGATION
    # =========================================================
    def activate_top_button(self, name):

        for bname, btn in self.top_buttons.items():

            if bname == name:
                btn.setStyleSheet(
                    TOPBAR_BUTTON_ACTIVE_STYLE
                )

            else:
                btn.setStyleSheet(
                    TOPBAR_BUTTON_STYLE
                )

        self.stack.setCurrentWidget(
            self.pages[name]
        )

        self.update_status_message(
            f"Switched to {name} page",
            "info"
        )

    # =========================================================
    # CLOSE EVENT
    # =========================================================
    def closeEvent(self, event):

        self.update_status_message(
            "Shutting down...",
            "info"
        )

        if hasattr(self, 'plc'):
            self.plc.disconnect()

        self.datetime_timer.stop()
        self.uptime_timer.stop()
        self.status_clear_timer.stop()

        event.accept()


# =============================================================
# MAIN
# =============================================================
if __name__ == "__main__":

    app = QApplication(sys.argv)

    app.setFont(QFont("Segoe UI", 9))

    window = MainWindow()

    window.resize(1280, 750)

    window.setMinimumSize(1024, 600)

    window.show()

    sys.exit(app.exec())