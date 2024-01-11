$path = $Args[0]
$shell = New-Object -COMObject Shell.Application
$folder = Split-Path $path
$file = Split-Path $path -Leaf
$shellfolder = $shell.Namespace($folder)
$shellfile = $shellfolder.ParseName($file)
$videoduration = [timespan]::Parse($shellfolder.GetDetailsOf($shellfile, 27)).TotalSeconds
echo $videoduration