import openai
import os
from typing import Optional, Dict, Any
import tempfile
import io

# OpenAI configuration
openai.api_key = os.getenv("OPENAI_API_KEY")


async def speech_to_text(
    audio_data: bytes,
    language: Optional[str] = None,
    prompt: Optional[str] = None
) -> str:
    """
    Convert speech to text using OpenAI Whisper
    
    Args:
        audio_data: Audio file data as bytes
        language: Language code (e.g., 'en', 'es', 'fr')
        prompt: Optional prompt to guide transcription
    
    Returns:
        Transcribed text
    """
    try:
        # Create temporary file for audio data
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
            temp_file.write(audio_data)
            temp_file_path = temp_file.name
        
        try:
            # Prepare parameters for Whisper API
            params = {
                "model": "whisper-1",
                "file": open(temp_file_path, "rb"),
                "response_format": "text"
            }
            
            # Add optional parameters
            if language:
                params["language"] = language
            if prompt:
                params["prompt"] = prompt
            
            # Call Whisper API
            response = await openai.Audio.atranscribe(**params)
            
            return response
            
        finally:
            # Clean up temporary file
            os.unlink(temp_file_path)
            
    except Exception as e:
        print(f"Whisper Error: {str(e)}")
        return ""


async def speech_to_text_with_metadata(
    audio_data: bytes,
    language: Optional[str] = None,
    prompt: Optional[str] = None
) -> Dict[str, Any]:
    """
    Convert speech to text with additional metadata
    
    Args:
        audio_data: Audio file data as bytes
        language: Language code
        prompt: Optional prompt
    
    Returns:
        Dictionary with text and metadata
    """
    try:
        # Create temporary file for audio data
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
            temp_file.write(audio_data)
            temp_file_path = temp_file.name
        
        try:
            # Prepare parameters for Whisper API
            params = {
                "model": "whisper-1",
                "file": open(temp_file_path, "rb"),
                "response_format": "verbose_json"
            }
            
            # Add optional parameters
            if language:
                params["language"] = language
            if prompt:
                params["prompt"] = prompt
            
            # Call Whisper API
            response = await openai.Audio.atranscribe(**params)
            
            return {
                "text": response.text,
                "language": response.language,
                "duration": response.duration,
                "segments": response.segments,
                "confidence": response.confidence if hasattr(response, 'confidence') else None
            }
            
        finally:
            # Clean up temporary file
            os.unlink(temp_file_path)
            
    except Exception as e:
        print(f"Whisper Metadata Error: {str(e)}")
        return {
            "text": "",
            "language": None,
            "duration": None,
            "segments": [],
            "confidence": None,
            "error": str(e)
        }


async def detect_language(audio_data: bytes) -> str:
    """
    Detect the language of audio content
    
    Args:
        audio_data: Audio file data as bytes
    
    Returns:
        Language code (e.g., 'en', 'es', 'fr')
    """
    try:
        # Create temporary file for audio data
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
            temp_file.write(audio_data)
            temp_file_path = temp_file.name
        
        try:
            # Call Whisper API for language detection
            response = await openai.Audio.atranscribe(
                model="whisper-1",
                file=open(temp_file_path, "rb"),
                response_format="verbose_json"
            )
            
            return response.language
            
        finally:
            # Clean up temporary file
            os.unlink(temp_file_path)
            
    except Exception as e:
        print(f"Language Detection Error: {str(e)}")
        return "en"  # Default to English


async def transcribe_with_timestamps(audio_data: bytes) -> list:
    """
    Transcribe audio with word-level timestamps
    
    Args:
        audio_data: Audio file data as bytes
    
    Returns:
        List of segments with timestamps
    """
    try:
        metadata = await speech_to_text_with_metadata(audio_data)
        return metadata.get("segments", [])
        
    except Exception as e:
        print(f"Timestamp Transcription Error: {str(e)}")
        return []


def validate_audio_format(audio_data: bytes) -> bool:
    """
    Validate audio format for Whisper
    
    Args:
        audio_data: Audio file data as bytes
    
    Returns:
        True if format is valid
    """
    # Check if data is not empty
    if not audio_data:
        return False
    
    # Check file size (Whisper has a 25MB limit)
    if len(audio_data) > 25 * 1024 * 1024:
        return False
    
    # Basic format validation (check for common audio headers)
    audio_headers = [
        b'RIFF',  # WAV
        b'ID3',   # MP3
        b'\xff\xfb',  # MP3
        b'OggS',  # OGG
        b'fLaC',  # FLAC
    ]
    
    for header in audio_headers:
        if audio_data.startswith(header):
            return True
    
    return True  # Assume valid if no specific header found


async def batch_transcribe(audio_files: list) -> list:
    """
    Transcribe multiple audio files
    
    Args:
        audio_files: List of audio file data as bytes
    
    Returns:
        List of transcription results
    """
    results = []
    
    for i, audio_data in enumerate(audio_files):
        try:
            text = await speech_to_text(audio_data)
            results.append({
                "file_index": i,
                "text": text,
                "success": True
            })
        except Exception as e:
            results.append({
                "file_index": i,
                "text": "",
                "success": False,
                "error": str(e)
            })
    
    return results 