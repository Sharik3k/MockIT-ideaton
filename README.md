# MockIT - Recruiter Tool for Hackathon

A comprehensive recruiter tool that helps manage vacancies, candidates, and provides mock AI analysis for demo purposes. Built for a 5-hour hackathon with FastAPI backend and vanilla JavaScript frontend.

## 🚀 Features

### Backend (FastAPI)
- **Authentication**: Simple token-based auth for recruiters
- **Workspace Management**: Company/workspace profile with onboarding
- **Team Invites**: Simple in-memory team invitation system
- **Vacancy Management**: Create, view, and update job vacancies
- **Candidate Management**: Track candidates with skills and notes
- **Resume Upload**: File upload for candidate resumes (PDF/DOCX)
- **Candidate-Vacancy Linking**: Connect candidates to specific vacancies
- **Mock AI Analysis**: Demo match analysis and interview questions

### Frontend (HTML/CSS/JS)
- **Modern UI**: Clean, responsive design with Tailwind-inspired styling
- **Onboarding Flow**: Complete setup wizard for new recruiters
- **Dashboard**: Main workspace with all key features
- **Company Setup**: Configure company profile and hiring preferences
- **Hiring Management**: Manage vacancies and candidates
- **Team Invitations**: Invite team members to collaborate
- **Authentication**: Login and registration screens

## 📁 Project Structure

```
MockIT/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── core/           # Store, config, utilities
│   │   ├── schemas/        # Pydantic models
│   │   ├── services/       # Business logic
│   │   ├── routes/         # API endpoints
│   │   └── main.py         # FastAPI app
│   ├── uploads/            # Resume storage
│   ├── requirements.txt    # Dependencies
│   └── README.md          # Backend docs
├── frontend/               # HTML/CSS/JS frontend
│   ├── index.html         # Main dashboard
│   ├── login.html         # Authentication
│   ├── welcome.html       # Onboarding welcome
│   ├── company.html       # Company setup
│   ├── hiring.html        # Hiring preferences
│   ├── invite.html        # Team invitations
│   ├── styles.css         # Complete styling
│   ├── script.js          # Frontend logic
│   └── assets/            # Images and icons
└── README.md              # This file
```

## 🛠 Tech Stack

### Backend
- **FastAPI**: Modern Python web framework
- **Uvicorn**: ASGI server
- **Pydantic**: Data validation
- **Python-multipart**: File upload support
- **In-memory storage**: No database required

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Modern styling with animations
- **Vanilla JavaScript**: No framework dependencies
- **Responsive Design**: Mobile-friendly interface

## 🚀 Quick Start

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Start the server:
```bash
python -m app.main
```

Backend will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Open `index.html` in your browser or use a local server:
```bash
python -m http.server 8001
```

Frontend will be available at `http://localhost:8001`

## 📚 API Documentation

Backend API documentation is available at:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### Key Endpoints

#### Authentication
- `POST /auth/register` - Register new user and workspace
- `POST /auth/login` - Login user
- `GET /auth/me` - Get current user and workspace

#### Workspace
- `GET /workspace` - Get current workspace
- `PATCH /workspace` - Update workspace with onboarding data

#### Team Invites
- `POST /workspace/invites` - Create team invite
- `GET /workspace/invites` - List workspace invites
- `PATCH /workspace/invites/{id}` - Update invite status

#### Vacancies
- `POST /vacancies` - Create vacancy
- `GET /vacancies` - List workspace vacancies
- `GET /vacancies/{id}` - Get vacancy details
- `PATCH /vacancies/{id}` - Update vacancy

#### Candidates
- `POST /candidates` - Create candidate
- `GET /candidates` - List workspace candidates
- `GET /candidates/{id}` - Get candidate details
- `PATCH /candidates/{id}` - Update candidate

#### Resumes
- `POST /candidates/{candidate_id}/resumes` - Upload resume
- `GET /candidates/{candidate_id}/resumes` - List candidate resumes

#### Links (Candidate-Vacancy)
- `POST /links` - Link candidate to vacancy
- `GET /vacancies/{vacancy_id}/candidates` - Get linked candidates
- `GET /candidates/{candidate_id}/vacancies` - Get linked vacancies

#### Mock Analysis
- `POST /analysis/mock-match` - Generate mock match analysis
- `POST /analysis/mock-questions` - Generate mock interview questions

## 🎯 Frontend Features

### Onboarding Flow
1. **Welcome Screen**: Introduction to MockIT
2. **Company Setup**: Basic company information
3. **Hiring Preferences**: Goals, roles, and volume
4. **Team Invitations**: Add team members
5. **Complete Setup**: Start using the platform

### Main Dashboard
- **Navigation**: Easy access to all features
- **Quick Stats**: Overview of hiring activity
- **Recent Activity**: Latest candidates and vacancies
- **Quick Actions**: Create new vacancies or candidates

### Management Screens
- **Vacancy Management**: Create, edit, and track job postings
- **Candidate Management**: Add candidates with skills and resumes
- **Team Management**: Invite and manage team members
- **Settings**: Update workspace and profile information

## ⚠️ Important Notes

- **Data Storage**: All data is stored in memory and resets when the server restarts
- **File Uploads**: Resume files are stored locally in `backend/uploads/`
- **Mock AI**: Analysis endpoints use rule-based logic for demo purposes
- **No Database**: Intentionally designed for rapid hackathon development
- **Email**: Team invites don't send real emails (demo only)

## 🔧 Development Notes

- Built for a 5-hour hackathon MVP
- Prioritizes speed and simplicity over scalability
- Clean, modular structure for easy extension
- Frontend-friendly JSON responses
- Comprehensive error handling and validation
- CORS enabled for local development

## 🚀 Future Enhancements

- Replace in-memory storage with PostgreSQL/MongoDB
- Implement real AI analysis with OpenAI API
- Add email notifications for team invites
- Implement advanced search and filtering
- Add file parsing for resume text extraction
- Implement role-based permissions and access control
- Add audit logging and activity tracking
- Create mobile app version
- Add integrations with job boards and LinkedIn

## 📄 License

MIT License - feel free to use for your projects!

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

**Built with ❤️ for hackathon demo purposes**
