@echo off
echo try to reset the branch
cd /d %~dp0
cd minimap_renderer
git fetch --all
git reset --hard origin/master
git pull
pause