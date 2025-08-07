"""
Configuration with improved prompt for better intervention vs persona parameter mapping
"""

# WASH 2021 Model Features (73 total)
WASH_FEATURES = [
    # Demographics (5)
    'age_category', 'gender', 'education_level', 'employment_status', 'annual_income',
    
    # IT Background & Security History (7)
    'has_it_training', 'has_it_job', 
    'previous_incidents_phishing_email', 'previous_incidents_data_breach', 
    'previous_incidents_computer_virus', 'previous_incidents_device_hacked',
    'previous_incidents_credit_card_fraud', 'previous_incidents_identity_theft', 
    'previous_incidents_any',
    
    # Digital Literacy (10)
    'digital_literacy_wiki', 'digital_literacy_meme', 'digital_literacy_phishing',
    'digital_literacy_bookmark', 'digital_literacy_cache', 'digital_literacy_ssl',
    'digital_literacy_ajax', 'digital_literacy_rss', 'digital_literacy_other',
    'digital_literacy_total',
    
    # Emotions (9)
    'emotion_dread', 'emotion_terror', 'emotion_anxiety', 'emotion_nervous',
    'emotion_scared', 'emotion_panic', 'emotion_fear', 'emotion_worry',
    'emotion_total',
    
    # Investigation (3)
    'investigated_sender', 'investigated_links', 'investigated_external',
    
    # Email Context (36)
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
    
    # Confidence & Perception (3)
    'suspicion_confidence', 'overall_suspicion', 'perceived_harm'
]

# Oliver 2022 Model Features (12 total)
OLIVER_FEATURES = [
    # Demographics (4)
    'age_category', 'gender', 'education_level', 'employment_status',
    
    # IT Background (3)
    'it_job', 'phishing_victim', 'phishing_victim_count',
    
    # PMT Constructs (5)
    'perceived_knowledge', 'perceived_self_efficacy', 'perceived_severity', 
    'perceived_vulnerability', 'email_trust'
]

# Lorin 2025 Model Features (17 total)
LORIN_FEATURES = [
    # Demographics (5)
    'age_category', 'education_level', 'it_experience', 'email_frequency', 'security_training_prior',
    
    # Personality (5)
    'personality_extraversion', 'personality_agreeableness', 'personality_conscientiousness',
    'personality_neuroticism', 'personality_openness',
    
    # Security Attitudes (5)
    'pre_security_engagement', 'pre_security_attentiveness', 'pre_security_resistance',
    'pre_security_concern', 'pre_security_attitude_total',
    
    # Capabilities (2)
    'knowledge_total', 'proficiency'
]

# Improved LLM prompt with correct intervention vs persona parameter mapping
PERSONA_ANALYSIS_PROMPT = """
You are an expert cybersecurity behavioral analyst. Analyze the PERSONA and INTERVENTION separately to extract parameters for phishing behavior prediction models.

**PERSONA DESCRIPTION**: {persona}
**INTERVENTION SCENARIO**: {intervention}

CRITICAL INSTRUCTIONS:
1. PERSONA → Personal characteristics, traits, behaviors, knowledge, attitudes
2. INTERVENTION → Scenario context (threat characteristics, what's being simulated/tested)

Extract realistic values for ALL parameters. Use the mapping guidance below:

=== WASH 2021 MODEL (Real incident behavior) ===

**FROM PERSONA** (Personal traits, knowledge & behaviors):
Demographics & Background:
- age_category: 1-5 (1=18-25, 2=26-35, 3=36-45, 4=46-55, 5=56+)
- gender: 0-1 (0=female, 1=male)  
- education_level: 1-4 (1=high school, 2=some college, 3=bachelor, 4=graduate)
- employment_status: 0-1 (0=unemployed, 1=employed)
- annual_income: 1-4 (1=<35k, 2=35-75k, 3=75-150k, 4=150k+)

IT Background & Security History:
- has_it_training: 0-1, has_it_job: 0-1
- previous_incidents_*: 0-1 (person's security incident history)

Digital Literacy (person's technical knowledge) - standardized -2 to 2:
- digital_literacy_wiki, digital_literacy_meme, digital_literacy_phishing
- digital_literacy_bookmark, digital_literacy_cache, digital_literacy_ssl
- digital_literacy_ajax, digital_literacy_rss, digital_literacy_other, digital_literacy_total

Emotional Profile (person's emotional tendencies) - standardized -2 to 2:
- emotion_dread, emotion_terror, emotion_anxiety, emotion_nervous
- emotion_scared, emotion_panic, emotion_fear, emotion_worry, emotion_total

Personal Behaviors (how this person typically acts):
- investigated_sender: 0-1 (person's tendency to check senders)
- investigated_links: 0-1 (person's tendency to verify links)
- investigated_external: 0-1 (person's tendency to use external verification)
- noticed_sender_issues: 0-1, noticed_content_issues: 0-1, noticed_technical_issues: 0-1
- suspicion_confidence: -2 to 2, overall_suspicion: 0-1, perceived_harm: -2 to 2

Email Usage Patterns (person's work/life context):
- email_recency: 1-5, email_account_*: 0-1, email_content_*: 0-1
- email_sender_*: 0-1, sender_relationship_duration: 1-6
- expected_this_email: 0-1, felt_similar_before: 1-5
- previous_sender_emails: 0-1, previous_sender_interaction: 0-1, email_seemed_different: 1-5

**FROM INTERVENTION** (Scenario being simulated/tested):
Email Characteristics (what the intervention contains):
- actions_requested_click_link: 0-1 (intervention asks to click links)
- actions_requested_open_attachment: 0-1 (intervention includes attachments)
- actions_requested_respond_info: 0-1 (intervention requests information)
- actions_requested_external_action: 0-1 (intervention requests external action)

Email Issue Patterns (what the intervention simulates):
- sender_issues_none: 0-1, sender_issues_name_different: 0-1, sender_issues_email_different: 0-1
- subject_line_issues_none: 0-1, subject_line_issues_different: 0-1
- email_body_issues_*: 0-1 (what issues the intervention email contains)

=== OLIVER 2022 MODEL (Competence assessment) ===

**FROM PERSONA** (Personal characteristics & perceptions):
Demographics: age_category, gender, education_level, employment_status (same as WASH)
IT Background: it_job: 0-1, phishing_victim: 0-1, phishing_victim_count: -2 to 2

PMT Personal Perceptions - standardized -2 to 2:
- perceived_knowledge: Person's confidence in their security knowledge
- perceived_self_efficacy: Person's confidence in handling threats
- email_trust: Person's general trust in email communications

**FROM INTERVENTION** (Threat context being assessed):
PMT Threat Characteristics - standardized -2 to 2:
- perceived_severity: Severity of threats in intervention scenario
- perceived_vulnerability: Vulnerability level tested by intervention

=== LORIN 2025 MODEL (Personality-based) ===

**FROM PERSONA** (Personal characteristics):
Demographics: age_category, education_level, it_experience, email_frequency

Big Five Personality (inherent traits) - standardized -2 to 2:
- personality_extraversion, personality_agreeableness, personality_conscientiousness
- personality_neuroticism, personality_openness

Personal Security Attitudes - standardized -2 to 2:
- pre_security_engagement: Person's engagement with security
- pre_security_attentiveness: Person's attention to security
- pre_security_resistance: Person's resistance to security measures
- pre_security_concern: Person's concern about threats
- pre_security_attitude_total: Person's overall security attitude

Personal Capabilities - standardized -2 to 2:
- knowledge_total: Person's security knowledge level
- proficiency: Person's security skill level

**FROM INTERVENTION** (Training provision):
- security_training_prior: 0-1 (whether intervention provides/includes training)

**MAPPING EXAMPLES:**
- Persona: "cautious accountant, detail-oriented" → investigated_sender=1, personality_conscientiousness=1
- Intervention: "phishing email with urgent payment request" → actions_requested_click_link=1, perceived_severity=1
- Persona: "tech-savvy developer, confident" → perceived_knowledge=1, digital_literacy_total=1
- Intervention: "quarterly simulation with training" → security_training_prior=1

Respond with ONLY a JSON object containing all 102 parameters:
{{
  "wash": {{all 73 parameters}},
  "oliver": {{all 12 parameters}},
  "lorin": {{all 17 parameters}}
}}
"""

MODEL_CONFIGS = {
    'wash': {
        'features': WASH_FEATURES,
        'predictor_file': 'wash_predictor.joblib',
        'metadata_file': 'wash_metadata.joblib'
    },
    'oliver': {
        'features': OLIVER_FEATURES,
        'predictor_file': 'oliver_predictor.joblib',
        'metadata_file': 'oliver_metadata.joblib'
    },
    'lorin': {
        'features': LORIN_FEATURES,
        'predictor_file': 'lorin_predictor.joblib',
        'metadata_file': 'lorin_metadata.joblib'
    }
}