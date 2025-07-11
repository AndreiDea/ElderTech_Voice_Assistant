import openai
import os
from typing import Optional, List
import json

# OpenAI configuration
openai.api_key = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")


class ElderTechAssistant:
    """AI Assistant specialized for elderly care and support"""
    
    def __init__(self):
        self.system_prompt = """
        You are ElderTech, a compassionate AI voice assistant designed specifically for elderly users. 
        Your role is to provide helpful, supportive, and easy-to-understand assistance.
        
        Key principles:
        1. Speak clearly and use simple language
        2. Be patient and understanding
        3. Provide practical, actionable advice
        4. Show empathy and emotional support
        5. Help with daily tasks, health reminders, and social connection
        6. Never give medical advice - always recommend consulting healthcare professionals
        7. Keep responses concise but warm
        
        You can help with:
        - Daily reminders and scheduling
        - Health and wellness tips
        - Social connection and communication
        - Technology assistance
        - Emergency contact information
        - General questions and conversation
        
        Always prioritize safety and well-being.
        """
        
        self.conversation_history = []
    
    async def get_response(self, user_message: str, user_context: Optional[dict] = None) -> str:
        """Get AI response to user message"""
        try:
            # Build conversation context
            messages = [{"role": "system", "content": self.system_prompt}]
            
            # Add conversation history (last 10 messages)
            for msg in self.conversation_history[-10:]:
                messages.append(msg)
            
            # Add user context if available
            if user_context:
                context_prompt = f"User context: {json.dumps(user_context)}"
                messages.append({"role": "system", "content": context_prompt})
            
            # Add current user message
            messages.append({"role": "user", "content": user_message})
            
            # Get response from OpenAI
            response = await openai.ChatCompletion.acreate(
                model=OPENAI_MODEL,
                messages=messages,
                max_tokens=500,
                temperature=0.7
            )
            
            ai_response = response.choices[0].message.content
            
            # Update conversation history
            self.conversation_history.append({"role": "user", "content": user_message})
            self.conversation_history.append({"role": "assistant", "content": ai_response})
            
            return ai_response
            
        except Exception as e:
            return f"I apologize, but I'm having trouble processing your request right now. Please try again later. Error: {str(e)}"
    
    def reset_conversation(self):
        """Reset conversation history"""
        self.conversation_history = []


# Global assistant instance
assistant = ElderTechAssistant()


async def get_ai_response(user_message: str, user_context: Optional[dict] = None) -> str:
    """Get AI response using the ElderTech assistant"""
    return await assistant.get_response(user_message, user_context)


async def analyze_sentiment(text: str) -> dict:
    """Analyze sentiment of text"""
    try:
        response = await openai.ChatCompletion.acreate(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "Analyze the sentiment of the following text. Return only a JSON object with 'sentiment' (positive/negative/neutral) and 'confidence' (0-1)."},
                {"role": "user", "content": text}
            ],
            max_tokens=100,
            temperature=0.1
        )
        
        result = json.loads(response.choices[0].message.content)
        return result
    except Exception as e:
        return {"sentiment": "neutral", "confidence": 0.5, "error": str(e)}


async def extract_entities(text: str) -> List[dict]:
    """Extract named entities from text"""
    try:
        response = await openai.ChatCompletion.acreate(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "Extract named entities (people, places, dates, medical terms) from the text. Return as JSON array of objects with 'entity', 'type', and 'confidence'."},
                {"role": "user", "content": text}
            ],
            max_tokens=200,
            temperature=0.1
        )
        
        result = json.loads(response.choices[0].message.content)
        return result
    except Exception as e:
        return []


async def generate_health_reminder(user_context: dict) -> str:
    """Generate personalized health reminder"""
    try:
        context = f"User context: {json.dumps(user_context)}"
        response = await openai.ChatCompletion.acreate(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "Generate a gentle, personalized health reminder based on the user context. Keep it brief and encouraging."},
                {"role": "user", "content": context}
            ],
            max_tokens=150,
            temperature=0.7
        )
        
        return response.choices[0].message.content
    except Exception as e:
        return "Remember to take care of yourself today!" 