# Models Directory
# =================
# This directory stores versioned model artefacts.
#
# Naming convention:
#   models/YYYYMMDD_HHMM/
#     ├── restaurant-sentiment-mnb-model.pkl
#     ├── cv-transform.pkl
#     └── metadata.json
#
# Create a timestamped snapshot:
#   # Linux/macOS:
#   mkdir -p models/$(date +%Y%m%d_%H%M)
#   cp restaurant-sentiment-mnb-model.pkl cv-transform.pkl models/$(date +%Y%m%d_%H%M)/
#
#   # Windows PowerShell:
#   $ts = Get-Date -Format "yyyyMMdd_HHmm"
#   New-Item -ItemType Directory -Force -Path "models/$ts"
#   Copy-Item restaurant-sentiment-mnb-model.pkl, cv-transform.pkl -Destination "models/$ts/"
#
# Use Git tags to mark model versions:
#   git tag -a v1.0.0 -m "Initial MNB model, F1=0.78"
#   git push --tags
