#!/bin/sh
echo 'WSrocessStart'
#nohup /Users/deepansh.aggarwal/anaconda3/anaconda3/bin/python /Users/deepansh.aggarwal/Study/Projects/LinksWiki/code/Main/manage.py runserver > logWS.txt &
/Users/deepansh.aggarwal/anaconda3/anaconda3/bin/python /Users/deepansh.aggarwal/Study/Projects/LinksWiki/code/Main/manage.py runserver > logWS.txt
echo 'WSProcessEnd'
