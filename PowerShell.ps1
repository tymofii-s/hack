$pythonInstaller = "https://www.python.org/ftp/python/3.12.1/python-3.12.1-amd64.exe"
$installerPath = "$env:TEMP\python_installer.exe"
$scriptPath = "C:\Users\Timka\Desktop\progects\hack\start.py"  # Change this path

# Downloading the installer
Invoke-WebRequest -Uri $pythonInstaller -OutFile $installerPath

# Running the installer (silent installation)
Start-Process -FilePath $installerPath -ArgumentList "/quiet InstallAllUsers=1 PrependPath=1" -Wait

# Uninstalling the installer
Remove-Item -Path $installerPath -Force

# Running a Python script
Start-Process -FilePath "python" -ArgumentList "`"$scriptPath`"" -Wait
