# 🚀 TalentScout AI Hiring Assistant

## Project Overview

TalentScout is an intelligent AI-powered hiring assistant designed to streamline the initial candidate screening process. Leveraging Google's Gemini AI, the application provides an automated, privacy-focused approach to collecting candidate information and conducting technical assessments.

<img width="1430" alt="Screenshot 2025-04-02 at 5 02 16 PM" src="https://github.com/user-attachments/assets/50326bf7-968f-4ebd-9037-816cce167345" />


## Key Capabilities

- Automated candidate information collection
- Dynamic, tech-stack specific technical interview question generation
- Secure data anonymization and privacy protection
- Adaptive conversational interface
- Comprehensive candidate profiling

## Installation Instructions

### 1. Prerequisites

- Python 3.8+
- Google Generative AI API Key
- Pip package manager

### 2. Step-by-Step Setup

#### 1. Clone the repository:
```bash
git clone https://github.com/yourusername/Hiring-Assistant.git
cd Hiring-Assistant
```

#### 2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

#### 3. Install required dependencies:
```bash
pip install -r requirements.txt
```

#### 4. Configure API Key:
- Obtain a Google Generative AI API key from Google AI Studio
- Replace `GOOGLE_API_KEY` in the script with your actual API key

#### 5. Run the application:
```bash
streamlit run app.py
```

## Usage Guide

1. Launch the application
2. Follow the conversational prompts to provide:
   - Personal information
   - Professional experience
   - Technical skills
3. Complete the technical assessment questions
4. Receive a confirmation with an anonymized identifier

## Technical Details

### 1. Libraries and Frameworks
- **Streamlit**: Web application framework
- **Google Generative AI**: AI-powered question generation
- **Hashlib**: Secure data hashing
- **Secrets**: Secure token generation
- **Datetime**: Timestamp management

### 2. Architectural Decisions

 #### 2.1. Privacy-First Design
- Implemented `DataPrivacyManager` to handle sensitive information
- SHA-256 hashing for personal identifiers
- Secure, anonymized data storage
- Dynamic data anonymization techniques

 #### 2.2. AI-Powered Question Generation
- Tech stack-aware prompt engineering
- Adaptive question difficulty
- Comprehensive skill assessment approach

### 3. Model Details
- **AI Model**: Google Gemini 2.0 Flash
- **Prompt Generation Strategy**: Context-aware, technology-specific prompts
- **Safety Settings**: Configured to prevent inappropriate content generation

## Prompt Design Strategy

### 1. Information Gathering Prompts
- Structured, step-by-step conversational flow
- Validation at each stage (email, phone, experience)
- Clear, concise instructions for user input

### 2. Technical Question Generation
1. Analyze candidate's declared tech stack
2. Create context-aware prompts
3. Generate questions testing:
   - Theoretical understanding
   - Practical application
   - Problem-solving skills
   - Conceptual depth

### 3. Example Prompt Structure
```python
prompt = f"""
Generate technical questions for a candidate with: {tech_stack}

Guidelines:
1. Test practical understanding
2. Avoid yes/no questions
3. Focus on problem-solving
"""
```

## Challenges & Solutions

### 1. Dynamic Question Generation
**Challenge**: Creating relevant, technology-specific questions
**Solution**: 
- Implemented tech stack categorization
- Used AI to generate adaptive questions
- Fallback mechanism for question generation

### 2. Data Privacy
**Challenge**: Protecting candidate information
**Solution**:
- Implemented anonymization techniques
- Used secure hashing for sensitive data
- Created unique, non-reversible identifiers

### 3. Conversational Flow Management
**Challenge**: Maintaining context across conversation stages
**Solution**:
- State machine approach in conversation management
- Clear stage transitions
- Error handling for unexpected inputs

## Future Roadmap
- [ ] Multi-language support
- [ ] Advanced candidate scoring
- [ ] ATS (Applicant Tracking System) integration
- [ ] Enhanced AI assessment capabilities

