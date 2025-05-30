# PowerShell script to clone subprojects and set up Python and Node.js environments

$repos = @{
    'TruCtrl-API'  = 'https://github.com/YourOrg/TruCtrl-API.git'
    'TruCtrl-App'  = 'https://github.com/YourOrg/TruCtrl-App.git'
    'TruCtrl-Docs' = 'https://github.com/YourOrg/TruCtrl-Docs.git'
    'TruCtrl-Web'  = 'https://github.com/YourOrg/TruCtrl-Web.git'
}

foreach ($name in $repos.Keys) {
    if (-not (Test-Path $name)) {
        git clone $repos[$name]
    }
    $req = Join-Path $name 'requirements.txt'
    if (Test-Path $req) {
        $venvPath = Join-Path $name '.venv'
        if (-not (Test-Path $venvPath)) {
            python -m venv $venvPath
        }
        & "$venvPath\Scripts\pip.exe" install -r $req
    }
    $pkg = Join-Path $name 'package.json'
    if (Test-Path $pkg) {
        Push-Location $name
        if (Test-Path 'yarn.lock') {
            yarn install
        } else {
            npm install
        }
        Pop-Location
    }
}

Write-Host "All subprojects cloned and Python/Node.js environments set up."
