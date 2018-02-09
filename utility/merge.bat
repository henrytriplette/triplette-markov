cd input\
copy /a *.txt combination.txt
echo n|MOVE /-y combination.txt ..\combination.txt
cd ..
del /q input\*
for /d %%x in (input\*) do @rd /s /q "%%x"
pause
