# 🎙️ Podcast Generator MCP Server

<div align="center">

![Podcast Generator](https://img.shields.io/badge/Podcast-Generator-blue)
![MCP](https://img.shields.io/badge/MCP-Model_Context_Protocol-green)
![OpenAI](https://img.shields.io/badge/OpenAI-TTS-orange)
![Python](https://img.shields.io/badge/Python-3.8+-yellow)
![License](https://img.shields.io/badge/License-MIT-red)

</div>

## 🔥 Overview

**Podcast Generator MCP** is a powerful Model Context Protocol (MCP) server that converts text content into realistic podcast conversations. Using OpenAI's advanced Text-to-Speech technology, it creates natural dialogue between two AI speakers with customizable voices and speech patterns.

### ✨ Key Features

- 🤖 **Dual AI Hosts**: Configurable speaker names and voices
- 🗣️ **Natural Speech**: Supports pauses, emphasis, breaths, and thoughtful moments
- 🎯 **Customizable Length**: Adjustable podcast duration (1-60 minutes)
- 📝 **Smart Text Processing**: Handles long content with intelligent chunking
- 🔊 **Multiple Voices**: All OpenAI TTS voices supported
- 📁 **Organized Output**: Timestamped MP3 files with metadata

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- OpenAI API Key
- `uv` package manager (or pip)

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/mwaqas-sudo/podcast_mcp.git
   cd podcast_mcp
   ```

2. **Install dependencies**

   ```bash
   # Using uv (recommended)
   uv pip install -r requirements.txt

   # Or using pip
   pip install -r requirements.txt
   ```

3. **Set up your OpenAI API key**
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```

### Configuration

The server can be configured through environment variables:

```python
# Default Configuration
SPEAKER1_NAME = "Alex"           # First speaker name
SPEAKER2_NAME = "Jordan"         # Second speaker name
SPEAKER1_VOICE = "alloy"         # First speaker voice
SPEAKER2_VOICE = "nova"          # Second speaker voice
DEFAULT_PODCAST_LENGTH = "10"    # Default podcast length in minutes
OUTPUT_DIRECTORY = "./podcasts"  # Output directory for MP3 files
OPENAI_TTS_MODEL = "tts-1"      # OpenAI TTS model
OPENAI_GPT_MODEL = "gpt-4o-mini" # OpenAI GPT model (for future features)
```

---

## 📖 Usage

### 1. As an MCP Server

Add to your MCP client configuration (e.g., Claude Desktop):

```json
{
  "podcast-generator": {
    "command": "uv",
    "args": ["--directory", "/path/to/podcast-mcp", "run", "podcast_server.py"],
    "env": {
      "OPENAI_API_KEY": "your-key-here",
      "SPEAKER1_NAME": "Michael",
      "SPEAKER2_NAME": "Sarah",
      "SPEAKER1_VOICE": "onyx",
      "SPEAKER2_VOICE": "nova"
    }
  }
}
```

### 2. Direct Usage

```python
from podcast_server import PodcastGenerator, ServerConfig

# Create configuration
config = ServerConfig(
    openai_api_key="your-key-here",
    speaker1_name="Alex",
    speaker2_name="Jordan"
)

# Generate podcast
generator = PodcastGenerator(config)
result = await generator.generate_podcast(request)
```

---

## 🎯 How It Works

<div align="center">

<img width="181" alt="Image" src="https://github.com/user-attachments/assets/05a446a2-d6ee-461f-b171-30fcb863ab4e" />

</div>

### Processing Flow

1. **Input Parsing**: Takes title and dialogue text
2. **Speaker Assignment**: Identifies and assigns text to speakers
3. **Text Processing**: Handles speech markers and formatting
4. **Voice Synthesis**: Converts text to speech using OpenAI TTS
5. **Audio Assembly**: Combines segments with appropriate pauses
6. **Export**: Saves final podcast as timestamped MP3 file

---

## 🎙️ Speech Markers

Enhance your dialogue with natural speech patterns:

```
[pause-short]     # 0.3s pause
[pause-medium]    # 0.7s pause
[pause-long]      # 1.2s pause
[emphasis]text[/emphasis]  # Emphasize text
[breath]          # Natural breath sound
[thoughtful]      # Moment of consideration
```

### Example Dialogue

```
Michael: Welcome to our podcast! [pause-short] Today we're discussing AI.
Sarah: Thanks for having me, Michael. [breath] I'm really excited to dive into this topic.
Michael: [thoughtful] You know, AI has been [emphasis]transforming[/emphasis] everything lately.
```

---

## 🗣️ Available Voices

Choose from OpenAI's voice options:

| Voice     | Characteristics               |
| --------- | ----------------------------- |
| `alloy`   | Neutral, versatile            |
| `echo`    | Warm, engaging                |
| `fable`   | British accent, authoritative |
| `onyx`    | Deep, resonant                |
| `nova`    | Young, energetic              |
| `shimmer` | Soft, soothing                |

---

## 📁 Project Structure

```
podcast_mcp/
├── podcast_server.py      # Main MCP server
├── requirements.txt       # Python dependencies
├── README.md             # Documentation
├── examples/             # Example configurations
│   ├── sample_dialogue.txt
│   └── config_examples.py

```

---

## 🔧 Advanced Features

### Custom Speech Processing

```python
# Create custom speech markers
markers = SpeechMarker(
    pause_short="[brief]",
    emphasis_start="[strong]",
    emphasis_end="[/strong]"
)

processor = TextProcessor(markers)
```

### Batch Processing

```python
# Generate multiple podcasts
requests = [
    PodcastRequest(title="Episode 1", dialogue="..."),
    PodcastRequest(title="Episode 2", dialogue="..."),
]

for request in requests:
    result = await generator.generate_podcast(request)
```

---

## 📊 Performance Metrics

The server provides detailed metrics for each podcast:

```json
{
  "title": "My Podcast",
  "target_duration_min": 10,
  "actual_duration_min": 9.8,
  "word_count": 1275,
  "segments_processed": 42,
  "file_size_mb": 14.2,
  "success": true
}
```

---

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙋‍♂️ Support

- **GitHub Issues**: Report bugs or request features
- **Email**: Contact waqasbilal02@gmail.com

---

## 📈 Roadmap

- [ ] Add background music support
- [ ] Implement emotion detection
- [ ] Multi-language support
- [ ] Real-time streaming
- [ ] Advanced editing features

---

<div align="center">

**Created by Muhammad Waqas** 🚀

[GitHub](https://github.com/mwaqas-sudo) | [LinkedIn](https://linkedin.com/in/mwaqas-sudo)

</div>

---

## 🔥 Examples

### Basic Podcast Generation

```python
dialogue = """
Michael: Welcome to Tech Talk! I'm Michael.
Sarah: And I'm Sarah. Today we're discussing the future of AI.
Michael: It's fascinating how quickly AI is evolving. [pause-short] What are your thoughts?
Sarah: [thoughtful] I think we're just scratching the surface.
"""

result = await generate_podcast_tool(
    title="Tech Talk Episode 1",
    dialogue=dialogue,
    podcast_length=5
)
```

### Custom Configuration

```json
{
  "env": {
    "OPENAI_API_KEY": "sk-...",
    "SPEAKER1_NAME": "Dr. Smith",
    "SPEAKER2_NAME": "Prof. Johnson",
    "SPEAKER1_VOICE": "fable",
    "SPEAKER2_VOICE": "echo",
    "DEFAULT_PODCAST_LENGTH": "15"
  }
}
```

---

## 🏆 Why Choose Podcast Generator MCP?

1. **Easy Integration**: Works seamlessly with MCP clients
2. **High Quality**: OpenAI's state-of-the-art TTS technology
3. **Customizable**: Full control over voices, speakers, and timing
4. **Production Ready**: Robust error handling and validation
5. **Open Source**: Free to use and modify

Start creating amazing podcasts today! 🎙️✨
