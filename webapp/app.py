"""
Main Streamlit app for Phishing Intervention Predictor
Minimal modular implementation with complete functionality
"""

import streamlit as st
import os
from llm_processor import LLMProcessor
from predictor import ModelPredictor
from results import display_all_results, display_parameter_summary, display_parameters_passed_to_models

# Configure page
st.set_page_config(
    page_title="Phishing Intervention Predictor",
    layout="wide"
)

@st.cache_resource
def initialize_components():
    """Initialize LLM processor and model predictor"""
    # Get OpenAI API key
    api_key = st.secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
    if not api_key:
        st.error("OpenAI API key not found. Set OPENAI_API_KEY in secrets or environment.")
        st.stop()
    
    # Initialize components
    llm_processor = LLMProcessor(api_key)
    model_predictor = ModelPredictor()
    
    return llm_processor, model_predictor

def main():
    st.title("Phishing Intervention Predictor")
    st.write("AI-powered security behavior analysis using behavioral prediction models")
    
    # Initialize components
    llm_processor, model_predictor = initialize_components()
    
    # Show model status
    model_status = model_predictor.get_model_status()
    loaded_models = [name for name, status in model_status.items() if status['loaded']]
    
    # st.write(f"**Loaded Models**: {', '.join(loaded_models).upper()}")
    
    if not loaded_models:
        st.error("No models loaded. Check your models directory.")
        st.stop()
    
    # Input section
    st.header("Input")
    
    col1, col2 = st.columns(2)
    
    with col1:
        intervention = st.text_area(
            "Phishing Intervention Scenario:",
            height=150,
            placeholder="Describe the phishing intervention you want to test (e.g., quarterly phishing simulation with immediate feedback and remedial training for employees who click suspicious links...)",
            help="Provide details about the intervention type, frequency, target behaviors, and expected outcomes."
        )
    
    with col2:
        persona = st.text_area(
            "Target Persona:",
            height=150,
            placeholder="Describe the target user profile (e.g., 35-year-old marketing manager, college graduate, moderate IT experience, uses email frequently, has received basic security training...)",
            help="Include demographics, job role, IT experience, personality traits, and security awareness level."
        )
    
    # Analysis button
    analyze_clicked = st.button("Analyze Intervention Impact", type="primary")
    
    if analyze_clicked:
        if not intervention.strip() or not persona.strip():
            st.error("Please provide both intervention scenario and persona description.")
        else:
            # Process with LLM
            with st.spinner("Analyzing persona and intervention with LLM..."):
                parameters = llm_processor.extract_parameters(persona, intervention)
            
            if parameters:
                # Show what parameters are being passed to models
                display_parameters_passed_to_models(parameters)
                # st.divider()
                
                # Show parameter extraction summary
                summary = llm_processor.get_parameter_summary(parameters)
                # display_parameter_summary(parameters, summary)
                # st.divider()
                
                # Make predictions
                with st.spinner("Generating predictions from behavioral models..."):
                    results = model_predictor.predict_all(parameters)
                
                # Display results
                display_all_results(results)
                
                # Show recommendations
                st.header("Recommendations")
                
                # Simple recommendation logic based on results
                recommendations = generate_recommendations(results)
                
                for rec in recommendations:
                    st.write(f"- {rec}")
            
            else:
                st.error("Failed to extract parameters from persona description. Please provide more detailed information.")

def generate_recommendations(results):
    """Generate simple recommendations based on prediction results"""
    recommendations = []
    
    # WASH-based recommendations
    if results.get('wash'):
        wash = results['wash']
        
        if 'final_decision' in wash:
            safety_prob = wash['final_decision'].get('probability', 0.5)
            if safety_prob < 0.3:
                recommendations.append("High risk user - implement immediate targeted phishing training")
            elif safety_prob > 0.7:
                recommendations.append("Low risk user - maintain current security practices")
        
        if 'actions_taken_clicked' in wash:
            click_prob = wash['actions_taken_clicked'].get('probability', 0)
            if click_prob > 0.5:
                recommendations.append("High click risk - provide link verification training")
        
        if 'actions_taken_reported' in wash:
            report_prob = wash['actions_taken_reported'].get('probability', 0)
            if report_prob < 0.3:
                recommendations.append("Low reporting behavior - encourage suspicious email reporting")
    
    # Oliver-based recommendations
    if results.get('oliver'):
        oliver = results['oliver']
        
        if 'phishing_test_percent_correct' in oliver:
            score = oliver['phishing_test_percent_correct'].get('prediction', 0)
            pct = max(0, min(100, 50 + score * 15))
            
            if pct < 60:
                recommendations.append("Below average phishing detection - intensive awareness training needed")
            elif pct > 80:
                recommendations.append("Strong phishing detection skills - consider as security champion")
        
        if 'knowledge_test_percent_correct' in oliver:
            score = oliver['knowledge_test_percent_correct'].get('prediction', 0)
            pct = max(0, min(100, 50 + score * 15))
            
            if pct < 60:
                recommendations.append("Security knowledge gap - foundational training required")
    
    # Lorin-based recommendations
    if results.get('lorin'):
        lorin = results['lorin']
        
        if 'class_phish_accuracy' in lorin:
            acc = lorin['class_phish_accuracy'].get('prediction', 0.5)
            pct = acc * 100
            
            if pct < 50:
                recommendations.append("Personality traits suggest high vulnerability - personalized training approach needed")
            elif pct > 75:
                recommendations.append("Natural protection from personality - leverage strengths in training others")
    
    # Default recommendations if none generated
    if not recommendations:
        recommendations = [
            "Implement regular phishing simulations",
            "Provide security awareness training",
            "Monitor email behavior patterns",
            "Establish clear reporting procedures"
        ]
    
    return recommendations

if __name__ == "__main__":
    main()