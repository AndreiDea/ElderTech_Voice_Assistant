import openai
import os
from typing import Optional
import io

# OpenAI configuration
openai.api_key = os.getenv("OPENAI_API_KEY")


async def text_to_speech(
    text: str,
    voice: str = "alloy",
    speed: float = 1.0
) -> bytes:
    """
    Convert text to speech using OpenAI TTS
    
    Args:
        text: Text to convert to speech
        voice: Voice to use (alloy, echo, fable, onyx, nova, shimmer)
        speed: Speed of speech (0.25 to 4.0)
    
    Returns:
        Audio data as bytes
    """
    try:
        # Validate voice parameter
        valid_voices = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
        if voice not in valid_voices:
            voice = "alloy"
        
        # Validate speed parameter
        if speed < 0.25 or speed > 4.0:
            speed = 1.0
        
        # Generate speech using OpenAI TTS
        response = await openai.Audio.acreate(
            model="tts-1",
            voice=voice,
            input=text,
            speed=speed
        )
        
        # Read audio data
        audio_data = response.content
        
        return audio_data
        
    except Exception as e:
        # Return empty audio data on error
        print(f"TTS Error: {str(e)}")
        return b""


async def text_to_speech_stream(
    text: str,
    voice: str = "alloy",
    speed: float = 1.0
):
    """
    Convert text to speech and return as streaming response
    
    Args:
        text: Text to convert to speech
        voice: Voice to use
        speed: Speed of speech
    
    Returns:
        StreamingResponse with audio data
    """
    try:
        audio_data = await text_to_speech(text, voice, speed)
        
        return io.BytesIO(audio_data)
        
    except Exception as e:
        print(f"TTS Stream Error: {str(e)}")
        return io.BytesIO(b"")


def get_available_voices() -> list:
    """Get list of available TTS voices"""
    return [
        {
            "id": "alloy",
            "name": "Alloy",
            "description": "Balanced and versatile voice",
            "gender": "neutral"
        },
        {
            "id": "echo",
            "name": "Echo",
            "description": "Clear and professional voice",
            "gender": "male"
        },
        {
            "id": "fable",
            "name": "Fable",
            "description": "Warm and friendly voice",
            "gender": "female"
        },
        {
            "id": "onyx",
            "name": "Onyx",
            "description": "Deep and authoritative voice",
            "gender": "male"
        },
        {
            "id": "nova",
            "name": "Nova",
            "description": "Bright and energetic voice",
            "gender": "female"
        },
        {
            "id": "shimmer",
            "name": "Shimmer",
            "description": "Soft and gentle voice",
            "gender": "female"
        }
    ]


async def optimize_text_for_speech(text: str) -> str:
    """
    Optimize text for better speech synthesis
    
    Args:
        text: Original text
    
    Returns:
        Optimized text for TTS
    """
    # Basic text optimization for TTS
    optimized = text.strip()
    
    # Add pauses for better speech flow
    optimized = optimized.replace(".", ". ")
    optimized = optimized.replace("!", "! ")
    optimized = optimized.replace("?", "? ")
    optimized = optimized.replace(",", ", ")
    
    # Remove extra whitespace
    optimized = " ".join(optimized.split())
    
    return optimized


async def create_audio_file(
    text: str,
    voice: str = "alloy",
    speed: float = 1.0,
    filename: Optional[str] = None
) -> str:
    """
    Create an audio file from text
    
    Args:
        text: Text to convert
        voice: Voice to use
        speed: Speed of speech
        filename: Optional filename (without extension)
    
    Returns:
        Path to created audio file
    """
    try:
        audio_data = await text_to_speech(text, voice, speed)
        
        if not filename:
            filename = f"speech_{voice}_{int(speed * 100)}"
        
        filepath = f"audio/{filename}.mp3"
        
        # Ensure audio directory exists
        os.makedirs("audio", exist_ok=True)
        
        # Write audio data to file
        with open(filepath, "wb") as f:
            f.write(audio_data)
        
        return filepath
        
    except Exception as e:
        print(f"Audio file creation error: {str(e)}")
        return "" 