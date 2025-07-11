# ElderTech Voice Assistant - Backend

This is the FastAPI backend for the ElderTech Voice Assistant, providing AI-powered voice interaction, conversation management, and knowledge base functionality.

## 🏗️ Architecture

```
backend/
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Python dependencies
├── env.example            # Environment variables template
├── routers/               # API route handlers
│   ├── __init__.py
│   ├── auth.py           # Authentication endpoints
│   ├── chat.py           # Chat/conversation endpoints
│   ├── faqs.py           # FAQ management endpoints
│   └── whisper.py        # Speech processing endpoints
├── services/              # Business logic and external integrations
│   ├── __init__.py
│   ├── db.py             # Database models and operations
│   ├── openai.py         # OpenAI GPT integration
│   ├── tts.py            # Text-to-speech service
│   └── whisper.py        # Speech-to-text service
└── scripts/               # Utility scripts
    ├── __init__.py
    └── nightly_faq_clustering.py  # FAQ organization script
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- OpenAI API key
- SQLite (or PostgreSQL for production)

### Installation

1. **Clone the repository**
   ```bash
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp env.example .env
   # Edit .env with your actual values
   ```

5. **Run the application**
   ```bash
   python main.py
   ```

The API will be available at `http://localhost:8000`

## 📚 API Documentation

Once the server is running, you can access:
- **Interactive API docs**: http://localhost:8000/docs
- **ReDoc documentation**: http://localhost:8000/redoc
- **Health check**: http://localhost:8000/health

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | Database connection string | `sqlite:///./eldertech.db` |
| `OPENAI_API_KEY` | OpenAI API key | Required |
| `OPENAI_MODEL` | OpenAI model to use | `gpt-4o-mini` |
| `JWT_SECRET_KEY` | JWT signing key | Required |
| `JWT_ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration time | `30` |
| `HOST` | Server host | `0.0.0.0` |
| `PORT` | Server port | `8000` |
| `DEBUG` | Debug mode | `True` |

## 🗄️ Database

The application uses SQLAlchemy with SQLite by default. The database includes:

- **Users**: User accounts and profiles
- **Conversations**: Chat conversation history
- **Messages**: Individual messages within conversations
- **FAQs**: Knowledge base entries
- **FAQ Categories**: Organization of FAQs
- **FAQ Feedback**: User feedback on FAQ helpfulness

### Database Setup

The database is automatically created when you first run the application. For production, consider using PostgreSQL:

```bash
# Update DATABASE_URL in .env
DATABASE_URL=postgresql://user:password@localhost/eldertech
```

## 🔐 Authentication

The API uses JWT tokens for authentication. Endpoints are protected with:

```python
from fastapi.security import HTTPBearer
security = HTTPBearer()
```

## 🎤 Voice Processing

### Speech-to-Text (Whisper)
- Supports multiple audio formats (WAV, MP3, OGG, FLAC)
- Automatic language detection
- Word-level timestamps
- Batch processing

### Text-to-Speech (OpenAI TTS)
- Multiple voice options (Alloy, Echo, Fable, Onyx, Nova, Shimmer)
- Adjustable speech speed
- Streaming audio responses

## 🤖 AI Integration

The ElderTech assistant is specialized for elderly care with:
- Compassionate, patient responses
- Simple, clear language
- Health and wellness support
- Emergency contact assistance
- Daily task reminders

## 📊 FAQ Management

The system includes intelligent FAQ organization:
- Semantic clustering
- Gap analysis
- Priority scoring
- User feedback collection
- Nightly clustering script

## 🧪 Testing

Run tests with pytest:

```bash
pytest
```

## 📝 Development

### Code Structure

- **Routers**: Handle HTTP requests and responses
- **Services**: Contain business logic and external API calls
- **Models**: Database schema definitions
- **Scripts**: Utility scripts for maintenance tasks

### Adding New Features

1. Create new router in `routers/`
2. Add business logic in `services/`
3. Update database models if needed
4. Add tests
5. Update documentation

## 🚀 Deployment

### Production Considerations

1. **Use PostgreSQL** instead of SQLite
2. **Set up proper logging**
3. **Configure CORS** for your frontend domain
4. **Use environment variables** for all secrets
5. **Set up monitoring** and health checks
6. **Configure rate limiting**
7. **Use HTTPS** in production

### Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
