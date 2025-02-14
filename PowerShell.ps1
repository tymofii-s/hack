$scriptPath = "start.py"  # Зміни цей шлях

# Перевірка, чи Python уже встановлений
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "Python не знайдено, починаємо встановлення..."
    $pythonInstaller = "https://www.python.org/ftp/python/3.12.1/python-3.12.1-amd64.exe"
    $installerPath = "$env:TEMP\python_installer.exe"

    # Завантаження інсталятора
    Invoke-WebRequest -Uri $pythonInstaller -OutFile $installerPath

    # Запуск інсталятора (тиха установка)
    Start-Process -FilePath $installerPath -ArgumentList "/quiet InstallAllUsers=1 PrependPath=1" -Wait

    # Видалення інсталятора
    Remove-Item -Path $installerPath -Force

    Write-Host "Python успішно встановлений."
}

# Запуск Python-скрипта
Start-Process -FilePath "python" -ArgumentList "`"$scriptPath`"" -Wait
