call setn intdaily
call clean
call del *.mod 
call csv2modb manual.txt manual.dic manual.mod
pause
call trim manual.mod trim.mod 3 4
call dlxprep trim.mod @chk=asis
pause
call dlxfed trim.mod
call chkupd intdaily
