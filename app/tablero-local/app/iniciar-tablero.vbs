' Arranca el servidor del tablero sin ventana. Lo usa el acceso directo de Inicio de Windows.
Set sh = CreateObject("WScript.Shell")
sh.CurrentDirectory = "C:\jornada-bot\tablero"
sh.Run "cmd /c node servidor.js >> C:\jornada-bot\logs\tablero.log 2>&1", 0, False
