from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QFrame, QHBoxLayout,
    QLineEdit, QPushButton, QGridLayout, QGroupBox, QDialog, QDialogButtonBox,
    QMessageBox, QListWidget, QListWidgetItem, QFormLayout, QTextEdit, QScrollArea
)
from PyQt6.QtCore import Qt
import sys, os, json
from pathlib import Path
from PyQt6 import QtWidgets
from datetime import datetime

# Add parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from styles import *


# ===========================
# NEW PRODUCTION DIALOG
# ===========================
class NewProductionDialog(QDialog):
    """Dialog for creating a new production file."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("New Production File")
        self.setGeometry(100, 100, 700, 800)
        self.setMinimumSize(600, 700)
        
        # Apply stylesheet
        self.setStyleSheet(f"background-color: {LIGHT_GREY};")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)
        
        # Scroll area for form
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        
        form_widget = QWidget()
        form_layout = QGridLayout(form_widget)
        form_layout.setSpacing(10)
        
        # Store input fields
        self.inputs = {}
        
        # Define all fields
        fields = [
            "File Name",
            "Work Order ID",
            "Batch ID",
            "ID",
            "Color",
            "Description",
            "Blend",
            "Width [mm]",
            "Target Prod",
            "Style",
            "Size",
            "Shape ID",
            "Shape Label",
            "Weight Loaded",
            "Component",
            "Q-Turn ID",
            "Default Cycle Time [sec]",
            "Layers",
            "S [mm]",
            "L [mm]",
            "SS [mm]",
            "Fabric Thickness [mm]",
            "Conveyor Offset [mm]"
        ]
        
        # Create form fields - FIXED: Added black text color to labels
        for i, field in enumerate(fields):
            label = QLabel(f"{field}:")
            label.setStyleSheet("color: black; font-weight: bold; font-size: 12px;")  # Changed to black
            
            if field == "Description":
                # Use QTextEdit for description (multi-line)
                input_widget = QTextEdit()
                input_widget.setFixedHeight(80)
            else:
                input_widget = QLineEdit()
            
            input_widget.setStyleSheet(PRODUCTION_FORM_INPUT_STYLE)
            
            form_layout.addWidget(label, i, 0)
            form_layout.addWidget(input_widget, i, 1)
            
            # Store reference with normalized key
            key = field.replace(" ", "_").replace("[", "").replace("]", "").lower()
            self.inputs[key] = input_widget
        
        scroll.setWidget(form_widget)
        layout.addWidget(scroll)
        
        # Dialog buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        save_btn = QPushButton("Save")
        save_btn.setStyleSheet(PRODUCTION_BUTTON_STYLE)
        save_btn.setFixedHeight(40)
        save_btn.clicked.connect(self.accept)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet(PRODUCTION_BUTTON_STYLE)
        cancel_btn.setFixedHeight(40)
        cancel_btn.clicked.connect(self.reject)
        
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)
    
    def get_data(self):
        """Get all form data as a dictionary."""
        data = {}
        for key, widget in self.inputs.items():
            if isinstance(widget, QTextEdit):
                data[key] = widget.toPlainText()
            else:
                data[key] = widget.text()
        return data


# ===========================
# SELECT PRODUCTION DIALOG
# ===========================
class SelectProductionDialog(QDialog):
    """Dialog for selecting an existing production file."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Production File")
        self.setGeometry(100, 100, 500, 600)
        self.setMinimumSize(400, 400)
        
        self.setStyleSheet(f"background-color: {LIGHT_GREY};")
        
        self.selected_file = None
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Title - FIXED: Changed to black text
        title = QLabel("Available Production Files:")
        title.setStyleSheet("color: black; font-weight: bold; font-size: 14px;")
        layout.addWidget(title)
        
        # File list - FIXED: Set text color to black
        self.file_list = QListWidget()
        self.file_list.setStyleSheet("""
            QListWidget {
                background-color: white;
                color: black;
                border: 1px solid #CCCCCC;
                border-radius: 4px;
                padding: 5px;
            }
            QListWidget::item {
                padding: 5px;
                color: black;
            }
            QListWidget::item:selected {
                background-color: #1B2A49;
                color: white;
            }
        """)
        self.populate_file_list()
        layout.addWidget(self.file_list)
        
        # Dialog buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        select_btn = QPushButton("Select")
        select_btn.setStyleSheet(PRODUCTION_BUTTON_STYLE)
        select_btn.setFixedHeight(40)
        select_btn.clicked.connect(self.select_file)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet(PRODUCTION_BUTTON_STYLE)
        cancel_btn.setFixedHeight(40)
        cancel_btn.clicked.connect(self.reject)
        
        button_layout.addWidget(select_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)
    
    def populate_file_list(self):
        """Populate list with available production files."""
        prod_dir = self.get_production_dir()
        self.file_list.clear()
        
        if not prod_dir.exists():
            return
        
        json_files = sorted(prod_dir.glob("*.json"))
        for json_file in json_files:
            # Show filename without .json extension
            file_name = json_file.stem
            item = QListWidgetItem(file_name)
            item.setData(Qt.ItemDataRole.UserRole, str(json_file))
            self.file_list.addItem(item)
    
    def select_file(self):
        """Confirm file selection."""
        current_item = self.file_list.currentItem()
        if current_item:
            self.selected_file = current_item.data(Qt.ItemDataRole.UserRole)
            self.accept()
        else:
            QMessageBox.warning(self, "Selection", "Please select a file first.")
    
    @staticmethod
    def get_production_dir():
        """Get or create production files directory."""
        prod_dir = Path(__file__).parent.parent / "production_files"
        prod_dir.mkdir(exist_ok=True)
        return prod_dir


# ===========================
# RENAME PRODUCTION DIALOG
# ===========================
class RenameProductionDialog(QDialog):
    """Dialog for renaming a production file."""
    
    def __init__(self, current_name, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Rename Production File")
        self.setGeometry(100, 100, 400, 150)
        
        self.setStyleSheet(f"background-color: {LIGHT_GREY};")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Label - FIXED: Changed to black text
        label = QLabel("New File Name:")
        label.setStyleSheet("color: black; font-weight: bold; font-size: 12px;")
        layout.addWidget(label)
        
        # Input - FIXED: Set text color to black
        self.name_input = QLineEdit()
        self.name_input.setText(current_name)
        self.name_input.setStyleSheet("""
            QLineEdit {
                background-color: white;
                color: black;
                border: 1px solid #CCCCCC;
                border-radius: 4px;
                padding: 5px;
            }
        """)
        self.name_input.setFixedHeight(40)
        self.name_input.selectAll()
        layout.addWidget(self.name_input)
        
        # Dialog buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        ok_btn = QPushButton("OK")
        ok_btn.setStyleSheet(PRODUCTION_BUTTON_STYLE)
        ok_btn.setFixedHeight(40)
        ok_btn.clicked.connect(self.accept)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet(PRODUCTION_BUTTON_STYLE)
        cancel_btn.setFixedHeight(40)
        cancel_btn.clicked.connect(self.reject)
        
        button_layout.addWidget(ok_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)
    
    def get_new_name(self):
        """Get the new filename."""
        return self.name_input.text().strip()


# ===========================
# MAIN PRODUCTION PAGE
# ===========================
class ProductionPage(QWidget):
    def __init__(self, main_window=None):
        super().__init__()
        self.main_window = main_window  # Reference to main window to access home page
        self.setStyleSheet(f"background-color: {LIGHT_GREY};")
        
        # Store currently loaded file
        self.current_file = None

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
        title_label = QLabel("PRODUCTION")
        title_label.setStyleSheet(PRODUCTION_TITLE_LABEL_STYLE)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_layout.addWidget(title_label)
        layout.addWidget(title_bar)

        # -------------------------
        # First Row (Work Order + Batch ID + Button)
        # -------------------------
        input_frame = QFrame()
        input_frame.setObjectName("first_row_frame")
        input_frame.setStyleSheet(PRODUCTION_FIRST_ROW_STYLE)
        input_frame.setFixedHeight(50)

        input_layout = QHBoxLayout(input_frame)
        input_layout.setContentsMargins(10, 5, 10, 5)
        input_layout.setSpacing(20)

        workorder_label = QLabel("Work Order ID:")
        workorder_label.setStyleSheet("color: black; font-weight: bold;")  # FIXED: Changed to black
        self.workorder_input = QLineEdit()
        self.workorder_input.setStyleSheet(PRODUCTION_INPUT_BOX_STYLE)

        batch_label = QLabel("Batch ID:")
        batch_label.setStyleSheet("color: black; font-weight: bold;")  # FIXED: Changed to black
        self.batch_input = QLineEdit()
        self.batch_input.setStyleSheet(PRODUCTION_INPUT_BOX_STYLE)

        close_batch_btn = QPushButton("CLOSE BATCH")
        close_batch_btn.setStyleSheet(PRODUCTION_BUTTON_STYLE)

        input_layout.addWidget(workorder_label)
        input_layout.addWidget(self.workorder_input)
        input_layout.addWidget(batch_label)
        input_layout.addWidget(self.batch_input)
        input_layout.addWidget(close_batch_btn)
        layout.addWidget(input_frame)

        # -------------------------
        # Second Row (Left + Right Columns)
        # -------------------------
        second_row = QFrame()
        second_row.setStyleSheet(PRODUCTION_SECOND_ROW_STYLE)

        second_layout = QHBoxLayout(second_row)
        second_layout.setSpacing(60)  # gap between left and right
        second_layout.setContentsMargins(10, 10, 10, 10)

        # ---- Left Column ----
        left_col = QFrame()
        left_layout = QGridLayout(left_col)
        left_layout.setVerticalSpacing(10)
        left_layout.setColumnStretch(1, 1)

        # Store left column inputs
        # FIXED: _add_row now uses black text
        self.target_prod_input = self._add_row(left_layout, 0, "Target Prod :")
        self.style_input = self._add_row(left_layout, 1, "Style :")
        self.size_input = self._add_row(left_layout, 2, "Size :")
        self.shape_id_input = self._add_row(left_layout, 3, "Shape ID :")
        self.shape_label_input = self._add_row(left_layout, 4, "Shape Label :")
        self.weight_loaded_input = self._add_row(left_layout, 5, "Weight Loaded :")
        self.component_input = self._add_row(left_layout, 6, "Component :")
        self.qturn_id_input = self._add_row(left_layout, 7, "Q-Turn ID :")
        self.default_cycle_time_input = self._add_row(left_layout, 8, "Default Cycle Time [sec] :")

        second_layout.addWidget(left_col, 2)

        # ---- Right Column (Fabric GroupBox) ----
        right_col = QGroupBox("Fabric")
        right_col.setStyleSheet(PRODUCTION_LEGEND_STYLE)

        right_layout = QGridLayout(right_col)
        right_layout.setVerticalSpacing(10)

        # Store right column inputs
        # FIXED: _add_right_row now uses black text
        self.fabric_id_input = self._add_right_row(right_layout, 0, "ID :")
        self.color_input = self._add_right_row(right_layout, 1, "Color :")
        self.fabric_description_input = self._add_right_row(right_layout, 2, "Description :", height=60)
        self.blend_input = self._add_right_row(right_layout, 3, "Blend :")
        self.width_input = self._add_right_row(right_layout, 4, "Width [mm] :")

        second_layout.addWidget(right_col, 3)
        layout.addWidget(second_row)

        # -------------------------
        # Third Row (Cutting File Info)
        # -------------------------
        third_row = QGroupBox("Cutting File Info")
        third_row.setStyleSheet(PRODUCTION_LEGEND_STYLE)

        third_layout = QVBoxLayout(third_row)
        third_layout.setContentsMargins(15, 15, 15, 15)
        third_layout.setSpacing(15)

        # ---- First Row: File + Buttons ----
        first_row_frame = QFrame()
        first_row_layout = QHBoxLayout(first_row_frame)
        first_row_layout.setContentsMargins(0, 0, 0, 0)
        first_row_layout.setSpacing(20)

        # Left half: File
        file_frame = QFrame()
        file_layout = QHBoxLayout(file_frame)
        file_layout.setContentsMargins(0, 0, 0, 0)
        file_layout.setSpacing(5)

        file_label = QLabel("File:")
        file_label.setStyleSheet("color: black; font-weight: bold; font-size: 12px;")  # FIXED: Changed to black

        self.file_input = QLineEdit()
        self.file_input.setReadOnly(True)
        self.file_input.setStyleSheet("""
            QLineEdit {
                background-color: #F0F0F0;
                color: black;
                border: 1px solid #CCCCCC;
                border-radius: 4px;
                padding: 5px;
            }
        """)
        self.file_input.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)

        file_layout.addWidget(file_label)
        file_layout.addWidget(self.file_input)
        file_frame.setLayout(file_layout)
        first_row_layout.addWidget(file_frame, 1)

        # Right half: Buttons
        buttons_frame = QFrame()
        buttons_layout = QHBoxLayout(buttons_frame)
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        buttons_layout.setSpacing(10)

        select_btn = QPushButton("Select")
        select_btn.setStyleSheet(PRODUCTION_BUTTON_STYLE)
        select_btn.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        select_btn.clicked.connect(self.on_select_clicked)

        delete_btn = QPushButton("Delete")
        delete_btn.setStyleSheet(PRODUCTION_BUTTON_STYLE)
        delete_btn.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        delete_btn.clicked.connect(self.on_delete_clicked)

        rename_btn = QPushButton("Rename")
        rename_btn.setStyleSheet(PRODUCTION_BUTTON_STYLE)
        rename_btn.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        rename_btn.clicked.connect(self.on_rename_clicked)

        buttons_layout.addWidget(select_btn)
        buttons_layout.addWidget(delete_btn)
        buttons_layout.addWidget(rename_btn)
        buttons_frame.setLayout(buttons_layout)
        first_row_layout.addWidget(buttons_frame, 1)

        third_layout.addWidget(first_row_frame)

        # ---- Second Row: Description + New/Copy ----
        second_row_frame = QFrame()
        second_row_layout = QHBoxLayout(second_row_frame)
        second_row_layout.setContentsMargins(0, 0, 0, 0)
        second_row_layout.setSpacing(10)

        # Left: Description (3/4 width)
        description_frame = QFrame()
        description_layout = QHBoxLayout(description_frame)
        description_layout.setContentsMargins(0, 0, 0, 0)
        description_label = QLabel("Description:")
        description_label.setStyleSheet("color: black; font-weight: bold; font-size: 12px;")  # FIXED: Changed to black
        self.cutting_file_description_input = QLineEdit()
        self.cutting_file_description_input.setStyleSheet("""
            QLineEdit {
                background-color: white;
                color: black;
                border: 1px solid #CCCCCC;
                border-radius: 4px;
                padding: 5px;
            }
        """)
        self.cutting_file_description_input.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)

        description_layout.addWidget(description_label)
        description_layout.addWidget(self.cutting_file_description_input)
        description_frame.setLayout(description_layout)
        second_row_layout.addWidget(description_frame, 3)

        # Right: New + Copy (1/4 width)
        right_buttons_frame = QFrame()
        right_buttons_layout = QHBoxLayout(right_buttons_frame)
        right_buttons_layout.setContentsMargins(0, 0, 0, 0)
        right_buttons_layout.setSpacing(10)

        new_btn = QPushButton("New")
        new_btn.setStyleSheet(PRODUCTION_BUTTON_STYLE)
        new_btn.clicked.connect(self.on_new_clicked)
        new_btn.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)

        copy_btn = QPushButton("Copy")
        copy_btn.setStyleSheet(PRODUCTION_BUTTON_STYLE)
        copy_btn.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)

        right_buttons_layout.addWidget(new_btn)
        right_buttons_layout.addWidget(copy_btn)
        right_buttons_frame.setLayout(right_buttons_layout)
        second_row_layout.addWidget(right_buttons_frame, 1)

        third_layout.addWidget(second_row_frame)

        # Add third_row to main layout
        layout.addWidget(third_row)

    # ===========================
    # HELPER METHODS FOR UI BUILDING
    # ===========================
    
    def _add_row(self, layout, row, label_text):
        """Add a single input row and return the input widget."""
        lbl = QLabel(label_text)
        lbl.setStyleSheet("color: black; font-weight: bold; font-size: 12px;")  # FIXED: Changed to black
        box = QLineEdit()
        box.setStyleSheet("""
            QLineEdit {
                background-color: white;
                color: black;
                border: 1px solid #CCCCCC;
                border-radius: 4px;
                padding: 5px;
            }
        """)
        layout.addWidget(lbl, row, 0)
        layout.addWidget(box, row, 1)
        return box

    def _add_right_row(self, layout, row, label_text, height=None):
        """Add a single input row to right column and return the input widget."""
        lbl = QLabel(label_text)
        lbl.setStyleSheet("color: black; font-weight: bold; font-size: 12px;")  # FIXED: Changed to black
        box = QLineEdit()
        box.setStyleSheet("""
            QLineEdit {
                background-color: white;
                color: black;
                border: 1px solid #CCCCCC;
                border-radius: 4px;
                padding: 5px;
            }
        """)
        if height:
            box.setFixedHeight(height)
        layout.addWidget(lbl, row, 0)
        layout.addWidget(box, row, 1)
        return box

    # ===========================
    # PRODUCTION FILE MANAGEMENT METHODS
    # ===========================

    @staticmethod
    def get_production_dir():
        """Get or create production files directory."""
        prod_dir = Path(__file__).parent.parent / "production_files"
        prod_dir.mkdir(exist_ok=True)
        return prod_dir

    def get_form_data(self):
        """Get all form data as a dictionary."""
        data = {
            "file_name": self.file_input.text(),
            "work_order_id": self.workorder_input.text(),
            "batch_id": self.batch_input.text(),
            "id": self.fabric_id_input.text(),
            "color": self.color_input.text(),
            "description": self.fabric_description_input.text(),
            "blend": self.blend_input.text(),
            "width_mm": self.width_input.text(),
            "target_prod": self.target_prod_input.text(),
            "style": self.style_input.text(),
            "size": self.size_input.text(),
            "shape_id": self.shape_id_input.text(),
            "shape_label": self.shape_label_input.text(),
            "weight_loaded": self.weight_loaded_input.text(),
            "component": self.component_input.text(),
            "qturn_id": self.qturn_id_input.text(),
            "default_cycle_time_sec": self.default_cycle_time_input.text(),
            "cutting_file_description": self.cutting_file_description_input.text(),
        }
        return data

    def populate_fields(self, data):
        """Populate form fields from data dictionary."""
        try:
            # Populate production page fields
            self.file_input.setText(data.get("file_name", ""))
            self.workorder_input.setText(data.get("work_order_id", ""))
            self.batch_input.setText(data.get("batch_id", ""))
            self.fabric_id_input.setText(data.get("id", ""))
            self.color_input.setText(data.get("color", ""))
            self.fabric_description_input.setText(data.get("description", ""))
            self.blend_input.setText(data.get("blend", ""))
            self.width_input.setText(data.get("width_mm", ""))
            self.target_prod_input.setText(data.get("target_prod", ""))
            self.style_input.setText(data.get("style", ""))
            self.size_input.setText(data.get("size", ""))
            self.shape_id_input.setText(data.get("shape_id", ""))
            self.shape_label_input.setText(data.get("shape_label", ""))
            self.weight_loaded_input.setText(data.get("weight_loaded", ""))
            self.component_input.setText(data.get("component", ""))
            self.qturn_id_input.setText(data.get("qturn_id", ""))
            self.default_cycle_time_input.setText(data.get("default_cycle_time_sec", ""))
            self.cutting_file_description_input.setText(data.get("cutting_file_description", ""))
            
            # Populate home page fields if main window reference exists
            if self.main_window and hasattr(self.main_window, 'pages') and 'Home' in self.main_window.pages:
                home_page = self.main_window.pages['Home']
                if hasattr(home_page, 'batch_input'):
                    home_page.batch_input.setText(data.get("batch_id", ""))
                if hasattr(home_page, 'target_input'):
                    home_page.target_input.setText(data.get("target_prod", ""))
                if hasattr(home_page, 'file_input'):
                    home_page.file_input.setText(data.get("file_name", ""))
                if hasattr(home_page, 'layers_input'):
                    home_page.layers_input.setText(data.get("layers", ""))
                if hasattr(home_page, 's_input'):
                    home_page.s_input.setText(data.get("s_mm", ""))
                if hasattr(home_page, 'l_input'):
                    home_page.l_input.setText(data.get("l_mm", ""))
                if hasattr(home_page, 'ss_input'):
                    home_page.ss_input.setText(data.get("ss_mm", ""))
                if hasattr(home_page, 'fabric_input'):
                    home_page.fabric_input.setText(data.get("fabric_thickness_mm", ""))
                if hasattr(home_page, 'conveyor_input'):
                    home_page.conveyor_input.setText(data.get("conveyor_offset_mm", ""))
            
            # Refresh production data page
            if self.main_window and hasattr(self.main_window, 'pages'):
                prod_data_page = self.main_window.pages.get("Production Data")
                if prod_data_page and hasattr(prod_data_page, 'refresh_all'):
                    prod_data_page.refresh_all()
                    
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to populate fields: {str(e)}")

    def save_production_file(self, data, filename):
        """Save production data to JSON file."""
        try:
            prod_dir = self.get_production_dir()
            file_path = prod_dir / f"{filename}.json"
            
            # Clean filename
            if not filename.strip():
                QMessageBox.warning(self, "Error", "File name cannot be empty.")
                return False
            
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2)
            
            self.current_file = str(file_path)
            self.file_input.setText(filename)
            QMessageBox.information(self, "Success", f"Production file '{filename}' saved successfully.")
            return True
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save file: {str(e)}")
            return False

    def load_production_file(self, file_path):
        """Load production data from JSON file."""
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            self.current_file = file_path
            self.populate_fields(data)
            QMessageBox.information(self, "Success", "Production file loaded successfully.")
            return True
        except json.JSONDecodeError:
            QMessageBox.critical(self, "Error", "Invalid JSON file format. File may be corrupted.")
            return False
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load file: {str(e)}")
            return False

    def clear_all_fields(self):
        """Clear all form input fields."""
        self.workorder_input.clear()
        self.batch_input.clear()
        self.fabric_id_input.clear()
        self.color_input.clear()
        self.fabric_description_input.clear()
        self.blend_input.clear()
        self.width_input.clear()
        self.target_prod_input.clear()
        self.style_input.clear()
        self.size_input.clear()
        self.shape_id_input.clear()
        self.shape_label_input.clear()
        self.weight_loaded_input.clear()
        self.component_input.clear()
        self.qturn_id_input.clear()
        self.default_cycle_time_input.clear()
        self.cutting_file_description_input.clear()
        self.file_input.clear()
        self.current_file = None

    def delete_production_file(self, file_path):
        """Delete a production JSON file."""
        try:
            Path(file_path).unlink()
            self.clear_all_fields()
            QMessageBox.information(self, "Success", "Production file deleted successfully.")
            return True
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to delete file: {str(e)}")
            return False

    def rename_production_file(self, old_path, new_name):
        """Rename a production JSON file."""
        try:
            old_path_obj = Path(old_path)
            prod_dir = self.get_production_dir()
            new_path = prod_dir / f"{new_name}.json"
            
            if new_path.exists():
                QMessageBox.warning(self, "Error", f"File '{new_name}.json' already exists.")
                return False
            
            old_path_obj.rename(new_path)
            
            if self.current_file == str(old_path_obj):
                self.current_file = str(new_path)
                self.file_input.setText(new_name)
            
            QMessageBox.information(self, "Success", f"File renamed to '{new_name}' successfully.")
            return True
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to rename file: {str(e)}")
            return False

    # ===========================
    # BUTTON HANDLERS
    # ===========================

    def on_new_clicked(self):
        """Handle 'New' button click - open new production dialog."""
        dialog = NewProductionDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            filename = data.get("file_name", "").strip()
            
            if not filename:
                QMessageBox.warning(self, "Error", "File name is required.")
                return
            
            if self.save_production_file(data, filename):
                # Automatically populate both production page and homeduction page and home page fields with the saved data
                self.populate_fields(data)

    def on_select_clicked(self):
        """Handle 'Select' button click - open file selection dialog."""
        dialog = SelectProductionDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted and dialog.selected_file:
            self.load_production_file(dialog.selected_file)

    def on_delete_clicked(self):
        """Handle 'Delete' button click - delete selected file."""
        if not self.current_file:
            QMessageBox.warning(self, "Warning", "No file selected to delete.")
            return
        
        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            f"Are you sure you want to delete this file?\nThis action cannot be undone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.delete_production_file(self.current_file)

    def on_rename_clicked(self):
        """Handle 'Rename' button click - rename selected file."""
        if not self.current_file:
            QMessageBox.warning(self, "Warning", "No file selected to rename.")
            return
        
        current_filename = Path(self.current_file).stem
        dialog = RenameProductionDialog(current_filename, self)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_name = dialog.get_new_name()
            if new_name:
                self.rename_production_file(self.current_file, new_name)

    # ===========================
    # LOGGING METHODS
    # ===========================

    def get_log_path(self):
        """Get or create production log file"""
        log_dir = Path(__file__).parent.parent / "logs"
        log_dir.mkdir(exist_ok=True)
        return log_dir / "production_log.csv"
    
    def log_production_entry(self, batch_id, work_order, target, actual, status, operator="SYSTEM"):
        """Log a production entry to CSV"""
        import csv
        log_path = self.get_log_path()
        file_exists = log_path.exists()
        
        try:
            with open(log_path, 'a', newline='') as f:
                writer = csv.writer(f)
                if not file_exists:
                    writer.writerow(["Timestamp", "Batch ID", "Work Order", "Target", "Actual", "Status", "Operator"])
                writer.writerow([
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    batch_id,
                    work_order,
                    target,
                    actual,
                    status,
                    operator
                ])
            
            # Notify production data page if available
            if self.main_window and hasattr(self.main_window, 'pages'):
                prod_data_page = self.main_window.pages.get("Production Data")
                if prod_data_page and hasattr(prod_data_page, 'refresh_all'):
                    prod_data_page.refresh_all()
            
            return True
        except Exception as e:
            print(f"Error logging production: {e}")
            return False
    
    def log_batch_started(self):
        """Log when a batch is started"""
        data = self.get_form_data()
        batch_id = data.get('batch_id', 'N/A')
        work_order = data.get('work_order_id', 'N/A')
        target = data.get('target_prod', '0')
        
        if batch_id and batch_id != 'N/A':
            self.log_production_entry(
                batch_id=batch_id,
                work_order=work_order,
                target=target,
                actual=0,
                status="STARTED",
                operator="SYSTEM"
            )
            self.rename_production_file(self.current_file, new_name)