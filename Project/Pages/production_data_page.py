from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox, QFileDialog,
    QTabWidget, QGroupBox, QGridLayout, QLineEdit
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor
from styles import *
from pathlib import Path
import csv
import json
from datetime import datetime


class ProductionDataPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(f"background-color: {LIGHT_GREY};")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Title Bar
        title_bar = QFrame()
        title_bar.setStyleSheet(PRODUCTION_TITLEBAR_STYLE)
        title_bar.setFixedHeight(50)
        title_layout = QHBoxLayout(title_bar)
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_label = QLabel("PRODUCTION DATA")
        title_label.setStyleSheet(PRODUCTION_TITLE_LABEL_STYLE)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_layout.addWidget(title_label)
        layout.addWidget(title_bar)
        
        # Create Tab Widget - FIXED: Changed text color to black
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #CCCCCC;
                background-color: white;
            }
            QTabBar::tab {
                background-color: #E0E0E0;
                padding: 8px 20px;
                font-weight: bold;
                color: black;
            }
            QTabBar::tab:selected {
                background-color: #1B2A49;
                color: white;
            }
        """)
        
        # Tab 1: Production Log
        self.setup_log_tab()
        
        # Tab 2: Current Batch Status
        self.setup_batch_tab()
        
        # Tab 3: Machine Statistics
        self.setup_stats_tab()
        
        layout.addWidget(self.tabs)
        
        # Auto-refresh timer (every 5 seconds)
        self.timer = QTimer()
        self.timer.timeout.connect(self.refresh_all)
        self.timer.start(5000)
        
        # Initial load
        self.refresh_all()
    
    # ===========================
    # TAB 1: PRODUCTION LOG
    # ===========================
    
    def setup_log_tab(self):
        """Setup production log tab"""
        log_tab = QWidget()
        log_layout = QVBoxLayout(log_tab)
        log_layout.setContentsMargins(10, 10, 10, 10)
        log_layout.setSpacing(10)
        
        # Button row
        button_row = QHBoxLayout()
        button_row.setSpacing(10)
        
        self.refresh_btn = QPushButton("🔄 Refresh")
        self.refresh_btn.setStyleSheet(PRODUCTION_BUTTON_STYLE)
        self.refresh_btn.setFixedHeight(35)
        self.refresh_btn.clicked.connect(self.refresh_log)
        
        self.export_btn = QPushButton("📎 Export CSV")
        self.export_btn.setStyleSheet(PRODUCTION_BUTTON_STYLE)
        self.export_btn.setFixedHeight(35)
        self.export_btn.clicked.connect(self.export_csv)
        
        self.clear_btn = QPushButton("🗑 Clear Log")
        self.clear_btn.setStyleSheet(PRODUCTION_BUTTON_STYLE)
        self.clear_btn.setFixedHeight(35)
        self.clear_btn.clicked.connect(self.clear_log)
        
        button_row.addWidget(self.refresh_btn)
        button_row.addWidget(self.export_btn)
        button_row.addWidget(self.clear_btn)
        button_row.addStretch()
        log_layout.addLayout(button_row)
        
        # Production table - FIXED: Changed header text color to white (kept as is since dark background)
        self.log_table = QTableWidget()
        self.log_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                alternate-background-color: #F5F5F5;
                gridline-color: #CCCCCC;
            }
            QHeaderView::section {
                background-color: #1B2A49;
                color: white;
                padding: 8px;
                font-weight: bold;
            }
        """)
        self.log_table.setAlternatingRowColors(True)
        self.log_table.setSortingEnabled(True)
        self.log_table.horizontalHeader().setStretchLastSection(True)
        
        log_layout.addWidget(self.log_table)
        
        self.tabs.addTab(log_tab, "📋 Production Log")
    
    # ===========================
    # TAB 2: CURRENT BATCH STATUS
    # ===========================
    
    def setup_batch_tab(self):
        """Setup current batch status tab"""
        batch_tab = QWidget()
        batch_layout = QVBoxLayout(batch_tab)
        batch_layout.setContentsMargins(20, 20, 20, 20)
        batch_layout.setSpacing(20)
        
        # Current Batch Info Group
        batch_group = QGroupBox("Current Batch Information")
        batch_group.setStyleSheet(PRODUCTION_LEGEND_STYLE)
        batch_group.setMinimumHeight(200)
        
        batch_grid = QGridLayout(batch_group)
        batch_grid.setVerticalSpacing(15)
        batch_grid.setHorizontalSpacing(30)
        
        # FIXED: Added black text color to all labels
        # Create labels with black text
        label_style = "color: black; font-weight: bold;"
        
        # Labels and values
        self.batch_id_value = QLabel("---")
        self.batch_id_value.setStyleSheet("color: #1B2A49; font-weight: bold; font-size: 14px;")
        
        self.work_order_value = QLabel("---")
        self.work_order_value.setStyleSheet("color: #1B2A49; font-weight: bold; font-size: 14px;")
        
        self.target_value = QLabel("---")
        self.target_value.setStyleSheet("color: #1B2A49; font-weight: bold; font-size: 14px;")
        
        self.produced_value = QLabel("0")
        self.produced_value.setStyleSheet("color: #2196F3; font-weight: bold; font-size: 18px;")
        
        self.remaining_value = QLabel("---")
        self.remaining_value.setStyleSheet("color: #FF8C42; font-weight: bold; font-size: 14px;")
        
        self.batch_status_value = QLabel("NOT STARTED")
        self.batch_status_value.setStyleSheet("background-color: #D9534F; color: white; padding: 5px; border-radius: 4px;")
        self.batch_status_value.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Add to grid - FIXED: Set label text color to black
        batch_grid.addWidget(self.create_label("Batch ID:"), 0, 0)
        batch_grid.addWidget(self.batch_id_value, 0, 1)
        batch_grid.addWidget(self.create_label("Work Order:"), 0, 2)
        batch_grid.addWidget(self.work_order_value, 0, 3)
        
        batch_grid.addWidget(self.create_label("Target Production:"), 1, 0)
        batch_grid.addWidget(self.target_value, 1, 1)
        batch_grid.addWidget(self.create_label("Produced So Far:"), 1, 2)
        batch_grid.addWidget(self.produced_value, 1, 3)
        
        batch_grid.addWidget(self.create_label("Remaining:"), 2, 0)
        batch_grid.addWidget(self.remaining_value, 2, 1)
        batch_grid.addWidget(self.create_label("Status:"), 2, 2)
        batch_grid.addWidget(self.batch_status_value, 2, 3)
        
        batch_layout.addWidget(batch_group)
        
        # Progress indicators placeholder
        progress_group = QGroupBox("Production Progress")
        progress_group.setStyleSheet(PRODUCTION_LEGEND_STYLE)
        
        progress_layout = QVBoxLayout(progress_group)
        
        self.progress_label = QLabel("No active batch")
        self.progress_label.setStyleSheet("font-size: 16px; color: black; padding: 20px;")  # FIXED: Changed from #666 to black
        self.progress_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        progress_layout.addWidget(self.progress_label)
        batch_layout.addWidget(progress_group)
        
        batch_layout.addStretch()
        
        self.tabs.addTab(batch_tab, "📊 Current Batch")
    
    # ===========================
    # TAB 3: MACHINE STATISTICS
    # ===========================
    
    def setup_stats_tab(self):
        """Setup machine statistics tab"""
        stats_tab = QWidget()
        stats_layout = QGridLayout(stats_tab)
        stats_layout.setContentsMargins(20, 20, 20, 20)
        stats_layout.setSpacing(20)
        
        # Today's Stats Box
        today_group = QGroupBox("Today's Statistics")
        today_group.setStyleSheet(PRODUCTION_LEGEND_STYLE)
        today_layout = QGridLayout(today_group)
        today_layout.setVerticalSpacing(15)
        today_layout.setHorizontalSpacing(30)
        
        self.today_batches_value = QLabel("0")
        self.today_batches_value.setStyleSheet("color: #1B2A49; font-size: 24px; font-weight: bold;")
        
        self.today_cuts_value = QLabel("0")
        self.today_cuts_value.setStyleSheet("color: #1B2A49; font-size: 24px; font-weight: bold;")
        
        self.today_material_value = QLabel("0 m")
        self.today_material_value.setStyleSheet("color: #1B2A49; font-size: 24px; font-weight: bold;")
        
        self.today_uptime_value = QLabel("0 hrs")
        self.today_uptime_value.setStyleSheet("color: #1B2A49; font-size: 24px; font-weight: bold;")
        
        # FIXED: Added black text color to all labels
        today_layout.addWidget(self.create_label("Batches Completed:"), 0, 0)
        today_layout.addWidget(self.today_batches_value, 0, 1)
        today_layout.addWidget(self.create_label("Total Cuts:"), 0, 2)
        today_layout.addWidget(self.today_cuts_value, 0, 3)
        today_layout.addWidget(self.create_label("Material Used:"), 1, 0)
        today_layout.addWidget(self.today_material_value, 1, 1)
        today_layout.addWidget(self.create_label("Machine Uptime:"), 1, 2)
        today_layout.addWidget(self.today_uptime_value, 1, 3)
        
        stats_layout.addWidget(today_group, 0, 0, 1, 2)
        
        # All Time Stats Box
        alltime_group = QGroupBox("All Time Statistics")
        alltime_group.setStyleSheet(PRODUCTION_LEGEND_STYLE)
        alltime_layout = QGridLayout(alltime_group)
        alltime_layout.setVerticalSpacing(15)
        alltime_layout.setHorizontalSpacing(30)
        
        self.total_batches_value = QLabel("0")
        self.total_batches_value.setStyleSheet("color: #1B2A49; font-size: 24px; font-weight: bold;")
        
        self.total_cuts_value = QLabel("0")
        self.total_cuts_value.setStyleSheet("color: #1B2A49; font-size: 24px; font-weight: bold;")
        
        self.total_material_value = QLabel("0 m")
        self.total_material_value.setStyleSheet("color: #1B2A49; font-size: 24px; font-weight: bold;")
        
        self.avg_efficiency_value = QLabel("0%")
        self.avg_efficiency_value.setStyleSheet("color: #1B2A49; font-size: 24px; font-weight: bold;")
        
        # FIXED: Added black text color to all labels
        alltime_layout.addWidget(self.create_label("Total Batches:"), 0, 0)
        alltime_layout.addWidget(self.total_batches_value, 0, 1)
        alltime_layout.addWidget(self.create_label("Total Cuts:"), 0, 2)
        alltime_layout.addWidget(self.total_cuts_value, 0, 3)
        alltime_layout.addWidget(self.create_label("Total Material:"), 1, 0)
        alltime_layout.addWidget(self.total_material_value, 1, 1)
        alltime_layout.addWidget(self.create_label("Avg Efficiency:"), 1, 2)
        alltime_layout.addWidget(self.avg_efficiency_value, 1, 3)
        
        stats_layout.addWidget(alltime_group, 1, 0, 1, 2)
        
        stats_layout.setRowStretch(2, 1)
        
        self.tabs.addTab(stats_tab, "📈 Statistics")
    
    # ===========================
    # HELPER METHODS
    # ===========================
    
    def create_label(self, text):
        """Helper method to create a label with black text"""
        label = QLabel(text)
        label.setStyleSheet("color: black; font-weight: bold;")
        return label
    
    def get_log_path(self):
        """Get path to production log file"""
        log_dir = Path(__file__).parent.parent / "logs"
        log_dir.mkdir(exist_ok=True)
        return log_dir / "production_log.csv"
    
    def refresh_all(self):
        """Refresh all tabs"""
        self.refresh_log()
        self.refresh_batch_status()
        self.refresh_statistics()
    
    def refresh_log(self):
        """Refresh production log table"""
        log_path = self.get_log_path()
        
        headers = ["Timestamp", "Batch ID", "Work Order", "Target", "Actual", "Status", "Operator"]
        
        if not log_path.exists():
            self.log_table.setColumnCount(len(headers))
            self.log_table.setHorizontalHeaderLabels(headers)
            self.log_table.setRowCount(0)
            return
        
        try:
            with open(log_path, 'r') as f:
                reader = csv.reader(f)
                rows = list(reader)
            
            if rows and rows[0] and rows[0][0] == "Timestamp":
                data_rows = rows[1:]
            else:
                data_rows = rows
            
            self.log_table.setColumnCount(len(headers))
            self.log_table.setHorizontalHeaderLabels(headers)
            self.log_table.setRowCount(len(data_rows))
            
            for row_idx, row in enumerate(data_rows):
                for col_idx, value in enumerate(row):
                    if col_idx < len(headers):
                        item = QTableWidgetItem(value)
                        
                        # FIXED: Set text color to black for all cells
                        item.setForeground(QColor("black"))
                        
                        # Color code status column
                        if col_idx == 5:  # Status column
                            if value == "COMPLETED":
                                item.setBackground(QColor("#A0D995"))
                            elif value == "FAILED":
                                item.setBackground(QColor("#D9534F"))
                                item.setForeground(QColor("white"))  # Keep white text on red background
                            elif value == "RUNNING":
                                item.setBackground(QColor("#FFD95A"))
                        
                        self.log_table.setItem(row_idx, col_idx, item)
            
            self.log_table.resizeColumnsToContents()
            
        except Exception as e:
            print(f"Error refreshing log: {e}")
    
    def refresh_batch_status(self):
        """Refresh current batch information"""
        # Try to get current batch info from production page
        try:
            from .production_page import ProductionPage
            # This will be populated when main window passes reference
            if hasattr(self, 'production_page') and self.production_page:
                data = self.production_page.get_form_data()
                
                self.batch_id_value.setText(data.get('batch_id', '---') or '---')
                self.work_order_value.setText(data.get('work_order_id', '---') or '---')
                self.target_value.setText(data.get('target_prod', '---') or '---')
                
                # Update progress label - FIXED: Set text color to black
                target = data.get('target_prod', '0')
                self.progress_label.setText(f"Target: {target} units")
                self.progress_label.setStyleSheet("font-size: 16px; color: black; padding: 20px;")
                
                if data.get('batch_id'):
                    self.batch_status_value.setText("ACTIVE")
                    self.batch_status_value.setStyleSheet("background-color: #A0D995; color: black; padding: 5px; border-radius: 4px;")
        except:
            pass
    
    def refresh_statistics(self):
        """Refresh statistics from log data"""
        log_path = self.get_log_path()
        
        if not log_path.exists():
            return
        
        try:
            with open(log_path, 'r') as f:
                reader = csv.reader(f)
                rows = list(reader)
            
            if len(rows) <= 1:
                return
            
            # Skip header if present
            data_rows = rows[1:] if rows[0][0] == "Timestamp" else rows
            
            today = datetime.now().strftime("%Y-%m-%d")
            today_batches = 0
            today_cuts = 0
            total_batches = 0
            total_cuts = 0
            
            for row in data_rows:
                if len(row) >= 6:
                    # Count completed batches
                    if row[5] == "COMPLETED":
                        total_batches += 1
                        if row[0].startswith(today):
                            today_batches += 1
                    
                    # Sum cuts (actual column)
                    try:
                        actual = int(row[4]) if row[4].isdigit() else 0
                        total_cuts += actual
                        if row[0].startswith(today):
                            today_cuts += actual
                    except:
                        pass
            
            self.today_batches_value.setText(str(today_batches))
            self.today_cuts_value.setText(str(today_cuts))
            self.total_batches_value.setText(str(total_batches))
            self.total_cuts_value.setText(str(total_cuts))
            
        except Exception as e:
            print(f"Error refreshing stats: {e}")
    
    def export_csv(self):
        """Export table data to CSV file"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Export CSV", "", "CSV Files (*.csv)"
        )
        
        if not file_path:
            return
        
        try:
            log_path = self.get_log_path()
            if log_path.exists():
                import shutil
                shutil.copy(log_path, file_path)
                QMessageBox.information(self, "Success", f"Data exported to {file_path}")
            else:
                QMessageBox.warning(self, "Warning", "No data to export.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Export failed: {str(e)}")
    
    def clear_log(self):
        """Clear production log"""
        reply = QMessageBox.question(
            self, "Confirm Clear",
            "Are you sure you want to clear ALL production logs?\nThis action cannot be undone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            log_path = self.get_log_path()
            try:
                if log_path.exists():
                    log_path.unlink()
                # Recreate with headers
                with open(log_path, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(["Timestamp", "Batch ID", "Work Order", "Target", "Actual", "Status", "Operator"])
                self.refresh_all()
                QMessageBox.information(self, "Success", "Log cleared successfully.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to clear log: {str(e)}")
    
    def log_production_entry(self, batch_id, work_order, target, actual, status, operator=""):
        """Add a production entry to log"""
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
            self.refresh_all()
            return True
        except Exception as e:
            print(f"Error logging production: {e}")
            return False
    
    def set_production_page_reference(self, production_page):
        """Set reference to production page for getting current batch data"""
        self.production_page = production_page