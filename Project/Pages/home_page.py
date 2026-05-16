import sys
import os

# Add parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from styles import *

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QFrame, QSizePolicy, QScrollBar, QGroupBox, QGridLayout,
    QRadioButton, QCheckBox, QPushButton
)
from PyQt6.QtCore import Qt


class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
    
    def setup_ui(self):
        # Main layout - everything aligned from top
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # -------------------------
        # 1st Row: Blue background box
        # -------------------------
        blue_box = QFrame()
        blue_box.setObjectName("home_first_row")
        blue_box.setFixedHeight(90)
        blue_box.setStyleSheet(HOME_FIRST_ROW_STYLE)
        
        # Horizontal layout inside blue box for left alignment
        blue_layout = QHBoxLayout(blue_box)
        blue_layout.setContentsMargins(20, 0, 20, 0)
        blue_layout.setSpacing(40)
        blue_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        
        # Batch ID
        batch_label = QLabel("Batch ID:")
        batch_label.setStyleSheet(HOME_LABEL_STYLE)
        self.batch_input = QLineEdit()
        self.batch_input.setStyleSheet(HOME_INPUT_STYLE)
        
        # Target Production
        target_label = QLabel("Target Prod:")
        target_label.setStyleSheet(HOME_LABEL_STYLE)
        self.target_input = QLineEdit()
        self.target_input.setStyleSheet(HOME_INPUT_STYLE)
        
        # File
        file_label = QLabel("File:")
        file_label.setStyleSheet(HOME_LABEL_STYLE)
        self.file_input = QLineEdit()
        self.file_input.setStyleSheet(HOME_INPUT_STYLE)
        
        # Add all to blue box layout directly
        blue_layout.addWidget(batch_label)
        blue_layout.addWidget(self.batch_input)
        blue_layout.addSpacing(40)
        
        blue_layout.addWidget(target_label)
        blue_layout.addWidget(self.target_input)
        blue_layout.addSpacing(40)
        
        blue_layout.addWidget(file_label)
        blue_layout.addWidget(self.file_input)
        
        # Add blue box to main layout
        main_layout.addWidget(blue_box)
        
        # -------------------------
        # 2nd Row: Layers, S[mm], L[mm], SS[mm]
        # -------------------------
        second_row = QWidget()
        second_layout = QHBoxLayout(second_row)
        second_layout.setContentsMargins(0, 0, 0, 0)
        second_layout.setSpacing(40)
        second_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        # Layers
        layers_label = QLabel("Layers:")
        layers_label.setStyleSheet(HOME_LABEL_STYLE)
        self.layers_input = QLineEdit()
        self.layers_input.setStyleSheet(HOME_INPUT_STYLE)
        
        # S[mm]
        s_label = QLabel("S[mm]:")
        s_label.setStyleSheet(HOME_LABEL_STYLE)
        self.s_input = QLineEdit()
        self.s_input.setStyleSheet(HOME_INPUT_STYLE)
        
        # L[mm]
        l_label = QLabel("L[mm]:")
        l_label.setStyleSheet(HOME_LABEL_STYLE)
        self.l_input = QLineEdit()
        self.l_input.setStyleSheet(HOME_INPUT_STYLE)
        
        # SS[mm]
        ss_label = QLabel("SS[mm]:")
        ss_label.setStyleSheet(HOME_LABEL_STYLE)
        self.ss_input = QLineEdit()
        self.ss_input.setStyleSheet(HOME_INPUT_STYLE)
        
        # Add all to second row layout
        second_layout.addWidget(layers_label)
        second_layout.addWidget(self.layers_input)
        second_layout.addWidget(s_label)
        second_layout.addWidget(self.s_input)
        second_layout.addWidget(l_label)
        second_layout.addWidget(self.l_input)
        second_layout.addWidget(ss_label)
        second_layout.addWidget(self.ss_input)
        
        # Add second row to main layout
        main_layout.addWidget(second_row)
        
        # -------------------------
        # Add space between second and third row
        # -------------------------
        main_layout.addSpacing(15)
        
        # -------------------------
        # 3rd Row: Fabric Thickness, Conveyor Offset
        # -------------------------
        third_row = QWidget()
        third_layout = QHBoxLayout(third_row)
        third_layout.setContentsMargins(0, 0, 0, 0)
        third_layout.setSpacing(40)
        third_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        # Fabric Thickness[mm] - Group label and input together
        fabric_widget = QWidget()
        fabric_layout = QHBoxLayout(fabric_widget)
        fabric_layout.setContentsMargins(0, 0, 0, 0)
        fabric_layout.setSpacing(10)
        fabric_label = QLabel("Fabric Thickness [mm]:")
        fabric_label.setStyleSheet(HOME_LABEL_STYLE)
        self.fabric_input = QLineEdit()
        self.fabric_input.setFixedWidth(150)
        self.fabric_input.setStyleSheet(HOME_INPUT_STYLE)
        fabric_layout.addWidget(fabric_label)
        fabric_layout.addWidget(self.fabric_input)
        fabric_widget.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        
        # Conveyor Offset[mm] - Group label and input together
        conveyor_widget = QWidget()
        conveyor_layout = QHBoxLayout(conveyor_widget)
        conveyor_layout.setContentsMargins(0, 0, 0, 0)
        conveyor_layout.setSpacing(10)
        conveyor_label = QLabel("Conveyor Offset [mm]:")
        conveyor_label.setStyleSheet(HOME_LABEL_STYLE)
        self.conveyor_input = QLineEdit()
        self.conveyor_input.setFixedWidth(150)
        self.conveyor_input.setStyleSheet(HOME_INPUT_STYLE)
        conveyor_layout.addWidget(conveyor_label)
        conveyor_layout.addWidget(self.conveyor_input)
        conveyor_widget.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        
        # Add all grouped widgets to third row layout
        third_layout.addWidget(fabric_widget)
        third_layout.addWidget(conveyor_widget)
        
        # Add third row to main layout
        main_layout.addWidget(third_row)
        
        # -------------------------
        # Add space between third and fourth row
        # -------------------------
        main_layout.addSpacing(15)
        
        # -------------------------
        # 4th Row: Left - Trolley Speed Controls, Right - Selective Movement Box
        # -------------------------
        fourth_row = QWidget()
        fourth_layout = QHBoxLayout(fourth_row)
        fourth_layout.setContentsMargins(0, 0, 0, 0)
        fourth_layout.setSpacing(30)
        fourth_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # -------------------------
        # LEFT PART: Trolley Speed Controls
        # -------------------------
        left_part = QWidget()
        left_layout = QVBoxLayout(left_part)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(20)
        left_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Trolley Feeding Speed
        feeding_widget = QWidget()
        feeding_layout = QHBoxLayout(feeding_widget)
        feeding_layout.setContentsMargins(0, 0, 0, 0)
        feeding_layout.setSpacing(15)

        feeding_label = QLabel("Trolley feeding speed:")
        feeding_label.setStyleSheet(HOME_LABEL_STYLE)
        self.feeding_scrollbar = QScrollBar(Qt.Orientation.Horizontal)
        self.feeding_scrollbar.setRange(1, 10)
        self.feeding_scrollbar.setValue(5)
        self.feeding_scrollbar.setFixedWidth(150)
        self.feeding_scrollbar.setStyleSheet(POINTER_SCROLLBAR_STYLE)
        self.feeding_value = QLabel("5")
        self.feeding_value.setStyleSheet(HOME_LABEL_STYLE)
        self.feeding_value.setFixedWidth(20)

        self.feeding_scrollbar.valueChanged.connect(
            lambda value: self.feeding_value.setText(str(value))
        )

        feeding_layout.addWidget(feeding_label)
        feeding_layout.addWidget(self.feeding_scrollbar)
        feeding_layout.addWidget(self.feeding_value)

        # Trolley Unloading Speed
        unloading_widget = QWidget()
        unloading_layout = QHBoxLayout(unloading_widget)
        unloading_layout.setContentsMargins(0, 0, 0, 0)
        unloading_layout.setSpacing(15)

        unloading_label = QLabel("Trolley Unloading speed:")
        unloading_label.setStyleSheet(HOME_LABEL_STYLE)
        self.unloading_scrollbar = QScrollBar(Qt.Orientation.Horizontal)
        self.unloading_scrollbar.setRange(1, 10)
        self.unloading_scrollbar.setValue(5)
        self.unloading_scrollbar.setFixedWidth(150)
        self.unloading_scrollbar.setStyleSheet(POINTER_SCROLLBAR_STYLE)
        self.unloading_value = QLabel("5")
        self.unloading_value.setStyleSheet(HOME_LABEL_STYLE)
        self.unloading_value.setFixedWidth(20)

        self.unloading_scrollbar.valueChanged.connect(
            lambda value: self.unloading_value.setText(str(value))
        )

        unloading_layout.addWidget(unloading_label)
        unloading_layout.addWidget(self.unloading_scrollbar)
        unloading_layout.addWidget(self.unloading_value)

        # Trolley Upstroke Speed
        upstroke_widget = QWidget()
        upstroke_layout = QHBoxLayout(upstroke_widget)
        upstroke_layout.setContentsMargins(0, 0, 0, 0)
        upstroke_layout.setSpacing(15)

        upstroke_label = QLabel("Trolley Upstroke speed:")
        upstroke_label.setStyleSheet(HOME_LABEL_STYLE)
        self.upstroke_scrollbar = QScrollBar(Qt.Orientation.Horizontal)
        self.upstroke_scrollbar.setRange(1, 10)
        self.upstroke_scrollbar.setValue(5)
        self.upstroke_scrollbar.setFixedWidth(150)
        self.upstroke_scrollbar.setStyleSheet(POINTER_SCROLLBAR_STYLE)
        self.upstroke_value = QLabel("5")
        self.upstroke_value.setStyleSheet(HOME_LABEL_STYLE)
        self.upstroke_value.setFixedWidth(20)

        self.upstroke_scrollbar.valueChanged.connect(
            lambda value: self.upstroke_value.setText(str(value))
        )

        upstroke_layout.addWidget(upstroke_label)
        upstroke_layout.addWidget(self.upstroke_scrollbar)
        upstroke_layout.addWidget(self.upstroke_value)

        # Add widgets with stretch factors for vertical distribution
        left_layout.addWidget(feeding_widget)
        left_layout.addStretch(1)
        left_layout.addWidget(unloading_widget)
        left_layout.addStretch(1)
        left_layout.addWidget(upstroke_widget)
        left_layout.addStretch(2)
        
        # -------------------------
        # RIGHT PART: Selective Movement Box
        # -------------------------
        right_part = QGroupBox("Selective Movement")
        right_part.setStyleSheet(HOME_LEGEND_STYLE)
        right_part.setMinimumHeight(250)

        # THIS FIXES THE HALF-HIDDEN ISSUE
        right_part.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred
        )

        right_layout = QGridLayout(right_part)
        
        # Row 0: Radio buttons
        self.standard_radio = QRadioButton("Standard")
        self.standard_radio.setStyleSheet(HOME_RADIO_BUTTON_STYLE)
        self.bundle_shift_radio = QRadioButton("Bundle Shift")
        self.bundle_shift_radio.setStyleSheet(HOME_RADIO_BUTTON_STYLE)
        self.multi_step_radio = QRadioButton("Multi Step")
        self.multi_step_radio.setStyleSheet(HOME_RADIO_BUTTON_STYLE)
        self.standard_radio.setChecked(True)
        
        radio_layout = QHBoxLayout()
        radio_layout.setSpacing(20)
        radio_layout.addWidget(self.standard_radio)
        radio_layout.addWidget(self.bundle_shift_radio)
        radio_layout.addWidget(self.multi_step_radio)
        radio_layout.addStretch()
        
        right_layout.addLayout(radio_layout, 0, 0, 1, 5)
        
        # Row 1: Length label and text boxes
        length_label = QLabel("Length[mm]:")
        length_label.setStyleSheet(HOME_LABEL_STYLE)
        
        self.text_box1 = QLineEdit()
        self.text_box1.setStyleSheet(HOME_INPUT_STYLE)
        self.text_box1.setFixedWidth(120)
        self.text_box1.setPlaceholderText("Text 1")
        
        self.text_box2 = QLineEdit()
        self.text_box2.setStyleSheet(HOME_INPUT_STYLE)
        self.text_box2.setFixedWidth(120)
        self.text_box2.setPlaceholderText("Text 2")
        
        clear_button = QPushButton("Clear")
        clear_button.setStyleSheet(CLEAR_BUTTON_STYLE)
        clear_button.setFixedSize(80, 30)
        
        # Length row
        right_layout.addWidget(length_label, 1, 0, Qt.AlignmentFlag.AlignLeft)

        # Align textboxes with columns below
        right_layout.addWidget(self.text_box1, 1, 2, Qt.AlignmentFlag.AlignLeft)
        right_layout.addWidget(self.text_box2, 1, 3, Qt.AlignmentFlag.AlignLeft)

        # Clear button
        right_layout.addWidget(clear_button, 1, 4, Qt.AlignmentFlag.AlignRight)
        

        # Row 3: L1
        l1_label = QLabel("L1")
        l1_label.setStyleSheet(HOME_LABEL_STYLE)
        self.l1_checkbox = QCheckBox()
        self.l1_checkbox.setStyleSheet(HOME_CHECKBOX_STYLE)
        self.l1_input = QLineEdit()
        self.l1_input.setStyleSheet(HOME_INPUT_STYLE)
        self.l1_input.setFixedWidth(100)
        self.l1_counter_input = QLineEdit()
        self.l1_counter_input.setStyleSheet(HOME_INPUT_STYLE)
        self.l1_counter_input.setFixedWidth(100)
        self.l1_cuts_input = QLineEdit()
        self.l1_cuts_input.setStyleSheet(HOME_INPUT_STYLE)
        self.l1_cuts_input.setFixedWidth(100)
        
        right_layout.addWidget(l1_label, 3, 0)
        right_layout.addWidget(self.l1_checkbox, 3, 1)
        right_layout.addWidget(self.l1_input, 3, 2)
        right_layout.addWidget(self.l1_counter_input, 3, 3)
        right_layout.addWidget(self.l1_cuts_input, 3, 4)
        
        # Row 4: L2
        l2_label = QLabel("L2")
        l2_label.setStyleSheet(HOME_LABEL_STYLE)
        self.l2_checkbox = QCheckBox()
        self.l2_checkbox.setStyleSheet(HOME_CHECKBOX_STYLE)
        self.l2_input = QLineEdit()
        self.l2_input.setStyleSheet(HOME_INPUT_STYLE)
        self.l2_input.setFixedWidth(100)
        self.l2_counter_input = QLineEdit()
        self.l2_counter_input.setStyleSheet(HOME_INPUT_STYLE)
        self.l2_counter_input.setFixedWidth(100)
        self.l2_cuts_input = QLineEdit()
        self.l2_cuts_input.setStyleSheet(HOME_INPUT_STYLE)
        self.l2_cuts_input.setFixedWidth(100)
        
        right_layout.addWidget(l2_label, 4, 0)
        right_layout.addWidget(self.l2_checkbox, 4, 1)
        right_layout.addWidget(self.l2_input, 4, 2)
        right_layout.addWidget(self.l2_counter_input, 4, 3)
        right_layout.addWidget(self.l2_cuts_input, 4, 4)
        
        # Row 5: L3
        l3_label = QLabel("L3")
        l3_label.setStyleSheet(HOME_LABEL_STYLE)
        self.l3_checkbox = QCheckBox()
        self.l3_checkbox.setStyleSheet(HOME_CHECKBOX_STYLE)
        self.l3_input = QLineEdit()
        self.l3_input.setStyleSheet(HOME_INPUT_STYLE)
        self.l3_input.setFixedWidth(100)
        self.l3_counter_input = QLineEdit()
        self.l3_counter_input.setStyleSheet(HOME_INPUT_STYLE)
        self.l3_counter_input.setFixedWidth(100)
        self.l3_cuts_input = QLineEdit()
        self.l3_cuts_input.setStyleSheet(HOME_INPUT_STYLE)
        self.l3_cuts_input.setFixedWidth(100)
        
        right_layout.addWidget(l3_label, 5, 0)
        right_layout.addWidget(self.l3_checkbox, 5, 1)
        right_layout.addWidget(self.l3_input, 5, 2)
        right_layout.addWidget(self.l3_counter_input, 5, 3)
        right_layout.addWidget(self.l3_cuts_input, 5, 4)
        
        # Row 6: L4
        l4_label = QLabel("L4")
        l4_label.setStyleSheet(HOME_LABEL_STYLE)
        self.l4_checkbox = QCheckBox()
        self.l4_checkbox.setStyleSheet(HOME_CHECKBOX_STYLE)
        self.l4_input = QLineEdit()
        self.l4_input.setStyleSheet(HOME_INPUT_STYLE)
        self.l4_input.setFixedWidth(100)
        self.l4_counter_input = QLineEdit()
        self.l4_counter_input.setStyleSheet(HOME_INPUT_STYLE)
        self.l4_counter_input.setFixedWidth(100)
        self.l4_cuts_input = QLineEdit()
        self.l4_cuts_input.setStyleSheet(HOME_INPUT_STYLE)
        self.l4_cuts_input.setFixedWidth(100)
        
        right_layout.addWidget(l4_label, 6, 0)
        right_layout.addWidget(self.l4_checkbox, 6, 1)
        right_layout.addWidget(self.l4_input, 6, 2)
        right_layout.addWidget(self.l4_counter_input, 6, 3)
        right_layout.addWidget(self.l4_cuts_input, 6, 4)
        
        # Set column stretches
        right_layout.setColumnStretch(0, 0)  # Layer label
        right_layout.setColumnStretch(1, 0)  # Enable checkbox
        right_layout.setColumnStretch(2, 1)  # Value input
        right_layout.setColumnStretch(3, 1)  # Counter input
        right_layout.setColumnStretch(4, 1)  # Cuts input
        
        # Add left and right parts to fourth row
        fourth_layout.addWidget(left_part, 1)
        fourth_layout.addWidget(right_part, 1)
        
        # Add fourth row to main layout
        main_layout.addWidget(fourth_row)

        # -------------------------
        # Add space between fourth and fifth row
        # -------------------------
        main_layout.addSpacing(15)

        # -------------------------
        # 5th Row: Black border box with reset button and icons
        # -------------------------
        black_border_box = QFrame()
        black_border_box.setFixedWidth(500)
        black_border_box.setFixedHeight(70)
        black_border_box.setStyleSheet(BLACK_BORDER_BOX_STYLE)

        inner_layout = QHBoxLayout(black_border_box)
        inner_layout.setContentsMargins(20, 15, 20, 15)
        inner_layout.setSpacing(0)

        # Left: Reset Tubular button
        reset_button = QPushButton("Reset Tubular")
        reset_button.setFixedSize(150, 35)
        reset_button.setStyleSheet(HOME_BUTTON_STYLE)
        inner_layout.addWidget(reset_button, alignment=Qt.AlignmentFlag.AlignLeft)

        inner_layout.addStretch(1)

        # Right: 4 mini icon buttons (placeholders)
        icon_layout = QHBoxLayout()
        icon_layout.setSpacing(0)
        for i in range(4):
            icon_btn = QPushButton()
            icon_btn.setFixedSize(50, 50)
            icon_btn.setStyleSheet(STYLES_MINIICON_STYLE)
            icon_layout.addWidget(icon_btn)

        inner_layout.addLayout(icon_layout)
        main_layout.addWidget(black_border_box, alignment=Qt.AlignmentFlag.AlignLeft)
        
    def connect_to_plc(self, plc_handler):
        """Connect all UI controls to PLC handler"""
        self.plc = plc_handler
        
        # Connect speed scrollbars to PLC
        if hasattr(self, 'feeding_scrollbar'):
            self.feeding_scrollbar.valueChanged.connect(
                lambda v: self.plc.set_speed('feeding', v) if self.plc and self.plc.connected else None
            )
        if hasattr(self, 'unloading_scrollbar'):
            self.unloading_scrollbar.valueChanged.connect(
                lambda v: self.plc.set_speed('unloading', v) if self.plc and self.plc.connected else None
            )
        if hasattr(self, 'upstroke_scrollbar'):
            self.upstroke_scrollbar.valueChanged.connect(
                lambda v: self.plc.set_speed('upstroke', v) if self.plc and self.plc.connected else None
            )
        
        # Connect numeric inputs validation
        numeric_inputs = ['layers_input', 's_input', 'l_input', 'ss_input', 'fabric_input', 'conveyor_input']
        for inp_name in numeric_inputs:
            if hasattr(self, inp_name):
                getattr(self, inp_name).textChanged.connect(self.validate_numeric_input)
    
    def validate_numeric_input(self, text):
        """Validate numeric input fields"""
        sender = self.sender()
        if sender and text:
            try:
                float(text)
                sender.setStyleSheet(HOME_INPUT_STYLE)
            except ValueError:
                sender.setStyleSheet("background-color: #FFCCCC; border: 1px solid red;")
        elif sender:
            sender.setStyleSheet(HOME_INPUT_STYLE)
    
    def get_all_parameters(self):
        """Get all home page parameters as dictionary for PLC"""
        return {
            'batch_id': self.batch_input.text(),
            'target_prod': self.target_input.text(),
            'file': self.file_input.text(),
            'layers': self.layers_input.text(),
            's_mm': self.s_input.text(),
            'l_mm': self.l_input.text(),
            'ss_mm': self.ss_input.text(),
            'fabric_thickness_mm': self.fabric_input.text(),
            'conveyor_offset_mm': self.conveyor_input.text(),
            'feeding_speed': self.feeding_scrollbar.value() if hasattr(self, 'feeding_scrollbar') else 5,
            'unloading_speed': self.unloading_scrollbar.value() if hasattr(self, 'unloading_scrollbar') else 5,
            'upstroke_speed': self.upstroke_scrollbar.value() if hasattr(self, 'upstroke_scrollbar') else 5,
            'selective_mode': self.get_selected_mode(),
            'l1_enabled': self.l1_checkbox.isChecked() if hasattr(self, 'l1_checkbox') else False,
            'l1_value': self.l1_input.text() if hasattr(self, 'l1_input') else '',
            'l2_enabled': self.l2_checkbox.isChecked() if hasattr(self, 'l2_checkbox') else False,
            'l2_value': self.l2_input.text() if hasattr(self, 'l2_input') else '',
            'l3_enabled': self.l3_checkbox.isChecked() if hasattr(self, 'l3_checkbox') else False,
            'l3_value': self.l3_input.text() if hasattr(self, 'l3_input') else '',
            'l4_enabled': self.l4_checkbox.isChecked() if hasattr(self, 'l4_checkbox') else False,
            'l4_value': self.l4_input.text() if hasattr(self, 'l4_input') else '',
        }
    
    def get_selected_mode(self):
        """Get selected selective movement mode"""
        if hasattr(self, 'standard_radio') and self.standard_radio.isChecked():
            return 'Standard'
        elif hasattr(self, 'bundle_shift_radio') and self.bundle_shift_radio.isChecked():
            return 'Bundle Shift'
        elif hasattr(self, 'multi_step_radio') and self.multi_step_radio.isChecked():
            return 'Multi Step'
        return 'Standard'