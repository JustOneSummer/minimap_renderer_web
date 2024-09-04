@echo off
chcp 65001
cd minimap_renderer
:: 激活虚拟环境
call .\venv\Scripts\activate && (

:: 进入 src 目录
cd src && (

:: 启动 uvicorn 服务器
uvicorn render_web:app --host "0.0.0.0" --port 9876
)
)

pause