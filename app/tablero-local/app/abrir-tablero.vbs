' Abre el tablero en una ventana propia de Chrome. Si el servidor no está corriendo, lo arranca antes.
Set sh = CreateObject("WScript.Shell")
URL = "http://localhost:8090"

Function Anda()
  On Error Resume Next
  Set h = CreateObject("MSXML2.ServerXMLHTTP.6.0")
  h.setTimeouts 2000, 2000, 2000, 2000
  h.open "GET", URL & "/api/choferes", False
  h.send
  Anda = (Err.Number = 0 And h.status = 200)
End Function

If Not Anda() Then
  sh.Run "wscript """ & "C:\jornada-bot\tablero\iniciar-tablero.vbs""", 0, False
  For i = 1 To 20
    WScript.Sleep 500
    If Anda() Then Exit For
  Next
End If

On Error Resume Next
sh.Run "chrome --app=" & URL, 1, False
If Err.Number <> 0 Then
  Err.Clear
  sh.Run "msedge --app=" & URL, 1, False
End If
