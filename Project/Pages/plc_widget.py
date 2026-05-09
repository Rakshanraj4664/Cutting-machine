# Pages/plc_widget.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame
from PyQt6.QtCore import Qt

class PLCWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.current_data = None
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(5)
        
        # Connection indicator
        self.status_label = QLabel("🔴 PLC: Offline")
        self.status_label.setStyleSheet("font-weight: bold; padding: 3px;")
        layout.addWidget(self.status_label)
        
        # Sensor frame
        frame = QFrame()
        frame.setStyleSheet("border: 1px solid #ccc; border-radius: 5px; padding: 5px;")
        grid = QVBoxLayout(frame)
        
        # Sensor values
        self.sensor_labels = {}
        sensors = ['Sensor1', 'Sensor2', 'Sensor3', 'Sensor4']
        for s in sensors:
            lbl = QLabel(f"{s}: ---")
            lbl.setStyleSheet("font-size: 11px;")
            grid.addWidget(lbl)
            self.sensor_labels[s] = lbl
        
        # Machine status
        self.status_disp = QLabel("Machine: ---")
        self.status_disp.setStyleSheet("font-weight: bold; color: blue;")
        grid.addWidget(self.status_disp)
        
        layout.addWidget(frame)
        self.setMaximumHeight(200)
    
    def update_data(self, data):
        self.current_data = data
        # Update sensor display
        sensors = data.get('sensors', {})
        for i, (name, label) in enumerate(self.sensor_labels.items(), 1):
            val = sensors.get(f's{i}', False)
            status = "● ON" if val else "○ OFF"
            color = "green" if val else "gray"
            label.setText(f"{name}: {status}")
            label.setStyleSheet(f"font-size: 11px; color: {color};")
        
        # Update machine status
        status = data.get('status', 'UNKNOWN')
        self.status_disp.setText(f"Machine: {status}")
    
    def set_connection_status(self, connected):
        if connected:
            self.status_label.setText("🟢 PLC: Online")
            self.status_label.setStyleSheet("font-weight: bold; padding: 3px; color: green;")
        else:
            self.status_label.setText("🔴 PLC: Offline")
            self.status_label.setStyleSheet("font-weight: bold; padding: 3px; color: red;")