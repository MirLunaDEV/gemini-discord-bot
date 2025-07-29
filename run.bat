@echo off
echo Starting Gemini AI Discord Bot...
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install required packages
echo Installing required packages...
pip install -r requirements.txt

REM Run the bot
echo.
echo Running bot...
python main.py

REM Keep window open on error
if %ERRORLEVEL% neq 0 (
    echo.
    echo An error occurred. Please check the logs.
    pause
)
