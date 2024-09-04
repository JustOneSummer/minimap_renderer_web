@echo off
chcp 65001
python --version >nul 2>&1
if errorlevel 1 goto errorNoPython

echo 下载 minimap_renderer
:: git clone https://gitee.com/yuyukosama/minimap_renderer.git
git clone https://github.com/WoWs-Builder-Team/minimap_renderer.git
if errorlevel 1 goto errorGit

set "source_file_token=token.json"
set "source_file_render_web=src\render_web.py"
set "target_dir_token=minimap_renderer"
set "target_dir_render_web=minimap_renderer\src"
copy "%source_file_token%" "%target_dir_token%"
copy "%source_file_render_web%" "%target_dir_render_web%"

cd minimap_renderer

md temp

echo 开始安装环境依赖...

pip3 install virtualenv >nul 2>&1
if errorlevel 1 goto errorPip

virtualenv venv >nul 2>&1
if errorlevel 1 goto errorVirtualenv

call .\venv\Scripts\activate
if errorlevel 1 goto errorActivate

echo 安装minimap_renderer依赖
pip3 install -r requirements.txt -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple >nul 2>&1
if errorlevel 1 goto errorInstall

echo 安装fastapi
pip3 install fastapi -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple >nul 2>&1
if errorlevel 1 goto errorInstall

pip3 install python-multipart -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple >nul 2>&1
if errorlevel 1 goto errorInstall

echo 安装uvicorn
pip3 install uvicorn -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple >nul 2>&1
if errorlevel 1 goto errorInstall

echo 安装结束...
pause
exit /b 0

:errorNoPython
echo [错误] 没有检测到 Python，请确保 Python 已安装并在 PATH 中。
goto end

:errorPip
echo [错误] 安装 virtualenv 时出现问题，请检查 pip 配置。
goto end

:errorVirtualenv
echo [错误] 创建虚拟环境时出现问题，请检查 virtualenv 配置。
goto end

:errorActivate
echo [错误] 激活虚拟环境时出现问题。
goto end

:errorInstall
echo [错误] 安装依赖项时出现问题，请检查网络连接或 pip 配置。
goto end

:errorGit
echo [错误] git获取仓库信息出现问题，请检查网络连接或 更换仓库为国内源。
goto end

:end
pause
exit /b 1
