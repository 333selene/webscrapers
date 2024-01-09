md new
md csvs
del *.mod *.csv codes_existing.lst
del .\csvs\*.csv
call clean
call setn intdaily
call dlxlist <in.txt
call ren dlxlist.txt codes_existing.lst 
call python fxauct.py
pause
call csv2modb fxauct.*
pause
call dwsplit fxauct.mod g:\util\23daily.txt
call dlxprep out.mod @chk=asis
pause
call dlxfed out.mod
call chkupd intdaily
