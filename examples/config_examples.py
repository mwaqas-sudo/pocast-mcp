#!/usr/bin/env python3
"""
Configuration Examples for Podcast Generator MCP
Created by Muhammad Waqas

This file contains various configuration examples for the Podcast Generator MCP.
You can use these as templates to customize your podcast generation setup.
"""

from pathlib import Path
from enum import Enum
from typing import Dict, Any


# Example 1: Basic Configuration
BASIC_CONFIG = {
    "OPENAI_API_KEY": "sk-your-api-key-here",
    "OPENAI_TTS_MODEL": "tts-1",
    "OPENAI_GPT_MODEL": "gpt-4o-mini",
    "SPEAKER1_NAME": "Alex",
    "SPEAKER2_NAME": "Jordan",
    "SPEAKER1_VOICE": "alloy",
    "SPEAKER2_VOICE": "nova",
    "DEFAULT_PODCAST_LENGTH": "10",
    "OUTPUT_DIRECTORY": "./podcasts"
}


# Example 2: Educational Podcast Configuration
EDUCATIONAL_CONFIG = {
    "OPENAI_API_KEY": "sk-your-api-key-here",
    "OPENAI_TTS_MODEL": "tts-1-hd",  # Higher quality for educational content
    "OPENAI_GPT_MODEL": "gpt-4",
    "SPEAKER1_NAME": "Professor Smith",
    "SPEAKER2_NAME": "Dr. Johnson",
    "SPEAKER1_VOICE": "fable",  # More authoritative voice
    "SPEAKER2_VOICE": "echo",   # Warm, engaging voice
    "DEFAULT_PODCAST_LENGTH": "20",
    "OUTPUT_DIRECTORY": "./educational_podcasts"
}


# Example 3: News & Current Events Configuration
NEWS_CONFIG = {
    "OPENAI_API_KEY": "sk-your-api-key-here",
    "OPENAI_TTS_MODEL": "tts-1",
    "OPENAI_GPT_MODEL": "gpt-4o-mini",
    "SPEAKER1_NAME": "Sarah",
    "SPEAKER2_NAME": "Michael",
    "SPEAKER1_VOICE": "nova",    # Clear, professional voice
    "SPEAKER2_VOICE": "onyx",    # Deep, serious tone
    "DEFAULT_PODCAST_LENGTH": "15",
    "OUTPUT_DIRECTORY": "./news_podcasts"
}


# Example 4: Casual Chat Configuration
CASUAL_CONFIG = {
    "OPENAI_API_KEY": "sk-your-api-key-here",
    "OPENAI_TTS_MODEL": "tts-1",
    "OPENAI_GPT_MODEL": "gpt-4o-mini",
    "SPEAKER1_NAME": "Emma",
    "SPEAKER2_NAME": "Jake",
    "SPEAKER1_VOICE": "shimmer",  # Soft, friendly voice
    "SPEAKER2_VOICE": "alloy",    # Neutral, versatile voice
    "DEFAULT_PODCAST_LENGTH": "5",
    "OUTPUT_DIRECTORY": "./casual_podcasts"
}


# Example 5: International Voices Configuration
INTERNATIONAL_CONFIG = {
    "OPENAI_API_KEY": "sk-your-api-key-here",
    "OPENAI_TTS_MODEL": "tts-1",
    "OPENAI_GPT_MODEL": "gpt-4o-mini",
    "SPEAKER1_NAME": "Chen",      # Asian-sounding name
    "SPEAKER2_NAME": "Sophia",    # European-sounding name
    "SPEAKER1_VOICE": "echo",
    "SPEAKER2_VOICE": "fable",    # British accent
    "DEFAULT_PODCAST_LENGTH": "12",
    "OUTPUT_DIRECTORY": "./international_podcasts"
}


# Example 6: Custom Speech Markers Configuration
CUSTOM_SPEECH_MARKERS = {
    "pause_short": "[brief-pause]",
    "pause_medium": "[pause]",
    "pause_long": "[long-pause]",
    "emphasis_start": "[strong]",
    "emphasis_end": "[/strong]",
    "breath": "[inhale]",
    "thoughtful": "[hmm]"
}


# Example 7: Production Configuration with Logging
PRODUCTION_CONFIG = {
    "OPENAI_API_KEY": "sk-your-api-key-here",
    "OPENAI_TTS_MODEL": "tts-1-hd",
    "OPENAI_GPT_MODEL": "gpt-4",
    "SPEAKER1_NAME": "Host",
    "SPEAKER2_NAME": "Guest",
    "SPEAKER1_VOICE": "alloy",
    "SPEAKER2_VOICE": "nova",
    "DEFAULT_PODCAST_LENGTH": "30",
    "OUTPUT_DIRECTORY": "/var/podcasts/production",
    "LOG_LEVEL": "INFO",
    "LOG_FILE": "/var/log/podcast-generator.log"
}


# Example 8: Development Configuration
DEVELOPMENT_CONFIG = {
    "OPENAI_API_KEY": "sk-your-api-key-here",
    "OPENAI_TTS_MODEL": "tts-1",  # Lower cost for development
    "OPENAI_GPT_MODEL": "gpt-3.5-turbo",
    "SPEAKER1_NAME": "TestSpeaker1",
    "SPEAKER2_NAME": "TestSpeaker2",
    "SPEAKER1_VOICE": "alloy",
    "SPEAKER2_VOICE": "nova",
    "DEFAULT_PODCAST_LENGTH": "1",  # Short for testing
    "OUTPUT_DIRECTORY": "./test_podcasts"
}


# Example 9: MCP Client Configuration (for Claude Desktop)
MCP_CLIENT_CONFIG = {
    "podcast-generator": {
        "command": "uv",
        "args": [
            "--directory",
            "/path/to/podcast-mcp",
            "run",
            "podcast_server.py"
        ],
        "env": BASIC_CONFIG
    }
}


# Example 10: Custom Voice Mapping
class VoicePersonalities:
    """Define voice personalities for different use cases"""
    
    PROFESSIONAL = {
        "SPEAKER1_VOICE": "fable",    # Authoritative
        "SPEAKER2_VOICE": "echo"      # Warm but professional
    }
    
    CASUAL = {
        "SPEAKER1_VOICE": "alloy",    # Friendly
        "SPEAKER2_VOICE": "shimmer"   # Soft and engaging
    }
    
    DRAMATIC = {
        "SPEAKER1_VOICE": "onyx",     # Deep and dramatic
        "SPEAKER2_VOICE": "nova"      # Clear and expressive
    }


# Example Usage Functions
def get_config_for_genre(genre: str) -> Dict[str, Any]:
    """Get configuration based on podcast genre"""
    genre_configs = {
        "education": EDUCATIONAL_CONFIG,
        "news": NEWS_CONFIG,
        "casual": CASUAL_CONFIG,
        "tech": BASIC_CONFIG,
        "international": INTERNATIONAL_CONFIG
    }
    
    return genre_configs.get(genre.lower(), BASIC_CONFIG)


def create_custom_config(
    speakers: tuple,
    voices: tuple,
    duration: int = 10,
    quality: str = "standard"
) -> Dict[str, Any]:
    """Create a custom configuration"""
    tts_model = "tts-1-hd" if quality == "high" else "tts-1"
    
    return {
        "OPENAI_API_KEY": "sk-your-api-key-here",
        "OPENAI_TTS_MODEL": tts_model,
        "OPENAI_GPT_MODEL": "gpt-4o-mini",
        "SPEAKER1_NAME": speakers[0],
        "SPEAKER2_NAME": speakers[1],
        "SPEAKER1_VOICE": voices[0],
        "SPEAKER2_VOICE": voices[1],
        "DEFAULT_PODCAST_LENGTH": str(duration),
        "OUTPUT_DIRECTORY": f"./podcasts_{speakers[0].lower()}_{speakers[1].lower()}"
    }


# Example configuration templates for specific scenarios
SCENARIO_TEMPLATES = {
    "tech_interview": {
        "speakers": ("Interviewer", "CTO"),
        "voices": ("alloy", "onyx"),
        "duration": 25,
        "style": "professional"
    },
    
    "startup_pitch": {
        "speakers": ("Founder", "Investor"),
        "voices": ("nova", "fable"),
        "duration": 15,
        "style": "business"
    },
    
    "science_podcast": {
        "speakers": ("Dr. Smith", "Prof. Johnson"),
        "voices": ("echo", "fable"),
        "duration": 30,
        "style": "educational"
    }
}


if __name__ == "__main__":
    # Example of how to use these configurations
    print("Available configuration examples:")
    
    configs = [
        ("Basic", BASIC_CONFIG),
        ("Educational", EDUCATIONAL_CONFIG),
        ("News", NEWS_CONFIG),
        ("Casual", CASUAL_CONFIG),
        ("Production", PRODUCTION_CONFIG)
    ]
    
    for name, config in configs:
        print(f"\n{name} Configuration:")
        print(f"  Speakers: {config['SPEAKER1_NAME']} and {config['SPEAKER2_NAME']}")
        print(f"  Voices: {config['SPEAKER1_VOICE']} and {config['SPEAKER2_VOICE']}")
        print(f"  Duration: {config['DEFAULT_PODCAST_LENGTH']} minutes")
        print(f"  Model: {config['OPENAI_TTS_MODEL']}")
    
    # Example of creating a custom configuration
    print("\nCustom configuration example:")
    custom = create_custom_config(
        speakers=("Alice", "Bob"),
        voices=("shimmer", "onyx"),
        duration=8,
        quality="high"
    )
    print(f"Custom config created for {custom['SPEAKER1_NAME']} and {custom['SPEAKER2_NAME']}")
    
    print("\n--- Created by Muhammad Waqas ---")