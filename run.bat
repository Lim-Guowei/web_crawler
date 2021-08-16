@ECHO OFF
setlocal
ECHO Reddit Web Crawler application
set /p condapath=<condapath.txt
set CONDAPATH=%condapath%
call conda activate web-crawler
python manage.py runserver
endlocal
PAUSE