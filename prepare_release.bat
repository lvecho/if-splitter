@echo off
echo 正在准备发布包...

rem 创建发布目录
mkdir "TIF图像分割工具_v1.0"
cd "TIF图像分割工具_v1.0"

rem 复制必要文件
copy ..\dist\TIF图像分割工具.exe .
copy ..\使用说明.txt .
copy ..\创建桌面快捷方式.bat .

rem 返回上级目录
cd ..

rem 创建ZIP包
powershell Compress-Archive -Path "TIF图像分割工具_v1.0" -DestinationPath "TIF图像分割工具_v1.0.zip" -Force

rem 清理临时文件
rmdir /s /q "TIF图像分割工具_v1.0"

echo 发布包准备完成！
echo 生成的文件：TIF图像分割工具_v1.0.zip
pause 