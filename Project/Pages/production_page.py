from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QFrame, QHBoxLayout,
    QLineEdit, QPushButton, QGridLayout, QGroupBox, QDialog, QDialogButtonBox
)
from PyQt6.QtCore import Qt
import sys, os
from PyQt6 import QtWidgets

# Add parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from styles import *

class ProductionPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(f"background-color: {LIGHT_GREY};")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(15)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # -------------------------
        # Title Bar
        # -------------------------
        title_bar = QFrame()
        title_bar.setStyleSheet(PRODUCTION_TITLEBAR_STYLE)
        title_bar.setFixedHeight(50)

        title_layout = QHBoxLayout(title_bar)
        title_layout.setContentsMargins(0,0,0,0)
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
        input_layout.setContentsMargins(10,5,10,5)
        input_layout.setSpacing(20)

        workorder_label = QLabel("Work Order ID:")
        workorder_label.setStyleSheet(PRODUCTION_LABEL_STYLE)
        workorder_input = QLineEdit()
        workorder_input.setStyleSheet(PRODUCTION_INPUT_BOX_STYLE)

        batch_label = QLabel("Batch ID:")
        batch_label.setStyleSheet(PRODUCTION_LABEL_STYLE)
        batch_input = QLineEdit()
        batch_input.setStyleSheet(PRODUCTION_INPUT_BOX_STYLE)

        close_batch_btn = QPushButton("CLOSE BATCH")
        close_batch_btn.setStyleSheet(PRODUCTION_BUTTON_STYLE)

        input_layout.addWidget(workorder_label)
        input_layout.addWidget(workorder_input)
        input_layout.addWidget(batch_label)
        input_layout.addWidget(batch_input)
        input_layout.addWidget(close_batch_btn)
        layout.addWidget(input_frame)

        # -------------------------
        # Second Row (Left + Right Columns)
        # -------------------------
        second_row = QFrame()
        second_row.setStyleSheet(PRODUCTION_SECOND_ROW_STYLE)

        second_layout = QHBoxLayout(second_row)
        second_layout.setSpacing(60)  # gap between left and right
        second_layout.setContentsMargins(10,10,10,10)

        # ---- Left Column ----
        left_col = QFrame()
        left_layout = QGridLayout(left_col)
        left_layout.setVerticalSpacing(10)
        left_layout.setColumnStretch(1, 1)

        def add_row(row, label_text, multi_input=False, height=None):
            lbl = QLabel(label_text)
            lbl.setStyleSheet(PRODUCTION_FORM_LABEL_STYLE)
            if multi_input:
                box1 = QLineEdit()
                box1.setStyleSheet(PRODUCTION_FORM_INPUT_STYLE)
                box2 = QLineEdit()
                box2.setStyleSheet(PRODUCTION_FORM_INPUT_STYLE)
                left_layout.addWidget(lbl, row, 0)
                left_layout.addWidget(box1, row, 1)
                left_layout.addWidget(box2, row, 2)
            else:
                box = QLineEdit()
                box.setStyleSheet(PRODUCTION_FORM_INPUT_STYLE)
                if height: box.setFixedHeight(height)
                left_layout.addWidget(lbl, row, 0)
                left_layout.addWidget(box, row, 1)

        add_row(0, "Target Prod :")
        add_row(1, "Styles :")
        add_row(2, "Size :")
        add_row(3, "Shape ID :", multi_input=True)
        add_row(4, "Shape Label :")
        add_row(5, "Weight Loaded :")
        add_row(6, "Component :")
        add_row(7, "Q-Turn ID :")
        add_row(8, "Default Cycle Time [sec] :")

        second_layout.addWidget(left_col, 2)

        # ---- Right Column (Fabric GroupBox) ----
        right_col = QGroupBox("Fabric")
        right_col.setStyleSheet(PRODUCTION_LEGEND_STYLE)

        right_layout = QGridLayout(right_col)
        right_layout.setVerticalSpacing(10)

        def add_right_row(row, label_text, height=None):
            lbl = QLabel(label_text)
            lbl.setStyleSheet(PRODUCTION_FORM_LABEL_STYLE)
            box = QLineEdit()
            box.setStyleSheet(PRODUCTION_FORM_INPUT_STYLE)
            if height: box.setFixedHeight(height)
            right_layout.addWidget(lbl, row, 0)
            right_layout.addWidget(box, row, 1)

        add_right_row(0, "ID :")
        add_right_row(1, "Color :")
        add_right_row(2, "Description :", height=60)
        add_right_row(3, "Blend :")
        add_right_row(4, "Width [mm] :")

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
        file_label.setStyleSheet(PRODUCTION_FORM_LABEL_STYLE)

        file_input = QLineEdit()
        file_input.setText("gibberishword1 gibberishword2 gibberishword3 ...")  # 10 words
        file_input.setStyleSheet(PRODUCTION_FORM_INPUT_STYLE)
        file_input.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)

        file_layout.addWidget(file_label)
        file_layout.addWidget(file_input)
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

        delete_btn = QPushButton("Delete")
        delete_btn.setStyleSheet(PRODUCTION_BUTTON_STYLE)
        delete_btn.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)

        rename_btn = QPushButton("Rename")
        rename_btn.setStyleSheet(PRODUCTION_BUTTON_STYLE)
        rename_btn.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)

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
        description_label.setStyleSheet(PRODUCTION_FORM_LABEL_STYLE)
        description_input = QLineEdit()
        description_input.setStyleSheet(PRODUCTION_FORM_INPUT_STYLE)
        description_input.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)

        description_layout.addWidget(description_label)
        description_layout.addWidget(description_input)
        description_frame.setLayout(description_layout)
        second_row_layout.addWidget(description_frame, 3)

        # Right: New + Copy (1/4 width)
        right_buttons_frame = QFrame()
        right_buttons_layout = QHBoxLayout(right_buttons_frame)
        right_buttons_layout.setContentsMargins(0, 0, 0, 0)
        right_buttons_layout.setSpacing(10)

        def new_popup():
            popup = QtWidgets.QMessageBox()
            popup.setWindowTitle("New Item")
            popup.setText("New pop-up content goes here.")
            popup.exec()

        new_btn = QPushButton("New")
        new_btn.setStyleSheet(PRODUCTION_BUTTON_STYLE)
        new_btn.clicked.connect(new_popup)
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
