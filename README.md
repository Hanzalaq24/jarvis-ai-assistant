# 🤖 JARVIS - AI Voice Assistant

A sophisticated AI voice assistant inspired by Tony Stark's JARVIS, built with Python, Flask, and modern web technologies. Features natural language processing, song recognition, system control, and intelligent responses.

## ✨ Features

### 🎤 Voice & Audio
- **Voice Recognition**: Real-time speech-to-text processing
- **Text-to-Speech**: Natural voice responses
- **Song Recognition**: Identify songs from singing, humming, or background audio
- **Audio Analysis**: Advanced frequency analysis for song identification

### 🧠 AI Intelligence
- **Natural Conversations**: Powered by Groq API (Llama 3) for intelligent responses
- **Built-in Knowledge**: Extensive knowledge base for common queries
- **Multi-language Support**: English, Hindi, and Gujarati
- **Context Awareness**: Maintains conversation context

### 🖥️ System Control
- **Screenshot Capture**: Take and save screenshots
- **Photo Capture**: Camera integration for photos
- **Volume Control**: System volume management
- **Application Launcher**: Open applications and websites
- **File Operations**: Search and manage files

### 🔍 Smart Search
- **Web Search**: Google, YouTube, Wikipedia integration
- **File Search**: Intelligent file finding with fuzzy matching
- **Song Search**: Lyrics-based song identification
- **Multi-platform Search**: Various search engines and platforms

### 📁 Improved File Operations (New)
- Implicit file creation: commands like "create note.txt" or "create notes" work
- Smarter delete/restore to Trash on macOS, permanent delete option
- Enhanced search with numbered open: "open file 1" after a search
- Optional auto-open for captured photos
- Modular improvements via `improved_file_operations` and `improved_command_processor` if present

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- macOS/Linux/Windows
- Microphone access
- Internet connection

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/Hanzalaq24/jarvis-ai-assistant.git
cd jarvis-ai-assistant
```

2. **Create virtual environment**
```bash
python -m venv jarvis_env
source jarvis_env/bin/activate  # On Windows: jarvis_env\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up API keys (Optional but recommended)**
```bash
echo "GROQ_API_KEY=your_groq_api_key_here" > .env   # Or export in your shell
# export GROQ_API_KEY="your_groq_api_key_here"
```
Get your free API key from [Groq Console](https://console.groq.com/)

5. **Run JARVIS**
```bash
python app.py
```

6. **Open in browser**
Navigate to `http://localhost:8888`
   - The server binds to `127.0.0.1:8888` by default. If the port is busy, change the port in `app.py`.

### Alternative run
```bash
export FLASK_APP=app.py
export FLASK_RUN_PORT=8888
flask run
```

## 🎯 Usage Examples

### Voice Commands
- **"Hey JARVIS, what time is it?"**
- **"Hey JARVIS, take a screenshot"**
- **"Hey JARVIS, recognize this song"** (while music is playing)
- **"Hey JARVIS, search for Python tutorials"**
- **"Hey JARVIS, open YouTube"**
- **"Hey JARVIS, the song goes: we are the champions"**

### Song Recognition
- **Background Music**: "recognize this song" - JARVIS listens to background audio
- **Singing/Humming**: "listen to me sing" - Record yourself singing
- **Lyrics Search**: "the song goes: shape of you" - Search by lyrics

### System Control
- **Screenshots**: "take a screenshot"
- **Photos**: "take a photo"
- **Volume**: "volume up", "mute volume"
- **Applications**: "open Chrome", "open Spotify"

### File commands (quick examples)
- Create file: "create file note.txt" or simply "create note" (creates note.txt on Desktop)
- Create folder: "create folder MyWork"
- Find: "find file report.pdf"
- Open from results: "open file 1"
- Delete: "delete file report.pdf" or "delete file report.pdf permanently"
- Restore: "restore file report.pdf"
- Rename: "rename file report.pdf to final_report.pdf"

## 🛠️ Technical Architecture

### Backend (Python/Flask)
- **Flask Web Server**: RESTful API endpoints
- **Speech Recognition**: Real-time audio processing
- **AI Integration**: Groq API for intelligent responses
- **System Integration**: OS-level operations
- **Audio Processing**: Song recognition and analysis

### Frontend (HTML/CSS/JavaScript)
- **Modern UI**: Responsive design with animations
- **Voice Interface**: Web Speech API integration
- **Real-time Updates**: WebSocket-like communication
- **Audio Visualization**: Recording indicators and feedback

### Key Components
- `app.py` - Main Flask application and command processing
- `ai_assistant.py` - AI intelligence and response generation
- `static/js/jarvis.js` - Frontend voice interface and interactions
- `templates/index.html` - Main web interface
 - (Optional) `improved_file_operations.py` and `improved_command_processor.py` - enhanced file features

## 🔌 REST API

All endpoints are served from `http://127.0.0.1:8888` by default.

- `POST /api/command` — execute a natural-language command
  - Body: `{ "command": "create note.txt" }`
- `POST /api/speak` — server-side TTS
  - Body: `{ "text": "Hello", "language": "en" }`
- `POST /api/translate` — translate text (if libs installed)
  - Body: `{ "text": "Hello", "target_lang": "hi" }`
- `GET /api/system-status` — feature availability and permissions
- `POST /api/capture-photo` — capture a photo
- `POST /api/take-screenshot` — take a screenshot
- `POST /api/ai-query` — direct AI query
- `POST /api/song-recognition` — lyrics or recording-based flow
- `POST /api/test-file-operation` — quick file ops self-test

## 🔧 Configuration

### Environment Variables
```bash
# Optional: Enhanced AI responses
export GROQ_API_KEY="your_groq_api_key"

# Optional: Custom wake word
export WAKE_WORD="jarvis"
```

### Supported Platforms
- ✅ macOS (Full support)
- ✅ Linux (Full support)
- ⚠️ Windows (Limited TTS support)

## 🎵 Song Recognition System

JARVIS features an advanced song recognition system with multiple identification methods:

### Recognition Methods
1. **Background Audio Analysis**: Listens to songs playing from speakers
2. **Singing/Humming Recognition**: Records and analyzes your voice
3. **Lyrics-based Search**: Matches song lyrics to database

### How It Works
1. **Audio Capture**: Uses Web Audio API for real-time audio processing
2. **Frequency Analysis**: Extracts dominant frequencies and patterns
3. **Pattern Matching**: Compares audio fingerprints
4. **Lyrics Integration**: Combines audio analysis with lyric matching
5. **YouTube Integration**: Automatically plays identified songs

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit changes**: `git commit -m 'Add amazing feature'`
4. **Push to branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**

### Development Setup
```bash
# Use the main requirements for dev as well
pip install -r requirements.txt

# (If you add tests later)
# python -m pytest tests/

# Code quality (both are included in requirements.txt)
black . && flake8 .
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Developer

**Hanzala Qureshi**
- GitHub: [@Hanzalaq24](https://github.com/Hanzalaq24)
- Email: hanzalaqureshi24@gmail.com

## 🙏 Acknowledgments

- Inspired by Tony Stark's JARVIS from Marvel
- Built with modern web technologies and AI
- Thanks to the open-source community for amazing libraries

## 🐛 Known Issues & Troubleshooting

### Common Issues
1. **Microphone Access**: Ensure browser has microphone permissions
2. **TTS Not Working**: Some systems may have limited TTS support
3. **Song Recognition**: Requires clear audio for best results

### Performance Tips
- Use Chrome/Firefox for best compatibility
- Ensure stable internet connection for AI features
- Close other audio applications for better song recognition

### Port and binding
- Default bind is `127.0.0.1:8888`. If you can’t access it:
  - Ensure the server is running without errors: `python3 app.py`
  - Check for conflicts: `lsof -iTCP:8888 -sTCP:LISTEN`
  - Change port in the `if __name__ == '__main__':` block in `app.py`

### macOS permissions
- Allow microphone access in your browser for voice features
- If photo/screenshot fail, grant screen/camera permissions in System Settings

## 🔮 Future Enhancements

- [ ] Mobile app version
- [ ] Smart home integration
- [ ] Advanced AI conversation memory
- [ ] Custom voice training
- [ ] Plugin system for extensions
- [ ] Real-time language translation
- [ ] Enhanced song database
- [ ] Offline mode capabilities

---

**Made with ❤️ by Hanzala Qureshi**

*"Sometimes you gotta run before you can walk." - Tony Stark*