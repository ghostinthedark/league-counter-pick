@echo off
echo Starting League Counter Pick on http://127.0.0.1:8000
cd /d %~dp0..
python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
