from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, QSpinBox, QCheckBox,
                             QFileDialog, QMessageBox)
from PyQt6.QtCore import Qt
import os
from utils.image_processor import ImageProcessor

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TIF图像分割工具 v1.0")
        self.setMinimumSize(800, 600)
        self.image_processor = ImageProcessor()
        self.split_regions = []
        self.setup_ui()

    def setup_ui(self):
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # 文件选择区域
        file_layout = QHBoxLayout()
        self.file_path = QLineEdit()
        self.file_path.setPlaceholderText("请选择TIF图像文件")
        select_file_btn = QPushButton("选择图像文件")
        file_layout.addWidget(self.file_path)
        file_layout.addWidget(select_file_btn)
        main_layout.addLayout(file_layout)

        # 图像信息显示区域
        image_info_layout = QHBoxLayout()
        self.width_label = QLabel("载入图像宽 pxc:")
        self.width_value = QLabel("-1")
        self.height_label = QLabel("载入图像高 pxc:")
        self.height_value = QLabel("-1")
        image_info_layout.addWidget(self.width_label)
        image_info_layout.addWidget(self.width_value)
        image_info_layout.addWidget(self.height_label)
        image_info_layout.addWidget(self.height_value)
        main_layout.addLayout(image_info_layout)

        # 分割设置区域
        settings_layout = QVBoxLayout()
        
        # 切割后单页纸张大小设置
        paper_size_layout = QHBoxLayout()
        paper_size_layout.addWidget(QLabel("切割后单页纸张大小:"))
        self.paper_width = QSpinBox()
        self.paper_width.setRange(1, 10000)
        self.paper_width.setValue(2315)
        self.paper_height = QSpinBox()
        self.paper_height.setRange(1, 10000)
        self.paper_height.setValue(3274)
        paper_size_layout.addWidget(QLabel("宽(列) pxc:"))
        paper_size_layout.addWidget(self.paper_width)
        paper_size_layout.addWidget(QLabel("高(行) pxc:"))
        paper_size_layout.addWidget(self.paper_height)
        settings_layout.addLayout(paper_size_layout)

        # 切割后图像区域大小设置
        image_size_layout = QHBoxLayout()
        image_size_layout.addWidget(QLabel("切割后图像区域大小:"))
        self.image_width = QSpinBox()
        self.image_width.setRange(1, 10000)
        self.image_width.setValue(1800)
        self.image_height = QSpinBox()
        self.image_height.setRange(1, 10000)
        self.image_height.setValue(2800)
        image_size_layout.addWidget(QLabel("宽(列) pxc:"))
        image_size_layout.addWidget(self.image_width)
        image_size_layout.addWidget(QLabel("高(行) pxc:"))
        image_size_layout.addWidget(self.image_height)
        settings_layout.addLayout(image_size_layout)

        # 边距设置
        margin_layout = QHBoxLayout()
        margin_layout.addWidget(QLabel("画心图像四周边距 (px):"))
        self.margin = QSpinBox()
        self.margin.setRange(0, 1000)
        self.margin.setValue(440)
        margin_layout.addWidget(self.margin)
        settings_layout.addLayout(margin_layout)

        main_layout.addLayout(settings_layout)

        # PDF导出选项
        export_layout = QHBoxLayout()
        self.export_pdf = QCheckBox("是否导出pdf")
        export_layout.addWidget(self.export_pdf)
        main_layout.addLayout(export_layout)

        # 操作按钮区域
        button_layout = QHBoxLayout()
        self.calc_btn = QPushButton("计算")
        self.auto_btn = QPushButton("自动分配")
        self.start_btn = QPushButton("开始分割")
        button_layout.addWidget(self.calc_btn)
        button_layout.addWidget(self.auto_btn)
        button_layout.addWidget(self.start_btn)
        main_layout.addLayout(button_layout)

        # 连接信号
        select_file_btn.clicked.connect(self.select_file)
        self.calc_btn.clicked.connect(self.calculate)
        self.auto_btn.clicked.connect(self.auto_assign)
        self.start_btn.clicked.connect(self.start_split)

    def select_file(self):
        """选择TIF图像文件"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择TIF图像文件", "",
            "TIF Files (*.tif *.tiff);;All Files (*)"
        )
        
        if file_path:
            self.file_path.setText(file_path)
            success, message = self.image_processor.load_image(file_path)
            
            if success:
                self.width_value.setText(str(self.image_processor.width))
                self.height_value.setText(str(self.image_processor.height))
            else:
                QMessageBox.warning(self, "错误", message)

    def calculate(self):
        """计算分割预览"""
        if not self.image_processor.image:
            QMessageBox.warning(self, "错误", "请先选择图像文件")
            return

        paper_size = (self.paper_width.value(), self.paper_height.value())
        image_size = (self.image_width.value(), self.image_height.value())
        margin = self.margin.value()

        success, message, regions = self.image_processor.calculate_split_info(
            paper_size, image_size, margin
        )

        if success:
            self.split_regions = regions
            QMessageBox.information(self, "计算结果", message)
        else:
            QMessageBox.warning(self, "错误", message)

    def auto_assign(self):
        """自动分配参数"""
        if not self.image_processor.image:
            QMessageBox.warning(self, "错误", "请先选择图像文件")
            return

        # 根据图像尺寸自动计算合适的参数
        img_width = self.image_processor.width
        img_height = self.image_processor.height

        # 设置纸张大小为图像尺寸的1.2倍
        paper_width = int(img_width * 1.2)
        paper_height = int(img_height * 1.2)
        self.paper_width.setValue(paper_width)
        self.paper_height.setValue(paper_height)

        # 设置图像区域大小为图像尺寸的0.8倍
        image_width = int(img_width * 0.8)
        image_height = int(img_height * 0.8)
        self.image_width.setValue(image_width)
        self.image_height.setValue(image_height)

        # 设置边距为较小的尺寸的10%
        margin = int(min(image_width, image_height) * 0.1)
        self.margin.setValue(margin)

        QMessageBox.information(self, "自动分配", "参数已自动设置")

    def start_split(self):
        """开始分割图像"""
        if not self.image_processor.image:
            QMessageBox.warning(self, "错误", "请先选择图像文件")
            return

        if not self.split_regions:
            QMessageBox.warning(self, "错误", "请先计算分割预览")
            return

        # 选择输出目录
        output_dir = QFileDialog.getExistingDirectory(
            self, "选择输出目录", ""
        )

        if output_dir:
            success, message = self.image_processor.split_image(
                self.split_regions,
                output_dir,
                self.export_pdf.isChecked()
            )

            if success:
                QMessageBox.information(self, "完成", message)
            else:
                QMessageBox.warning(self, "错误", message) 