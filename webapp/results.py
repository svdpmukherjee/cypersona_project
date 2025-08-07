"""
Results display with separate intervention and persona parameter views
"""

import streamlit as st
from config import MODEL_CONFIGS

def display_parameters_passed_to_models(parameters):
    """Display parameters separated by intervention vs persona triggers"""
    with st.expander("Parameters Extracted from Analysis"):
        # Create main tabs for intervention vs persona
        main_tabs = st.tabs(["Intervention Parameters", "Persona Parameters", "All Parameters"])
        
        with main_tabs[0]:
            st.write("**Parameters triggered by intervention scenario:**")
            display_intervention_parameters(parameters)
        
        with main_tabs[1]:
            st.write("**Parameters triggered by persona description:**")
            display_persona_parameters(parameters)
        
        with main_tabs[2]:
            st.write("**Complete parameter set for all models:**")
            display_all_parameters_compact(parameters)

def display_intervention_parameters(parameters):
    """Show parameters that should be influenced by intervention description"""
    intervention_params = {
        'wash': [
            # Email issue detection patterns (what intervention teaches to recognize)
            'sender_issues_none', 'sender_issues_name_different', 'sender_issues_email_different',
            'subject_line_issues_none', 'subject_line_issues_different',
            'email_body_issues_none', 'email_body_issues_typos', 'email_body_issues_missing',
            'email_body_issues_strange', 'email_body_issues_more_info', 'email_body_issues_less_info',
            # Typical phishing characteristics (intervention scenarios)
            'actions_requested_click_link', 'actions_requested_open_attachment',
            'actions_requested_respond_info', 'actions_requested_external_action'
        ],
        'oliver': [
            # PMT threat perceptions (intervention context)
            'perceived_severity', 'perceived_vulnerability'
        ],
        'lorin': [
            # Training provision
            'security_training_prior'
        ]
    }
    
    display_categorized_parameters(parameters, intervention_params, "intervention")

def display_persona_parameters(parameters):
    """Show parameters that should be influenced by persona description"""
    persona_params = {
        'wash': [
            # Demographics
            'age_category', 'gender', 'education_level', 'employment_status', 'annual_income',
            # IT background & history
            'has_it_training', 'has_it_job',
            'previous_incidents_phishing_email', 'previous_incidents_data_breach',
            'previous_incidents_computer_virus', 'previous_incidents_device_hacked',
            'previous_incidents_credit_card_fraud', 'previous_incidents_identity_theft',
            'previous_incidents_any',
            # Digital literacy (personal knowledge)
            'digital_literacy_wiki', 'digital_literacy_meme', 'digital_literacy_phishing',
            'digital_literacy_bookmark', 'digital_literacy_cache', 'digital_literacy_ssl',
            'digital_literacy_ajax', 'digital_literacy_rss', 'digital_literacy_other',
            'digital_literacy_total',
            # Emotional responses (personality-based)
            'emotion_dread', 'emotion_terror', 'emotion_anxiety', 'emotion_nervous',
            'emotion_scared', 'emotion_panic', 'emotion_fear', 'emotion_worry',
            'emotion_total',
            # Personal behaviors and traits
            'investigated_sender', 'investigated_links', 'investigated_external',
            'noticed_sender_issues', 'noticed_content_issues', 'noticed_technical_issues',
            'suspicion_confidence', 'overall_suspicion', 'perceived_harm',
            # Email usage patterns
            'email_recency', 'email_account_work', 'email_account_student', 'email_account_personal',
            'email_content_work_related', 'email_content_personal',
            'email_sender_work_colleague', 'email_sender_friend_family',
            'email_sender_acquaintance', 'email_sender_organization',
            'sender_relationship_duration', 'expected_this_email', 'felt_similar_before',
            'previous_sender_emails', 'previous_sender_interaction', 'email_seemed_different'
        ],
        'oliver': [
            # Demographics
            'age_category', 'gender', 'education_level', 'employment_status',
            # IT background
            'it_job', 'phishing_victim', 'phishing_victim_count',
            # Personal perceptions
            'perceived_knowledge', 'perceived_self_efficacy', 'email_trust'
        ],
        'lorin': [
            # Demographics
            'age_category', 'education_level', 'it_experience', 'email_frequency',
            # Big Five personality traits
            'personality_extraversion', 'personality_agreeableness', 
            'personality_conscientiousness', 'personality_neuroticism', 'personality_openness',
            # Personal security attitudes
            'pre_security_engagement', 'pre_security_attentiveness', 
            'pre_security_resistance', 'pre_security_concern', 'pre_security_attitude_total',
            # Personal capabilities
            'knowledge_total', 'proficiency'
        ]
    }
    
    display_categorized_parameters(parameters, persona_params, "persona")

def display_categorized_parameters(parameters, param_categories, category_type):
    """Display parameters in organized categories"""
    model_tabs = st.tabs(["WASH", "Oliver", "Lorin"])
    
    for i, (model_key, tab) in enumerate(zip(['wash', 'oliver', 'lorin'], model_tabs)):
        with tab:
            if model_key in parameters and model_key in param_categories:
                model_params = parameters[model_key]
                relevant_params = param_categories[model_key]
                
                # Group parameters by logical categories
                if model_key == 'wash':
                    if category_type == "intervention":
                        groups = {
                            "Investigation Behaviors": [p for p in relevant_params if 'investigated' in p],
                            "Threat Recognition": [p for p in relevant_params if 'noticed' in p or 'suspicion' in p or 'harm' in p],
                            "Email Actions": [p for p in relevant_params if 'actions_requested' in p]
                        }
                    else:  # persona
                        groups = {
                            "Demographics": [p for p in relevant_params if any(x in p for x in ['age', 'gender', 'education', 'employment', 'income'])],
                            "IT Background": [p for p in relevant_params if any(x in p for x in ['it_', 'incidents'])],
                            "Digital Literacy": [p for p in relevant_params if 'literacy' in p],
                            "Emotional Profile": [p for p in relevant_params if 'emotion' in p],
                            "Email Context": [p for p in relevant_params if any(x in p for x in ['email_', 'sender_'])]
                        }
                elif model_key == 'oliver':
                    if category_type == "intervention":
                        groups = {"PMT Constructs": relevant_params}
                    else:  # persona
                        groups = {
                            "Demographics": [p for p in relevant_params if any(x in p for x in ['age', 'gender', 'education', 'employment'])],
                            "IT Background": [p for p in relevant_params if any(x in p for x in ['it_', 'phishing'])]
                        }
                else:  # lorin
                    if category_type == "intervention":
                        groups = {
                            "Security Attitudes": [p for p in relevant_params if 'security' in p],
                            "Capabilities": [p for p in relevant_params if any(x in p for x in ['knowledge', 'proficiency'])],
                            "Training": [p for p in relevant_params if 'training' in p]
                        }
                    else:  # persona
                        groups = {
                            "Demographics": [p for p in relevant_params if any(x in p for x in ['age', 'education', 'experience', 'frequency'])],
                            "Personality": [p for p in relevant_params if 'personality' in p]
                        }
                
                # Display grouped parameters
                for group_name, group_params in groups.items():
                    if group_params:
                        st.write(f"**{group_name}:**")
                        cols = st.columns(2)
                        for j, param in enumerate(group_params):
                            if param in model_params:
                                value = model_params[param]
                                col_idx = j % 2
                                with cols[col_idx]:
                                    # Format value for display
                                    if isinstance(value, float):
                                        if -2 <= value <= 2:  # Standardized
                                            display_val = f"{value:.2f}"
                                        else:
                                            display_val = f"{value:.1f}"
                                    else:
                                        display_val = str(value)
                                    st.write(f"• {param.replace('_', ' ').title()}: **{display_val}**")
                        st.write("")  # Space between groups
            else:
                st.info(f"No {category_type} parameters extracted for {model_key.upper()}")

def display_all_parameters_compact(parameters):
    """Compact view of all parameters"""
    tabs = st.tabs(["WASH", "Oliver", "Lorin"])
    
    for i, (model_key, tab) in enumerate(zip(['wash', 'oliver', 'lorin'], tabs)):
        with tab:
            if model_key in parameters:
                model_params = parameters[model_key]
                config = MODEL_CONFIGS[model_key]
                
                st.write(f"**{len(model_params)}/{len(config['features'])} parameters**")
                
                # Show in 3 columns for compact display
                param_list = list(model_params.items())
                cols = st.columns(3)
                
                for idx, (param, value) in enumerate(param_list):
                    col_idx = idx % 3
                    with cols[col_idx]:
                        if isinstance(value, float):
                            if -2 <= value <= 2:
                                display_val = f"{value:.2f}"
                            else:
                                display_val = f"{value:.1f}"
                        else:
                            display_val = str(value)
                        st.write(f"**{param}**: {display_val}")

# Keep existing result display functions unchanged
def display_wash_results(predictions):
    """Display WASH results"""
    st.subheader("WASH 2021 - Real Incident Behavior")
    
    if not predictions:
        st.error("No WASH predictions")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        if 'final_decision' in predictions:
            decision = predictions['final_decision']
            prediction_val = decision.get('prediction', 0)
            probability = decision.get('probability', None)
            
            if prediction_val == 1:
                st.success("✅ Decision Likely: Email is safe")
            else:
                st.error("⚠️ Decision Likely: Email is unsafe")
            
            # if probability:
            #     st.write(f"Confidence: {probability*100:.1f}%")
    
    with col2:
        if 'decision_confidence' in predictions:
            conf_pred = predictions['decision_confidence'].get('prediction', 0)
            conf_pct = max(0, min(100, 50 + conf_pred * 25))
            st.metric("Decision Confidence", f"{conf_pct:.0f}%")

def display_oliver_results(predictions):
    """Display Oliver results"""
    st.subheader("Oliver 2022 - Competence Assessment")
    
    if not predictions:
        st.error("No Oliver predictions")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        if 'phishing_test_percent_correct' in predictions:
            score = predictions['phishing_test_percent_correct'].get('prediction', 0)
            pct = max(0, min(100, 50 + score * 15))
            st.metric("Phishing Detection", f"{pct:.0f}%")
            
            if pct < 60:
                st.warning("Below average")
            elif pct > 80:
                st.success("Above average")
    
    with col2:
        if 'knowledge_test_percent_correct' in predictions:
            score = predictions['knowledge_test_percent_correct'].get('prediction', 0)
            pct = max(0, min(100, 50 + score * 15))
            st.metric("Security Knowledge", f"{pct:.0f}%")

def display_lorin_results(predictions):
    """Display Lorin results"""
    st.subheader("Lorin 2025 - Personality-Based")
    
    if not predictions:
        st.error("No Lorin predictions")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        if 'class_phish_accuracy' in predictions:
            acc = predictions['class_phish_accuracy'].get('prediction', 0.5)
            pct = max(0, min(100, acc * 100))
            st.metric("Phishing Detection", f"{pct:.0f}%")
    
    with col2:
        if 'class_nophish_accuracy' in predictions:
            acc = predictions['class_nophish_accuracy'].get('prediction', 0.5)
            pct = max(0, min(100, acc * 100))
            st.metric("Legitimate Email Recognition", f"{pct:.0f}%")

def display_all_results(results):
    """Display all model results"""
    st.header("Prediction Results")
    
    available_results = {k: v for k, v in results.items() if v is not None}
    
    if not available_results:
        st.error("No results available")
        return
    
    if 'wash' in available_results:
        display_wash_results(available_results['wash'])
        st.divider()
    
    if 'oliver' in available_results:
        display_oliver_results(available_results['oliver'])
        st.divider()
    
    if 'lorin' in available_results:
        display_lorin_results(available_results['lorin'])

def display_parameter_summary(parameters, summary):
    """Display simple parameter summary"""
    st.subheader("Extraction Summary")
    
    cols = st.columns(3)
    for i, (model_name, stats) in enumerate(summary.items()):
        with cols[i]:
            completeness = stats['completeness'] * 100
            st.metric(
                f"{model_name.upper()}", 
                f"{completeness:.0f}%",
                f"{stats['extracted']}/{stats['total']}"
            )