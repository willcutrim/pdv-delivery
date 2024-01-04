@echo off

rem Verifica se o Python está instalado
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Python não encontrado. Certifique-se de que o Python está instalado no seu sistema.
    exit /b 1
)

rem Define a porta padrão
set porta=8000

rem Verifica se o usuário especificou uma porta como argumento
if not "%1"=="" (
    set porta=%1
)

echo Iniciando o servidor Django na porta %porta% em segundo plano...
start "Meu Servidor Django" /min python manage.py runserver %porta%

rem Aguarda alguns segundos para garantir que o servidor tenha iniciado antes de fechar a janela do prompt
timeout /nobreak /t 5 >nul

echo Servidor Django iniciado em segundo plano na porta %porta%.
