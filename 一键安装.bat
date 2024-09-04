@echo off
chcp 65001

python --version 3>NUL
if errorlevel 1 goto errorNoPython

git -v git>NUL
if errorlevel 1 goto errorNoGit

echo 下载 minimap_renderer

git clone https://github.com/WoWs-Builder-Team/minimap_renderer.git

echo 安装依赖

set "source_file_token=token.json"
set "source_file_render_web=src\render_web.py"
set "target_dir_token=minimap_renderer"
set "target_dir_render_web=minimap_renderer\src"
copy "%source_file_token%" "%target_dir_token%"
copy "%source_file_render_web%" "%target_dir_render_web%"

cd minimap_renderer

md temp

pip3 install virtualenv

virtualenv venv

.\venv\Scripts\activate

pip3 install -r requirements.txt -i  https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple some-package

pip3 install fastapi -i  https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple some-package

pip3 install python-multipart -i  https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple some-package

pip3 install uvicorn -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple some-package

echo 安装结束...

pause