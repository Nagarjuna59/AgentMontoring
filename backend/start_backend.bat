@echo off
echo Starting MongoDB...
start "MongoDB" mongod --dbpath C:\data\db
timeout /t 3
echo.
echo Starting FastAPI Backend...
python app.py
