# Crea las 3 tareas de Windows de hr-deducir (modo sombra). Correr como admin.
$ErrorActionPreference = 'Stop'
$svc = New-Object -ComObject Schedule.Service; $svc.Connect(); $folder = $svc.GetFolder("\")
function Tarea($nombre, $desc, $hora, $repetirHoras, $arg) {
  $def = $svc.NewTask(0)
  $def.RegistrationInfo.Description = $desc
  $t = $def.Triggers.Create(2); $t.StartBoundary = "2026-01-01T$hora"; $t.DaysInterval = 1; $t.Enabled = $true
  if ($repetirHoras -gt 0) { $t.Repetition.Interval = "PT1H"; $t.Repetition.Duration = "PT$($repetirHoras)H" }
  $a = $def.Actions.Create(0); $a.Path = "C:\jornada-bot\hr-deducir\correr.bat"; $a.Arguments = $arg
  $a.WorkingDirectory = "C:\jornada-bot\hr-deducir"
  $def.Principal.LogonType = 3; $def.Principal.RunLevel = 0      # sesión del usuario (Outlook abierto)
  $def.Settings.MultipleInstances = 2; $def.Settings.StartWhenAvailable = $true
  $def.Settings.ExecutionTimeLimit = "PT30M"; $def.Settings.DisallowStartIfOnBatteries = $false
  $folder.RegisterTaskDefinition($nombre, $def, 6, $null, $null, 3) | Out-Null
  Write-Host "Tarea '$nombre' creada." -ForegroundColor Green
}
Tarea "HR deducir - mails"   "Baja de Outlook los mails de cargas LIN/LOX y arma rutas.json" "14:10:00" 7 "mails"
Tarea "HR deducir - recorrido" "Propone la HR de cada cisterna por su recorrido (modo sombra)" "08:20:00" 14 "deducir"
Tarea "HR deducir - noche"   "Aprende ubicaciones con las HR confirmadas y mide aciertos" "22:40:00" 0 "noche"
