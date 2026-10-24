@echo off
cd /d "%~dp0"
if not exist .venv\Scripts\python.exe python -m venv .venv
call .venv\Scripts\activate
python -m pip install -r requirements.txt
echo.
echo En esta PC: http://localhost:8501
echo En el celular, misma WiFi, usa la direccion Network que aparece abajo.
echo.
streamlit run app.py --server.address 0.0.0.0 --server.port 8501
