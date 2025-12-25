import hashlib
import io
import json
import os
import secrets
import patches

from typing import Annotated

from fastapi import FastAPI, UploadFile, Depends, HTTPException, status, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.middleware.cors import CORSMiddleware

from renderer.render import Renderer
from replay_parser import ReplayParser

app = FastAPI()
security = HTTPBasic()

# 重要：配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "null",                     # 允许file://协议（可选）
        "*"                         # 开发环境可以用*，生产环境不要用
    ],
    allow_credentials=True,
    allow_methods=["*"],           # 允许所有HTTP方法
    allow_headers=["*"],           # 允许所有HTTP头
)


def get_current_username(
        credentials: Annotated[HTTPBasicCredentials, Depends(security)],
):
    with open(os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + "/token.json", 'r', encoding='utf8') as json_f:
        json_data = json.load(json_f)

    current_username_bytes = credentials.username.encode("utf8")
    correct_username_bytes = str(json_data['username']).encode("utf8")
    is_correct_username = secrets.compare_digest(
        current_username_bytes, correct_username_bytes
    )
    current_password_bytes = credentials.password.encode("utf8")
    correct_password_bytes = str(json_data['password']).encode("utf8")
    is_correct_password = secrets.compare_digest(
        current_password_bytes, correct_password_bytes
    )
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    # 读取 HTML 文件
    with open("index.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)

@app.post("/upload_replays_video", summary="上传rep文件返回视频流")
async def upload_replays_video(file: UploadFile, username: Annotated[str, Depends(get_current_username)]):
    binary_bytes = file.file.read()
    binary_stream = io.BytesIO(binary_bytes)
    uuid_str_mp4 = os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + '/temp/' + hashlib.sha256(binary_bytes).hexdigest() + '.mp4'
    if not os.path.exists(uuid_str_mp4):
        replay_info = ReplayParser(
            binary_stream, strict=True, raw_data_output=False
        ).get_info()
        renderer = Renderer(
            replay_info["hidden"]["replay_data"],
            logs=True,
            enable_chat=True,
            use_tqdm=True,
        )
        renderer.start(str(uuid_str_mp4))
    return FileResponse(uuid_str_mp4, media_type="video/mp4")

@app.options("/upload_replays_video")
async def options_upload_replays_video():
    """处理OPTIONS预检请求"""
    return JSONResponse(
        content={"message": "CORS预检请求通过"},
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Max-Age": "3600"
        }
    )

@app.post("/upload_replays_video_url", summary="上传rep文件返回视频名称")
async def upload_replays_video_url(file: UploadFile, username: Annotated[str, Depends(get_current_username)]):
    binary_bytes = file.file.read()
    binary_stream = io.BytesIO(binary_bytes)
    video_name = hashlib.sha256(binary_bytes).hexdigest() + '.mp4'
    uuid_str_mp4 = os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + '/temp/' + video_name
    if not os.path.exists(uuid_str_mp4):
        replay_info = ReplayParser(
            binary_stream, strict=True, raw_data_output=False
        ).get_info()
        renderer = Renderer(
            replay_info["hidden"]["replay_data"],
            logs=True,
            enable_chat=True,
            use_tqdm=True,
        )
        renderer.start(str(uuid_str_mp4))
    return video_name


@app.get("/video_url", summary="上传rep文件返回视频地址")
async def video_url(file_name: str):
    file = os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + '/temp/' + file_name
    if os.path.exists(file):
        return FileResponse(file, media_type="video/mp4")
    return HTTPException(status_code=404, detail="文件不存在")


def del_file(file_name):
    os.remove(file_name)
