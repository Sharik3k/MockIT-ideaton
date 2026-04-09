# MockIT Backend

A lightweight FastAPI backend for a hackathon recruiter tool that helps manage vacancies, candidates, and provides mock AI analysis for demo purposes.

## Features

- **Authentication**: Simple token-based auth for recruiters
- **Workspace Management**: Company/workspace profile management
- **Onboarding Support**: Hiring goals, role types, volume tracking
- **Team Invites**: Simple in-memory team invitation system
- **Vacancy Management**: Create, view, and update job vacancies
- **Candidate Management**: Track candidates with skills and notes
- **Resume Upload**: File upload for candidate resumes (PDF/DOCX)
- **Candidate-Vacancy Linking**: Connect candidates to specific vacancies
- **Mock AI Analysis**: Demo match analysis and interview questions

## Tech Stack

- **FastAPI**: Modern Python web framework
- **Uvicorn**: ASGI server
- **Pydantic**: Data validation
- **Python-multipart**: File upload support
- **In-memory storage**: No database required (data resets on server restart)

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create uploads directory (optional, will be created automatically):
```bash
mkdir uploads
```

## Running the Server

Start the development server:

```bash
python -m app.main
```

Or using uvicorn directly:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Available Endpoints

### Authentication
- `POST /auth/register` - Register new user and workspace
- `POST /auth/login` - Login user
- `GET /auth/me` - Get current user and workspace

### Workspace
- `GET /workspace` - Get current workspace
- `PATCH /workspace` - Update workspace

### Team Invites
- `POST /workspace/invites` - Create team invite
- `GET /workspace/invites` - List workspace invites
- `PATCH /workspace/invites/{id}` - Update invite status

### Vacancies
- `POST /vacancies` - Create vacancy
- `GET /vacancies` - List workspace vacancies
- `GET /vacancies/{id}` - Get vacancy details
- `PATCH /vacancies/{id}` - Update vacancy

### Candidates
- `POST /candidates` - Create candidate
- `GET /candidates` - List workspace candidates
- `GET /candidates/{id}` - Get candidate details
- `PATCH /candidates/{id}` - Update candidate

### Resumes
- `POST /candidates/{candidate_id}/resumes` - Upload resume
- `GET /candidates/{candidate_id}/resumes` - List candidate resumes

### Links (Candidate-Vacancy)
- `POST /links` - Link candidate to vacancy
- `GET /vacancies/{vacancy_id}/candidates` - Get linked candidates for vacancy
- `GET /candidates/{candidate_id}/vacancies` - Get linked vacancies for candidate

### Mock Analysis
- `POST /analysis/mock-match` - Generate mock match analysis
- `POST /analysis/mock-questions` - Generate mock interview questions

## Authentication

The API uses simple token-based authentication:

1. Register or login to get a token
2. Include the token in the `Authorization` header: `Bearer <token>`
3. All protected endpoints require valid authentication

## File Upload

- **Supported formats**: PDF, DOCX
- **Max file size**: 10MB
- **Storage location**: `uploads/` directory
- **Files are stored locally with unique filenames**

## Data Storage

⚠️ **Important**: This is a hackathon MVP with temporary storage

- All data is stored in memory and resets when the server restarts
- No database is used (intentionally for rapid development)
- File uploads persist in the `uploads/` directory
- This is acceptable for demo purposes but not for production

## Mock AI Analysis

The analysis endpoints provide realistic demo data:

### Match Analysis
- Calculates skill overlap between candidate and vacancy
- Generates match scores (0-100)
- Identifies missing skills and potential risks
- Uses simple rule-based logic

### Interview Questions
- Generates 4-8 relevant interview questions
- Categories: resume, skill verification, project, behavioral
- Questions adapt to candidate skills and vacancy requirements
- Provides reasoning for each generated question

## Future Enhancements

- Replace in-memory storage with PostgreSQL/MongoDB
- Implement real AI analysis with OpenAI API
- Add email notifications
- Implement advanced search and filtering
- Add file parsing for resume text extraction
- Implement role-based permissions
- Add audit logging

## Development Notes

- Built for a 5-hour hackathon MVP
- Prioritizes speed and simplicity over scalability
- Clean, modular structure for easy extension
- Frontend-friendly JSON responses
- Comprehensive error handling and validation

## CORS Configuration

The API is configured to work with local React development servers:
- `http://localhost:3000`
- `http://127.0.0.1:3000`
- `http://localhost:5173`
- `http://127.0.0.1:5173`

## License

MIT License - feel free to use for your projects!
