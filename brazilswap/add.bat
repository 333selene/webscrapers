@echo off
md new
del new\*.csv
del fxauct.csv
call copy h+fxauct_.csv fxauct.csv
copy fxauct.csv new
cd new
del newdat* *.mod *.cre
call clean
copy f:\intdaily\brazil\fxauct\new\* 
call csv2modb fxauct.csv add.dic add.mod
call python genLabPar.py
pause
call colorful green "Use add.mod, add.dic, fxauct.csv, out.cre to add series. Make sure to verify with the source."
pause
call mod2cre <i
call shelldb usd
call setl
call colorful red "CONFIRM TARGET DB SETL = NEWDAT. DOUBLE CHECK DLXFED TARGET!"
pause
call colorful red "CONFIRM TARGET DB SETL = NEWDAT. DOUBLE CHECK DLXFED TARGET!"
pause
call dlxfed add.cre
pause
call dlxfed add.mod 
pause
call dlxfed new.par
pause
call dlxfed new.lab
pause
call copy NUL newdat.kda
call copy NUL newdat.cci
call copy NUL newdat.gap
call copy NUL newdat.prs
call copy NUL newdat.xms
call copy NUL newdat.dps
