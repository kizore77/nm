"""
Utility functions for leaf health check system.
Handles image preprocessing and color-based damage detection.
"""

import cv2
import numpy as np
from PIL import Image
from io import BytesIO


def resize_image(image, target_size=(224, 224)):
    """
    Resize image to a standard size for analysis.
    
    Args:
        image: Input image (numpy array or PIL Image)
        target_size: Target dimensions (width, height)
    
    Returns:
        Resized image as numpy array
    """
    if isinstance(image, Image.Image):
        image = np.array(image)
    
    # Resize using OpenCV
    resized = cv2.resize(image, target_size)
    return resized


def normalize_pixels(image):
    """
    Normalize pixel values to 0-1 range.
    
    Args:
        image: Input image (numpy array)
    
    Returns:
        Normalized image
    """
    # Convert to float and normalize to 0-1
    normalized = image.astype(np.float32) / 255.0
    return normalized


def convert_to_rgb(image):
    """
    Convert image to RGB format.
    
    Args:
        image: Input image (may be BGR from OpenCV or PIL)
    
    Returns:
        RGB image as numpy array
    """
    if isinstance(image, Image.Image):
        if image.mode != 'RGB':
            image = image.convert('RGB')
        return np.array(image)
    
    # If it's a numpy array, assume BGR and convert to RGB
    if len(image.shape) == 3 and image.shape[2] == 3:
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return image_rgb
    
    return image


def remove_noise(image):
    """
    Apply bilateral filter to remove noise while preserving edges.
    
    Args:
        image: Input image (numpy array)
    
    Returns:
        Denoised image
    """
    # Apply bilateral filter for edge-preserving smoothing
    if len(image.shape) == 3:
        denoised = cv2.bilateralFilter(image, 9, 75, 75)
    else:
        denoised = cv2.bilateralFilter(image, 9, 75, 75)
    
    return denoised


def enhance_brightness(image, alpha=1.2, beta=30):
    """
    Enhance image brightness and contrast.
    Formula: output = alpha * image + beta
    
    Args:
        image: Input image (numpy array)
        alpha: Contrast factor (1.2 adds 20% more contrast)
        beta: Brightness offset
    
    Returns:
        Enhanced image
    """
    # Ensure image is in correct format
    if image.dtype == np.float32:
        image = (image * 255).astype(np.uint8)
    
    # Apply brightness/contrast enhancement
    enhanced = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
    
    return enhanced


def detect_damaged_areas(image):
    """
    Detect discolored/damaged areas in the leaf using HSV color space.
    
    Looks for:
    - Yellow spots (disease indicators)
    - Brown spots (necrosis)
    - Dark patches (severe damage)
    
    Args:
        image: Input RGB image (numpy array)
    
    Returns:
        Damage mask and damage percentage
    """
    # Convert to HSV color space for better disease detection
    image_rgb = image if image.dtype == np.uint8 else (image * 255).astype(np.uint8)
    hsv = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2HSV)
    
    # Initialize damage mask
    damage_mask = np.zeros(image_rgb.shape[:2], dtype=np.uint8)
    
    # Detect yellow spots (H: 15-35, saturation varies)
    lower_yellow = np.array([15, 40, 40])
    upper_yellow = np.array([35, 255, 255])
    yellow_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    damage_mask += yellow_mask
    
    # Detect brown spots (H: 10-25, low saturation, medium value)
    lower_brown = np.array([10, 30, 50])
    upper_brown = np.array([25, 200, 200])
    brown_mask = cv2.inRange(hsv, lower_brown, upper_brown)
    damage_mask += brown_mask
    
    # Detect dark patches (low value, any hue/saturation)
    lower_dark = np.array([0, 0, 0])
    upper_dark = np.array([180, 255, 60])
    dark_mask = cv2.inRange(hsv, lower_dark, upper_dark)
    damage_mask += dark_mask
    
    # Normalize damage mask
    damage_mask = np.clip(damage_mask, 0, 255).astype(np.uint8)
    
    # Apply morphological operations to reduce noise
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    damage_mask = cv2.morphologyEx(damage_mask, cv2.MORPH_CLOSE, kernel)
    damage_mask = cv2.morphologyEx(damage_mask, cv2.MORPH_OPEN, kernel)
    
    # Calculate damage percentage
    total_pixels = damage_mask.size
    damaged_pixels = np.count_nonzero(damage_mask)
    damage_percentage = (damaged_pixels / total_pixels) * 100
    
    return damage_mask, damage_percentage


def preprocess_image(image_input):
    """
    Complete preprocessing pipeline for leaf images.
    
    Steps:
    1. Load and convert to RGB
    2. Resize to standard size
    3. Remove noise
    4. Enhance brightness
    5. Normalize pixels
    
    Args:
        image_input: Can be file path, PIL Image, or numpy array
    
    Returns:
        Preprocessed image (numpy array)
    """
    # Load image if it's a file path
    if isinstance(image_input, str):
        image = cv2.imread(image_input)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    elif isinstance(image_input, Image.Image):
        image = np.array(image_input)
    else:
        image = image_input
    
    # Ensure we're working with RGB
    if len(image.shape) == 2:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    elif image.shape[2] == 4:  # RGBA
        image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)
    
    # Preprocessing pipeline
    image = resize_image(image, target_size=(224, 224))
    image = remove_noise(image)
    image = enhance_brightness(image, alpha=1.2, beta=30)
    image = normalize_pixels(image)
    
    return image


def visualize_damage(original_image, damage_mask):
    """
    Create visualization of damage on the original image.
    
    Args:
        original_image: Original RGB image (numpy array)
        damage_mask: Binary mask of damaged areas
    
    Returns:
        Overlay image showing detected damage in red
    """
    # Ensure original image is uint8
    if original_image.dtype == np.float32:
        original_image = (original_image * 255).astype(np.uint8)
    
    # Copy original image
    overlay = original_image.copy()
    
    # Convert damage mask to 3-channel
    damage_mask_3ch = cv2.cvtColor(damage_mask, cv2.COLOR_GRAY2RGB)
    
    # Create red overlay for damaged areas
    overlay[damage_mask > 0] = [255, 0, 0]
    
    # Blend original with overlay
    blended = cv2.addWeighted(original_image, 0.7, overlay, 0.3, 0)
    
    return blended.astype(np.uint8)


def load_image_from_bytes(uploaded_file):
    """
    Load image from uploaded file (Streamlit upload object).
    
    Args:
        uploaded_file: Streamlit UploadedFile object
    
    Returns:
        PIL Image object
    """
    image = Image.open(uploaded_file)
    return image


def save_results(damage_percentage, severity, diagnosis, tips, format='txt'):
    """
    Format analysis results for export.
    
    Args:
        damage_percentage: Float representing damage percentage
        severity: String indicating severity level
        diagnosis: String with disease diagnosis
        tips: List of 3 rescue tips
        format: 'txt' or 'json'
    
    Returns:
        Formatted string or JSON data
    """
    if format == 'txt':
        result = f"""
=====================================
LEAF HEALTH ANALYSIS REPORT
=====================================

DAMAGE ASSESSMENT:
- Damage Percentage: {damage_percentage:.2f}%
- Severity Level: {severity}

DIAGNOSIS:
{diagnosis}

RESCUE RECOMMENDATIONS:
"""
        for i, tip in enumerate(tips, 1):
            result += f"{i}. {tip}\n"
        
        result += "\n====================================="
        return result
    
    elif format == 'json':
        import json
        data = {
            "damage_percentage": round(damage_percentage, 2),
            "severity_level": severity,
            "diagnosis": diagnosis,
            "rescue_tips": tips
        }
        return json.dumps(data, indent=2)
    
    return ""
