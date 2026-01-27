"""
Prevention recommendation engine
Generates personalized prevention plans based on disease, risk class, and user profile
"""

import json
from typing import Dict, List, Any


def load_guidelines():
    """Load prevention guidelines from JSON"""
    try:
        with open('data/guidelines.json', 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading guidelines: {e}")
        return {}


def get_personalized_prevention(
    disease_id: str,
    risk_class: str,
    user_data: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Generate personalized prevention plan
    
    Args:
        disease_id: Disease identifier
        risk_class: 'I', 'II', 'III', or 'IV'
        user_data: User profile with lifestyle, basic_info, etc.
    
    Returns:
        Dictionary with:
            - summary: Brief prevention summary
            - diet: Dietary recommendations
            - exercise: Exercise recommendations  
            - lifestyle: Lifestyle modifications
            - monitoring: What to monitor
            - urgency: How urgently to act
    """
    
    guidelines = load_guidelines()
    
    # Get disease-specific prevention
    disease_prevention = guidelines.get('disease_specific_prevention', {}).get(disease_id, {})
    
    # Get risk class guidance
    risk_info = guidelines.get('risk_classes', {}).get(risk_class, {})
    
    # Build personalized plan
    plan = {
        'summary': get_prevention_summary(disease_id, risk_class),
        'diet': personalize_diet_recommendations(disease_prevention.get('diet', []), user_data),
        'exercise': personalize_exercise_recommendations(disease_prevention.get('exercise', []), user_data),
        'lifestyle': personalize_lifestyle_recommendations(disease_prevention.get('lifestyle', []), user_data),
        'monitoring': get_monitoring_recommendations(disease_id, risk_class),
        'urgency': risk_info.get('consult', 'Routine checkup'),
        'risk_class_guidance': risk_info.get('prevention', [])
    }
    
    return plan


def get_prevention_summary(disease_id: str, risk_class: str) -> str:
    """Generate brief prevention summary"""
    
    summaries = {
        'type2_diabetes': {
            'I': "Maintain healthy weight and balanced diet to keep diabetes risk low.",
            'II': "Focus on reducing sugar intake and increasing physical activity.",
            'III': "Immediate dietary changes and regular exercise essential to prevent diabetes.",
            'IV': "Aggressive lifestyle intervention required - consult doctor for prevention plan."
        },
        'cad': {
            'I': "Continue heart-healthy habits with regular cardiovascular exercise.",
            'II': "Reduce saturated fats and increase aerobic activity.",
            'III': "Strict heart-healthy diet and exercise plan needed - medical guidance recommended.",
            'IV': "Urgent cardiology consultation required along with intensive lifestyle changes."
        },
        'hypertension': {
            'I': "Maintain low-sodium diet and regular exercise.",
            'II': "DASH diet and stress management recommended.",
            'III': "Aggressive sodium reduction and daily exercise essential.",
            'IV': "Urgent blood pressure management needed - immediate medical consultation."
        },
        'breast_ovarian_cancer': {
            'I': "Continue healthy lifestyle and routine self-examinations.",
            'II': "Consider genetic counseling and increased screening frequency.",
            'III': "Genetic testing strongly recommended - discuss preventive options with doctor.",
            'IV': "Urgent genetic counseling and comprehensive screening essential."
        }
    }
    
    default_summary = {
        'I': "Maintain current healthy habits with routine monitoring.",
        'II': "Adopt preventive lifestyle changes and schedule appropriate screening.",
        'III': "Significant lifestyle changes needed - consult healthcare provider soon.",
        'IV': "Urgent medical consultation required for comprehensive risk management."
    }
    
    return summaries.get(disease_id, default_summary).get(risk_class, default_summary[risk_class])


def personalize_diet_recommendations(base_diet: List[str], user_data: Dict) -> List[str]:
    """Personalize diet recommendations based on user profile"""
    
    recommendations = list(base_diet[:5])  # Start with base recommendations
    
    lifestyle = user_data.get('lifestyle', {})
    basic_info = user_data.get('basic_info', {})
    
    diet_type = lifestyle.get('diet', 'balanced')
    bmi = basic_info.get('bmi', 22)
    
    # Add personalized recommendations
    if bmi >= 25:
        recommendations.insert(0, "Focus on calorie control for weight management")
    
    if diet_type in ['high_sugar', 'poor']:
        recommendations.insert(0, "Eliminate sugary drinks and desserts immediately")
    
    if diet_type in ['high_fat', 'fast_food']:
        recommendations.insert(0, "Replace fried foods with grilled or baked alternatives")
    
    return recommendations[:6]  # Keep top 6


def personalize_exercise_recommendations(base_exercise: List[str], user_data: Dict) -> List[str]:
    """Personalize exercise recommendations"""
    
    recommendations = list(base_exercise)
    
    lifestyle = user_data.get('lifestyle', {})
    basic_info = user_data.get('basic_info', {})
    
    exercise_level = lifestyle.get('exercise', 'regular')
    age = basic_info.get('age', 30)
    bmi = basic_info.get('bmi', 22)
    
    # Customize based on current activity level
    if exercise_level in ['sedentary', 'none']:
        recommendations.insert(0, "Start with 10-minute walks, gradually increase to 30 minutes daily")
        recommendations.append("Begin with low-impact activities like walking or swimming")
    
    if bmi >= 30:
        recommendations.insert(0, "Focus on low-impact cardio to protect joints (swimming, cycling)")
    
    if age > 50:
        recommendations.append("Include balance and flexibility exercises")
    
    return recommendations[:5]


def personalize_lifestyle_recommendations(base_lifestyle: List[str], user_data: Dict) -> List[str]:
    """Personalize lifestyle recommendations"""
    
    recommendations = list(base_lifestyle)
    
    lifestyle = user_data.get('lifestyle', {})
    
    # Add specific recommendations based on user's current habits
    if lifestyle.get('smoking', False):
        recommendations.insert(0, "PRIORITY: Quit smoking - seek cessation support immediately")
    
    stress_level = lifestyle.get('stress_level', 'low')
    if stress_level in ['high', 'severe']:
        recommendations.insert(0, "Implement daily stress management (meditation, yoga, breathing exercises)")
    
    sleep_hours = lifestyle.get('sleep_hours', 7)
    if sleep_hours < 6:
        recommendations.append(f"Increase sleep from {sleep_hours} to 7-8 hours nightly")
    
    alcohol = lifestyle.get('alcohol', 'none')
    if alcohol in ['heavy', 'frequent']:
        recommendations.insert(1, "Reduce alcohol consumption significantly")
    
    return recommendations[:6]


def get_monitoring_recommendations(disease_id: str, risk_class: str) -> List[str]:
    """Get monitoring recommendations"""
    
    monitoring = {
        'type2_diabetes': [
            "Monitor blood sugar if at high risk",
            "Track weight weekly",
            "Keep food diary for 2 weeks",
            "Note any unusual thirst or fatigue"
        ],
        'cad': [
            "Monitor blood pressure weekly",
            "Track any chest discomfort or unusual fatigue",
            "Log exercise tolerance",
            "Note family history changes"
        ],
        'hypertension': [
            "Home blood pressure monitoring 2-3x weekly",
            "Track sodium intake",
            "Monitor headaches or dizziness",
            "Keep stress journal"
        ],
        'breast_ovarian_cancer': [
            "Monthly breast self-examination",
            "Track any breast changes or lumps",
            "Note family diagnoses",
            "Monitor menstrual irregularities"
        ]
    }
    
    default = [
        "Regular self-monitoring of symptoms",
        "Track relevant health metrics",
        "Note any concerning changes",
        "Maintain health diary"
    ]
    
    recommendations = monitoring.get(disease_id, default)
    
    # Add frequency based on risk class
    if risk_class in ['III', 'IV']:
        recommendations.insert(0, "Weekly health metric tracking essential")
    
    return recommendations[:5]


def get_action_timeline(risk_class: str) -> Dict[str, str]:
    """Get recommended action timeline"""
    
    timelines = {
        'I': {
            'immediate': 'Continue current habits',
            'this_month': 'Schedule annual checkup if due',
            'this_quarter': 'Review and maintain preventive measures',
            'this_year': 'Annual comprehensive health screening'
        },
        'II': {
            'immediate': 'Begin lifestyle modifications today',
            'this_month': 'Schedule screening tests',
            'this_quarter': 'Follow up with healthcare provider',
            'this_year': 'Comprehensive health assessment and monitoring'
        },
        'III': {
            'immediate': 'Start prevention plan immediately',
            'this_week': 'Schedule doctor consultation',
            'this_month': 'Complete recommended tests, begin interventions',
            'this_quarter': 'Regular monitoring and follow-ups'
        },
        'IV': {
            'immediate': 'Contact healthcare provider urgently',
            'this_week': 'Medical consultation and comprehensive testing',
            'this_month': 'Aggressive treatment/prevention plan in place',
            'ongoing': 'Frequent monitoring and professional oversight'
        }
    }
    
    return timelines.get(risk_class, timelines['II'])