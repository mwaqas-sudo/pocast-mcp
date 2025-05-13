from typing import List, Optional, Union
import io
import os
import re
from pathlib import Path
import logging
from datetime import datetime
from enum import Enum
from mcp.server.fastmcp import FastMCP
import openai
from pydub import AudioSegment
import tempfile
from pydantic import BaseModel, Field, field_validator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

mcp = FastMCP("podcast-generator")

# Enums for better type safety
class VoiceType(str, Enum):
    ALLOY = "alloy"
    ECHO = "echo"
    FABLE = "fable"
    ONYX = "onyx"
    NOVA = "nova"
    SHIMMER = "shimmer"


class ServerConfig(BaseModel):
    """Server configuration model"""
    openai_api_key: str = Field(..., description="OpenAI API key")
    tts_model: str = Field(..., description="OpenAI TTS model to use")
    gpt_model: str = Field(default=..., description="OpenAI GPT model to use")
    speaker1_name: str = Field(default="Alex", description="Name of the first speaker")
    speaker2_name: str = Field(default="Jordan", description="Name of the second speaker")
    speaker1_voice: VoiceType = Field(default=VoiceType.ALLOY, description="Voice for speaker 1")
    speaker2_voice: VoiceType = Field(default=VoiceType.NOVA, description="Voice for speaker 2")
    default_podcast_length: int = Field(default=10, ge=1, le=60, description="Default podcast length in minutes")
    output_directory: Path = Field(default=Path.cwd(), description="Directory to save podcast files")
    
    @field_validator('openai_api_key')
    def validate_api_key(cls, v):
        if not v:
            raise ValueError("OpenAI API key must be provided")
        return v
    
    @field_validator('output_directory')
    def validate_output_directory(cls, v):
        v = Path(v)
        v.mkdir(parents=True, exist_ok=True)
        return v

class SpeechMarker(BaseModel):
    """Model for speech markers in dialogue"""
    pause_short: str = Field(default="[pause-short]", description="Short pause marker")
    pause_medium: str = Field(default="[pause-medium]", description="Medium pause marker")
    pause_long: str = Field(default="[pause-long]", description="Long pause marker")
    emphasis_start: str = Field(default="[emphasis]", description="Emphasis start marker")
    emphasis_end: str = Field(default="[/emphasis]", description="Emphasis end marker")
    breath: str = Field(default="[breath]", description="Breath marker")
    thoughtful: str = Field(default="[thoughtful]", description="Thoughtful moment marker")

class SpeakerLine(BaseModel):
    """Model for a single speaker line"""
    speaker: str = Field(..., description="Speaker name")
    text: str = Field(..., description="Speaker text")
    
    @field_validator('text')
    def validate_text(cls, v):
        if not v.strip():
            raise ValueError("Speaker text cannot be empty")
        return v.strip()

class DialogueInput(BaseModel):
    """Model for dialogue input"""
    raw_dialogue: str = Field(..., description="Raw dialogue text")
    
    @field_validator('raw_dialogue')
    def validate_dialogue(cls, v):
        if not v.strip():
            raise ValueError("Dialogue cannot be empty")
        return v.strip()

class PodcastRequest(BaseModel):
    """Model for podcast generation request"""
    title: str = Field(..., min_length=1, max_length=200, description="Podcast title")
    dialogue: str = Field(..., min_length=10, description="Dialogue between speakers")
    podcast_length: int = Field(default=10, ge=1, le=60, description="Target podcast length in minutes")
    
    @field_validator('title')
    def validate_title(cls, v):
        if not v.strip():
            raise ValueError("Title cannot be empty")
        return v.strip()

class AudioSegmentInfo(BaseModel):
    """Model for audio segment information"""
    speaker: str
    text: str
    voice: VoiceType
    duration_ms: Optional[int] = None
    audio_data: Optional[bytes] = None

class PodcastResponse(BaseModel):
    """Model for podcast generation response"""
    title: str
    target_duration_min: int
    actual_duration_min: float
    word_count: int
    speakers: str
    gpt_model_used: str
    tts_model_used: str
    success: bool
    audio_path: str
    file_size_mb: Optional[float] = None
    created_at: datetime = Field(default_factory=datetime.now)
    segments_processed: int = 0
    
    @field_validator('audio_path')
    def validate_audio_path(cls, v):
        path = Path(v)
        if not path.exists():
            raise ValueError(f"Audio file does not exist at path: {v}")
        return str(path.absolute())

class PodcastError(BaseModel):
    """Model for podcast generation errors"""
    error: str
    success: bool = False
    error_type: str = "generation_error"
    timestamp: datetime = Field(default_factory=datetime.now)

# Server configuration
def load_config() -> ServerConfig:
    """Load server configuration from environment variables"""
    try:
        return ServerConfig(
            openai_api_key=os.getenv("OPENAI_API_KEY", ""),
            tts_model=os.getenv("OPENAI_TTS_MODEL", "tts-1"),
            gpt_model=os.getenv("OPENAI_GPT_MODEL", "gpt-4o-mini"),
            speaker1_name=os.getenv("SPEAKER1_NAME", "Alex"),
            speaker2_name=os.getenv("SPEAKER2_NAME", "Jordan"),
            speaker1_voice=VoiceType(os.getenv("SPEAKER1_VOICE", "alloy")),
            speaker2_voice=VoiceType(os.getenv("SPEAKER2_VOICE", "nova")),
            default_podcast_length=int(os.getenv("DEFAULT_PODCAST_LENGTH", "10")),
            output_directory=Path(os.getenv("OUTPUT_DIRECTORY", os.getcwd()))
        )
    except Exception as e:
        logger.error(f"Error loading configuration: {e}")
        raise

# Global configuration
config = load_config()

openai.api_key = config.openai_api_key

class TextProcessor:
    """Class for processing text for TTS"""
    
    def __init__(self, markers: SpeechMarker = None):
        self.markers = markers or SpeechMarker()
    
    def preprocess_text_for_tts(self, text: str) -> str:
        """Preprocess text for better TTS results."""
        try:
            processed_text = text
            
            processed_text = re.sub(r'^[A-Z][A-Za-z\s\-\']+:\s+', '', processed_text)
            
            # Replace pause markers with punctuation
            processed_text = processed_text.replace(self.markers.pause_short, ",")
            processed_text = processed_text.replace(self.markers.pause_medium, ".")
            processed_text = processed_text.replace(self.markers.pause_long, "...")
            
            # Process emphasis markers
            emphasis_pattern = rf'{re.escape(self.markers.emphasis_start)}(.*?){re.escape(self.markers.emphasis_end)}'
            processed_text = re.sub(emphasis_pattern, r'\1', processed_text)
            
            # Process other markers
            processed_text = processed_text.replace(self.markers.breath, ",")
            processed_text = processed_text.replace(self.markers.thoughtful, "...")
            
            # Clean up any remaining markers
            processed_text = re.sub(r'\[.*?\]', '', processed_text)
            
            return processed_text.strip()
        except Exception as e:
            logger.error(f"Error preprocessing text: {e}")
            raise

class DialogueParser:
    """Class for parsing dialogue text"""
    
    def __init__(self, speaker1_name: str, speaker2_name: str):
        self.speaker1_name = speaker1_name
        self.speaker2_name = speaker2_name
    
    def parse_dialogue(self, dialogue: str) -> List[SpeakerLine]:
        """Parse dialogue text into speaker lines"""
        try:
            pattern = rf"({re.escape(self.speaker1_name)}|{re.escape(self.speaker2_name)}): (.*?)(?=\n{re.escape(self.speaker1_name)}:|{re.escape(self.speaker2_name)}:|$)"
            segments = re.findall(pattern, dialogue, re.DOTALL)
            
            speaker_lines = []
            for speaker, text in segments:
                cleaned_text = text.strip()
                if cleaned_text:
                    speaker_lines.append(SpeakerLine(speaker=speaker, text=cleaned_text))
            
            if not speaker_lines:
                raise ValueError("No valid speaker lines found in dialogue")
            
            return speaker_lines
        except Exception as e:
            logger.error(f"Error parsing dialogue: {e}")
            raise

class TTSService:
    """Service for text-to-speech conversion"""
    
    def __init__(self, model):
        self.model = model
        self.max_chunk_size = 4000
    
    async def text_to_speech(self, text: str, voice: VoiceType) -> bytes:
        """Convert text to speech using OpenAI's TTS API"""
        try:
            logger.info(f"Converting text to speech: model={self.model}, voice={voice}")
            
            # Handle shorter text segments
            if len(text) <= self.max_chunk_size:
                response = openai.audio.speech.create(
                    model=self.model,
                    voice=voice.value,
                    input=text
                )
                return response.content
            
            # Chunk the text for longer content
            chunks = [text[i:i+self.max_chunk_size] for i in range(0, len(text), self.max_chunk_size)]
            
            audio_segments = []
            for chunk in chunks:
                response = openai.audio.speech.create(
                    model=self.model,
                    voice=voice.value,
                    input=chunk
                )
                
                with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_file:
                    temp_file.write(response.content)
                    temp_path = temp_file.name
                
                segment = AudioSegment.from_file(temp_path, format="mp3")
                audio_segments.append(segment)
                os.unlink(temp_path)
            
            # Combine audio segments
            combined = sum(audio_segments) if audio_segments else AudioSegment.empty()
            
            # Export to MP3
            buffer = io.BytesIO()
            combined.export(buffer, format="mp3")
            buffer.seek(0)
            return buffer.read()
        
        except Exception as e:
            logger.error(f"Error in text_to_speech: {e}")
            raise

class PodcastGenerator:
    """Main class for podcast generation"""
    
    def __init__(self, config: ServerConfig):
        self.config = config
        self.text_processor = TextProcessor()
        self.dialogue_parser = DialogueParser(config.speaker1_name, config.speaker2_name)
        self.tts_service = TTSService(config.tts_model)
    
    async def generate_podcast(self, request: PodcastRequest) -> Union[PodcastResponse, PodcastError]:
        """Generate a podcast from the request"""
        try:
            logger.info(f"Generating podcast: {request.title}")
            
            # Parse dialogue
            speaker_lines = self.dialogue_parser.parse_dialogue(request.dialogue)
            
            # Process audio segments
            audio_segments = []
            short_pause = AudioSegment.silent(duration=500)
            segments_processed = 0
            
            for line in speaker_lines:
                # Preprocess text for TTS
                processed_text = self.text_processor.preprocess_text_for_tts(line.text)
                
                # Select voice based on speaker
                voice = (self.config.speaker1_voice 
                        if line.speaker == self.config.speaker1_name 
                        else self.config.speaker2_voice)
                
                # Convert to speech
                audio_data = await self.tts_service.text_to_speech(processed_text, voice)
                
                # Create audio segment
                with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_file:
                    temp_file.write(audio_data)
                    temp_path = temp_file.name
                
                segment = AudioSegment.from_file(temp_path, format="mp3")
                audio_segments.append(segment)
                audio_segments.append(short_pause)
                
                os.unlink(temp_path)
                segments_processed += 1
            
            # Combine all segments
            combined = sum(audio_segments) if audio_segments else AudioSegment.empty()
            
            # Generate output path
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_title = re.sub(r'[^\w\s-]', '', request.title).strip()[:50]
            filename = f"podcast_{safe_title}_{timestamp}.mp3"
            output_path = self.config.output_directory / filename
            
            # Export final audio file
            combined.export(str(output_path), format="mp3")
            
            # Calculate file size
            file_size_mb = output_path.stat().st_size / (1024 * 1024)
            
            # Create response
            response = PodcastResponse(
                title=request.title,
                target_duration_min=request.podcast_length,
                actual_duration_min=round(len(combined) / (1000 * 60), 1),
                word_count=len(request.dialogue.split()),
                speakers=f"{self.config.speaker1_name} and {self.config.speaker2_name}",
                gpt_model_used=self.config.gpt_model,
                tts_model_used=self.config.tts_model,
                success=True,
                audio_path=str(output_path),
                file_size_mb=round(file_size_mb, 2),
                segments_processed=segments_processed
            )
            
            logger.info(f"Podcast generated successfully: {output_path}")
            return response
            
        except Exception as e:
            logger.error(f"Error generating podcast: {e}")
            return PodcastError(
                error=str(e),
                error_type="generation_error"
            )

# Initialize podcast generator
podcast_generator = PodcastGenerator(config)

# Tool registration with proper Pydantic validation
@mcp.tool("generate_podcast", description=f"""This tool is responsible for creating a podcast between two people named {config.speaker1_name} and {config.speaker2_name}. 

IMPORTANT: The podcast should be approximately 10 minutes when spoken if not specified by the user (about 1275 words per 10 minutes in total).

Make it sound like a real conversation with back-and-forth discussion, questions, insights, and occasional humor.
Include an introduction where the hosts introduce themselves and the topic, and a conclusion where they wrap up.

If the provided content is too lengthy, extract and discuss the most important points only.
If the content is too brief, expand on it with relevant discussion and context.

Format the output like this:
{config.speaker1_name}: [Speaker 1's dialogue]
{config.speaker2_name}: [Speaker 2's dialogue]
...and so on.

Generate a complete, natural conversational script formatted with:
- Each speaker's lines as "SPEAKER NAME: Their dialogue text"
- Natural speech markers:
    * [pause-short] for brief pauses (0.3s)
    * [pause-medium] for medium pauses (0.7s)
    * [pause-long] for longer pauses (1.2s)
    * [emphasis] around emphasized words
    * [breath] where speakers would naturally take a breath
    * [thoughtful] for moments of consideration
- Include natural filler words like "um", "uh", "you know" occasionally
- Mark sound effects as [SOUND EFFECT: description]
- Mark transitions as [TRANSITION]

At the end this tool will return the path where it stores the mp3 file""")
async def generate_podcast_tool(title: str, dialogue: str, podcast_length: int = 10):
    """Generate a podcast from dialogue between two speakers.
    
    Args:
        title (str): Podcast title
        dialogue (str): Dialogue between two speakers
        podcast_length (int, optional): Length of the podcast in minutes. Defaults to 10.
    
    Returns:
        dict: Podcast generation result
    """
    try:
        # Validate input using Pydantic
        request = PodcastRequest(
            title=title,
            dialogue=dialogue,
            podcast_length=podcast_length
        )
        
        # Generate podcast
        result = await podcast_generator.generate_podcast(request)
        
        # Convert result to dict for JSON serialization
        if isinstance(result, PodcastResponse):
            return result.dict()
        else:
            return result.dict()
            
    except Exception as e:
        logger.error(f"Error in generate_podcast_tool: {e}")
        return PodcastError(error=str(e)).dict()

# Health check endpoint
@mcp.tool("health_check", description="Check the health of the podcast generation server")
async def health_check():
    """Check the health of the podcast generation server"""
    try:
        return {
            "status": "healthy",
            "config": {
                "speakers": f"{config.speaker1_name} and {config.speaker2_name}",
                "tts_model": config.tts_model,
                "gpt_model": config.gpt_model,
                "output_directory": str(config.output_directory)
            },
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

if __name__ == "__main__":
    logger.info("Starting enhanced podcast generator MCP server...")
    logger.info(f"Using GPT model: {config.gpt_model}")
    logger.info(f"Using TTS model: {config.tts_model}")
    logger.info(f"Default podcast length: {config.default_podcast_length} minutes")
    logger.info(f"Speakers: {config.speaker1_name} (voice: {config.speaker1_voice.value}) and {config.speaker2_name} (voice: {config.speaker2_voice.value})")
    logger.info(f"Output directory: {config.output_directory}")
    
    try:
        mcp.run(transport='stdio')
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        raise