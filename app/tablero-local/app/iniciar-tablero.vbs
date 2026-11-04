' Arranca el servidor del tablero sin ventana. Lo usa el acceso directo de Inicio de Windows.
Set sh = CreateObject("WScript.Shell")
sh.Run "cmd /c C:\jornada-bot\tablero\tablero-loop.bat", 0, False
