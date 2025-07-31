# Open General Agent

A basic Python agent example that searches for articles from the web and Wikipedia using LangChain and Google's Gemini AI. This is a simple demonstration of how to build an AI-powered search agent with FastAPI.

## Features

- 🔍 Web search integration using DuckDuckGo
- 📚 Wikipedia search integration
- 🤖 AI-powered response generation using Google Gemini
- 🚀 FastAPI REST API
- 📊 Structured JSON responses
- 🔧 Easy setup and configuration

## Prerequisites

- Python 3.10 or higher
- Google Gemini API key

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd back-open-agent
   ```

2. **Create a virtual environment**
   ```bash
   python3 -m venv .venv
   ```

3. **Activate the virtual environment**
   
   **On Linux/macOS:**
   ```bash
   source .venv/bin/activate
   ```
   
   **On Windows:**
   ```bash
   .venv\Scripts\activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. **Copy the environment file**
   ```bash
   cp .env.example .env
   ```

2. **Edit the `.env` file**
   ```bash
   nano .env
   ```
   
   Add your Google Gemini API key:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

   **Note:** You need to obtain a Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey).

## Running the Application

### Development Mode

Start the server with auto-reload:
```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`

### Production Mode

Start the server without auto-reload:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## API Usage

### Search Articles

**Endpoint:** `GET /api/agent/articles`

**Parameters:**
- `query` (required): The search query
- `limit` (optional): Number of results to return (default: 10)

**Example Request:**
```bash
curl "http://127.0.0.1:8000/api/agent/articles?query=capital%20of%20argentina&limit=3"
```

**Example Response:**
```json
{
  "articles": [
    {
      "title": "Buenos Aires - Wikipedia",
      "description": "Comprehensive information about Buenos Aires, the capital of Argentina",
      "image_url": "https://example.com/image.jpg",
      "link": "https://en.wikipedia.org/wiki/Buenos_Aires",
      "score": 0.95
    }
  ]
}
```

### Root Endpoint

**Endpoint:** `GET /`

Returns a simple welcome message:
```json
{
  "message": "Open General Agent API"
}
```

## Project Structure

```
back-open-agent/
├── api/
│   ├── endpoints/
│   │   └── agent.py          # API endpoints
│   └── schemas/
│       └── responseSchemas.py # Pydantic models
├── repositories/
│   └── articles_repository.py # Business logic
├── tools/
│   └── tools.py              # LangChain tools
├── main.py                   # FastAPI application
├── requirements.txt          # Python dependencies
├── .env.example             # Environment variables template
└── README.md                # This file
```

## Dependencies

- **FastAPI**: Modern web framework for building APIs
- **LangChain**: Framework for developing applications with LLMs
- **Google Generative AI**: Integration with Google's Gemini model
- **DuckDuckGo Search**: Web search functionality
- **Wikipedia**: Wikipedia search integration
- **Pydantic**: Data validation using Python type annotations
- **Uvicorn**: ASGI server for running FastAPI applications

## Development

### Adding New Tools

To add new search tools, modify the `tools/tools.py` file and add them to the `tools` list in `repositories/articles_repository.py`.

### Modifying Response Schema

To change the response format, update the `ArticlesResearchResponse` model in `api/schemas/responseSchemas.py`.

## Troubleshooting

### Common Issues

1. **"GEMINI_API_KEY not found"**
   - Make sure you've created a `.env` file with your API key
   - Verify the API key is valid and has sufficient credits

2. **"Module not found" errors**
   - Ensure you're in the virtual environment
   - Run `pip install -r requirements.txt` again

3. **"Port already in use"**
   - Change the port: `uvicorn main:app --reload --port 8001`
   - Or kill the existing process using the port

### Logs

The application provides detailed logs when running in verbose mode. Check the terminal output for debugging information.

## Contributing

This is a basic example project. Feel free to fork and extend it with additional features like:

- Database integration
- User authentication
- Rate limiting
- Caching
- Additional search sources
- More sophisticated response processing

## License

This project is provided as an educational example. Use it as a starting point for your own AI agent projects.

## Support

For issues related to:
- **Google Gemini API**: Check the [Google AI documentation](https://ai.google.dev/)
- **LangChain**: Visit the [LangChain documentation](https://python.langchain.com/)
- **FastAPI**: Check the [FastAPI documentation](https://fastapi.tiangolo.com/) 