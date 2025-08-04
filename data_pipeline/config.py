from pathlib import Path
import pandas as pd

class Config:
    ROOT_DIR = Path(__file__).parent.parent
    RAW_DATA_DIR = ROOT_DIR / "data" / "raw_data"
    CLEANED_DATA_DIR = ROOT_DIR / "data" / "cleaned_data"
    FEATURES_DIR = ROOT_DIR / "data" / "features"
    MODELS_DIR = ROOT_DIR / "models"
    PERSONAS_DIR = ROOT_DIR / "personas"
    
    # Ensure directories exist
    CLEANED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    FEATURES_DIR.mkdir(parents=True, exist_ok=True)
    MODELS_DIR.mkdir(parents=True, exist_ok=True)