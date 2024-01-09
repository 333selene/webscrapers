@echo off
call setn intdaily
del *.csv *.mod *.upd
call clean
call python getstock.py
dir *.csv
call csv2modb ipc.*
call csv2modb bloom.* 
pause
copy ipc.mod+bloom.mod all.mod
dlxprep all.mod @chk=adj
pause
call dlxfed all.mod
call chkupd intdaily
