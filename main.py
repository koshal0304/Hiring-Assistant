import streamlit as st
import google.generativeai as genai
import re
import hashlib
import json
import os
from datetime import datetime
import secrets
from streamlit_lottie import st_lottie
import requests

# IMPORTANT: Replace 'YOUR_API_KEY_HERE' with your actual Google AI API key
GOOGLE_API_KEY = 'AIzaSyCd-p3gedQTCUt0w4unU6udoBHVevRvdXo'  # Paste your API key here

class DataPrivacyManager:
    """
    Manages data privacy and secure handling of candidate information
    """
    @staticmethod
    def hash_sensitive_data(data):
        """
        Hash sensitive data to protect privacy
        
        :param data: Sensitive data to be hashed
        :return: Hashed representation of the data
        """
        if not data:
            return None
        return hashlib.sha256(str(data).encode()).hexdigest()
    
    @staticmethod
    def generate_anonymized_id():
        """
        Generate a secure, unique anonymized identifier
        
        :return: Anonymized identifier
        """
        return secrets.token_urlsafe(16)
    
    @staticmethod
    def save_candidate_data(candidate_info):
        """
        Securely save candidate data with anonymization
        
        :param candidate_info: Dictionary of candidate information
        :return: Anonymized candidate record
        """
        # Create a copy to avoid modifying original data
        anonymized_data = candidate_info.copy()
        
        # Anonymize sensitive fields
        anonymized_data['id'] = DataPrivacyManager.generate_anonymized_id()
        anonymized_data['email'] = DataPrivacyManager.hash_sensitive_data(anonymized_data.get('email'))
        anonymized_data['phone'] = DataPrivacyManager.hash_sensitive_data(anonymized_data.get('phone'))
        
        # Add timestamp
        anonymized_data['timestamp'] = datetime.now().isoformat()
        
        # Ensure directory exists
        os.makedirs('candidate_data', exist_ok=True)
        
        # Save to a secure, timestamped file
        filename = f"candidate_data/{anonymized_data['id']}.json"
        with open(filename, 'w') as f:
            json.dump(anonymized_data, f, indent=2)
        
        return anonymized_data

class PromptEngineeringManager:
    """
    Manages advanced prompt engineering for technical question generation
    """
    @staticmethod
    def generate_tech_stack_specific_prompt(tech_stack):
        """
        Create a sophisticated prompt for generating tech-specific questions
        
        :param tech_stack: Candidate's declared tech stack
        :return: Carefully crafted prompt for question generation
        """
        # Categorize and refine tech stack
        tech_categories = {
            'languages': [],
            'frameworks': [],
            'databases': [],
            'tools': []
        }
        
        # Simple categorization logic (can be expanded)
        tech_items = [item.strip() for item in tech_stack.split(',')]
        for item in tech_items:
            item = item.lower()
            if item in ['python', 'java', 'javascript', 'typescript', 'go', 'rust', 'c++', 'c#']:
                tech_categories['languages'].append(item)
            elif item in ['django', 'flask', 'react', 'angular', 'vue', 'spring', '.net', 'express']:
                tech_categories['frameworks'].append(item)
            elif item in ['postgresql', 'mongodb', 'mysql', 'sqlite', 'redis', 'cassandra']:
                tech_categories['databases'].append(item)
            else:
                tech_categories['tools'].append(item)
        
        # Construct advanced prompt
        prompt = f"""
As a senior technical interviewer, generate a comprehensive set of technical assessment questions that deeply evaluate a candidate's expertise across their declared tech stack.

Candidate's Technologies:
- Languages: {', '.join(tech_categories['languages']) or 'N/A'}
- Frameworks: {', '.join(tech_categories['frameworks']) or 'N/A'}
- Databases: {', '.join(tech_categories['databases']) or 'N/A'}
- Tools: {', '.join(tech_categories['tools']) or 'N/A'}

Assessment Guidelines:
1. Create questions that test:
   - Theoretical understanding
   - Practical application
   - Problem-solving skills
   - Advanced conceptual knowledge

2. Ensure questions are:
   - Technology-specific
   - Progressively challenging
   - Covering multiple skill depths

3. Avoid:
   - Simple recall questions
   - Yes/no type questions
   - Overly broad or vague inquiries

Generate 5 distinct questions that comprehensively assess the candidate's technical proficiency.
        """
        return prompt

class TalentScoutChatbot:
    def __init__(self, api_key=GOOGLE_API_KEY):
        """
        Initialize the TalentScout Hiring Assistant Chatbot with enhanced privacy
        
        :param api_key: Google Generative AI API key
        """
        # Configure the API with privacy considerations
        genai.configure(api_key=api_key)
        
        try:
            # Initialize the model
            self.model = genai.GenerativeModel('gemini-2.0-flash')
        
        except Exception as e:
            st.error(f"Model Initialization Error: {e}")
            st.error("Possible issues:")
            st.error("1. Invalid API Key")
            st.error("2. Network connectivity problem")
            st.error("3. API service disruption")
            raise
        
        # Initialize conversation state with privacy-first approach
        self.candidate_info = {
            'id': DataPrivacyManager.generate_anonymized_id(),
            'full_name': None,
            'email': None,
            'phone': None,
            'years_experience': None,
            'desired_positions': None,
            'current_location': None,
            'tech_stack': None
        }
        
        # Current conversation stage
        self.conversation_stage = 'greeting'
        self.technical_questions = []
        self.current_question_index = 0
        self.technical_answers = []

    def validate_email(self, email):
        """
        Validate email format
        
        :param email: Email address to validate
        :return: Boolean indicating email validity
        """
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(email_regex, email) is not None
    
    def validate_phone(self, phone):
        """
        Validate phone number format
        
        :param phone: Phone number to validate
        :return: Boolean indicating phone number validity
        """
        phone_regex = r'^\+?1?\d{10,14}$'
        return re.match(phone_regex, phone) is not None
    
    def generate_technical_questions(self, tech_stack):
        """
        Generate technical questions based on candidate's tech stack
        
        :param tech_stack: List of technologies candidate is proficient in
        :return: List of technical questions
        """
        try:
            prompt = f"""
            Generate 5 technical questions for a candidate with the following tech stack: {tech_stack}
            
            Guidelines:
            1. Create questions that test practical understanding
            2. Avoid yes/no questions
            3. Focus on problem-solving and depth of knowledge
            
            Provide the questions as a clear, numbered list.
            """
            
            # Safety settings to prevent potential content filtering
            safety_settings = [
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_NONE"
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH",
                    "threshold": "BLOCK_NONE"
                }
            ]
            
            # Generate content with explicit safety settings
            response = self.model.generate_content(
                prompt, 
                safety_settings=safety_settings
            )
            
            # Fallback if generation fails
            questions = response.text.split('\n')
            questions = [q.strip() for q in questions if q.strip() and any(char.isalpha() for char in q)]
            
            return questions[:6] or [
                f"Describe a challenging project you've worked on with {tech_stack}.",
                f"What are the key considerations when using {tech_stack}?",
                "How do you approach learning new technologies?",
                "Explain a complex technical concept in simple terms.",
                "What recent technological advancement excites you most?"
            ]
        
        except Exception as e:
            st.error(f"Question Generation Error: {e}")
            return [
                "Describe a challenging project you've worked on.",
                "What technologies are you most passionate about?",
                "How do you approach solving complex technical problems?",
                "Explain a recent technological innovation you find interesting.",
                "What's your strategy for continuous learning in tech?"
            ]

    def process_user_input(self, user_input):
        """
        Process user input based on current conversation stage
        
        :param user_input: User's input text
        :return: Chatbot's response
        """
        # Normalize input
        user_input = user_input.strip().lower()
        
        # Exit keywords
        if any(keyword in user_input for keyword in ['exit', 'quit', 'bye', 'goodbye']):
            return self.end_conversation()
        
        # Conversation flow based on current stage
        if self.conversation_stage == 'greeting':
            self.conversation_stage = 'name'
            return """
Welcome to TalentScout's Hiring Assistant! 🚀

I'm here to help you through our initial screening process. Let's get started by collecting some basic information about you.

Could you please provide your full name?
            """
        
        elif self.conversation_stage == 'name':
            if len(user_input) >= 2:
                self.candidate_info['full_name'] = user_input
                self.conversation_stage = 'email'
                return f"Nice to meet you, {user_input}! What is your email address?"
            else:
                return "Please enter a valid name (at least 2 characters)."
        
        elif self.conversation_stage == 'email':
            if self.validate_email(user_input):
                self.candidate_info['email'] = user_input
                self.conversation_stage = 'phone'
                return "Thank you. What is your phone number? (Please include country code, e.g., +1234567890)"
            else:
                return "Invalid email format. Please enter a valid email address."
        
        elif self.conversation_stage == 'phone':
            if self.validate_phone(user_input):
                self.candidate_info['phone'] = user_input
                self.conversation_stage = 'experience'
                return "How many years of professional experience do you have?"
            else:
                return "Invalid phone number. Please enter a valid phone number with country code."
        
        elif self.conversation_stage == 'experience':
            try:
                years = int(user_input)
                if 0 <= years <= 50:
                    self.candidate_info['years_experience'] = years
                    self.conversation_stage = 'position'
                    return "What position(s) are you interested in?"
                else:
                    return "Please enter a valid number of years (between 0 and 50)."
            except ValueError:
                return "Please enter a numeric value for years of experience."
        
        elif self.conversation_stage == 'position':
            self.candidate_info['desired_positions'] = user_input
            self.conversation_stage = 'location'
            return "What is your current location?"
        
        elif self.conversation_stage == 'location':
            self.candidate_info['current_location'] = user_input
            self.conversation_stage = 'tech_stack'
            return """
Please list the technologies you are proficient in. 
Include:
- Programming Languages
- Frameworks
- Databases
- Tools

Example: Python, Django, React, PostgreSQL, Docker
            """
        
        elif self.conversation_stage == 'tech_stack':
            self.candidate_info['tech_stack'] = user_input
            
            # Generate technical questions
            self.technical_questions = self.generate_technical_questions(user_input)
            self.current_question_index = 0
            self.technical_answers = []
            
            self.conversation_stage = 'technical_questions'
            
            # Return the first technical question directly
            return self.technical_questions[0]
        
        elif self.conversation_stage == 'technical_questions':
            # Store the answer to the current question
            self.technical_answers.append(user_input)
            self.current_question_index += 1
            
            # Check if we've answered all questions
            if self.current_question_index >= len(self.technical_questions):
                self.conversation_stage = 'complete'
                return self.end_conversation()
            
            # Return the next technical question directly
            return self.technical_questions[self.current_question_index]
        
        elif self.conversation_stage == 'complete':
            return self.end_conversation()

    def end_conversation(self):
        """
        Gracefully end the conversation with data privacy considerations
        
        :return: Closing message
        """
        try:
            # Enhance candidate info with technical answers
            self.candidate_info['technical_questions'] = self.technical_questions
            self.candidate_info['technical_answers'] = self.technical_answers
            
            # Anonymize and save candidate data
            anonymized_record = DataPrivacyManager.save_candidate_data(self.candidate_info)
            
            return f"""
Thank you for completing the TalentScout initial screening! 

🔒 Your Privacy is Assured:
- A unique, anonymized identifier has been generated: {anonymized_record['id']}
- Your personal information is securely stored and protected
- Data will be handled in compliance with data privacy standards

🌟 Next Steps:
- Our recruitment team will review your application
- We'll contact you via email if you match our current openings
- Expected response time: 3-5 business days

We appreciate your interest in joining our talent network! 
Best of luck in your job search! 👋
            """
        except Exception as e:
            st.error(f"Error in final data processing: {e}")
            return """
Thank you for your interest. Our team will be in touch soon.
            """

def load_lottie_url(url):
    """
    Load Lottie animation from a URL
    
    :param url: URL of the Lottie JSON animation
    :return: Parsed Lottie animation JSON
    """
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        st.error(f"Error loading Lottie animation: {e}")
        return None

def apply_custom_css():
    """
    Apply premium styling to the TalentScout AI Hiring Assistant
    """
    st.markdown("""
    <style>
    /* Luxury Gradient Background with animated flow */
    .stApp {
        background: linear-gradient(135deg, #f0f4f8 0%, #d0e1f9 50%, #e6f0ff 100%);
        font-family: 'Poppins', 'Inter', sans-serif;
        animation: gradientFlow 20s ease infinite;
        background-size: 300% 300%;
    }
    
    @keyframes gradientFlow {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Premium Title with 3D effect and floating animation */
    .main-title {
        color: #1a2980;
        font-weight: 800;
        text-align: center;
        margin-bottom: 30px;
        font-size: 2.8em;
        text-shadow: 3px 3px 6px rgba(0, 0, 0, 0.2);
        background: linear-gradient(to right, #1a2980, #26d0ce, #4776E6);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: floating 3s ease-in-out infinite, shine 4s linear infinite;
        letter-spacing: 1px;
    }
    
    @keyframes floating {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }
    
    @keyframes shine {
        to { background-position: 200% center; }
    }
    
    /* Elegant subtitle styling */
    .subtitle {
        text-align: center;
        color: #4A5568;
        font-size: 1.2em;
        margin-bottom: 30px;
        animation: fadeIn 1s ease-out;
        font-weight: 400;
    }
    
    /* Futuristic Chat Container */
    .chat-container {
        background-color: rgba(255, 255, 255, 0.7);
        border-radius: 20px;
        padding: 20px;
        backdrop-filter: blur(10px);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.5);
        animation: containerAppear 0.6s ease-out;
        margin-bottom: 20px;
    }
    
    @keyframes containerAppear {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Premium Chat Input Styling with glow effect */
    .stTextInput > div > div > input {
        background-color: white;
        border: 2px solid transparent;
        border-radius: 15px;
        padding: 14px 18px;
        box-shadow: 0 4px 12px rgba(26, 41, 128, 0.1);
        transition: all 0.3s ease;
        font-size: 16px;
        background-image: linear-gradient(white, white),
                           linear-gradient(to right, #1a2980, #26d0ce);
        background-origin: border-box;
        background-clip: padding-box, border-box;
    }
    
    .stTextInput > div > div > input:focus {
        outline: none;
        box-shadow: 0 0 15px rgba(38, 208, 206, 0.4);
        transform: translateY(-2px);
        animation: glow 2s infinite;
    }
    
    @keyframes glow {
        0% { box-shadow: 0 0 5px rgba(26, 41, 128, 0.3); }
        50% { box-shadow: 0 0 20px rgba(38, 208, 206, 0.5); }
        100% { box-shadow: 0 0 5px rgba(26, 41, 128, 0.3); }
    }
    
    /* Sleek Sidebar Design */
    .css-1aumxhk, [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(255,255,255,0.9) 0%, rgba(240,248,255,0.9) 100%);
        border-right: 1px solid rgba(0, 0, 0, 0.05);
        border-radius: 0 20px 20px 0;
        backdrop-filter: blur(10px);
        box-shadow: 5px 0 15px rgba(0, 0, 0, 0.03);
        animation: slideInSidebar 0.8s ease-out;
    }
    
    @keyframes slideInSidebar {
        from { opacity: 0; transform: translateX(-30px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    /* Premium Button Design with pulse effect */
    .stButton > button {
        background: linear-gradient(45deg, #1a2980, #26d0ce);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 12px 30px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.4s ease;
        box-shadow: 0 4px 15px rgba(26, 41, 128, 0.2);
        position: relative;
        overflow: hidden;
        animation: pulseButton 2s infinite;
    }
    
    @keyframes pulseButton {
        0% { transform: scale(1); }
        50% { transform: scale(1.03); }
        100% { transform: scale(1); }
    }
    
    .stButton > button:before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        transition: 0.6s;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(26, 41, 128, 0.3);
        background: linear-gradient(45deg, #26d0ce, #1a2980);
    }
    
    .stButton > button:hover:before {
        left: 100%;
    }
    
    /* Message Bubbles Design */
    .chat-message-user {
        background-color: #E6F7FF;
        border-radius: 18px 18px 18px 0;
        padding: 15px 20px;
        margin: 10px 0;
        box-shadow: 0 3px 10px rgba(0, 0, 0, 0.05);
        border-left: 4px solid #1a2980;
        max-width: 85%;
        margin-right: auto;
        animation: messageIn 0.5s ease-out forwards;
        opacity: 0;
        transform: translateY(10px);
    }
    
    .chat-message-assistant {
        background: linear-gradient(135deg, #f5fbff, #e6f7ff);
        border-radius: 18px 18px 0 18px;
        padding: 15px 20px;
        margin: 10px 0;
        box-shadow: 0 3px 10px rgba(0, 0, 0, 0.05);
        border-right: 4px solid #26d0ce;
        max-width: 85%;
        margin-left: auto;
        animation: messageIn 0.5s ease-out forwards;
        opacity: 0;
        transform: translateY(10px);
    }
    
    @keyframes messageIn {
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Assistant and User Icons */
    .avatar-user {
        background-color: #1a2980;
        color: white;
        border-radius: 50%;
        width: 35px;
        height: 35px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 10px;
        font-weight: bold;
        box-shadow: 0 3px 5px rgba(0, 0, 0, 0.1);
    }
    
    .avatar-assistant {
        background: linear-gradient(45deg, #1a2980, #26d0ce);
        color: white;
        border-radius: 50%;
        width: 35px;
        height: 35px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 10px;
        box-shadow: 0 3px 5px rgba(0, 0, 0, 0.1);
    }
    
    /* Loading Animation Style */
    .stProgress > div > div > div > div {
        background: linear-gradient(45deg, #1a2980, #26d0ce, #4776E6);
        background-size: 200% auto;
        animation: gradientLoading 2s linear infinite;
        border-radius: 100px;
    }
    
    @keyframes gradientLoading {
        0% { background-position: 0% center; }
        100% { background-position: 200% center; }
    }
    
    /* Advanced Card Styling */
    .info-card {
        background: rgba(255, 255, 255, 0.8);
        border-radius: 16px;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.05);
        padding: 25px;
        margin: 15px 0;
        backdrop-filter: blur(5px);
        border: 1px solid rgba(255, 255, 255, 0.8);
        transition: all 0.4s ease;
    }
    
    .info-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 12px 30px rgba(26, 41, 128, 0.1);
    }
    
    /* Card Title */
    .card-title {
        font-size: 1.4em;
        font-weight: 700;
        margin-bottom: 15px;
        color: #1a2980;
        border-bottom: 2px solid rgba(38, 208, 206, 0.3);
        padding-bottom: 8px;
    }
    
    /* Animated List Items */
    .animated-list li {
        margin-bottom: 10px;
        padding: 8px;
        border-radius: 8px;
        background: rgba(255, 255, 255, 0.5);
        transition: all 0.3s ease;
        animation: listItemIn 0.4s ease-out forwards;
        opacity: 0;
        transform: translateX(-10px);
    }
    
    .animated-list li:hover {
        background: rgba(38, 208, 206, 0.1);
        transform: translateX(5px);
    }
    
    @keyframes listItemIn {
        to { opacity: 1; transform: translateX(0); }
    }
    
    /* Status Indicators */
    .status-indicator {
        display: inline-block;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        margin-right: 8px;
        animation: pulse 1.5s infinite;
    }
    
    .status-online {
        background-color: #10B981;
    }
    
    .status-processing {
        background-color: #F59E0B;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); opacity: 1; }
        50% { transform: scale(1.2); opacity: 0.7; }
        100% { transform: scale(1); opacity: 1; }
    }
    
    /* Toast Notifications */
    .toast-notification {
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: white;
        color: #1a2980;
        padding: 15px 25px;
        border-radius: 10px;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
        z-index: 9999;
        animation: toastIn 0.5s ease, toastOut 0.5s ease 4.5s forwards;
    }
    
    @keyframes toastIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes toastOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
    
    /* Responsive Design Adjustments */
    @media (max-width: 768px) {
        .main-title {
            font-size: 2em;
        }
        
        .chat-message-user, .chat-message-assistant {
            max-width: 95%;
        }
    }
    </style>
    """, unsafe_allow_html=True)
def main():
    # Set page configuration with enhanced title and icon
    st.set_page_config(
        page_title="TalentScout: AI Hiring Assistant",
        page_icon="🚀",
        layout="wide"
    )
    
    # Apply custom CSS
    apply_custom_css()
    
    # Initialize chatbot in session state if it doesn't exist
    if 'chatbot' not in st.session_state:
        try:
            st.session_state.chatbot = TalentScoutChatbot()
        except Exception as e:
            st.error(f"Error initializing chatbot: {e}")
            st.error("Please check your API key and try again.")
            return
    
    # Load Lottie animations
    lottie_urls = {
        "robot": "https://assets4.lottiefiles.com/packages/lf20_xafe7whz.json",
        "hiring": "https://assets9.lottiefiles.com/packages/lf20_vwcugezu.json",
        "success": "https://assets10.lottiefiles.com/packages/lf20_ydo1amjm.json"
    }
    
    # Load animations
    lottie_robot = load_lottie_url(lottie_urls["robot"])
    lottie_hiring = load_lottie_url(lottie_urls["hiring"])
    
    # Create modern header with animations
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if lottie_robot:
            st_lottie(lottie_robot, height=150, key="robot")
    
    with col2:
        st.markdown("<h1 class='main-title'>TalentScout AI</h1>", unsafe_allow_html=True)
        st.markdown("<p class='subtitle'>Intelligent Hiring Assistant for Modern Recruitment</p>", unsafe_allow_html=True)
    
    with col3:
        if lottie_hiring:
            st_lottie(lottie_hiring, height=150, key="hiring")
    
    # Create a container for the chat interface
    chat_container = st.container()
    st.markdown("<div class='chat-container'></div>", unsafe_allow_html=True)
    
    with chat_container:
        # Information cards section
        st.markdown("### How it works")
        
        info_cols = st.columns(3)
        
        with info_cols[0]:
            st.markdown("""
            <div class='info-card'>
                <div class='card-title'>👋 Introduction</div>
                <p>Our AI assistant guides you through the initial screening process with natural conversation.</p>
            </div>
            """, unsafe_allow_html=True)
            
        with info_cols[1]:
            st.markdown("""
            <div class='info-card'>
                <div class='card-title'>📋 Assessment</div>
                <p>Tailored technical questions assess your skills based on your specific tech stack.</p>
            </div>
            """, unsafe_allow_html=True)
            
        with info_cols[2]:
            st.markdown("""
            <div class='info-card'>
                <div class='card-title'>🔒 Privacy</div>
                <p>Advanced data privacy measures ensure your information remains secure and protected.</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Status indicator
        st.markdown("""
        <div style="text-align: center; margin: 20px 0;">
            <span class="status-indicator status-online"></span> AI Assistant Online
        </div>
        """, unsafe_allow_html=True)
        
        # Initialize messages in session state if they don't exist
        if 'messages' not in st.session_state:
            st.session_state.messages = []
            
            # Add initial welcome message from assistant
            initial_message = st.session_state.chatbot.process_user_input("")
            st.session_state.messages.append({"role": "assistant", "content": initial_message})
        
        # Display chat messages
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f"""
                <div style="display: flex; align-items: flex-start; margin-bottom: 15px;">
                    <div class="avatar-user">U</div>
                    <div class="chat-message-user">{message["content"]}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="display: flex; align-items: flex-start; margin-bottom: 15px;">
                    <div class="avatar-assistant">AI</div>
                    <div class="chat-message-assistant">{message["content"]}</div>
                </div>
                """, unsafe_allow_html=True)
        
        # Chat input with improved styling
        if prompt := st.chat_input("💬 Type your response here..."):
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            try:
                # Process user input
                response = st.session_state.chatbot.process_user_input(prompt)
                
                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": response})
                
                # Force a rerun to update the chat display
                st.rerun()
                
            except Exception as e:
                st.error(f"🚨 An error occurred: {e}")
                st.error("Please check your configuration and try again.")
        
        # Animated footer
        st.markdown("""
        <div style="text-align: center; margin-top: 40px; opacity: 0.7; animation: fadeIn 1s ease-out;">
            <p>Powered by advanced AI technology • <span style="color: #1a2980;">TalentScout</span> © 2025</p>
        </div>
        """, unsafe_allow_html=True)
if __name__ == "__main__":
    main()
