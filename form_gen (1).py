import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QTextEdit, QPushButton, QVBoxLayout, QFileDialog, QMessageBox, QComboBox, QScrollArea, QHBoxLayout

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from fpdf import FPDF
import os
from datetime import datetime

class CablewayInspectionApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cableway Inspection Form")
        self.setGeometry(100, 100, 700, 800)
        self.images = []
        
        self.init_ui()

    #User Interface to input values for each field 
    def init_ui(self):                      
        # Create main layout
        main_layout = QVBoxLayout(self)

        # Create scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)  # Allows resizing
        main_layout.addWidget(scroll_area)

        # Create a widget to hold all form elements
        scroll_widget = QWidget()
        scroll_area.setWidget(scroll_widget)

        # Create a vertical layout for form elements
        layout = QVBoxLayout(scroll_widget)

        # Add form input fiels
        self.station_name_input = self.add_input(layout, "Station Name:")
        self.station_number_input = self.add_input(layout, "Station Number:")
        self.date_input = self.add_input(layout, "Date(YYYY-MM-DD):")
        self.temperature_input = self.add_input(layout, "Temperature (°C):")
        self.span_input = self.add_input(layout, "Span (m):")
        self.sag_input = self.add_input(layout, "Sag (m):")
        self.design_load_input = self.add_input(layout, "Design Load (kg):")
        
        # --------------------------------------------------------------------
        # CABLE FIELDS SECTION
        # --------------------------------------------------------------------
        cable_label = QLabel("=== Cable Fields ===")
        layout.addWidget(cable_label)

        diam_label = QLabel("Diameter (in):")
        layout.addWidget(diam_label)
        diam_layout = QHBoxLayout()
        self.cable_diam_main = QLineEdit()
        self.cable_diam_backstay = QLineEdit()
        self.cable_diam_aw = QLineEdit()
        diam_layout.addWidget(QLabel("Main:"))
        diam_layout.addWidget(self.cable_diam_main)
        diam_layout.addWidget(QLabel("LB/Backstay/RB:"))
        diam_layout.addWidget(self.cable_diam_backstay)
        diam_layout.addWidget(QLabel("Aircraft Warning:"))
        diam_layout.addWidget(self.cable_diam_aw)
        layout.addLayout(diam_layout)

        afv_label = QLabel("Angle from Vertical (deg):")
        layout.addWidget(afv_label)
        afv_layout = QHBoxLayout()
        self.cable_afv_yn = QComboBox()
        self.cable_afv_yn.addItems(["LB", "RB"])
        self.cable_afv_main = QLineEdit()
        self.cable_afv_backstay = QLineEdit()
        afv_layout.addWidget(QLabel("LB/RB:"))
        afv_layout.addWidget(self.cable_afv_yn)
        afv_layout.addWidget(QLabel("Main:"))
        afv_layout.addWidget(self.cable_afv_main)
        afv_layout.addWidget(QLabel("LB/Backstay/RB:"))
        afv_layout.addWidget(self.cable_afv_backstay)
        layout.addLayout(afv_layout)

        cable_type_label = QLabel("Cable Type:")
        layout.addWidget(cable_type_label)
        cable_type_layout = QHBoxLayout()
        self.cable_cabt_main = QLineEdit()
        self.cable_cabt_backstay = QLineEdit()
        self.cable_cabt_aw = QLineEdit()
        cable_type_layout.addWidget(QLabel("Main:"))
        cable_type_layout.addWidget(self.cable_cabt_main)
        cable_type_layout.addWidget(QLabel("LB/Backstay/RB:"))
        cable_type_layout.addWidget(self.cable_cabt_backstay)
        cable_type_layout.addWidget(QLabel("Aircraft Warning:"))
        cable_type_layout.addWidget(self.cable_cabt_aw)
        layout.addLayout(cable_type_layout)

        core_type_label = QLabel("Core Type:")
        layout.addWidget(core_type_label)
        core_type_layout = QHBoxLayout()
        self.cable_cort_fw = QComboBox()
        self.cable_cort_fw.addItems(["Fiber", "Wire"])
        self.cable_cort_main = QLineEdit()
        self.cable_cort_backstay = QLineEdit()
        self.cable_cort_aw = QLineEdit()
        core_type_layout.addWidget(QLabel("Fiber/Wire:"))
        core_type_layout.addWidget(self.cable_cort_fw)
        core_type_layout.addWidget(QLabel("Main:"))
        core_type_layout.addWidget(self.cable_cort_main)
        core_type_layout.addWidget(QLabel("LB/Backstay/RB:"))
        core_type_layout.addWidget(self.cable_cort_backstay)
        core_type_layout.addWidget(QLabel("Aircraft Warning:"))
        core_type_layout.addWidget(self.cable_cort_aw)
        layout.addLayout(core_type_layout)

        broken_wires_label = QLabel("Broken Wires (#):")
        layout.addWidget(broken_wires_label)
        bw_layout = QHBoxLayout()
        self.cable_bw_yn = QComboBox()
        self.cable_bw_yn.addItems(["Yes", "No"])
        self.cable_bw_main = QLineEdit()
        self.cable_bw_backstay = QLineEdit()
        self.cable_bw_aw = QLineEdit()
        bw_layout.addWidget(QLabel("Y/N:"))
        bw_layout.addWidget(self.cable_bw_yn)
        bw_layout.addWidget(QLabel("Main:"))
        bw_layout.addWidget(self.cable_bw_main)
        bw_layout.addWidget(QLabel("LB/Backstay/RB:"))
        bw_layout.addWidget(self.cable_bw_backstay)
        bw_layout.addWidget(QLabel("Aircraft Warning:"))
        bw_layout.addWidget(self.cable_bw_aw)
        layout.addLayout(bw_layout)

        pinched_label = QLabel("Pinched Wires(#):")
        layout.addWidget(pinched_label)
        pinched_layout = QHBoxLayout()
        self.cable_pw_yn = QComboBox()
        self.cable_pw_yn.addItems(["Yes", "No"])
        self.cable_pw_main = QLineEdit()
        self.cable_pw_backstay = QLineEdit()
        self.cable_pw_aw = QLineEdit()
        pinched_layout.addWidget(QLabel("Y/N:"))
        pinched_layout.addWidget(self.cable_pw_yn)
        pinched_layout.addWidget(QLabel("Main:"))
        pinched_layout.addWidget(self.cable_pw_main)
        pinched_layout.addWidget(QLabel("LB/Backstay/RB:"))
        pinched_layout.addWidget(self.cable_pw_backstay)
        pinched_layout.addWidget(QLabel("Aircraft Warning:"))
        pinched_layout.addWidget(self.cable_pw_aw)
        layout.addLayout(pinched_layout)

        bs_label = QLabel("Broken Strands(#):")
        layout.addWidget(bs_label)
        bs_layout = QHBoxLayout()
        self.cable_bs_yn = QComboBox()
        self.cable_bs_yn.addItems(["Yes", "No"])
        self.cable_bs_main = QLineEdit()
        self.cable_bs_backstay = QLineEdit()
        self.cable_bs_aw = QLineEdit()
        bs_layout.addWidget(QLabel("Y/N:"))
        bs_layout.addWidget(self.cable_bs_yn)
        bs_layout.addWidget(QLabel("Main:"))
        bs_layout.addWidget(self.cable_bs_main)
        bs_layout.addWidget(QLabel("LB/Backstay/RB:"))
        bs_layout.addWidget(self.cable_bs_backstay)
        bs_layout.addWidget(QLabel("Aircraft Warning:"))
        bs_layout.addWidget(self.cable_bs_aw)
        layout.addLayout(bs_layout)

        fray_label = QLabel("Frays (%):")
        layout.addWidget(fray_label)
        fray_layout = QHBoxLayout()
        self.cable_fray_yn = QComboBox()
        self.cable_fray_yn.addItems(["Yes", "No"])
        self.cable_fray_main = QLineEdit()
        self.cable_fray_backstay = QLineEdit()
        self.cable_fray_aw = QLineEdit()
        fray_layout.addWidget(QLabel("Y/N:"))
        fray_layout.addWidget(self.cable_fray_yn)
        fray_layout.addWidget(QLabel("Main:"))
        fray_layout.addWidget(self.cable_fray_main)
        fray_layout.addWidget(QLabel("LB/Backstay/RB:"))
        fray_layout.addWidget(self.cable_fray_backstay)
        fray_layout.addWidget(QLabel("Aircraft Warning:"))
        fray_layout.addWidget(self.cable_fray_aw)
        layout.addLayout(fray_layout)

        rust_label = QLabel("Rust (%):")
        layout.addWidget(rust_label)
        rust_layout = QHBoxLayout()
        self.cable_rust_yn = QComboBox()
        self.cable_rust_yn.addItems(["Yes", "No"])
        self.cable_rust_main = QLineEdit()
        self.cable_rust_backstay = QLineEdit()
        self.cable_rust_aw = QLineEdit()
        rust_layout.addWidget(QLabel("Y/N:"))
        rust_layout.addWidget(self.cable_rust_yn)
        rust_layout.addWidget(QLabel("Main:"))
        rust_layout.addWidget(self.cable_rust_main)
        rust_layout.addWidget(QLabel("LB/Backstay/RB:"))
        rust_layout.addWidget(self.cable_rust_backstay)
        rust_layout.addWidget(QLabel("Aircraft Warning:"))
        rust_layout.addWidget(self.cable_rust_aw)
        layout.addLayout(rust_layout)

        dist_label = QLabel("Distortion:")
        layout.addWidget(dist_label)
        dist_layout = QHBoxLayout()
        self.cable_dist_yn = QComboBox()
        self.cable_dist_yn.addItems(["Yes", "No"])
        self.cable_dist_main = QLineEdit()
        self.cable_dist_backstay = QLineEdit()
        self.cable_dist_aw = QLineEdit()
        dist_layout.addWidget(QLabel("Y/N:"))
        dist_layout.addWidget(self.cable_dist_yn)
        dist_layout.addWidget(QLabel("Main:"))
        dist_layout.addWidget(self.cable_dist_main)
        dist_layout.addWidget(QLabel("LB/Backstay/RB:"))
        dist_layout.addWidget(self.cable_dist_backstay)
        dist_layout.addWidget(QLabel("Aircraft Warning:"))
        dist_layout.addWidget(self.cable_dist_aw)
        layout.addLayout(dist_layout)

        chain_label = QLabel("Chainage Marks (Main):")
        layout.addWidget(chain_label)
        self.cable_cm_main = QComboBox()
        self.cable_cm_main.addItems(["Paint", "Tagged Line"])
        layout.addWidget(self.cable_cm_main)

        self.cables_comments_input = self.add_textarea(layout, "Cables - Comments:")

        # --------------------------------------------------
        # BRIDLE CABLES SECTION
        # --------------------------------------------------
        bridle_label = QLabel("=== Bridle Cables ===")
        layout.addWidget(bridle_label)

        bc_cabt_label = QLabel("Cable Type:")
        layout.addWidget(bc_cabt_label)
        bc_cabt_layout = QHBoxLayout()
        self.bc_cabt_rb = QLineEdit()
        self.bc_cabt_lb = QLineEdit()
        bc_cabt_layout.addWidget(QLabel("Right Bank:"))
        bc_cabt_layout.addWidget(self.bc_cabt_rb)
        bc_cabt_layout.addWidget(QLabel("Left Bank:"))
        bc_cabt_layout.addWidget(self.bc_cabt_lb)
        layout.addLayout(bc_cabt_layout)

        bc_diam_label = QLabel("Diameter (in):")
        layout.addWidget(bc_diam_label)
        bc_diam_layout = QHBoxLayout()
        self.bc_diam_rb = QLineEdit()
        self.bc_diam_lb = QLineEdit()
        bc_diam_layout.addWidget(QLabel("Right Bank:"))
        bc_diam_layout.addWidget(self.bc_diam_rb)
        bc_diam_layout.addWidget(QLabel("Left Bank:"))
        bc_diam_layout.addWidget(self.bc_diam_lb)
        layout.addLayout(bc_diam_layout)

        bc_cc_label = QLabel("Cable Clamps (#):")
        layout.addWidget(bc_cc_label)
        bc_cc_layout = QHBoxLayout()
        self.bc_cc_rb = QLineEdit()
        self.bc_cc_lb = QLineEdit()
        bc_cc_layout.addWidget(QLabel("Right Bank:"))
        bc_cc_layout.addWidget(self.bc_cc_rb)
        bc_cc_layout.addWidget(QLabel("Left Bank:"))
        bc_cc_layout.addWidget(self.bc_cc_lb)
        layout.addLayout(bc_cc_layout)

        bc_sa_label = QLabel("Spread Angle (deg):")
        layout.addWidget(bc_sa_label)
        bc_sa_layout = QHBoxLayout()
        self.bc_sa_rb = QLineEdit()
        self.bc_sa_lb = QLineEdit()
        bc_sa_layout.addWidget(QLabel("Right Bank:"))
        bc_sa_layout.addWidget(self.bc_sa_rb)
        bc_sa_layout.addWidget(QLabel("Left Bank:"))
        bc_sa_layout.addWidget(self.bc_sa_lb)
        layout.addLayout(bc_sa_layout)

        self.bridle_cables_comments_input = self.add_textarea(layout, "Bridle Cables - Comments:")
        
        # --------------------------------------------------
        # Fittings - Right Bank Section
        # --------------------------------------------------
        fittings_label = QLabel("=== Fittings - Right Bank ===")
        layout.addWidget(fittings_label)

        # Cable Clamps(#)
        frb_cc_label = QLabel("Cable Clamps (#):")
        layout.addWidget(frb_cc_label)
        frb_cc_layout = QHBoxLayout()
        self.frb_cc_main = QLineEdit()
        self.frb_cc_backstay = QLineEdit()
        self.frb_cc_aw = QLineEdit()
        frb_cc_layout.addWidget(QLabel("Main:"))
        frb_cc_layout.addWidget(self.frb_cc_main)
        frb_cc_layout.addWidget(QLabel("Top/Backstay/Btm:"))
        frb_cc_layout.addWidget(self.frb_cc_backstay)
        frb_cc_layout.addWidget(QLabel("Aircraft Warning:"))
        frb_cc_layout.addWidget(self.frb_cc_aw)
        layout.addLayout(frb_cc_layout)

        # Cable Torque(ft-lb)
        frb_ct_label = QLabel("Cable Torque (ft-lb):")
        layout.addWidget(frb_ct_label)
        frb_ct_layout = QHBoxLayout()
        self.frb_ct_main = QLineEdit()
        self.frb_ct_backstay = QLineEdit()
        self.frb_ct_aw = QLineEdit()
        frb_ct_layout.addWidget(QLabel("Main:"))
        frb_ct_layout.addWidget(self.frb_ct_main)
        frb_ct_layout.addWidget(QLabel("Top/Backstay/Btm:"))
        frb_ct_layout.addWidget(self.frb_ct_backstay)
        frb_ct_layout.addWidget(QLabel("Aircraft Warning:"))
        frb_ct_layout.addWidget(self.frb_ct_aw)
        layout.addLayout(frb_ct_layout)

        # Turnback Lengths(m)
        frb_tl_label = QLabel("Turnback Lengths (m):")
        layout.addWidget(frb_tl_label)
        frb_tl_layout = QHBoxLayout()
        self.frb_tl_main = QLineEdit()
        self.frb_tl_back_top = QLineEdit()
        self.frb_tl_back_bot = QLineEdit()
        self.frb_tl_aw = QLineEdit()
        frb_tl_layout.addWidget(QLabel("Main:"))
        frb_tl_layout.addWidget(self.frb_tl_main)
        frb_tl_layout.addWidget(QLabel("Backstay Top:"))
        frb_tl_layout.addWidget(self.frb_tl_back_top)
        frb_tl_layout.addWidget(QLabel("Backstay Bottom:"))
        frb_tl_layout.addWidget(self.frb_tl_back_bot)
        frb_tl_layout.addWidget(QLabel("Aircraft Warning:"))
        frb_tl_layout.addWidget(self.frb_tl_aw)
        layout.addLayout(frb_tl_layout)

        # Socket (Yes/No + Main field)
        frb_socket_label = QLabel("Socket Present:")
        layout.addWidget(frb_socket_label)
        frb_socket_layout = QHBoxLayout()
        self.frb_yn = QComboBox()
        self.frb_yn.addItems(["Yes", "No"])
        self.frb_sock_main = QLineEdit()
        frb_socket_layout.addWidget(QLabel("Yes/No:"))
        frb_socket_layout.addWidget(self.frb_yn)
        frb_socket_layout.addWidget(QLabel("Main Socket:"))
        frb_socket_layout.addWidget(self.frb_sock_main)
        layout.addLayout(frb_socket_layout)

        # Movement/Slip(m)
        frb_ms_label = QLabel("Movement/Slip (m):")
        layout.addWidget(frb_ms_label)
        frb_ms_layout = QHBoxLayout()
        self.frb_ms_main = QLineEdit()
        self.frb_ms_backstay = QLineEdit()
        self.frb_ms_aw = QLineEdit()
        frb_ms_layout.addWidget(QLabel("Main:"))
        frb_ms_layout.addWidget(self.frb_ms_main)
        frb_ms_layout.addWidget(QLabel("Top/Backstay/Btm:"))
        frb_ms_layout.addWidget(self.frb_ms_backstay)
        frb_ms_layout.addWidget(QLabel("Aircraft Warning:"))
        frb_ms_layout.addWidget(self.frb_ms_aw)
        layout.addLayout(frb_ms_layout)

        # Rust(%)
        frb_rust_label = QLabel("Rust (%):")
        layout.addWidget(frb_rust_label)
        frb_rust_layout = QHBoxLayout()
        self.frb_rust_main = QLineEdit()
        self.frb_rust_backstay = QLineEdit()
        self.frb_rust_aw = QLineEdit()
        frb_rust_layout.addWidget(QLabel("Main:"))
        frb_rust_layout.addWidget(self.frb_rust_main)
        frb_rust_layout.addWidget(QLabel("Top/Backstay/Btm:"))
        frb_rust_layout.addWidget(self.frb_rust_backstay)
        frb_rust_layout.addWidget(QLabel("Aircraft Warning:"))
        frb_rust_layout.addWidget(self.frb_rust_aw)
        layout.addLayout(frb_rust_layout)

        # Turnbuckle Size(in)
        frb_ts_label = QLabel("Turnbuckle Size (in):")
        layout.addWidget(frb_ts_label)
        frb_ts_layout = QHBoxLayout()
        self.frb_ts_main = QLineEdit()
        self.frb_ts_backstay = QLineEdit()
        self.frb_ts_aw = QLineEdit()
        frb_ts_layout.addWidget(QLabel("Main:"))
        frb_ts_layout.addWidget(self.frb_ts_main)
        frb_ts_layout.addWidget(QLabel("Top/Backstay/Btm:"))
        frb_ts_layout.addWidget(self.frb_ts_backstay)
        frb_ts_layout.addWidget(QLabel("Aircraft Warning:"))
        frb_ts_layout.addWidget(self.frb_ts_aw)
        layout.addLayout(frb_ts_layout)

        # Turnbuckle Condition
        frb_ts_cond_label = QLabel("Turnbuckle Condition:")
        layout.addWidget(frb_ts_cond_label)
        frb_ts_cond_layout = QHBoxLayout()
        self.frb_ts_cond_main = QLineEdit()
        self.frb_ts_cond_backstay = QLineEdit()
        self.frb_ts_cond_aw = QLineEdit()
        frb_ts_cond_layout.addWidget(QLabel("Main:"))
        frb_ts_cond_layout.addWidget(self.frb_ts_cond_main)
        frb_ts_cond_layout.addWidget(QLabel("Top/Backstay/Btm:"))
        frb_ts_cond_layout.addWidget(self.frb_ts_cond_backstay)
        frb_ts_cond_layout.addWidget(QLabel("Aircraft Warning:"))
        frb_ts_cond_layout.addWidget(self.frb_ts_cond_aw)
        layout.addLayout(frb_ts_cond_layout)

        # Turnbuckle Remaining Adjust.(m)
        frb_ts_ra_label = QLabel("Turnbuckle Remaining Adjust. (m):")
        layout.addWidget(frb_ts_ra_label)
        frb_ts_ra_layout = QHBoxLayout()
        self.frb_ts_ra_main = QLineEdit()
        self.frb_ts_ra_backstay = QLineEdit()
        self.frb_ts_ra_aw = QLineEdit()
        frb_ts_ra_layout.addWidget(QLabel("Main:"))
        frb_ts_ra_layout.addWidget(self.frb_ts_ra_main)
        frb_ts_ra_layout.addWidget(QLabel("Top/Backstay/Btm:"))
        frb_ts_ra_layout.addWidget(self.frb_ts_ra_backstay)
        frb_ts_ra_layout.addWidget(QLabel("Aircraft Warning:"))
        frb_ts_ra_layout.addWidget(self.frb_ts_ra_aw)
        layout.addLayout(frb_ts_ra_layout)

        # Clevice (Type)
        frb_clev_label = QLabel("Clevice (Type):")
        layout.addWidget(frb_clev_label)
        frb_clev_layout = QHBoxLayout()
        self.frb_clev_main = QLineEdit()
        self.frb_clev_backstay = QLineEdit()
        self.frb_clev_aw = QLineEdit()
        frb_clev_layout.addWidget(QLabel("Main:"))
        frb_clev_layout.addWidget(self.frb_clev_main)
        frb_clev_layout.addWidget(QLabel("Top/Backstay/Btm:"))
        frb_clev_layout.addWidget(self.frb_clev_backstay)
        frb_clev_layout.addWidget(QLabel("Aircraft Warning:"))
        frb_clev_layout.addWidget(self.frb_clev_aw)
        layout.addLayout(frb_clev_layout)

        # Clevice Condition
        frb_clev_cond_label = QLabel("Clevice Condition:")
        layout.addWidget(frb_clev_cond_label)
        frb_clev_cond_layout = QHBoxLayout()
        self.frb_clev_cond_main = QLineEdit()
        self.frb_clev_cond_backstay = QLineEdit()
        self.frb_clev_cond_aw = QLineEdit()
        frb_clev_cond_layout.addWidget(QLabel("Main:"))
        frb_clev_cond_layout.addWidget(self.frb_clev_cond_main)
        frb_clev_cond_layout.addWidget(QLabel("Top/Backstay/Btm:"))
        frb_clev_cond_layout.addWidget(self.frb_clev_cond_backstay)
        frb_clev_cond_layout.addWidget(QLabel("Aircraft Warning:"))
        frb_clev_cond_layout.addWidget(self.frb_clev_cond_aw)
        layout.addLayout(frb_clev_cond_layout)
        self.fittings_comments_input = self.add_textarea(layout, "Fittings - Right Bank Comments:")

        #DRAG & DROP AREA FOR IMAGES
        dragdrop_label = QLabel("=== Drag & Drop Images Here ===")
        dragdrop_label.setAlignment(Qt.AlignCenter)
        dragdrop_label.setStyleSheet("border: 2px dashed #aaa; padding: 20px; font-size: 14px;")
        # Enable drops on this label
        dragdrop_label.setAcceptDrops(True)
        # Redirect events to custom handlers
        dragdrop_label.dragEnterEvent = self.handle_drag_enter
        dragdrop_label.dropEvent = self.handle_drop_event
        layout.addWidget(dragdrop_label)

        # Image Upload Button
        self.upload_button = QPushButton("Upload Images")
        self.upload_button.clicked.connect(self.upload_images)
        layout.addWidget(self.upload_button)
        
        # Generate PDF Button
        self.generate_button = QPushButton("Generate PDF")
        self.generate_button.clicked.connect(self.generate_pdf)
        layout.addWidget(self.generate_button)

    def add_input(self, layout, label_text):
        label = QLabel(label_text)
        layout.addWidget(label)
        line_edit = QLineEdit()
        layout.addWidget(line_edit)
        return line_edit
    
    def add_textarea(self, layout, label_text):
        label = QLabel(label_text)
        layout.addWidget(label)
        text_area = QTextEdit()
        layout.addWidget(text_area)
        return text_area

    def add_dropdown(self, layout, label_text, options):
        label = QLabel(label_text)
        layout.addWidget(label)
        combo_box = QComboBox()
        combo_box.addItems(options)
        layout.addWidget(combo_box)
        return combo_box
    
    # Drag-and-drop event handlers
    def handle_drag_enter(self, event):
        """Accept drag if it has files (images)."""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def handle_drop_event(self, event):
        """Handle dropped files, append image paths to self.images."""
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            # Check extension
            if file_path.lower().endswith((".png", ".jpg", ".jpeg")):
                self.images.append(file_path)
        QMessageBox.information(self, "Images Uploaded", f"Images added via drag & drop.")
        event.acceptProposedAction()

    def upload_images(self):
        options = QFileDialog.Options()
        file_paths, _ = QFileDialog.getOpenFileNames(
            self, 
            "Select Images", 
            "", 
            "Images (*.png *.jpg *.jpeg);;All Files (*)", 
            options=options
        )
        if file_paths:
            for file_path in file_paths:
                file_path = os.path.normpath(file_path)

                if not file_path.lower().endswith((".png", ".jpg", ".jpeg")):
                    QMessageBox.warning(self, "Invalid File", f"Skipping non-image file: {file_path}")
                    continue
                
                pixmap = QPixmap(file_path)
                if pixmap.isNull():
                    QMessageBox.warning(self, "Invalid Image", f"Unable to open image: {file_path}")
                    continue

                self.images.append(file_path)
            
            QMessageBox.information(self, "Images Uploaded", f"{len(self.images)} total images now in list.")

    #Generates everything in the pdf
    def generate_pdf(self):
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", style="B", size=14)
        
        #Title
        pdf.cell(180, 10, "Cableway Inspection Report",border=1, ln=True, align="C")
        pdf.ln(5)
        
        #Top section
        pdf.set_font("Arial", size=12)
        pdf.cell(180, 10, f"Station Name: {self.station_name_input.text()}", border=1, ln=True)
        pdf.cell(90, 10, f"Station Number: {self.station_number_input.text()}", border=1)
        pdf.cell(90, 10, f"Date: {self.date_input.text()}", border=1, ln=True)
        
        pdf.set_font("Arial", size=11)
        pdf.cell(45, 10, f"Span (m): {self.span_input.text()}", border=1)
        pdf.cell(45, 10, f"Sag (m): {self.sag_input.text()}", border=1)
        pdf.cell(45, 10, f"Temperature: {self.temperature_input.text()}", border=1)
        pdf.cell(45, 10, f"Design Load (kg): {self.design_load_input.text()}", border=1, ln=True)
        pdf.ln(5)
        
        #Cables Section
        pdf.set_font("Arial", style="B", size=12)
        pdf.cell(180, 10, "CABLES", ln=True)
        pdf.cell(57, 10)
        pdf.cell(41, 10, f"Main", border=1)
        pdf.cell(41, 10, f"LB/Backstay/RB", border=1)
        pdf.cell(41, 10, f"Aircraft Warning", border=1, ln=True)
        pdf.set_font("Arial", size=11)
        pdf.cell(45, 10, f"Diameter(in)", border=1)
        pdf.cell(12, 10, border=1)
        pdf.cell(41, 10, f"{self.cable_diam_main.text()}", border=1)
        pdf.cell(41, 10, f"{self.cable_diam_backstay.text()}", border=1)
        pdf.cell(41, 10, f"{self.cable_diam_aw.text()}", border=1, ln=True)
        pdf.cell(45, 10, f"Angle from Vertical (deg)", border=1)
        pdf.cell(12, 10, f"{self.cable_afv_yn.currentText()}", border=1)
        pdf.cell(41, 10, f"{self.cable_afv_main.text()}", border=1)
        pdf.cell(41, 10, f"{self.cable_afv_backstay.text()}", border=1)
        pdf.cell(41, 10, f"n/a", border=1, ln=True)
        pdf.cell(45, 10, f"Cable Type", border=1)
        pdf.cell(12, 10, border=1)
        pdf.cell(41, 10, f"{self.cable_cabt_main.text()}", border=1)
        pdf.cell(41, 10, f"{self.cable_cabt_backstay.text()}", border=1)
        pdf.cell(41, 10, f"{self.cable_cabt_aw.text()}", border=1, ln=True)
        pdf.cell(45, 10, f"Core Type", border=1)
        pdf.cell(12, 10, f"{self.cable_cort_fw.currentText()}", border=1)
        pdf.cell(41, 10, f"{self.cable_cort_main.text()}", border=1)
        pdf.cell(41, 10, f"{self.cable_cort_backstay.text()}", border=1)
        pdf.cell(41, 10, f"{self.cable_cort_aw.text()}", border=1, ln=True)
        pdf.cell(45, 10, f"Broken Wires(#)", border=1)
        pdf.cell(12, 10, f"{self.cable_bw_yn.currentText()}", border=1)
        pdf.cell(41, 10, f"{self.cable_bw_main.text()}", border=1)
        pdf.cell(41, 10, f"{self.cable_bw_backstay.text()}", border=1)
        pdf.cell(41, 10, f"{self.cable_bw_aw.text()}", border=1, ln=True)
        pdf.cell(45, 10, f"Pinched Wires(#)", border=1)
        pdf.cell(12, 10, f"{self.cable_pw_yn.currentText()}", border=1)
        pdf.cell(41, 10, f"{self.cable_pw_main.text()}", border=1)
        pdf.cell(41, 10, f"{self.cable_pw_backstay.text()}", border=1)
        pdf.cell(41, 10, f"{self.cable_pw_aw.text()}", border=1, ln=True)
        pdf.cell(45, 10, f"Broken Strands(#)", border=1)
        pdf.cell(12, 10, f"{self.cable_bs_yn.currentText()}", border=1)
        pdf.cell(41, 10, f"{self.cable_bs_main.text()}", border=1)
        pdf.cell(41, 10, f"{self.cable_bs_backstay.text()}", border=1)
        pdf.cell(41, 10, f"{self.cable_bs_aw.text()}", border=1, ln=True)
        pdf.cell(45, 10, f"Frays(%)", border=1)
        pdf.cell(12, 10, f"{self.cable_fray_yn.currentText()}", border=1)
        pdf.cell(41, 10, f"{self.cable_fray_main.text()}", border=1)
        pdf.cell(41, 10, f"{self.cable_fray_backstay.text()}", border=1)
        pdf.cell(41, 10, f"{self.cable_fray_aw.text()}", border=1, ln=True)
        pdf.cell(45, 10, f"Rust(%)", border=1)
        pdf.cell(12, 10, f"{self.cable_rust_yn.currentText()}", border=1)
        pdf.cell(41, 10, f"{self.cable_rust_main.text()}", border=1)
        pdf.cell(41, 10, f"{self.cable_rust_backstay.text()}", border=1)
        pdf.cell(41, 10, f"{self.cable_rust_aw.text()}", border=1, ln=True)
        pdf.cell(45, 10, f"Distortion", border=1)
        pdf.cell(12, 10, f"{self.cable_dist_yn.currentText()}", border=1)
        pdf.cell(41, 10, f"{self.cable_dist_main.text()}", border=1)
        pdf.cell(41, 10, f"{self.cable_dist_backstay.text()}", border=1)
        pdf.cell(41, 10, f"{self.cable_dist_aw.text()}", border=1, ln=True)
        pdf.cell(45, 10, f"Chainage Marks", border=1)
        pdf.cell(12, 10, f" ", border=1)
        pdf.cell(41, 10, f"{self.cable_cm_main.currentText()}", border=1)
        pdf.cell(41, 10, f"n/a", border=1)
        pdf.cell(41, 10, f"n/a", border=1, ln=True)

        pdf.multi_cell(180, 8, f"Comments: (describe broken or damaged wire in one lay of cable, degree of rust, any bends or distortions of cable etc.)\n{self.cables_comments_input.toPlainText()}", border=1)
        pdf.ln(5)
        
        #Bridle Cables Section
        pdf.set_font("Arial", style="B", size=12)
        pdf.cell(180, 10, "BRIDLE CABLES", ln=True)
        pdf.cell(57, 10)
        pdf.cell(41, 10, f"Right Bank", border=1)
        pdf.cell(41, 10, f"Left Bank", border=1, ln = True)
        pdf.set_font("Arial", size=11)
        pdf.cell(45, 10, f"Cable Type", border=1)
        pdf.cell(12, 10, border=1)
        pdf.cell(41, 10, f"{self.bc_cabt_rb.text()}", border=1)
        pdf.cell(41, 10, f"{self.bc_cabt_lb.text()}", border=1, ln = True)
        pdf.cell(45, 10, f"Diameter(in)", border=1)
        pdf.cell(12, 10, border=1)
        pdf.cell(41, 10, f"{self.bc_diam_rb.text()}", border=1)
        pdf.cell(41, 10, f"{self.bc_diam_lb.text()}", border=1, ln = True)
        pdf.cell(45, 10, f"Cable Clamps(#)", border=1)
        pdf.cell(12, 10, border=1)
        pdf.cell(41, 10, f"{self.bc_cc_rb.text()}", border=1)
        pdf.cell(41, 10, f"{self.bc_cc_lb.text()}", border=1, ln = True)
        pdf.cell(45, 10, f"Spread Angle(deg)", border=1)
        pdf.cell(12, 10, border=1)
        pdf.cell(41, 10, f"{self.bc_sa_rb.text()}", border=1)
        pdf.cell(41, 10, f"{self.bc_sa_lb.text()}", border=1, ln = True)
        pdf.multi_cell(180, 8, f"Comments:\n{self.bridle_cables_comments_input.toPlainText()}", border=1)
        pdf.ln(5)
        
        #Fittings - Right Bank
        pdf.set_font("Arial", style="B", size=12)
        pdf.cell(180, 10, "FITTINGS - RIGHT BANK", ln=True)
        pdf.cell(57, 10)
        pdf.cell(41, 10, f"Main", border=1)
        pdf.cell(41, 10, f"Top/Backstay/Btm", border=1)
        pdf.cell(41, 10, f"Aircraft Warning", border=1, ln=True)
        pdf.set_font("Arial", size=11)
        pdf.cell(45, 10, f"Cable Clamps(#)", border=1)
        pdf.cell(12, 10, border=1)
        pdf.cell(41, 10, f"{self.frb_cc_main.text()}", border=1)
        pdf.cell(41, 10, f"{self.frb_cc_backstay.text()}", border=1)
        pdf.cell(41, 10, f"{self.frb_cc_aw.text()}", border=1, ln=True)
        pdf.cell(45, 10, f"Cable Torque(ft-lb))", border=1)
        pdf.cell(12, 10, border=1)
        pdf.cell(41, 10, f"{self.frb_ct_main.text()}", border=1)
        pdf.cell(41, 10, f"{self.frb_ct_backstay.text()}", border=1)
        pdf.cell(41, 10, f"{self.frb_ct_aw.text()}", border=1, ln=True)
        pdf.cell(45, 10, f"Turnback Lengths(m)", border=1)
        pdf.cell(12, 10, border=1)
        pdf.cell(41, 10, f"{self.frb_tl_main.text()}", border=1)
        pdf.cell(41, 10, f"Top-{self.frb_tl_back_top.text()}", border=1)
        pdf.cell(41, 10, f"{self.frb_tl_aw.text()}", border=1, ln=True)
        pdf.cell(45, 10, border=1)
        pdf.cell(12, 10, border=1)
        pdf.cell(41, 10, f"n/a", border=1)
        pdf.cell(41, 10, f"Bottom-{self.frb_tl_back_bot.text()}", border=1)
        pdf.cell(41, 10, f"n/a", border=1, ln=True)
        pdf.cell(45, 10, f"Socket", border=1)
        pdf.cell(12, 10, f"{self.frb_yn.currentText()}", border=1)
        pdf.cell(41, 10, f"{self.frb_sock_main.text()}", border=1)
        pdf.cell(41, 10, f"n/a", border=1)
        pdf.cell(41, 10, f"n/a", border=1, ln=True)
        pdf.cell(45, 10, f"Movement/Slip(m)", border=1)
        pdf.cell(12, 10, border=1)
        pdf.cell(41, 10, f"{self.frb_ms_main.text()}", border=1)
        pdf.cell(41, 10, f"{self.frb_ms_backstay.text()}", border=1)
        pdf.cell(41, 10, f"{self.frb_ms_aw.text()}", border=1, ln=True)
        pdf.cell(45, 10, f"Rust(%)", border=1)
        pdf.cell(12, 10, border=1)
        pdf.cell(41, 10, f"{self.frb_rust_main.text()}", border=1)
        pdf.cell(41, 10, f"{self.frb_rust_backstay.text()}", border=1)
        pdf.cell(41, 10, f"{self.frb_rust_aw.text()}", border=1, ln=True)
        pdf.cell(45, 10, f"Turnbuckle Size(in)", border=1)
        pdf.cell(12, 10, border=1)
        pdf.cell(41, 10, f"{self.frb_ts_main.text()}", border=1)
        pdf.cell(41, 10, f"{self.frb_ts_backstay.text()}", border=1)
        pdf.cell(41, 10, f"{self.frb_ts_aw.text()}", border=1, ln=True)
        pdf.set_font("Arial", size=9)
        pdf.cell(45, 10, f"- Condition", border=1)
        pdf.cell(12, 10, border=1)
        pdf.cell(41, 10, f"{self.frb_ts_cond_main.text()}", border=1)
        pdf.cell(41, 10, f"{self.frb_ts_cond_backstay.text()}", border=1)
        pdf.cell(41, 10, f"{self.frb_ts_cond_aw.text()}", border=1, ln=True)
        pdf.cell(45, 10, f"- Remaining Adjust.(m)", border=1)
        pdf.cell(12, 10, border=1)
        pdf.cell(41, 10, f"{self.frb_ts_ra_main.text()}", border=1)
        pdf.cell(41, 10, f"{self.frb_ts_ra_backstay.text()}", border=1)
        pdf.cell(41, 10, f"{self.frb_ts_ra_aw.text()}", border=1, ln=True)
        pdf.set_font("Arial", size=11)
        pdf.cell(45, 10, f"Clevice (Type)", border=1)
        pdf.cell(12, 10, border=1)
        pdf.cell(41, 10, f"{self.frb_clev_main.text()}", border=1)
        pdf.cell(41, 10, f"{self.frb_clev_backstay.text()}", border=1)
        pdf.cell(41, 10, f"{self.frb_clev_aw.text()}", border=1, ln=True)
        pdf.set_font("Arial", size=9)
        pdf.cell(45, 10, f"- Condition", border=1)
        pdf.cell(12, 10, border=1)
        pdf.cell(41, 10, f"{self.frb_clev_cond_main.text()}", border=1)
        pdf.cell(41, 10, f"{self.frb_clev_cond_backstay.text()}", border=1)
        pdf.cell(41, 10, f"{self.frb_clev_cond_aw.text()}", border=1, ln=True)
        pdf.multi_cell(180, 8, f"Comments:\n{self.fittings_comments_input.toPlainText()}", border=1)
        pdf.ln(5)
        
        
        pdf.set_font("Arial", style="B", size=12)
        pdf.cell(180, 10, "Uploaded Images:", ln=True)
        #image size
        IMAGE_WIDTH = 62
        IMAGE_HEIGHT = 62
        COL_SPACING = 5
        LEFT_MARGIN = 10
        
        col_count = 0
        current_y = pdf.get_y()
        
        # Arrange 3 images per row
        for i, img_path in enumerate(self.images):
            # Check if theres room for images on the page
            if current_y + IMAGE_HEIGHT > pdf.page_break_trigger:
                pdf.add_page()
                current_y = pdf.get_y()  # Reset current_y to top of new page
                col_count = 0  # Reset columns on new page

            x_pos = LEFT_MARGIN + col_count * (IMAGE_WIDTH + COL_SPACING)

            pdf.image(os.path.normpath(img_path), x=x_pos, y=current_y, w=IMAGE_WIDTH, h=IMAGE_HEIGHT)

            col_count += 1

            # Move to next row if theres 3 images
            if col_count == 3:
                col_count = 0
                current_y += (IMAGE_HEIGHT + COL_SPACING)

        if col_count != 0:
            current_y += (IMAGE_HEIGHT + COL_SPACING)


        pdf.set_y(current_y)

        filename = f"Cableway_Report_{self.date_input.text()}_{self.station_name_input.text()}_{self.station_number_input.text()}.pdf"
        pdf.output(filename)
        QMessageBox.information(self, "PDF Generated", f"PDF saved as {filename}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CablewayInspectionApp()
    window.show()
    sys.exit(app.exec_())
