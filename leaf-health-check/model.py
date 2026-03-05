"""
Leaf health analysis model and AI integration.
Handles severity classification and Gemini API integration for diagnosis.
"""

import os
import json
from typing import Dict, Tuple, List
import google.generativeai as genai


class LeafHealthAnalyzer:
    """
    Main analyzer class for leaf health assessment.
    Classifies damage severity and provides AI-based diagnosis.
    """
    
    # Severity classification thresholds
    SEVERITY_THRESHOLDS = {
        'healthy': (0, 5),
        'mild': (5, 20),
        'moderate': (20, 40),
        'severe': (40, 70),
        'dying': (70, 100)
    }
    
    # Severity colors for visualization
    SEVERITY_COLORS = {
        'healthy': (0, 255, 0),      # Green
        'mild': (255, 255, 0),       # Yellow
        'moderate': (255, 165, 0),   # Orange
        'severe': (255, 69, 0),      # Red-Orange
        'dying': (139, 0, 0)         # Dark Red
    }
    
    def __init__(self, use_gemini=True, api_key=None):
        """
        Initialize the leaf health analyzer.
        
        Args:
            use_gemini: Whether to use Gemini API for diagnosis
            api_key: Google Generative AI API key
        """
        self.use_gemini = use_gemini
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        
        # Configure Gemini API if key is provided
        if self.use_gemini and self.api_key:
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel('gemini-pro-vision')
            except Exception as e:
                print(f"Warning: Could not initialize Gemini API: {e}")
                self.use_gemini = False
    
    def classify_severity(self, damage_percentage: float) -> str:
        """
        Classify the severity level of leaf damage.
        
        Args:
            damage_percentage: Percentage of leaf area damaged (0-100)
        
        Returns:
            Severity level string
        """
        for severity, (lower, upper) in self.SEVERITY_THRESHOLDS.items():
            if lower <= damage_percentage < upper:
                return severity
        
        # Default to dying if damage > 100% (shouldn't happen, but safe)
        return 'dying'
    
    def get_severity_description(self, severity: str) -> str:
        """
        Get human-readable description of severity level.
        
        Args:
            severity: Severity level string
        
        Returns:
            Description of the severity
        """
        descriptions = {
            'healthy': 'The leaf appears to be in excellent condition with minimal or no damage.',
            'mild': 'The leaf shows early signs of disease or stress. Minor intervention recommended.',
            'moderate': 'The leaf is moderately affected. Treatment is recommended to prevent further spread.',
            'severe': 'The leaf is heavily damaged. Immediate action required to save the plant.',
            'dying': 'The leaf is critically damaged. The plant may not recover without urgent care.'
        }
        return descriptions.get(severity, 'Unknown condition')
    
    def analyze_with_mock_diagnosis(self, damage_percentage: float, severity: str) -> Dict:
        """
        Generate mock diagnosis when Gemini API is not available.
        
        Args:
            damage_percentage: Percentage of damage detected
            severity: Severity level classification
        
        Returns:
            Dictionary with disease info and tips
        """
        # Mock diagnosis based on severity
        mock_diagnoses = {
            'healthy': {
                'disease_name': 'No Disease Detected',
                'explanation': 'The leaf shows no signs of disease or stress.',
                'tips': [
                    'Continue regular watering with proper drainage',
                    'Maintain optimal sunlight exposure for your plant type',
                    'Monitor for any changes in leaf appearance'
                ]
            },
            'mild': {
                'disease_name': 'Early Leaf Spot / Minor Stress',
                'explanation': 'The leaf shows early signs of fungal infection or nutrient deficiency.',
                'tips': [
                    'Remove affected leaves if they worsen',
                    'Improve air circulation around the plant',
                    'Apply balanced fertilizer to strengthen the plant'
                ]
            },
            'moderate': {
                'disease_name': 'Fungal Disease / Significant Stress',
                'explanation': 'The leaf is affected by fungal infection or environmental stress.',
                'tips': [
                    'Apply fungicide according to product instructions',
                    'Remove heavily affected leaves to prevent spread',
                    'Adjust watering schedule - avoid wetting foliage'
                ]
            },
            'severe': {
                'disease_name': 'Advanced Fungal/Bacterial Disease',
                'explanation': 'The leaf shows signs of advanced disease that requires immediate treatment.',
                'tips': [
                    'Remove the affected leaf entirely to prevent contagion',
                    'Treat the plant with systemic fungicide',
                    'Isolate the plant and improve growing conditions'
                ]
            },
            'dying': {
                'disease_name': 'Critical Condition',
                'explanation': 'The leaf is in critical condition with severe disease or damage.',
                'tips': [
                    'Remove ALL affected leaves immediately',
                    'Apply intensive fungicide treatment',
                    'Consider professional plant care consultation'
                ]
            }
        }
        
        return mock_diagnoses.get(severity, mock_diagnoses['healthy'])
    
    def get_diagnosis_from_gemini(self, image_path: str, damage_percentage: float) -> Dict:
        """
        Get diagnosis from Google Gemini API.
        
        Args:
            image_path: Path to the leaf image
            damage_percentage: Detected damage percentage
        
        Returns:
            Dictionary with disease name, explanation, and tips
        """
        if not self.use_gemini or not self.api_key:
            return None
        
        try:
            # Read and encode the image
            with open(image_path, 'rb') as f:
                image_data = f.read()
            
            # Create prompt for Gemini
            prompt = f"""Analyze this plant leaf image and provide a diagnosis. 
            
Based on visual inspection, I've detected approximately {damage_percentage:.1f}% damage on this leaf.

Please provide:
1. A disease name or condition (e.g., "Powdery Mildew", "Leaf Spot", "Nutrient Deficiency")
2. A brief explanation of what you see (2-3 sentences)
3. Three specific rescue/treatment recommendations

Format your response as JSON:
{{
    "disease_name": "disease name",
    "explanation": "brief explanation",
    "tips": ["tip 1", "tip 2", "tip 3"]
}}
"""
            
            # Call Gemini API
            response = self.model.generate_content([
                {"mime_type": "image/jpeg", "data": image_data},
                prompt
            ])
            
            # Parse response
            response_text = response.text
            
            # Try to extract JSON from response
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            
            if start_idx != -1 and end_idx > start_idx:
                json_str = response_text[start_idx:end_idx]
                result = json.loads(json_str)
                return result
            else:
                # If JSON not found, parse manually
                return self._parse_text_response(response_text)
        
        except Exception as e:
            print(f"Gemini API error: {e}")
            return None
    
    def _parse_text_response(self, response_text: str) -> Dict:
        """
        Parse Gemini response if it's not in JSON format.
        
        Args:
            response_text: Text response from Gemini
        
        Returns:
            Parsed diagnosis dictionary
        """
        # Simple parsing fallback
        lines = response_text.strip().split('\n')
        
        return {
            'disease_name': 'Disease Analysis',
            'explanation': response_text[:200] + '...' if len(response_text) > 200 else response_text,
            'tips': [
                'Monitor the plant closely for changes',
                'Improve environmental conditions',
                'Seek professional plant care advice'
            ]
        }
    
    def analyze_leaf(self, image_path: str = None, damage_percentage: float = None) -> Dict:
        """
        Complete leaf analysis combining damage detection and AI diagnosis.
        
        Args:
            image_path: Path to the leaf image
            damage_percentage: Percentage of damage (if pre-calculated)
        
        Returns:
            Complete analysis dictionary
        """
        if damage_percentage is None:
            damage_percentage = 0
        
        # Ensure percentage is valid
        damage_percentage = max(0, min(100, damage_percentage))
        
        # Classify severity
        severity = self.classify_severity(damage_percentage)
        severity_description = self.get_severity_description(severity)
        
        # Try to get Gemini diagnosis, fall back to mock if unavailable
        if self.use_gemini and image_path:
            diagnosis = self.get_diagnosis_from_gemini(image_path, damage_percentage)
        else:
            diagnosis = None
        
        if diagnosis is None:
            diagnosis = self.analyze_with_mock_diagnosis(damage_percentage, severity)
        
        # Return complete analysis
        return {
            'damage_percentage': round(damage_percentage, 2),
            'severity': severity,
            'severity_description': severity_description,
            'disease_name': diagnosis['disease_name'],
            'explanation': diagnosis['explanation'],
            'tips': diagnosis['tips'],
            'severity_color': self.SEVERITY_COLORS[severity]
        }


def create_analyzer(use_gemini=True, api_key=None) -> LeafHealthAnalyzer:
    """
    Factory function to create a LeafHealthAnalyzer instance.
    
    Args:
        use_gemini: Whether to use Gemini API
        api_key: Gemini API key
    
    Returns:
        LeafHealthAnalyzer instance
    """
    return LeafHealthAnalyzer(use_gemini=use_gemini, api_key=api_key)
