# scripts/run_local.ps1
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
pip install -e .

# create logs folder
if (!(Test-Path -Path ".\logs")) { New-Item -ItemType Directory -Path ".\logs" }

Write-Host "Starting backend (uvicorn) ..."
Start-Process -NoNewWindow -FilePath "python" -ArgumentList "-m uvicorn backend.app:app --host 0.0.0.0 --port 8000" 

Write-Host "Starting frontend (streamlit) ..."
Start-Process -NoNewWindow -FilePath "python" -ArgumentList "-m streamlit run app/main.py --server.port 8501"
