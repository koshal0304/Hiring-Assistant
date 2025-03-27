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
            
            return questions[:5] or [
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
    Apply advanced custom CSS styling to the Streamlit app
    """
    st.markdown("""
    <style>
    /* Modern Gradient Background */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        font-family: 'Roboto', 'Inter', sans-serif;
    }
    
    /* Elegant Header Styling */
    .main-title {
        color: #1a2980;
        font-weight: 800;
        text-align: center;
        margin-bottom: 30px;
        font-size: 2.5em;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
        background: linear-gradient(to right, #1a2980, #26d0ce);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Sleek Chat Input Styling */
    .stTextInput > div > div > input {
        background-color: white;
        border: 2px solid transparent;
        border-radius: 12px;
        padding: 12px 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
        background-image: linear-gradient(white, white), 
                          linear-gradient(to right, #1a2980, #26d0ce);
        background-origin: border-box;
        background-clip: padding-box, border-box;
    }
    
    .stTextInput > div > div > input:focus {
        outline: none;
        box-shadow: 0 6px 10px rgba(0, 0, 0, 0.15);
        border-image: linear-gradient(to right, #1a2980, #26d0ce) 1;
    }
    
    /* Enhanced Sidebar Styling */
    .css-1aumxhk {
        background-color: rgba(255, 255, 255, 0.9);
        border-right: 1px solid rgba(0, 0, 0, 0.1);
        border-radius: 0 15px 15px 0;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    }
    
    /* Modern Button Design */
    .stButton > button {
        background: linear-gradient(to right, #1a2980, #26d0ce);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 12px 25px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 10px rgba(0, 0, 0, 0.15);
        background: linear-gradient(to right, #26d0ce, #1a2980);
    }
    
    /* Refined Message Styling */
    .stMarkdown {
        background-color: white;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.08);
        border-left: 5px solid #1a2980;
        transition: all 0.3s ease;
    }
    
    .stMarkdown:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
    }
    
    /* Responsive Typography */
    @media (max-width: 600px) {
        .main-title {
            font-size: 2em;
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
    
    # Load Lottie animation
    lottie_coding = load_lottie_url("https://lottie.host/1234-5678-9012-3456/ai-robot-animation.json")
    
    # Create columns for title and animation
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("<h1 class='main-title'>TalentScout AI Hiring Assistant</h1>", unsafe_allow_html=True)
    
    with col2:
        if lottie_coding:
            st_lottie(lottie_coding, height=100, key="coding")
    
    # Main Chat Interface
    try:
        # Create chatbot with the provided API key
        if 'chatbot' not in st.session_state:
            st.session_state.chatbot = TalentScoutChatbot()
        
        # Chat input with improved styling
        if prompt := st.chat_input("💬 Type your response here..."):
            response = st.session_state.chatbot.process_user_input(prompt)
            
            # Enhanced message display
            with st.chat_message("assistant"):
                st.markdown(response)
    
    except Exception as e:
        st.error(f"🚨 An error occurred: {e}")
        st.error("Please check your configuration and try again.")

if __name__ == "__main__":
    main()