@echo off
echo ========================================================
echo Pushing AI SECURITY FASTER to GitHub
echo Repository: https://github.com/doctorpraveen2011-netizen/AI-SECURITY-FASTER-DYANAMIC.git
echo ========================================================
echo.

git push -u origin main

echo.
if %ERRORLEVEL% EQU 0 (
    echo [SUCCESS] Code pushed successfully to GitHub!
) else (
    echo [NOTICE] If prompted for credentials, please sign in via browser or enter your GitHub Personal Access Token.
)

echo ========================================================
pause
