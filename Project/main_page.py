# main_page.py
import sys
import json
import os
from datetime import datetime
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QSizePolicy, QStackedWidget, QStatusBar, QLabel, QFrame
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

        # Initialize UI components
        self.left_status = None
        self.plc_indicator = None
        self.plc_status_label = None
        self.plc_ip_label = None
        self.system_status = None
        self.datetime_label = None
        self.uptime_label = None
        self.status_bar = None
        self.status_clear_timer = None
        
        # Setup main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Setup UI components
        self.setup_top_bar(main_layout)
        self.setup_content_area(main_layout)
        self.setup_bottom_status_bar(main_layout)
        
        # Setup timers
        self.setup_timers()
        
        # Activate default page
        self.activate_top_button("Home")
        
        # Initialize PLC
        self.init_plc()
    
    def setup_top_bar(self, main_layout):
        """Setup top navigation bar"""
        topbar = QFrame()
        topbar.setStyleSheet(TOPBAR_STYLE)
        topbar.setFixedHeight(80)
        topbar_layout = QHBoxLayout(topbar)
        topbar_layout.setContentsMargins(10, 5, 10, 5)

        # Create stacked widget for pages
        self.stack = QStackedWidget()
        self.pages = {
            "Home": HomePage(),
            "Production": ProductionPage(self),
            "TF Management": TFManagementPage(),
            "Production Data": ProductionDataPage()
        }

        for page in self.pages.values():
            self.stack.addWidget(page)

        # Create navigation buttons
        buttons_container = QWidget()
        buttons_layout = QHBoxLayout(buttons_container)
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        buttons_layout.setSpacing(5)

        self.top_buttons = {}
        for name in ["Home", "Production", "TF Management", "Production Data"]:
            btn = QPushButton(name)
            btn.setFixedHeight(60)
            btn.setMinimumWidth(120)
            btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            btn.setStyleSheet(TOPBAR_BUTTON_STYLE)
            buttons_layout.addWidget(btn)
            self.top_buttons[name] = btn
            btn.clicked.connect(lambda checked, n=name: self.activate_top_button(n))
        
        topbar_layout.addWidget(buttons_container)
        main_layout.addWidget(topbar)
    
    def setup_content_area(self, main_layout):
        """Setup main content area with sidebar and stack"""
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        # Setup sidebar
        sidebar = QFrame()
        sidebar.setStyleSheet(SIDEBAR_STYLE)
        sidebar.setFixedWidth(180)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setSpacing(10)
        sidebar_layout.setContentsMargins(10, 10, 10, 10)

        # Create sidebar buttons
        self.sidebar_buttons = {}
        for name, color in SIDEBAR_BUTTON_COLORS.items():
            btn = QPushButton(name)
            btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            btn.setMinimumHeight(50)
            btn.setStyleSheet(SIDEBAR_BUTTON_STYLE.format(bg=color))
            sidebar_layout.addWidget(btn)
            self.sidebar_buttons[name] = btn

        # Set initial button states
        for name, btn in self.sidebar_buttons.items():
            if name not in ["Restore", "Rest"]:
                btn.setDisabled(True)
                btn.setStyleSheet(SIDEBAR_BUTTON_STYLE.format(bg="#A0A0A0"))

        # Connect sidebar buttons
        def enable_all_buttons():
            for name, btn in self.sidebar_buttons.items():
                btn.setDisabled(False)
                btn.setStyleSheet(SIDEBAR_BUTTON_STYLE.format(bg=SIDEBAR_BUTTON_COLORS[name]))
            self.update_status_message("All controls enabled", "success")

        self.sidebar_buttons["Restore"].clicked.connect(enable_all_buttons)
        self.sidebar_buttons["Rest"].clicked.connect(enable_all_buttons)
        self.sidebar_buttons["Start"].clicked.connect(lambda: self.send_plc_command("START"))
        self.sidebar_buttons["Stop"].clicked.connect(lambda: self.send_plc_command("STOP"))
        self.sidebar_buttons["Production"].clicked.connect(lambda: self.activate_top_button("Production"))
        self.sidebar_buttons["Supply"].clicked.connect(lambda: self.update_status_message("Supply mode activated", "info"))

        content_layout.addWidget(sidebar, 0)
        content_layout.addWidget(self.stack, 1)
        main_layout.addLayout(content_layout)
    
    def setup_bottom_status_bar(self, main_layout):
        """Setup bottom status bar"""
        self.status_bar = QStatusBar()
        self.status_bar.setStyleSheet(STATUS_BAR_STYLE)
        self.status_bar.setFixedHeight(35)
        
        # Left side status message
        self.left_status = QLabel("✅ System Ready")
        self.left_status.setStyleSheet(STATUS_LEFT_STYLE)
        self.status_bar.addWidget(self.left_status, 2)
        
        # Center PLC status section
        plc_container = QFrame()
        plc_container.setStyleSheet(PLC_CONTAINER_STYLE)
        plc_layout = QHBoxLayout(plc_container)
        plc_layout.setContentsMargins(10, 2, 10, 2)
        plc_layout.setSpacing(10)
        
        self.plc_indicator = QLabel("🔴")
        self.plc_indicator.setStyleSheet(PLC_INDICATOR_STYLE)
        
        self.plc_status_label = QLabel("PLC: DISCONNECTED")
        self.plc_status_label.setStyleSheet(PLC_STATUS_DISCONNECTED_STYLE)
        
        self.plc_ip_label = QLabel("")
        self.plc_ip_label.setStyleSheet(PLC_IP_STYLE)
        
        plc_layout.addWidget(self.plc_indicator)
        plc_layout.addWidget(self.plc_status_label)
        plc_layout.addWidget(self.plc_ip_label)
        plc_layout.addStretch()
        
        self.status_bar.addPermanentWidget(plc_container, 1)
        
        # Right side system info
        right_container = QWidget()
        right_layout = QHBoxLayout(right_container)
        right_layout.setContentsMargins(0, 0, 10, 0)
        right_layout.setSpacing(15)
        
        self.system_status = QLabel("⏸️")
        self.system_status.setStyleSheet(SYSTEM_STATUS_STYLE)
        self.system_status.setToolTip("Machine Status")
        right_layout.addWidget(self.system_status)
        
        sep = QLabel("|")
        sep.setStyleSheet(SEPARATOR_STYLE)
        right_layout.addWidget(sep)
        
        self.datetime_label = QLabel("")
        self.datetime_label.setStyleSheet(DATETIME_STYLE)
        right_layout.addWidget(self.datetime_label)
        
        sep2 = QLabel("|")
        sep2.setStyleSheet(SEPARATOR_STYLE)
        right_layout.addWidget(sep2)
        
        self.uptime_label = QLabel("Uptime: 00:00:00")
        self.uptime_label.setStyleSheet(UPTIME_STYLE)
        right_layout.addWidget(self.uptime_label)
        
        self.status_bar.addPermanentWidget(right_container, 0)
        main_layout.addWidget(self.status_bar)
    
    def setup_timers(self):
        """Setup all timers"""
        # DateTime timer
        self.datetime_timer = QTimer()
        self.datetime_timer.timeout.connect(self.update_datetime)
        self.datetime_timer.start(1000)
        
        # Uptime timer
        self.start_time = datetime.now()
        self.uptime_timer = QTimer()
        self.uptime_timer.timeout.connect(self.update_uptime)
        self.uptime_timer.start(1000)
        
        # Status clear timer
        self.status_clear_timer = QTimer()
        self.status_clear_timer.setSingleShot(True)
        
        # Initialize displays
        self.update_datetime()
        self.update_uptime()
    
    def init_plc(self):
        """Initialize PLC communication"""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(current_dir, 'plc_config.json')
        try:
            with open('plc_config.json', 'r') as f:
                config = json.load(f)
        except FileNotFoundError:
            config = {
                "plc_ip": "192.168.1.5", 
                "port": 502, 
                "polling_interval_ms": 200,
                "auto_connect": True
            }
            with open('plc_config.json', 'w') as f:
                json.dump(config, f, indent=4)
        
        if self.plc_ip_label:
            self.plc_ip_label.setText(f"📡 {config['plc_ip']}:{config['port']}")
        
        self.plc = PLCHandler(config['plc_ip'], config['port'])
        self.plc.connection_status.connect(self.on_plc_connection)
        self.plc.data_updated.connect(self.on_plc_data)
        self.plc.connection_error.connect(self.on_plc_error)
        
        if config.get('auto_connect', True):
            self.update_status_message(f"Connecting to PLC at {config['plc_ip']}...", "info")
            if self.plc.connect():
                self.plc.start_polling(config.get('polling_interval_ms', 200))
                self.update_status_message("PLC Connected Successfully", "success")
                if hasattr(self, 'pages') and 'Home' in self.pages:
                    self.pages["Home"].connect_to_plc(self.plc)
            else:
                self.update_status_message("PLC Connection Failed - Check IP and network", "error")
    
    def send_plc_command(self, command):
        """Send command to PLC"""
        if hasattr(self, 'plc') and hasattr(self.plc, 'connected') and self.plc.connected:
            if self.plc.send_command(command):
                self.update_status_message(f"Command '{command}' sent to PLC", "success")
            else:
                self.update_status_message(f"Failed to send command '{command}'", "error")
        else:
            self.update_status_message("Cannot send command: PLC not connected", "warning")
    
    def on_plc_connection(self, connected):
        """Handle PLC connection status changes"""
        if connected:
            if self.plc_indicator:
                self.plc_indicator.setText("🟢")
            if self.plc_status_label:
                self.plc_status_label.setText("PLC: CONNECTED")
                self.plc_status_label.setStyleSheet(PLC_STATUS_CONNECTED_STYLE)
            self.update_status_message("PLC Connected Successfully", "success")
        else:
            if self.plc_indicator:
                self.plc_indicator.setText("🔴")
            if self.plc_status_label:
                self.plc_status_label.setText("PLC: DISCONNECTED")
                self.plc_status_label.setStyleSheet(PLC_STATUS_DISCONNECTED_STYLE)
            self.update_status_message("PLC Disconnected", "error")
    
    def on_plc_error(self, error_msg):
        """Handle PLC errors"""
        self.update_status_message(f"PLC Error: {error_msg}", "error")
    
    def on_plc_data(self, data):
        """Handle incoming PLC data"""
        status = data.get('status', 'UNKNOWN')
        
        status_icons = {
            'RUNNING': ('🏭', 'Machine Running'),
            'IDLE': ('⏸️', 'Machine Idle'),
            'ERROR': ('⚠️', 'Machine Error - Check PLC'),
            'STOPPED': ('⏹️', 'Machine Stopped')
        }
        
        if self.system_status and status in status_icons:
            icon, tooltip = status_icons[status]
            self.system_status.setText(icon)
            self.system_status.setToolTip(tooltip)
        
        if status == 'ERROR':
            self.update_status_message("Machine in ERROR state - Check PLC", "error")
    
    def update_status_message(self, message, msg_type="info"):
        """Update left status bar message"""
        if not self.left_status:
            return
        
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
        
        self.left_status.setText(f"{icons.get(msg_type, 'ℹ️')} {message}")
        self.left_status.setStyleSheet(styles.get(msg_type, STATUS_LEFT_INFO_STYLE))
        
        # Clear message after delay
        delay = STATUS_CLEAR_DELAYS.get(msg_type, 3000)
        self.status_clear_timer.stop()
        self.status_clear_timer.singleShot(delay, lambda: self.reset_status_message())
    
    def reset_status_message(self):
        """Reset status message to default"""
        if self.left_status:
            self.left_status.setText("✅ System Ready")
            self.left_status.setStyleSheet(STATUS_LEFT_STYLE)
    
    def update_datetime(self):
        """Update date and time display"""
        if self.datetime_label:
            now = datetime.now()
            self.datetime_label.setText(now.strftime("%d-%m-%Y %H:%M:%S"))
    
    def update_uptime(self):
        """Update system uptime display"""
        if self.uptime_label:
            elapsed = datetime.now() - self.start_time
            hours = elapsed.seconds // 3600
            minutes = (elapsed.seconds % 3600) // 60
            seconds = elapsed.seconds % 60
            self.uptime_label.setText(f"Uptime: {hours:02d}:{minutes:02d}:{seconds:02d}")
    
    def activate_top_button(self, name):
        """Activate top navigation button"""
        for bname, btn in self.top_buttons.items():
            if bname == name:
                btn.setStyleSheet(TOPBAR_BUTTON_ACTIVE_STYLE)
                self.update_status_message(f"Switched to {name} page", "info")
            else:
                btn.setStyleSheet(TOPBAR_BUTTON_STYLE)
        self.stack.setCurrentWidget(self.pages[name])
    
    def closeEvent(self, event):
        """Handle application close event"""
        self.update_status_message("Shutting down...", "info")
        
        if hasattr(self, 'plc'):
            self.plc.disconnect()
        
        if hasattr(self, 'datetime_timer'):
            self.datetime_timer.stop()
        if hasattr(self, 'uptime_timer'):
            self.uptime_timer.stop()
        if hasattr(self, 'status_clear_timer'):
            self.status_clear_timer.stop()
        
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 9))
    
    window = MainWindow()
    window.showMaximized()
    
    sys.exit(app.exec())