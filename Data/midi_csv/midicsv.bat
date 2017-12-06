CD ..\midi_data
FOR  /r %%f IN (*.mid) do (
	cd ..\midi_csv & START Midicsv.exe %%f ..\csv_data\%%~nf.csv & cd ..\midi_data
	)

pause