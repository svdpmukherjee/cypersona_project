"""
Model predictor for making predictions with all loaded models
"""

import joblib
import pandas as pd
from pathlib import Path
from config import MODEL_CONFIGS
from predictors import WashPredictor, OliverPredictor, LorinPredictor

class ModelPredictor:
    def __init__(self, models_path=None):
        # Auto-detect models path - check both relative and absolute
        if models_path is None:
            current_dir = Path(__file__).parent  # webapp directory
            potential_paths = [
                current_dir.parent / "models",  # ../models from webapp
                Path("models"),  # ./models from current directory
                Path("/Users/suvadeep.mukherjee/Documents/cypersona_project/models")  # absolute path
            ]
            
            for path in potential_paths:
                if path.exists():
                    self.models_path = path
                    break
            else:
                # Use the absolute path from your debug output
                self.models_path = Path("/Users/suvadeep.mukherjee/Documents/cypersona_project/models")
        else:
            self.models_path = Path(models_path)
            
        print(f"Using models path: {self.models_path.absolute()}")
        self.models = {}
        self._load_models()
    
    def _load_models(self):
        """Load all available models"""
        for model_name, config in MODEL_CONFIGS.items():
            try:
                predictor_path = self.models_path / config['predictor_file']
                
                print(f"Checking for {model_name} at: {predictor_path}")
                
                if predictor_path.exists():
                    predictor = joblib.load(predictor_path)
                    self.models[model_name] = predictor
                    print(f"✓ Loaded {model_name} model")
                else:
                    print(f"✗ Model file not found: {predictor_path}")
                    
            except Exception as e:
                print(f"✗ Error loading {model_name}: {e}")
    
    def predict_all(self, parameters):
        """Make predictions with all loaded models"""
        results = {}
        
        for model_name, model in self.models.items():
            if model_name in parameters:
                try:
                    model_params = parameters[model_name]
                    config = MODEL_CONFIGS[model_name]
                    input_data = {}
                    
                    for feature in config['features']:
                        input_data[feature] = model_params.get(feature, 0)
                    
                    df = pd.DataFrame([input_data])
                    prediction = model(df)
                    
                    results[model_name] = prediction
                    print(f"✓ Prediction successful for {model_name}")
                    
                except Exception as e:
                    print(f"✗ Prediction failed for {model_name}: {e}")
                    results[model_name] = None
            else:
                print(f"✗ No parameters provided for {model_name}")
                results[model_name] = None
        
        return results
    
    def get_model_status(self):
        """Get status of loaded models"""
        status = {}
        
        for model_name in MODEL_CONFIGS.keys():
            model_file = self.models_path / MODEL_CONFIGS[model_name]['predictor_file']
            status[model_name] = {
                'loaded': model_name in self.models,
                'file_path': str(model_file),
                'file_exists': model_file.exists()
            }
        
        return status