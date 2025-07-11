from fastapi import APIRouter, HTTPException, Depends, status, UploadFile, File
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional
import io

from services.tts import text_to_speech
from services.whisper import speech_to_text

router = APIRouter()
security = HTTPBearer()


class TTSRequest(BaseModel):
    text: str
    voice: str = "alloy"  # alloy, echo, fable, onyx, nova, shimmer
    speed: float = 1.0


@router.post("/speech-to-text")
async def convert_speech_to_text(
    audio_file: UploadFile = File(...),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Convert uploaded audio file to text using Whisper"""
    try:
        # Validate file type
        if not audio_file.content_type.startswith('audio/'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File must be an audio file"
            )
        
        # Read audio file
        audio_content = await audio_file.read()
        
        # Convert speech to text
        text = await speech_to_text(audio_content)
        
        return {
            "text": text,
            "confidence": 0.95,  # TODO: Get actual confidence from Whisper
            "language": "en"  # TODO: Detect language
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing audio: {str(e)}"
        )


@router.post("/text-to-speech")
async def convert_text_to_speech(
    request: TTSRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Convert text to speech using OpenAI TTS"""
    try:
        # Convert text to speech
        audio_data = await text_to_speech(
            text=request.text,
            voice=request.voice,
            speed=request.speed
        )
        
        # Return audio file as streaming response
        return StreamingResponse(
            io.BytesIO(audio_data),
            media_type="audio/mpeg",
            headers={
                "Content-Disposition": "attachment; filename=speech.mp3"
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating speech: {str(e)}"
        )


@router.get("/voices")
async def get_available_voices():
    """Get list of available TTS voices"""
    voices = [
        {"id": "alloy", "name": "Alloy", "description": "Balanced and versatile"},
        {"id": "echo", "name": "Echo", "description": "Clear and professional"},
        {"id": "fable", "name": "Fable", "description": "Warm and friendly"},
        {"id": "onyx", "name": "Onyx", "description": "Deep and authoritative"},
        {"id": "nova", "name": "Nova", "description": "Bright and energetic"},
        {"id": "shimmer", "name": "Shimmer", "description": "Soft and gentle"}
    ]
    return {"voices": voices}


@router.post("/transcribe-url")
async def transcribe_from_url(
    url: str,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Transcribe audio from a URL"""
    # TODO: Implement URL-based transcription
    return {"message": "URL transcription endpoint"}


@router.post("/batch-transcribe")
async def batch_transcribe(
    audio_files: list[UploadFile] = File(...),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Transcribe multiple audio files"""
    # TODO: Implement batch transcription
    return {"message": "Batch transcription endpoint"} 