#!/usr/bin/env python3
"""
AI-Powered Assistant for JARVIS
Handles intelligent responses using built-in intelligence and Wikipedia
"""

import os
import json
import requests
import time
import re
from datetime import datetime
from typing import Dict, Any, Optional

# Try to import Wikipedia
try:
    import wikipedia
    WIKIPEDIA_AVAILABLE = True
except ImportError:
    WIKIPEDIA_AVAILABLE = False
    print("⚠️ Wikipedia not available - install with: pip install wikipedia")

class AIAssistant:
    def __init__(self):
        """Initialize AI Assistant with built-in intelligence and API support"""
        self.knowledge_base = self.load_knowledge_base()
        # Load .env if available
        try:
            from dotenv import load_dotenv  # type: ignore
            load_dotenv()
        except Exception:
            pass
        self.groq_api_key = os.getenv('GROQ_API_KEY')
        
        # If no API key, provide instructions
        if not self.groq_api_key:
            print("🧠 AI Assistant initialized with built-in intelligence!")
            print("💡 For enhanced AI responses, set GROQ_API_KEY environment variable")
            print("   Get free API key from: https://console.groq.com/")
        else:
            print("🤖 AI Assistant initialized with Groq API support!")
        
    def load_knowledge_base(self):
        """Load built-in knowledge base for common questions"""
        return {
            # Technology
            'python': "Python is a high-level programming language known for its simplicity and readability. It's widely used in web development, data science, AI, and automation.",
            'javascript': "JavaScript is a programming language primarily used for web development. It enables interactive web pages and is essential for front-end development.",
            'artificial intelligence': "Artificial Intelligence (AI) refers to computer systems that can perform tasks typically requiring human intelligence, such as learning, reasoning, and problem-solving.",
            'machine learning': "Machine Learning is a subset of AI that enables computers to learn and improve from experience without being explicitly programmed.",
            'blockchain': "Blockchain is a distributed ledger technology that maintains a continuously growing list of records, called blocks, which are linked and secured using cryptography.",
            
            # Science
            'photosynthesis': "Photosynthesis is the process by which plants use sunlight, water, and carbon dioxide to produce glucose and oxygen. It's essential for life on Earth.",
            'gravity': "Gravity is a fundamental force that attracts objects with mass toward each other. On Earth, it gives weight to physical objects.",
            'dna': "DNA (Deoxyribonucleic Acid) is the hereditary material in humans and almost all other organisms. It contains genetic instructions for development and function.",
            
            # General Knowledge
            'solar system': "The Solar System consists of the Sun and the celestial objects that orbit it, including eight planets, moons, asteroids, and comets.",
            'internet': "The Internet is a global network of interconnected computers that communicate using standardized protocols, enabling worldwide information sharing.",
            'climate change': "Climate change refers to long-term shifts in global temperatures and weather patterns, primarily caused by human activities since the mid-20th century.",
            
            # Philosophy
            'meaning of life': "The meaning of life is a philosophical question concerning the significance of living. Different cultures and individuals have various perspectives on this profound question.",
            
            # Fun Facts
            'space': "Space is the boundless three-dimensional extent in which objects exist and events occur. It's mostly empty but contains galaxies, stars, planets, and other matter.",
            'ocean': "Earth's oceans cover about 71% of the planet's surface and contain 97% of Earth's water. They play a crucial role in climate regulation and support diverse marine life.",
            
            # Developer Information
            'hanzala qureshi': "Hanzala Qureshi is my creator and developer. He's a passionate programmer who designed and built me with advanced AI capabilities. You can find his projects on GitHub at https://github.com/Hanzalaq24.",
            'developer': "I was developed by Hanzala Qureshi, a skilled software developer with expertise in AI and web technologies. He created me to be a helpful and intelligent assistant.",
            'creator': "My creator is Hanzala Qureshi, a talented developer who built me from the ground up. He's passionate about AI and creating useful technology solutions.",
        }
    
    def get_intelligent_response(self, user_input: str, context: Dict[str, Any] = None) -> str:
        """Get intelligent response using available AI services"""
        
        # First, try to handle with built-in intelligence
        built_in_response = self.handle_built_in_queries(user_input)
        if built_in_response:
            return built_in_response
        
        # Try Groq API if available
        if self.groq_api_key:
            groq_response = self.query_groq_api(user_input)
            if groq_response:
                return groq_response
        
        # Try knowledge base lookup
        knowledge_response = self.search_knowledge_base(user_input)
        if knowledge_response:
            return knowledge_response
        
        # Try Wikipedia search (with better error handling)
        if WIKIPEDIA_AVAILABLE:
            wiki_response = self.search_wikipedia_safe(user_input)
            if wiki_response:
                return wiki_response
        
        # Final fallback - intelligent pattern matching
        return self.intelligent_fallback(user_input)
    
    def handle_built_in_queries(self, query: str) -> Optional[str]:
        """Handle common queries with built-in intelligence"""
        query_lower = query.lower().strip()
        
        # Song recognition queries - should NOT be handled by AI
        song_recognition_phrases = [
            'recognize this song', 'what song is this', 'identify this song', 
            'name this song', 'tell me this song', 'what is this song',
            'listen to this song', 'identify the song', 'recognize the song',
            'listen to me sing', 'i will sing', 'let me sing', 'i want to sing',
            'play song', 'find song', 'song with lyrics', 'song that goes', 'the song goes'
        ]
        
        if any(phrase in query_lower for phrase in song_recognition_phrases):
            # Return None so it gets handled by the main command processor
            return None
        
        # Time and date queries
        if any(word in query_lower for word in ['time', 'clock', 'समय', 'સમય']):
            current_time = datetime.now().strftime("%I:%M %p")
            return f"The current time is {current_time}, sir."
        
        if any(word in query_lower for word in ['date', 'today', 'तारीख', 'તારીખ']):
            current_date = datetime.now().strftime("%B %d, %Y")
            return f"Today's date is {current_date}, sir."
        
        # Developer recognition
        if any(word in query_lower for word in ['who created you', 'who made you', 'who is your developer', 'who built you', 'your creator', 'your developer']):
            return "I was created by Hanzala Qureshi, a talented developer and AI enthusiast. You can find his work on GitHub at https://github.com/Hanzalaq24, sir."
        
        if any(word in query_lower for word in ['hanzala', 'hanzala qureshi']):
            return "Hanzala Qureshi is my creator and developer, sir. He's a skilled programmer who built me with passion and dedication. You can check out his projects on GitHub at https://github.com/Hanzalaq24."
        
        # Weather queries (mock response - you can integrate real weather API)
        if any(word in query_lower for word in ['weather', 'temperature', 'मौसम', 'હવામાન']):
            return "I don't have access to real-time weather data yet, sir. You can check your local weather app or ask me to search for weather online."
        
        # Math calculations
        if any(word in query_lower for word in ['calculate', 'math', 'plus', 'minus', 'multiply', 'divide', '+', '-', '*', '/']):
            try:
                # Simple math evaluation (secure)
                math_result = self.safe_math_eval(query_lower)
                if math_result is not None:
                    return f"The result is {math_result}, sir."
            except:
                pass
        
        # Wikipedia queries
        if any(word in query_lower for word in ['who is', 'what is', 'tell me about', 'explain']):
            if WIKIPEDIA_AVAILABLE:
                wiki_result = self.search_wikipedia_safe(query)
                if wiki_result:
                    return wiki_result
        
        return None
    
    def search_knowledge_base(self, query: str) -> Optional[str]:
        """Search built-in knowledge base for answers"""
        query_lower = query.lower().strip()
        
        # Remove common question words
        for phrase in ['what is', 'tell me about', 'explain', 'define', 'describe']:
            query_lower = query_lower.replace(phrase, '').strip()
        
        # Search for exact matches first
        for topic, answer in self.knowledge_base.items():
            if topic in query_lower or query_lower in topic:
                return f"{answer} Would you like to know more about this topic, sir?"
        
        # Search for partial matches
        for topic, answer in self.knowledge_base.items():
            topic_words = topic.split()
            query_words = query_lower.split()
            
            # Check if any topic words are in the query
            if any(word in query_words for word in topic_words):
                return f"{answer} Is this what you were looking for, sir?"
        
        return None
    
    def safe_math_eval(self, expression: str) -> Optional[float]:
        """Safely evaluate mathematical expressions"""
        try:
            import re
            
            # Extract mathematical expressions
            expression = expression.lower()
            
            # Handle word-based math
            expression = expression.replace('plus', '+').replace('add', '+')
            expression = expression.replace('minus', '-').replace('subtract', '-')
            expression = expression.replace('times', '*').replace('multiply', '*').replace('multiplied by', '*')
            expression = expression.replace('divide', '/').replace('divided by', '/').replace('over', '/')
            
            # Find mathematical patterns
            math_patterns = [
                r'(\d+(?:\.\d+)?)\s*\+\s*(\d+(?:\.\d+)?)',  # addition
                r'(\d+(?:\.\d+)?)\s*\-\s*(\d+(?:\.\d+)?)',  # subtraction
                r'(\d+(?:\.\d+)?)\s*\*\s*(\d+(?:\.\d+)?)',  # multiplication
                r'(\d+(?:\.\d+)?)\s*/\s*(\d+(?:\.\d+)?)',   # division
            ]
            
            for pattern in math_patterns:
                match = re.search(pattern, expression)
                if match:
                    num1, num2 = float(match.group(1)), float(match.group(2))
                    if '+' in match.group(0):
                        return num1 + num2
                    elif '-' in match.group(0):
                        return num1 - num2
                    elif '*' in match.group(0):
                        return num1 * num2
                    elif '/' in match.group(0):
                        if num2 != 0:
                            return num1 / num2
            
            # Try simple eval for basic expressions
            math_expr = re.sub(r'[^0-9+\-*/(). ]', '', expression)
            if math_expr and all(c in '0123456789+-*/(). ' for c in math_expr):
                result = eval(math_expr)
                return result
                
        except Exception as e:
            pass
        return None
    
    def query_groq_api(self, user_input: str) -> Optional[str]:
        """Query Groq API for intelligent responses"""
        try:
            import requests
            
            headers = {
                'Authorization': f'Bearer {self.groq_api_key}',
                'Content-Type': 'application/json'
            }
            
            data = {
                'messages': [
                    {
                        'role': 'system',
                        'content': (
                            "You are JARVIS, Tony Stark's AI assistant. Be helpful, intelligent, and concise. "
                            "Address the user respectfully (e.g., 'sir' when natural). Avoid citing sources verbatim. "
                            "If you don't know, say so and suggest alternatives. Defer song recognition to built-in features."
                        )
                    },
                    {
                        'role': 'user',
                        'content': user_input
                    }
                ],
                'model': 'llama3-70b-8192',
                'max_tokens': 200,
                'temperature': 0.6
            }
            
            response = requests.post(
                'https://api.groq.com/openai/v1/chat/completions',
                headers=headers,
                json=data,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                if 'choices' in result and len(result['choices']) > 0:
                    return result['choices'][0]['message']['content'].strip()
            
        except Exception as e:
            print(f"Groq API error: {e}")
        
        return None
    
    def search_wikipedia_safe(self, query: str) -> Optional[str]:
        """Search Wikipedia with improved error handling - Natural responses like Siri/Google Assistant"""
        try:
            # Extract the main topic from the query
            topic = query.lower()
            for phrase in ['who is', 'what is', 'tell me about', 'explain', 'define']:
                topic = topic.replace(phrase, '').strip()
            
            if len(topic) < 2:
                return None
            
            # Try to search Wikipedia
            try:
                # First try exact search
                summary = wikipedia.summary(topic, sentences=2, auto_suggest=False)
                # Make response more natural - like Siri/Google Assistant
                return f"{summary}"
            except wikipedia.exceptions.DisambiguationError as e:
                # Try the first suggestion from disambiguation
                try:
                    if e.options and len(e.options) > 0:
                        summary = wikipedia.summary(e.options[0], sentences=2)
                        return f"{summary}"
                except:
                    return f"I found multiple topics related to '{topic}'. Could you be more specific, sir?"
            except wikipedia.exceptions.PageError:
                # Try with auto-suggest
                try:
                    summary = wikipedia.summary(topic, sentences=2, auto_suggest=True)
                    return f"{summary}"
                except:
                    return None
            
        except Exception as e:
            print(f"Wikipedia search error: {e}")
            return None
        
        return None
    
    def get_contextual_response(self, query: str) -> Optional[str]:
        """Get contextual responses based on query patterns"""
        query_lower = query.lower().strip()
        
        # Programming questions
        if any(word in query_lower for word in ['programming', 'code', 'coding', 'software', 'development']):
            return "Programming is the art of creating instructions for computers. I can help you with questions about various programming languages and concepts, sir."
        
        # Science questions
        if any(word in query_lower for word in ['science', 'physics', 'chemistry', 'biology', 'scientific']):
            return "Science is the systematic study of the natural world through observation and experimentation. I'd be happy to explain scientific concepts, sir."
        
        # Technology questions
        if any(word in query_lower for word in ['technology', 'computer', 'internet', 'digital', 'tech']):
            return "Technology encompasses the application of scientific knowledge for practical purposes. I can discuss various technological topics with you, sir."
        
        # History questions
        if any(word in query_lower for word in ['history', 'historical', 'past', 'ancient', 'civilization']):
            return "History is the study of past events and human civilization. I can share information about historical topics, sir."
        
        # Health questions
        if any(word in query_lower for word in ['health', 'medical', 'medicine', 'doctor', 'disease']):
            return "Health and medicine are important topics. For medical advice, please consult healthcare professionals. I can share general health information, sir."
        
        return None
    
    def intelligent_fallback(self, user_input: str) -> str:
        """Intelligent fallback responses based on pattern matching"""
        query_lower = user_input.lower().strip()
        
        # Try contextual response first
        contextual_response = self.get_contextual_response(query_lower)
        if contextual_response:
            return contextual_response
        
        # Question patterns
        if query_lower.startswith(('how', 'why', 'when', 'where', 'what', 'who')):
            question_responses = {
                'how': "That's an interesting 'how' question. I can help you find information about processes, methods, or procedures, sir.",
                'why': "That's a thoughtful 'why' question about reasons or causes. I'd be happy to help you explore this topic, sir.",
                'when': "For timing and scheduling questions, I can help you with time-related information, sir.",
                'where': "For location-based questions, I can assist with geographical or positional information, sir.",
                'what': "That's a good 'what' question about definitions or explanations. I can help clarify topics for you, sir.",
                'who': "For questions about people or entities, I can help you find biographical or identifying information, sir."
            }
            
            for key, response in question_responses.items():
                if query_lower.startswith(key):
                    return response
        
        # Greeting patterns with time-based response
        if any(word in query_lower for word in ['hello', 'hi', 'hey', 'good morning', 'good evening', 'greetings']):
            hour = datetime.now().hour
            if 5 <= hour < 12:
                greeting = "Good morning"
            elif 12 <= hour < 17:
                greeting = "Good afternoon"
            elif 17 <= hour < 21:
                greeting = "Good evening"
            else:
                greeting = "Good night"
            return f"{greeting}, sir! I'm JARVIS, your AI assistant. How may I help you today?"
        
        # Thank you patterns
        if any(word in query_lower for word in ['thank', 'thanks', 'appreciate', 'grateful']):
            return "You're very welcome, sir! I'm always here to help and assist you."
        
        # Compliment patterns
        if any(word in query_lower for word in ['good job', 'well done', 'excellent', 'great', 'awesome', 'amazing']):
            return "Thank you for the kind words, sir. I'm here to assist you to the best of my abilities."
        
        # Help patterns
        if any(word in query_lower for word in ['help', 'assist', 'support', 'guide']):
            return "I'm here to help, sir! I can answer questions, search the web, take photos and screenshots, control system functions, perform calculations, and much more. What would you like me to do?"
        
        # Opinion or preference questions
        if any(word in query_lower for word in ['think', 'opinion', 'believe', 'prefer', 'like', 'favorite']):
            return "As an AI assistant, I don't have personal opinions, but I can provide information and different perspectives on topics to help you form your own views, sir."
        
        # Capability questions
        if any(word in query_lower for word in ['can you', 'are you able', 'do you know', 'can jarvis']):
            return "I have many capabilities, sir! I can answer questions, control system functions, take photos and screenshots, perform calculations, search for information, and assist with various tasks. What would you like me to help you with?"
        
        # Default intelligent response
        return f"I understand you're asking about '{user_input}'. While I may not have specific information on that exact topic, I'm designed to be helpful and can assist you in various ways. Would you like me to help you search for information about this topic, or is there something else I can do for you, sir?"

# Global AI assistant instance
ai_assistant = AIAssistant()

def get_ai_response(user_input: str, context: Dict[str, Any] = None) -> str:
    """Get AI-powered response for any user input"""
    return ai_assistant.get_intelligent_response(user_input, context)