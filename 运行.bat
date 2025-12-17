@echo off
chcp 65001 >nul

:: 复制文件到minimap_renderer/src目录
if exist src\render_web.py copy /y src\render_web.py minimap_renderer\src\ >nul

:: 启动服务
cd minimap_renderer
call venv\Scripts\activate && cd src && uvicorn render_web:app --host 0.0.0.0 --port 9876

pause