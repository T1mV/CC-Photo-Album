## Setup
1. Create an `images` folder here and put your photos inside.
2. Install required libraries:
```powershell
pip install numpy pillow pillow-heif scikit-learn sentence-transformers pydantic google-genai
```
3. Set your API key in PowerShell:
```powershell
$env:GEMINI_API_KEY="Your API KEY"
```

## Run
There are two modes: selection by `color` and `clip`.

### 1. Clustering & Candidate Selection
```powershell
python 4_main.py clip
python 4_main.py color
```

### 2. Generate Chapter Themes & Hero Photos
```powershell
python 5_theme_generator.py output/selection_clip.json
python 5_theme_generator.py output/selection_color.json
```