"""
Fixed LLM processor with working OpenAI model
"""

import json
import re
from openai import OpenAI

class LLMProcessor:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)
    
    def extract_parameters(self, persona, intervention):
        """Extract parameters using available OpenAI model"""
        print("Analyzing with OpenAI...")
        
        # Use the complete detailed prompt from config.py
        from config import PERSONA_ANALYSIS_PROMPT
        prompt = PERSONA_ANALYSIS_PROMPT.format(
            persona=persona,
            intervention=intervention
        )
        
        # Try multiple models in order of preference
        models = ["gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"]
        
        for model in models:
            try:
                print(f"Trying {model}...")
                response = self.client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.1
                )
                
                content = response.choices[0].message.content.strip()
                print(f"Got response from {model}")
                
                # Parse JSON
                parsed = self._extract_json(content)
                if parsed:
                    expanded = self._expand_parameters(parsed)
                    print("✓ Successfully extracted parameters")
                    return expanded
                    
            except Exception as e:
                print(f"Model {model} failed: {e}")
                continue
        
        print("All models failed, using defaults")
        return self._get_defaults()
    
    def _extract_json(self, content):
        """Extract JSON robustly"""
        # Try direct parsing first
        try:
            return json.loads(content)
        except:
            pass
        
        # Find JSON in text
        patterns = [
            r'```json\s*(\{.*?\})\s*```',
            r'```\s*(\{.*?\})\s*```',
            r'(\{[^{}]*\{.*?\}[^{}]*\})',
            r'(\{.*?\})'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, content, re.DOTALL)
            for match in matches:
                try:
                    return json.loads(match.strip())
                except:
                    continue
        
        return None
    
    def _expand_parameters(self, core_params):
        """Use LLM output directly without expansion since it should be complete"""
        # The LLM should return all required parameters based on config.py prompt
        # Just fill any missing ones with defaults
        from config import MODEL_CONFIGS
        
        result = {}
        for model_name, config in MODEL_CONFIGS.items():
            result[model_name] = {}
            model_params = core_params.get(model_name, {})
            
            # Fill all required features
            for feature in config['features']:
                if feature in model_params:
                    result[model_name][feature] = model_params[feature]
                else:
                    # Default based on feature type
                    if 'issues_none' in feature or 'email_account_personal' in feature:
                        result[model_name][feature] = 1
                    elif any(x in feature for x in ['category', 'level', 'recency']):
                        result[model_name][feature] = 3
                    elif 'gender' in feature:
                        result[model_name][feature] = 0
                    else:
                        result[model_name][feature] = 0
        
        return result
    
    def _get_defaults(self):
        """Return default parameters"""
        return self._expand_parameters({})
    
    def get_parameter_summary(self, parameters):
        """Get parameter summary"""
        from config import MODEL_CONFIGS
        
        summary = {}
        for model_name, model_params in parameters.items():
            if model_name in MODEL_CONFIGS:
                config = MODEL_CONFIGS[model_name]
                total = len(config['features'])
                extracted = len(model_params)
                summary[model_name] = {
                    'extracted': extracted,
                    'total': total,
                    'completeness': extracted / total if total > 0 else 0
                }
        return summary