@echo off
SET /P versionNumber="Enter the version number [0.#]: "

REM Check if version number is provided
IF "%versionNumber%"=="" (
    echo Version number is required.
    exit /b 1
)

REM Set tag name
SET tagName="MinidimSharp v%versionNumber%"

REM Add deploy.bat to .gitignore if it's not already there
findstr /m /c:"deploy.bat" .gitignore || echo deploy.bat >> .gitignore

REM Commit changes
git add .
SET /P commitMessage="Enter your commit message: "
git commit -m "%commitMessage%"

REM Create a new tag
git tag -a %tagName% -m "Draft v%versionNumber%"

REM Push changes and tag
git push origin main
git push origin %tagName%

echo Deployment and tagging complete.
pause
