Param()
$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $MyInvocation.MyCommand.Definition
$img  = Join-Path $root "images"
$manifest = Join-Path $root "textures.json"
New-Item -ItemType Directory -Force -Path $img | Out-Null

$data = Get-Content $manifest | ConvertFrom-Json
foreach ($key in $data.PSObject.Properties.Name) {
  $url = $data.$key
  $out = Join-Path $img $key
  Write-Host "Downloading $key ..."
  Invoke-WebRequest -Uri $url -OutFile $out -UseBasicParsing
}
Write-Host "All textures downloaded to images/"
