from PIL import Image
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from typing import Tuple, List

class ImageProcessor:
    def __init__(self):
        self.image = None
        self.image_path = ""
        self.width = -1
        self.height = -1

    def load_image(self, image_path: str) -> Tuple[bool, str]:
        """加载TIF图像文件"""
        try:
            if not os.path.exists(image_path):
                return False, "文件不存在"
            
            if not image_path.lower().endswith('.tif'):
                return False, "不是TIF格式文件"

            self.image = Image.open(image_path)
            self.image_path = image_path
            self.width, self.height = self.image.size
            return True, "成功加载图像"
        except Exception as e:
            return False, f"加载图像失败: {str(e)}"

    def calculate_split_info(self, paper_size: Tuple[int, int], 
                           image_size: Tuple[int, int], 
                           margin: int) -> Tuple[bool, str, List[Tuple[int, int, int, int]]]:
        """计算分割信息"""
        if not self.image:
            return False, "未加载图像", []

        try:
            paper_width, paper_height = paper_size
            image_width, image_height = image_size
            
            # 计算可用区域
            available_width = paper_width - 2 * margin
            available_height = paper_height - 2 * margin
            
            if available_width <= 0 or available_height <= 0:
                return False, "边距过大，无可用区域", []
            
            if image_width > available_width or image_height > available_height:
                return False, "图像区域大小超过可用区域", []
            
            # 计算分割区域
            regions = []
            for y in range(0, self.height, image_height):
                for x in range(0, self.width, image_width):
                    region = (x, y, 
                             min(x + image_width, self.width),
                             min(y + image_height, self.height))
                    regions.append(region)
            
            return True, f"计算完成，共{len(regions)}个分割区域", regions
        except Exception as e:
            return False, f"计算分割信息失败: {str(e)}", []

    def split_image(self, regions: List[Tuple[int, int, int, int]], 
                   output_dir: str,
                   export_pdf: bool = False) -> Tuple[bool, str]:
        """执行图像分割"""
        if not self.image:
            return False, "未加载图像"

        try:
            # 创建输出目录
            os.makedirs(output_dir, exist_ok=True)
            base_name = os.path.splitext(os.path.basename(self.image_path))[0]
            
            # 分割并保存图像
            split_images = []
            for i, (x1, y1, x2, y2) in enumerate(regions):
                region = self.image.crop((x1, y1, x2, y2))
                output_path = os.path.join(output_dir, f"{base_name}_part_{i+1}.tif")
                region.save(output_path)
                split_images.append(output_path)
            
            # 导出PDF
            if export_pdf:
                pdf_path = os.path.join(output_dir, f"{base_name}_split.pdf")
                self._export_to_pdf(split_images, pdf_path)
            
            return True, f"分割完成，共处理{len(regions)}个区域"
        except Exception as e:
            return False, f"分割图像失败: {str(e)}"

    def _export_to_pdf(self, image_paths: List[str], pdf_path: str):
        """将分割后的图像导出为PDF"""
        c = canvas.Canvas(pdf_path, pagesize=A4)
        for img_path in image_paths:
            img = Image.open(img_path)
            img_width, img_height = img.size
            # 调整图像大小以适应A4页面
            aspect = img_height / float(img_width)
            if aspect > 1:
                img_width = A4[0] - 40
                img_height = img_width * aspect
            else:
                img_height = A4[1] - 40
                img_width = img_height / aspect
            
            c.drawImage(img_path, 20, A4[1] - img_height - 20,
                       width=img_width, height=img_height)
            c.showPage()
        c.save() 