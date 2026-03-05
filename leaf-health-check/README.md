# 🍃 Leaf Health Check

**Intelligent AI-Powered Plant Disease Detection System**

Leaf Health Check is a Streamlit-based web application that analyzes plant leaf health using artificial intelligence and advanced image processing. Upload an image of a plant leaf, and the system will automatically detect diseases, calculate damage severity, and provide personalized treatment recommendations.

---

## ✨ Features

### 🖼️ **Image Upload & Processing**
- Upload plant leaf images in multiple formats (PNG, JPG, JPEG, WebP, BMP)
- Automatic image preprocessing with enhanced clarity
- Noise reduction and brightness optimization

### 🔍 **Damage Detection**
- Advanced color-based analysis to detect:
  - Yellow spots (fungal infections, nutrient deficiency)
  - Brown spots (necrosis, tissue death)
  - Dark patches (severe damage)
- Calculates precise damage percentage of leaf area

### 🤖 **AI-Powered Diagnosis**
- Google Gemini AI integration for intelligent disease identification
- Provides disease name, explanation, and confidence
- Falls back to mock diagnosis when API unavailable
- Analyzes damage patterns alongside visual inspection

### 📊 **Severity Classification**
Automatically classifies leaf condition:
- **Healthy** (0–5% damage) ✅
- **Mild** (5–20% damage) ⚠️
- **Moderate** (20–40% damage) 🟠
- **Severe** (40–70% damage) 🔴
- **Dying** (70%+ damage) 💀

### 💡 **Smart Recommendations**
- Three personalized treatment/rescue tips
- Condition-specific care instructions
- Prevention and care tips
- Early intervention strategies

### 💾 **Result Export**
- Download analysis results as **TXT** file
- Download analysis results as **JSON** file
- Timestamped reports for record-keeping
- Easy reference and sharing

### 🧪 **Test Mode**
- Generate synthetic test images for demo
- Test the system without real leaf images
- Understand system behavior

---

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| **Python 3.8+** | Core language |
| **Streamlit** | Web UI framework |
| **Google Gemini AI** | AI diagnosis |
| **OpenCV** | Image processing |
| **NumPy** | Numerical operations |
| **Pillow (PIL)** | Image handling |
| **TensorFlow** | ML framework (optional) |

---

## 📁 Project Structure

```
leaf-health-check/
├── app.py                 # Main Streamlit application
├── utils.py              # Image processing utilities
├── model.py              # AI analysis model
├── requirements.txt      # Project dependencies
├── README.md             # This file
│
├── dataset/
│   ├── healthy/          # Healthy leaf samples
│   ├── mild/             # Mildly affected samples
│   ├── moderate/         # Moderately affected samples
│   └── severe/           # Severely affected samples
│
└── assets/
    └── sample_leaf.jpg   # Sample image for testing
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Google Gemini API key (optional, for AI diagnosis)

### Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd leaf-health-check
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables (optional):**
   ```bash
   # Create a .env file in the project root
   echo "GEMINI_API_KEY=your_api_key_here" > .env
   ```

### Running the Application

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

---

## 📖 How to Use

### Step 1: Home Page
- Read the introduction and features
- Understand how the system works
- See supported image formats

### Step 2: Go to Analysis Tab
- Click the "📊 Analysis" tab
- Upload a clear image of a plant leaf

### Step 3: Configure Settings (Optional)
- Enable/disable image enhancement
- Show/hide damage visualization
- Add Gemini API key for AI diagnosis

### Step 4: Analyze
- Click the "🚀 Analyze Leaf" button
- Wait for the analysis to complete

### Step 5: View Results
- See damage percentage
- Check severity classification
- Read AI diagnosis
- Review treatment recommendations
- View damage visualization

### Step 6: Export
- Download results as TXT or JSON
- Save for future reference
- Share with other plant enthusiasts

---

## 📊 Example Output

### Sample Analysis Result:

```
=====================================
LEAF HEALTH ANALYSIS REPORT
=====================================

DAMAGE ASSESSMENT:
- Damage Percentage: 32.45%
- Severity Level: Moderate

DIAGNOSIS:
Disease Identified: Fungal Leaf Spot
The leaf shows signs of a fungal infection with 
multiple necrotic lesions. This is a common 
condition in humid environments.

RESCUE RECOMMENDATIONS:
1. Remove heavily affected leaves to reduce disease spread
2. Apply fungicide treatment according to product instructions
3. Improve air circulation and reduce leaf wetness
=====================================
```

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# Google Gemini API Configuration
GEMINI_API_KEY=your_actual_api_key_here

# Optional: Other configurations
DEBUG=false
```

### Image Preprocessing Settings (in utils.py)

You can customize preprocessing parameters:
- **Image size:** Default 224x224 pixels
- **Brightness enhancement:** Alpha=1.2, Beta=30
- **Noise filter:** Bilateral filter with radius 9

### Severity Thresholds (in model.py)

Customize damage percentage thresholds:
```python
SEVERITY_THRESHOLDS = {
    'healthy': (0, 5),
    'mild': (5, 20),
    'moderate': (20, 40),
    'severe': (40, 70),
    'dying': (70, 100)
}
```

---

## 🎯 Key Functions

### Image Processing (utils.py)

| Function | Purpose |
|---|---|
| `preprocess_image()` | Complete preprocessing pipeline |
| `resize_image()` | Resize to standard dimensions |
| `convert_to_rgb()` | Ensure RGB color space |
| `remove_noise()` | Apply denoising filters |
| `enhance_brightness()` | Improve image clarity |
| `detect_damaged_areas()` | Find diseased regions |
| `visualize_damage()` | Create overlay visualization |

### Analysis (model.py)

| Class/Function | Purpose |
|---|---|
| `LeafHealthAnalyzer` | Main analysis class |
| `classify_severity()` | Determine damage severity |
| `analyze_leaf()` | Complete analysis pipeline |
| `get_diagnosis_from_gemini()` | AI diagnosis request |

---

## 🤖 AI Integration

### Using Google Gemini API

1. **Get API Key:**
   - Visit [Google AI Studio](https://aistudio.google.com)
   - Click "Create API Key"
   - Copy your API key

2. **Configure in App:**
   - Option A: Enter in sidebar when prompted
   - Option B: Set environment variable `GEMINI_API_KEY`
   - Option C: Paste in `.env` file

3. **Benefits:**
   - More accurate disease identification
   - Detailed explanations
   - Personalized recommendations

### Fallback Mode

If Gemini API is unavailable:
- System uses mock diagnosis
- Still provides severity classification
- Still offers treatment recommendations
- Completely functional without API

---

## ⚠️ Error Handling

The application handles:
- ✅ Missing image upload
- ✅ Invalid image formats
- ✅ Corrupted image files
- ✅ API connection errors
- ✅ Invalid API keys
- ✅ Memory constraints with large images

---

## 📊 Dataset Structure

The `dataset/` folder is organized by condition:

```
dataset/
├── healthy/      # 0-5% damage
├── mild/         # 5-20% damage
├── moderate/     # 20-40% damage
└── severe/       # 40-70% damage
```

You can populate these folders with leaf images for training purposes.

---

## 🧪 Testing

### Test Mode Features

1. **Generate Synthetic Images:**
   - Click "🧪 Test Mode" tab
   - Generate synthetic leaf images
   - Test analysis without real images

2. **Sample Images:**
   - Use `assets/sample_leaf.jpg`
   - Or add your own test images

3. **Unit Testing:**
   - Test individual functions
   - Verify image processing
   - Validate damage detection

---

## 🐛 Troubleshooting

### Issue: API Key Not Working
**Solution:**
- Verify API key is correct
- Check internet connection
- Ensure Gemini API is enabled in Google Cloud

### Issue: Image Not Uploading
**Solution:**
- Check file format (PNG, JPG, JPEG, WebP, BMP)
- Ensure file size is reasonable (<10MB)
- Re-upload the file

### Issue: Slow Analysis
**Solution:**
- Reduce image size
- Check CPU/RAM availability
- Close other applications

### Issue: Poor Damage Detection
**Solution:**
- Ensure good lighting in image
- Use clear, focused photos
- Upload images from multiple angles

---

## 📚 Code Documentation

All major functions include:
- **Docstrings** explaining purpose
- **Parameter descriptions** with types
- **Return value documentation**
- **Usage examples** in comments

Example:
```python
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
```

---

## 🔐 Security & Privacy

- ✅ All processing is local (except API calls)
- ✅ No image storage on server
- ✅ No tracking or analytics
- ✅ API key not logged
- ✅ HTTPS for API calls

---

## 🚀 Performance

- **Average Analysis Time:** 2-5 seconds
- **Supported Image Sizes:** Up to 4096x4096 pixels
- **Memory Usage:** ~200-500 MB
- **CPU Requirements:** Modern processor recommended

---

## 📝 Future Enhancements

- [ ] Multiple image upload
- [ ] Batch processing
- [ ] Disease history tracking
- [ ] Plant type specific analysis
- [ ] Mobile app version
- [ ] Cloud storage integration
- [ ] Real-time camera feed
- [ ] Advanced ML models

---

## 📄 License

This project is open-source and available for educational and commercial use.

---

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

---

## 📞 Support

For issues, questions, or suggestions:
- Check the troubleshooting section
- Review code comments
- Check error messages
- Test with sample images

---

## 🙏 Acknowledgments

- Streamlit for the amazing web framework
- Google for Gemini AI
- OpenCV community
- Plant disease research community

---

## 📖 Resources

- [Streamlit Documentation](https://docs.streamlit.io)
- [Google Gemini API](https://ai.google.dev)
- [OpenCV Documentation](https://docs.opencv.org)
- [Plant Disease Detection Research](https://plantvillage.psu.edu)

---

**Happy Leaf Analyzing! 🍃**

*Last Updated: 2024*
*Version: 1.0.0*
