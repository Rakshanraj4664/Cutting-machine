from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel, QLineEdit,
    QPushButton, QSpinBox, QGroupBox
)
from styles import *
from pathlib import Path
import json


class TFManagementPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(f"background-color: {LIGHT_GREY};")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(15)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # -------------------------
        # Title Bar
        # -------------------------
        title_bar = QFrame()
        title_bar.setStyleSheet(PRODUCTION_TITLEBAR_STYLE)
        title_bar.setFixedHeight(50)

        title_layout = QHBoxLayout(title_bar)
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_label = QLabel("TF Management")
        title_label.setStyleSheet(PRODUCTION_TITLE_LABEL_STYLE)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_layout.addWidget(title_label)

        layout.addWidget(title_bar)

        # -------------------------
        # First Black Bordered Box (TF Section)
        # -------------------------
        first_black_box = QFrame()
        first_black_box.setObjectName("outerBlackBox")
        first_black_box.setStyleSheet(TFMANAGEMENT_OUTER_BOX_STYLE)
        first_black_box.setFixedHeight(230)
        first_black_box_layout = QVBoxLayout(first_black_box)
        first_black_box_layout.setContentsMargins(20, 20, 20, 20)
        first_black_box_layout.setSpacing(15)

        # Timing row
        timing_row = QHBoxLayout()
        boost_label = QLabel("Boost time [ms]:")
        boost_label.setStyleSheet(PRODUCTION_LABEL_STYLE)
        boost_input = QLineEdit()
        boost_input.setStyleSheet(PRODUCTION_INPUT_BOX_STYLE)
        boost_input.setFixedWidth(80)
        boost_input.setFixedHeight(25)

        eclutch_label = QLabel("EClutch time [ms]:")
        eclutch_label.setStyleSheet(PRODUCTION_LABEL_STYLE)
        eclutch_input = QLineEdit()
        eclutch_input.setStyleSheet(PRODUCTION_INPUT_BOX_STYLE)
        eclutch_input.setFixedWidth(80)
        eclutch_input.setFixedHeight(25)

        timing_row.addWidget(boost_label)
        timing_row.addWidget(boost_input)
        timing_row.addSpacing(40)
        timing_row.addWidget(eclutch_label)
        timing_row.addWidget(eclutch_input)
        timing_row.addStretch()
        first_black_box_layout.addLayout(timing_row)
        first_black_box_layout.addSpacing(10)

        # TF Blocks Row + Buttons
        tf_main_row = QHBoxLayout()
        tf_blocks_layout = QHBoxLayout()
        tf_blocks_layout.setSpacing(15)

        for name in ["TF 4", "TF 3", "TF 2", "TF 1"]:
            tf_blocks_layout.addWidget(self.create_tf_block(name))
        tf_blocks_layout.addStretch()

        buttons_layout = QVBoxLayout()
        buttons_layout.addStretch()
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        link_button = QPushButton("LINK")
        link_button.setFixedSize(100, 30)
        link_button.setStyleSheet(PRODUCTION_BUTTON_STYLE)

        trace_button = QPushButton("TRACE")
        trace_button.setFixedSize(100, 30)
        trace_button.setStyleSheet(PRODUCTION_BUTTON_STYLE)

        buttons_layout.addWidget(link_button)
        buttons_layout.addWidget(trace_button)
        buttons_layout.setContentsMargins(0, 0, 15, 0)
        buttons_layout.setAlignment(Qt.AlignmentFlag.AlignBottom)

        tf_main_row.addLayout(tf_blocks_layout)
        tf_main_row.addLayout(buttons_layout)
        first_black_box_layout.addLayout(tf_main_row)

        layout.addWidget(first_black_box)

        # -------------------------
        # Second Black Bordered Box (Roller Section)
        # -------------------------
        roller_group = QGroupBox("Roller")
        roller_group.setObjectName("roller_groupbox")
        roller_group.setStyleSheet(TFMANAGEMENT_ROLLER_BOX_STYLE)
        roller_group.setFixedHeight(180)
        
        roller_layout = QHBoxLayout(roller_group)
        roller_layout.setContentsMargins(0, 20, 20, 20)
        roller_layout.setSpacing(25)
        
        adj_layout = QHBoxLayout()
        adj_layout.setSpacing(15)
        
        # Create Adj boxes
        adj_layout.addWidget(self.create_adj_box("Adj 4%"))
        adj_layout.addWidget(self.create_adj_box("Adj 3%"))
        adj_layout.addWidget(self.create_adj_box("Adj 2%"))
        adj_layout.addWidget(self.create_adj_box("Adj 1%"))
        adj_layout.addStretch()
        
        # Right-side LINK button
        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)
        link_btn = QPushButton("LINK")
        link_btn.setFixedSize(100, 30)
        link_btn.setStyleSheet(PRODUCTION_BUTTON_STYLE)
        right_layout.addWidget(link_btn, alignment=Qt.AlignmentFlag.AlignBottom)

        roller_layout.addLayout(adj_layout)
        roller_layout.addLayout(right_layout)
        
        layout.addWidget(roller_group)

        # ---------------------------------------------------
        # NEW ROW 1 — Input Belt % and Boost Roller %
        # ---------------------------------------------------
        percent_row = QHBoxLayout()
        percent_row.setSpacing(15)
        percent_row.setContentsMargins(20, 0, 20, 0)
        percent_row.addWidget(self.create_adj_box("Input belt %"))
        percent_row.addWidget(self.create_adj_box("Boost roller %"))
        percent_row.addStretch()
        layout.addLayout(percent_row)

        # ---------------------------------------------------
        # NEW ROW 2 — Black Bordered Box with Reset Tubular and Icons
        # ---------------------------------------------------
        black_border_box = QFrame()
        black_border_box.setFixedSize(600, 90)  # Fixed width 600, height 90
        black_border_box.setStyleSheet(BLACK_BORDER_BOX_STYLE)

        inner_layout = QHBoxLayout(black_border_box)
        inner_layout.setContentsMargins(20, 15, 20, 15)
        inner_layout.setSpacing(0)

        # Left: Reset Tubular button
        reset_button = QPushButton("Reset Tubular")
        reset_button.setFixedSize(150, 35)
        reset_button.setStyleSheet(PRODUCTION_BUTTON_STYLE)
        inner_layout.addWidget(reset_button, alignment=Qt.AlignmentFlag.AlignLeft)

        inner_layout.addStretch()

        # Right: 4 mini icon buttons (placeholders)
        icon_layout = QHBoxLayout()
        icon_layout.setSpacing(0)
        for i in range(4):
            icon_btn = QPushButton()
            icon_btn.setFixedSize(50, 50)
            icon_btn.setStyleSheet(TFMANAGEMENT_MINIICON_STYLE)
            icon_layout.addWidget(icon_btn)

        inner_layout.addLayout(icon_layout)
        layout.addWidget(black_border_box, alignment=Qt.AlignmentFlag.AlignLeft)


    # ----------------------------------------------------------------
    # Helper Function: Create TF block (TF 1–4)
    # ----------------------------------------------------------------
    def create_tf_block(self, title):
        block = QFrame()
        block.setFixedSize(180, 130)
        block.setStyleSheet(TFMANAGEMENT_TF_CONTAINER_STYLE)

        layout = QVBoxLayout(block)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        title_label = QLabel(title)
        title_label.setStyleSheet(TFMANAGEMENT_TF_TITLE_STYLE)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        grid_layout = QHBoxLayout()
        grid_layout.setSpacing(5)

        tags_layout = QVBoxLayout()
        tags_layout.setSpacing(8)
        boost_tag = QLabel("Boost:")
        boost_tag.setStyleSheet(TFMANAGEMENT_TF_TAG_STYLE)
        normal_tag = QLabel("Normal:")
        normal_tag.setStyleSheet(TFMANAGEMENT_TF_TAG_STYLE)
        tags_layout.addWidget(boost_tag)
        tags_layout.addWidget(normal_tag)

        inputs_layout = QVBoxLayout()
        inputs_layout.setSpacing(8)
        boost_input = QLineEdit()
        boost_input.setStyleSheet(TFMANAGEMENT_TF_INPUT_STYLE)
        boost_input.setFixedWidth(60)
        normal_input = QLineEdit()
        normal_input.setStyleSheet(TFMANAGEMENT_TF_INPUT_STYLE)
        normal_input.setFixedWidth(60)
        inputs_layout.addWidget(boost_input)
        inputs_layout.addWidget(normal_input)

        grid_layout.addLayout(tags_layout)
        grid_layout.addLayout(inputs_layout)
        grid_layout.addStretch()

        layout.addWidget(title_label)
        layout.addLayout(grid_layout)
        layout.addStretch()
        return block

    # ----------------------------------------------------------------
    # Helper Function: Create Adj-style box (used for Adj%, Input Belt %, Boost Roller %)
    # ----------------------------------------------------------------
    def create_adj_box(self, label_text):
        box = QFrame()
        box.setFixedSize(180, 90)
        box.setStyleSheet(TFMANAGEMENT_ADJ_BLOCK_STYLE)
        
        box_layout = QVBoxLayout(box)
        box_layout.setContentsMargins(15, 15, 15, 15)
        box_layout.setSpacing(10)
        
        label = QLabel(label_text)
        label.setStyleSheet(TFMANAGEMENT_ADJ_LABEL_STYLE)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        spin = QSpinBox()
        spin.setStyleSheet(TFMANAGEMENT_SPINBOX_STYLE)
        spin.setRange(0, 100)
        spin.setValue(0)
        spin.setFixedHeight(25)
        
        box_layout.addWidget(label)
        box_layout.addWidget(spin)
        box_layout.addStretch()
        
        return box
    
    def connect_to_plc(self, plc_handler):
        """Connect all UI controls to PLC handler"""
        self.plc = plc_handler

        # Store all input references for easy access
        self.inputs = {}

        # Find and store all line edits and spinboxes
        for child in self.findChildren(QLineEdit):
            if child.objectName():
                self.inputs[child.objectName()] = child
            else:
                # Set object names for unnamed inputs
                parent = child.parent()
                if parent and hasattr(parent, 'layout'):
                    child.setObjectName(f"input_{id(child)}")
                    self.inputs[child.objectName()] = child

        for child in self.findChildren(QSpinBox):
            if child.objectName():
                self.inputs[child.objectName()] = child
            else:
                child.setObjectName(f"spin_{id(child)}")
                self.inputs[child.objectName()] = child

        # Load saved values from config
        self.load_tf_config()

    def load_tf_config(self):
        """Load TF configuration from file"""
        config_path = Path(__file__).parent.parent / "tf_config.json"
        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    config = json.load(f)

                # Restore values to inputs
                for key, value in config.items():
                    for input_name, input_widget in self.inputs.items():
                        if key.lower() in input_name.lower() or input_name.lower().endswith(f"_{key.lower()}"):
                            if isinstance(input_widget, QLineEdit):
                                input_widget.setText(str(value))
                            elif isinstance(input_widget, QSpinBox):
                                input_widget.setValue(int(value))
            except Exception as e:
                print(f"Error loading TF config: {e}")

    def save_tf_config(self):
        """Save TF configuration to file"""
        config = {}

        # Collect all values
        for name, widget in self.inputs.items():
            if isinstance(widget, QLineEdit):
                config[name] = widget.text()
            elif isinstance(widget, QSpinBox):
                config[name] = widget.value()

        config_path = Path(__file__).parent.parent / "tf_config.json"
        try:
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving TF config: {e}")
            return False

    def send_tf_to_plc(self):
        """Send all TF values to PLC"""
        if not hasattr(self, 'plc') or not self.plc.connected:
            return False

        # Map UI elements to PLC addresses (adjust addresses as needed)
        tf_addresses = {
            'boost_time': 0x4200,
            'eclutch_time': 0x4201,
            'tf1_boost': 0x4210,
            'tf1_normal': 0x4211,
            'tf2_boost': 0x4212,
            'tf2_normal': 0x4213,
            'tf3_boost': 0x4214,
            'tf3_normal': 0x4215,
            'tf4_boost': 0x4216,
            'tf4_normal': 0x4217,
            'adj1': 0x4220,
            'adj2': 0x4221,
            'adj3': 0x4222,
            'adj4': 0x4223,
            'input_belt': 0x4224,
            'boost_roller': 0x4225,
        }

        # Find and send each value
        for child in self.findChildren(QLineEdit):
            for tf_key, address in tf_addresses.items():
                if tf_key.lower() in child.objectName().lower():
                    try:
                        value = int(float(child.text()) if child.text() else 0)
                        self.plc.write_register(address, value)
                    except ValueError:
                        pass
                    
        for child in self.findChildren(QSpinBox):
            for tf_key, address in tf_addresses.items():
                if tf_key.lower() in child.objectName().lower():
                    self.plc.write_register(address, child.value())

        return True

    def on_link_clicked(self):
        """Handle LINK button click - sync adjacent values"""
        # Find all TF blocks and sync values
        tf_blocks = []
        for child in self.findChildren(QFrame):
            if child.styleSheet() == TFMANAGEMENT_TF_CONTAINER_STYLE:
                tf_blocks.append(child)

        # Sync TF 1 with TF 2, TF 3 with TF 4 (example logic)
        for i in range(0, len(tf_blocks) - 1, 2):
            block1_inputs = tf_blocks[i].findChildren(QLineEdit)
            block2_inputs = tf_blocks[i + 1].findChildren(QLineEdit)

            for inp1, inp2 in zip(block1_inputs, block2_inputs):
                inp2.setText(inp1.text())

        self.save_tf_config()
        self.send_tf_to_plc()