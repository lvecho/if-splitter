@echo off
echo 正在创建虚拟环境...
python -m venv venv
call venv\Scripts\activate.bat

echo 正在安装依赖...
pip install -r requirements.txt

echo 正在打包程序...
pyinstaller --clean tif_splitter.spec

echo 打包完成！
echo 可执行文件位于 dist 目录下
pause 