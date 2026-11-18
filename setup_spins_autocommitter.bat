@echo off
title Push Auto Committer to spins
echo ========================================================
echo  Configuring Auto Committer for:
echo  https://github.com/Vansh-vps/spins
echo ========================================================

cd /d "%~dp0"

echo [1/3] Adding latest workflow and committer files...
git add .
git commit -m "ci: configure automated daily cloud heartbeat committer" 2>nul

echo [2/3] Setting remote to spins repository...
git remote set-url origin https://github.com/Vansh-vps/spins.git

echo [3/3] Pushing to spins...
git push -u origin main -f

echo.
echo ========================================================
echo  SUCCESS! Pushed to https://github.com/Vansh-vps/spins
echo.
echo  NEXT STEP (Takes 10 seconds):
echo  1. Open: https://github.com/Vansh-vps/spins/settings/actions
echo  2. Under 'Workflow permissions', select 'Read and write permissions'
echo  3. Click 'Save'
echo ========================================================
pause
