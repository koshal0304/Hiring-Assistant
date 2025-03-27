# 🚀 TalentScout AI Hiring Assistant

## Overview

TalentScout is an innovative AI-powered hiring assistant that streamlines the initial candidate screening process. Leveraging Google's Generative AI, this Streamlit application provides an intelligent, privacy-focused approach to collecting candidate information and conducting technical assessments.

<img width="1432" alt="Screenshot 2025-03-27 at 5 02 27 PM" src="https://github.com/user-attachments/assets/08269610-8efc-4154-99a1-9d56d043a8a7" />


## 🌟 Key Features

- **Intelligent Conversation Flow**: Guided interaction to collect candidate details
- **Dynamic Technical Assessment**: Generates tech-stack specific interview questions
- **Data Privacy**: Advanced anonymization and secure data handling
- **Flexible Tech Stack Support**: Adapts to various programming languages, frameworks, and tools
- **Modern UI/UX**: Sleek, responsive design with Lottie animations

## 🛠 Technologies Used

- Python
- Streamlit
- Google Generative AI (Gemini)
- Data Privacy Techniques
  - SHA-256 Hashing
  - Secure Token Generation
- Custom CSS Styling
- Lottie Animations

## 🔧 Prerequisites

- Python 3.8+
- Google AI API Key
- Required Python Packages:
  - streamlit
  - google-generativeai
  - requests
  - streamlit-lottie

## 🚦 Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/Hiring-Assistan.git
cd Hiring-Assistan
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up Google AI API Key:
- Replace `GOOGLE_API_KEY` in the script with your actual Google AI API key
- Ensure you have API access from Google AI Studio

## 🏃 Running the Application

```bash
streamlit run main.py
```

## 🔒 Privacy & Security

TalentScout prioritizes candidate data protection:
- All sensitive information is hashed
- Unique anonymized identifiers generated
- Secure, timestamped JSON storage
- Compliance with data privacy standards

## 📋 Conversation Flow

1. Collect Personal Information
   - Full Name
   - Email
   - Phone Number
   - Years of Experience
   - Desired Positions
   - Current Location
   - Tech Stack

2. Generate Tech-Specific Questions
   - Dynamically created based on candidate's technologies
   - Assess practical knowledge
   - Evaluate problem-solving skills

3. Technical Assessment
   - 5 adaptive technical questions
   - Captures candidate's depth of understanding



## 🎯 Future Roadmap

- [ ] Multi-language support
- [ ] Enhanced AI assessment capabilities
- [ ] Integration with ATS systems
- [ ] Advanced analytics dashboard
- [ ] Machine learning-based candidate scoring

