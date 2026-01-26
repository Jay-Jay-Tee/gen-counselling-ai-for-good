"""
Risk class assignment logic
Converts probability scores to Risk Class I, II, III, or IV
"""


def get_risk_class(probability: float) -> str:
    """
    Assign risk class based on probability
    
    Args:
        probability: Risk probability (0.0 to 1.0)
    
    Returns:
        Risk class: 'I', 'II', 'III', or 'IV'
    
    Thresholds:
        I:   0.00 - 0.30 (Low)
        II:  0.30 - 0.55 (Moderate)
        III: 0.55 - 0.75 (High)
        IV:  0.75 - 1.00 (Very High)
    """
    
    if probability < 0.30:
        return 'I'
    elif probability < 0.55:
        return 'II'
    elif probability < 0.75:
        return 'III'
    else:
        return 'IV'


def get_risk_class_info(risk_class: str) -> dict:
    """
    Get detailed information about a risk class
    
    Args:
        risk_class: 'I', 'II', 'III', or 'IV'
    
    Returns:
        Dictionary with label, description, color, and guidance
    """
    
    risk_classes = {
        'I': {
            'label': 'Low Risk',
            'description': 'Minimal genetic or lifestyle risk detected',
            'color': '#22c55e',
            'action': 'Maintain healthy habits and routine checkups'
        },
        'II': {
            'label': 'Moderate Risk',
            'description': 'Some risk factors present, preventive action advised',
            'color': '#eab308',
            'action': 'Lifestyle modifications and screening recommended'
        },
        'III': {
            'label': 'High Risk',
            'description': 'Significant risk factors detected, early action needed',
            'color': '#f97316',
            'action': 'Immediate lifestyle changes and medical consultation advised'
        },
        'IV': {
            'label': 'Very High Risk',
            'description': 'Critical risk level, urgent medical attention required',
            'color': '#ef4444',
            'action': 'Urgent medical consultation and comprehensive testing required'
        }
    }
    
    return risk_classes.get(risk_class, risk_classes['I'])


def get_all_risk_classes() -> dict:
    """
    Return all risk class definitions
    Used for legend/documentation in UI
    """
    return {
        'I': get_risk_class_info('I'),
        'II': get_risk_class_info('II'),
        'III': get_risk_class_info('III'),
        'IV': get_risk_class_info('IV')
    }