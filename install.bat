@ECHO OFF
setlocal
ECHO Begin installation for Reddit Web Crawler application
:PROMPT
SET /P AREYOUSURE=Are you sure (Y/[N])?
IF /I "%AREYOUSURE%" NEQ "Y" GOTO END
set /p condapath=<condapath.txt
set CONDAPATH=%condapath%
call conda create -y -n web-crawler python=3.6
call conda activate web-crawler
call conda install -y -c anaconda django
call conda install -y -c conda-forge praw
call pip install mysql-connector-python
call conda deactivate
ECHO Installation completed
endlocal
PAUSE