@ECHO off

CD "%~dp0.venv\Scripts\"

CALL "%~dp0.venv\Scripts\activate.bat"

"%~dp0.venv\Scripts\python.exe" "%~dp0insert_image_to_excel.py"

PAUSE