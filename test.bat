@echo off

REM jekyll serve --detach is not supported on Windows

start bundle exec jekyll serve --drafts --unpublished
timeout 5
start http://127.0.0.1:4000/

