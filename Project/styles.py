# -------------------------
# Color Palette
# -------------------------
DARK_BLUE = "#1B2A49"      # Industrial dark blue
LIGHT_GREY = "#E0E0E0"     # Mild grey for background
BRIGHT_ORANGE = "#FF8C42"  # Bright orange (Rest button)
LIGHT_YELLOW = "#FFD95A"   # Light yellow (Restore button)
BRIGHT_BLUE = "#2196F3"    # Blue for outer frame border
LIGHT_BLUE = "#ADD8E6"     # Light blue for Home page first row
GREEN_TICK = "green"       # Tick mark color

# -------------------------
# Sidebar Button Colors
# -------------------------
SIDEBAR_BUTTON_COLORS = {
    "Rest": BRIGHT_ORANGE,
    "Start": "#A0D995",
    "Stop": "#D9534F",
    "Restore": LIGHT_YELLOW,
    "Production": "#5BC0DE",
    "Supply": "#9C88FF"
}

# -------------------------
# Sidebar Buttons (3D look)
# -------------------------
SIDEBAR_BUTTON_STYLE = """
    QPushButton {{
        background-color: {bg};
        color: black;
        font-size: 16px;
        font-weight: bold;
        border: 2px solid #333;
        border-radius: 6px;
        padding: 10px;
    }}
    QPushButton:hover {{
        background-color: #f0f0f0;
    }}
    QPushButton:pressed {{
        border-style: inset;
        background-color: #dcdcdc;
    }}
"""

# -------------------------
# Top Bar Buttons
# -------------------------
TOPBAR_BUTTON_STYLE = """
    QPushButton {
        background-color: #1B2A49;
        color: white;
        font-size: 14px;
        padding: 8px;
        border: none;
    }
    QPushButton:hover {
        background-color: #2E3B5A;
        border-radius: 4px;
    }
"""

TOPBAR_BUTTON_ACTIVE_STYLE = """
    QPushButton {
        background-color: white;
        color: black;
        font-size: 14px;
        padding: 8px;
        border: none;
    }
"""

# -------------------------
# Main Window Style
# -------------------------
MAIN_WINDOW_STYLE = f"""
    QWidget {{
        background-color: {LIGHT_GREY};
    }}
"""

# -------------------------
# Sidebar Style
# -------------------------
SIDEBAR_STYLE = f"""
    QWidget {{
        background-color: {DARK_BLUE};
    }}
"""

# -------------------------
# Top Bar Style
# -------------------------
TOPBAR_STYLE = f"""
    QWidget {{
        background-color: {DARK_BLUE};
    }}
"""

# -------------------------
# Home Page First Row Styles
# -------------------------
HOME_FIRST_ROW_HEIGHT = 80
HOME_FIRST_ROW_STYLE = f"""
    QFrame#home_first_row {{
        background-color: {LIGHT_BLUE};
        border-radius: 5px;
    }}
"""
HOME_TICK_STYLE = f"""
    QLabel {{
        color: {GREEN_TICK};
        font-size: 16px;
    }}
"""
HOME_LABEL_STYLE = """
    QLabel {
        font-size: 14px;
        font-weight: bold;
        color: black;
        background-color: transparent;
    }
"""
HOME_INPUT_STYLE = """
    QLineEdit {
        background-color: white;
        border: 1px solid #ccc;
        padding: 4px;
        border-radius: 4px;
        color: black;
    }
"""

# -------------------------
# Modern Pointer Scrollbar Style
# -------------------------
POINTER_SCROLLBAR_STYLE = """
QScrollBar:horizontal {
    border: 1px solid #999999;
    background: #E0E0E0;
    height: 15px;
    margin: 0px;
    border-radius: 7px;
}
QScrollBar::handle:horizontal {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop: 0 #404040, stop: 0.5 #606060, stop: 1 #404040);
    border: 1px solid #202020;
    border-radius: 3px;
    min-width: 8px;
    max-width: 8px;
}
QScrollBar::handle:horizontal:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop: 0 #505050, stop: 0.5 #707070, stop: 1 #505050);
}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    border: none;
    background: none;
    width: 0px;
}
"""
HOME_LEGEND_STYLE = f"""
    QGroupBox {{
        border: 2px solid {BRIGHT_BLUE};
        border-radius: 4px;
        margin-top: 15px;
        padding: 15px;
        background-color: transparent;
    }}
    QGroupBox::title {{
        subcontrol-origin: margin;
        subcontrol-position: top left;
        padding: 0 10px;
        color: black;
        font-weight: bold;
        font-size: 20px;
        background-color: white;
    }}
"""

# -------------------------
# Home Page Checkbox and Radio Button Styles
# -------------------------
HOME_RADIO_BUTTON_STYLE = """
    QRadioButton {
        color: black;
        background-color: transparent;
        font-weight: bold;
    }
    QRadioButton::indicator {
        width: 14px;
        height: 14px;
    }
    QRadioButton::indicator:unchecked {
        border: 2px solid black;
        border-radius: 7px;
        background-color: white;
    }
    QRadioButton::indicator:checked {
        border: 2px solid black;
        border-radius: 7px;
        background-color: black;
    }
"""

HOME_CHECKBOX_STYLE = """
    QCheckBox {
        color: black;
        background-color: transparent;
        font-weight: bold;
    }
    QCheckBox::indicator {
        width: 14px;
        height: 14px;
    }
    QCheckBox::indicator:unchecked {
        border: 2px solid black;
        background-color: white;
    }
    QCheckBox::indicator:checked {
        border: 2px solid black;
        background-color: black;
    }
"""

CLEAR_BUTTON_STYLE = """
            QPushButton {
                background-color: white;
                color: black;
                border: 1px solid black;
                padding: 5px 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
            }
        """

# -------------------------
# Production Page Styles
# -------------------------

# Outer frame for first input row
PRODUCTION_FIRST_ROW_STYLE = f"""
    QFrame#first_row_frame {{
        border: 2px solid {BRIGHT_BLUE};
        border-radius: 4px;
        background-color: transparent;
    }}
"""

# Input boxes
PRODUCTION_INPUT_BOX_STYLE = """
    QLineEdit {
        background-color: white;
        border: 1px solid #ccc;
        padding: 5px;
        border-radius: 4px;
        color: black;
    }
"""

# Labels
PRODUCTION_LABEL_STYLE = """
    QLabel {
        font-size: 14px;
        font-weight: bold;
        color: black;
    }
"""

# Close Batch Button
PRODUCTION_BUTTON_STYLE = """
    QPushButton {
        background-color: white;
        color: black;
        border: 2px solid black;
        font-weight: bold;
        padding: 5px 15px;
    }
    QPushButton:hover {
        background-color: #f0f0f0;
    }
"""

# Production Title Bar
PRODUCTION_TITLEBAR_STYLE = """
    background-color: white;
    color: black;
    border: 2px solid black;
"""

PRODUCTION_TITLE_LABEL_STYLE = """
    color: black;
    font-size: 30px;
    font-weight: bold;
"""

# ------------------------------
# Production Second Row Styles
# ------------------------------

# Outer container (left + right columns)
PRODUCTION_SECOND_ROW_STYLE = """
    QFrame {
        background-color: transparent;
    }
"""

# Labels (black text, left aligned)
PRODUCTION_FORM_LABEL_STYLE = """
    QLabel {
        font-size: 14px;
        font-weight: bold;
        color: black;
    }
"""

# Input boxes (white background, no border except light grey)
PRODUCTION_FORM_INPUT_STYLE = """
    QLineEdit {
        background-color: white;
        border: 1px solid #ccc;
        padding: 4px;
        border-radius: 4px;
        color: black;
    }
"""

# Right column frame with blue border
PRODUCTION_RIGHT_COLUMN_STYLE = f"""
    QFrame#fabric_frame {{
        border: 2px solid {BRIGHT_BLUE};
        border-radius: 4px;
        margin-top: 15px;
        padding: 15px;
        background-color: transparent;
    }}
"""

# Legend (Fabric text)
PRODUCTION_QGROUPBOX_STYLE = """
    QLabel {
        font-size: 16px;
        font-weight: bold;
        color: black;
        background-color: white;
        padding: 0 5px;
    }
"""

PRODUCTION_LEGEND_STYLE = f"""
    QGroupBox {{
        border: 2px solid {BRIGHT_BLUE};
        border-radius: 4px;
        margin-top: 15px;
        padding: 15px;
        background-color: transparent;
    }}
    QGroupBox::title {{
        subcontrol-origin: margin;
        subcontrol-position: top left;
        padding: 0 10px;
        color: red;
        font-weight: bold;
        font-size: 20px;
        background-color: white;
    }}
"""

# Production Page Checkbox and Radio Button Styles
PRODUCTION_RADIO_BUTTON_STYLE = """
    QRadioButton {
        color: black;
        background-color: transparent;
        font-weight: bold;
    }
    QRadioButton::indicator {
        width: 14px;
        height: 14px;
    }
    QRadioButton::indicator:unchecked {
        border: 2px solid black;
        border-radius: 7px;
        background-color: white;
    }
    QRadioButton::indicator:checked {
        border: 2px solid black;
        border-radius: 7px;
        background-color: black;
    }
"""

PRODUCTION_CHECKBOX_STYLE = """
    QCheckBox {
        color: black;
        background-color: transparent;
        font-weight: bold;
    }
    QCheckBox::indicator {
        width: 14px;
        height: 14px;
    }
    QCheckBox::indicator:unchecked {
        border: 2px solid black;
        background-color: white;
    }
    QCheckBox::indicator:checked {
        border: 2px solid black;
        background-color: black;
    }
"""

# Production Page Scrollbar Style
PRODUCTION_SCROLLBAR_STYLE = """
QScrollBar:horizontal {
    border: 1px solid #999999;
    background: #E0E0E0;
    height: 15px;
    margin: 0px;
    border-radius: 7px;
}
QScrollBar::handle:horizontal {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop: 0 #404040, stop: 0.5 #606060, stop: 1 #404040);
    border: 1px solid #202020;
    border-radius: 3px;
    min-width: 8px;
    max-width: 8px;
}
QScrollBar::handle:horizontal:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop: 0 #505050, stop: 0.5 #707070, stop: 1 #505050);
}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    border: none;
    background: none;
    width: 0px;
}
"""

# Production Status Indicators
PRODUCTION_STATUS_STYLE = """
    QLabel {
        font-size: 16px;
        font-weight: bold;
        padding: 5px 10px;
        border-radius: 4px;
    }
"""

PRODUCTION_STATUS_ACTIVE = """
    QLabel {
        background-color: #A0D995;
        color: black;
        border: 1px solid #7CB342;
    }
"""

PRODUCTION_STATUS_INACTIVE = """
    QLabel {
        background-color: #D9534F;
        color: white;
        border: 1px solid #C9302C;
    }
"""

PRODUCTION_STATUS_PAUSED = """
    QLabel {
        background-color: #FFD95A;
        color: black;
        border: 1px solid #FFC107;
    }
"""

# ------------------------------
# TF Management Page Styles
# ------------------------------
TFMANAGEMENT_OUTER_BOX_STYLE = """
    QFrame#outerBlackBox {
        border: 2px solid black;
        border-radius: 20px;
        background-color: transparent;
    }
"""

TFMANAGEMENT_TF_BLOCK_STYLE = """
    QFrame {
        border: 1px solid black;
        background-color: #ADD8E6;  /* Light blue */
        border-radius: 5px;
    }
"""

TFMANAGEMENT_TF_LABEL_STYLE = """
    QLabel {
        color: black;
        font-weight: bold;
    }
"""

# TF Block Title Style
TFMANAGEMENT_TF_TITLE_STYLE = """
    QLabel {
        color: #000000;
        font-weight: bold;
        font-size: 16px;
        background-color: transparent;
        border: 1px solid #000000;
        padding: 2px;
    }
"""

# TF Block Tag Style (Boost:, Normal:)
TFMANAGEMENT_TF_TAG_STYLE = """
    QLabel {
        color: #000000;
        font-size: 12px;
        background-color: transparent;
        border: none;
    }
"""

# TF Block Input Style
TFMANAGEMENT_TF_INPUT_STYLE = """
    QLineEdit {
        background-color: white;
        border: 1px solid #000000;
        border-radius: 2px;
        padding: 2px;
        font-size: 12px;
        color: black;
    }
"""

# TF Block Container Style
TFMANAGEMENT_TF_CONTAINER_STYLE = """
    QFrame {
        background-color: #87CEEB;
        border: 2px solid #000000;
        border-radius: 4px;
    }
"""

# ------------------------------
# TF Management Roller Section Styles
# ------------------------------
TFMANAGEMENT_ROLLER_BOX_STYLE = """
    QGroupBox#roller_groupbox {
        border: 2px solid black;
        border-radius: 20px;
        background-color: transparent;
        margin-top: 15px;
        padding: 20px;
    }
    QGroupBox::title {
        subcontrol-origin: margin;
        subcontrol-position: top left;
        padding: 0 10px;
        color: black;
        font-weight: bold;
        font-size: 20px;
    }
"""

# Individual Adj blocks
TFMANAGEMENT_ADJ_BLOCK_STYLE = """
    QFrame {
        border: 2px solid black;
        border-radius: 5px;
        background-color: #ADD8E6;  /* light blue */
    }
"""

TFMANAGEMENT_ADJ_LABEL_STYLE = """
    QLabel {
        color: #000000;
        font-weight: bold;
        font-size: 16px;
        background-color: transparent;
        border: 1px solid #000000;
        padding: 2px;
    }
"""

TFMANAGEMENT_SPINBOX_STYLE = """
    QSpinBox {
        background-color: white;
        border: 1px solid #000000;
        border-radius: 4px;
        padding: 2px 6px;
        min-width: 60px;
        color: black;
    }
"""

TFMANAGEMENT_MINIICON_STYLE = """
    QPushButton {
        background-color: white;
        border: 1px solid #ccc;
        border-radius: 4px;
    }
    QPushButton:hover {
        background-color: #f0f0f0;
    }
"""

BLACK_BORDER_BOX_STYLE = f"""
    QFrame {{
        border: 2px solid black;
        border-radius: 5px;
        background-color: {LIGHT_GREY};
    }}
"""

# Home Button Style (same as PRODUCTION_BUTTON_STYLE but with different name)
HOME_BUTTON_STYLE = """
    QPushButton {
        background-color: #2E8B57;
        color: white;
        border: 1px solid #1C6B47;
        border-radius: 5px;
        font-weight: bold;
        font-size: 12px;
        padding: 5px 10px;
    }
    QPushButton:hover {
        background-color: #3CB371;
        border: 1px solid #2E8B57;
    }
    QPushButton:pressed {
        background-color: #1C6B47;
        border: 1px solid #145235;
    }
    QPushButton:disabled {
        background-color: #A9A9A9;
        color: #696969;
        border: 1px solid #808080;
    }
"""

# Styles Mini Icon Style (same as TFMANAGEMENT_MINIICON_STYLE but with different name)
STYLES_MINIICON_STYLE = """
    QPushButton {
        background-color: #4682B4;
        border: 1px solid #36648B;
        border-radius: 5px;
        margin: 2px;
    }
    QPushButton:hover {
        background-color: #5A9BD4;
        border: 1px solid #4682B4;
    }
    QPushButton:pressed {
        background-color: #36648B;
        border: 1px solid #2A4F6E;
    }
    QPushButton:disabled {
        background-color: #A9A9A9;
        border: 1px solid #808080;
    }
"""
# styles.py - Add these new styles at the end of the file

# -------------------------
# Bottom Status Bar Styles
# -------------------------

STATUS_BAR_STYLE = """
    QStatusBar {
        background-color: #2C3E50;
        color: white;
        font-size: 12px;
        padding: 3px;
        border-top: 2px solid #1A252F;
    }
    QStatusBar::item {
        border: none;
    }
"""

STATUS_LEFT_STYLE = "color: #A0D995; padding-left: 10px; font-weight: bold;"
STATUS_LEFT_SUCCESS_STYLE = "color: #A0D995; padding-left: 10px; font-weight: bold;"
STATUS_LEFT_ERROR_STYLE = "color: #FF6B6B; padding-left: 10px; font-weight: bold;"
STATUS_LEFT_WARNING_STYLE = "color: #FFD93D; padding-left: 10px; font-weight: bold;"
STATUS_LEFT_INFO_STYLE = "color: #87CEEB; padding-left: 10px; font-weight: bold;"

PLC_CONTAINER_STYLE = "background-color: #34495E; border-radius: 5px; padding: 2px;"
PLC_INDICATOR_STYLE = "font-size: 16px;"
PLC_STATUS_CONNECTED_STYLE = "color: #A0D995; font-weight: bold; font-size: 12px;"
PLC_STATUS_DISCONNECTED_STYLE = "color: #FF6B6B; font-weight: bold; font-size: 12px;"
PLC_IP_STYLE = "color: #BDC3C7; font-size: 10px;"

SYSTEM_STATUS_STYLE = "font-size: 16px;"
SEPARATOR_STYLE = "color: #7F8C8D;"
DATETIME_STYLE = "color: black; font-family: monospace; font-size: 11px;"
UPTIME_STYLE = "color: black; font-size: 10px;"

# Status message display times (in milliseconds)
STATUS_CLEAR_DELAYS = {
    "success": 3000,
    "error": 5000,
    "warning": 3000,
    "info": 2000
}