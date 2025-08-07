"""
Predictor classes for all models
"""

import joblib
from pathlib import Path
import pandas as pd

class WashPredictor:
    def __init__(self):
        self.model_files = {
            'final_decision': 'wash_final_decision_model.joblib',
            'actions_taken_clicked': 'wash_actions_taken_clicked_model.joblib',
            'actions_taken_reported': 'wash_actions_taken_reported_model.joblib', 
            'actions_taken_deleted': 'wash_actions_taken_deleted_model.joblib',
            'actions_taken_ignored': 'wash_actions_taken_ignored_model.joblib',
            'decision_confidence': 'wash_decision_confidence_model.joblib'
        }
        
        self.features = [
            'age_category', 'gender', 'education_level', 'employment_status', 'annual_income',
            'has_it_training', 'has_it_job', 
            'previous_incidents_phishing_email', 'previous_incidents_data_breach', 
            'previous_incidents_computer_virus', 'previous_incidents_device_hacked',
            'previous_incidents_credit_card_fraud', 'previous_incidents_identity_theft', 
            'previous_incidents_any',
            'digital_literacy_wiki', 'digital_literacy_meme', 'digital_literacy_phishing',
            'digital_literacy_bookmark', 'digital_literacy_cache', 'digital_literacy_ssl',
            'digital_literacy_ajax', 'digital_literacy_rss', 'digital_literacy_other',
            'digital_literacy_total',
            'emotion_dread', 'emotion_terror', 'emotion_anxiety', 'emotion_nervous',
            'emotion_scared', 'emotion_panic', 'emotion_fear', 'emotion_worry',
            'emotion_total',
            'investigated_sender', 'investigated_links', 'investigated_external',
            'email_recency', 'email_account_work', 'email_account_student', 'email_account_personal',
            'email_content_work_related', 'email_content_personal',
            'email_sender_work_colleague', 'email_sender_friend_family', 
            'email_sender_acquaintance', 'email_sender_organization',
            'sender_relationship_duration', 'expected_this_email', 'felt_similar_before',
            'previous_sender_emails', 'previous_sender_interaction', 'email_seemed_different',
            'noticed_sender_issues', 'noticed_content_issues', 'noticed_technical_issues',
            'actions_requested_click_link', 'actions_requested_open_attachment',
            'actions_requested_respond_info', 'actions_requested_external_action',
            'sender_issues_none', 'sender_issues_name_different', 'sender_issues_email_different',
            'subject_line_issues_none', 'subject_line_issues_different',
            'email_body_issues_none', 'email_body_issues_typos', 'email_body_issues_missing',
            'email_body_issues_strange', 'email_body_issues_more_info', 'email_body_issues_less_info',
            'suspicion_confidence', 'overall_suspicion', 'perceived_harm'
        ]
    
    def __call__(self, input_data):
        if isinstance(input_data, dict):
            input_data = pd.DataFrame([input_data])
        
        for f in self.features:
            if f not in input_data.columns:
                input_data[f] = 0
        
        input_data = input_data[self.features].fillna(0)
        
        predictions = {}
        models_dir = Path(__file__).parent.parent / "models"
        
        for target, model_file in self.model_files.items():
            try:
                model_path = models_dir / model_file
                if model_path.exists():
                    model = joblib.load(model_path)
                    pred = model.predict(input_data)
                    
                    if target in ['final_decision', 'actions_taken_clicked', 'actions_taken_reported', 
                                 'actions_taken_deleted', 'actions_taken_ignored']:
                        prob = None
                        if hasattr(model, 'predict_proba'):
                            prob_array = model.predict_proba(input_data)
                            if prob_array.shape[1] > 1:
                                prob = prob_array[0][1]
                        
                        predictions[target] = {
                            'prediction': int(pred[0]), 
                            'probability': float(prob) if prob is not None else None
                        }
                    else:
                        predictions[target] = {'prediction': float(pred[0])}
                        
            except Exception as e:
                print(f"Error loading {target}: {e}")
        
        return predictions

class OliverPredictor:
    def __init__(self):
        self.model_files = {
            'phishing_test_percent_correct': 'oliver_phishing_test_percent_correct_model.joblib',
            'knowledge_test_percent_correct': 'oliver_knowledge_test_percent_correct_model.joblib'
        }
        
        self.features = [
            'age_category', 'gender', 'education_level', 'employment_status',
            'it_job', 'phishing_victim', 'phishing_victim_count',
            'perceived_knowledge', 'perceived_self_efficacy', 'perceived_severity', 
            'perceived_vulnerability', 'email_trust'
        ]
    
    def __call__(self, input_data):
        if isinstance(input_data, dict):
            input_data = pd.DataFrame([input_data])
        
        for f in self.features:
            if f not in input_data.columns:
                input_data[f] = 0
        
        input_data = input_data[self.features].fillna(0)
        
        predictions = {}
        models_dir = Path(__file__).parent.parent / "models"
        
        for target, model_file in self.model_files.items():
            try:
                model_path = models_dir / model_file
                if model_path.exists():
                    model = joblib.load(model_path)
                    pred = model.predict(input_data)
                    predictions[target] = {'prediction': float(pred[0])}
                    
            except Exception as e:
                print(f"Error loading {target}: {e}")
        
        return predictions

class LorinPredictor:
    def __init__(self):
        self.model_files = {
            'class_phish_accuracy': 'lorin_class_phish_accuracy_model.joblib',
            'class_nophish_accuracy': 'lorin_class_nophish_accuracy_model.joblib'
        }
        
        self.features = [
            'age_category', 'education_level', 'it_experience', 'email_frequency', 'security_training_prior',
            'personality_extraversion', 'personality_agreeableness', 'personality_conscientiousness',
            'personality_neuroticism', 'personality_openness',
            'pre_security_engagement', 'pre_security_attentiveness', 'pre_security_resistance',
            'pre_security_concern', 'pre_security_attitude_total',
            'knowledge_total', 'proficiency'
        ]
    
    def __call__(self, input_data):
        if isinstance(input_data, dict):
            input_data = pd.DataFrame([input_data])
        
        for f in self.features:
            if f not in input_data.columns:
                input_data[f] = 0
        
        input_data = input_data[self.features].fillna(0)
        
        predictions = {}
        models_dir = Path(__file__).parent.parent / "models"
        
        for target, model_file in self.model_files.items():
            try:
                model_path = models_dir / model_file
                if model_path.exists():
                    model = joblib.load(model_path)
                    pred = model.predict(input_data)
                    predictions[target] = {'prediction': float(pred[0])}
                    
            except Exception as e:
                print(f"Error loading {target}: {e}")
        
        return predictions