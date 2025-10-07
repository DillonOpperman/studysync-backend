  The backend development for this app is the following.

Framework: Flask 2.3.3
AI/ML Libraries:
Sentence Transformers (BERT embeddings)
scikit-learn (cosine similarity, ML utilities)
PyTorch 2.0.1
Transformers 4.33.2

check the requirements.txt for more general information.

Ensure you have the folloiwng

Python 3.8+ installed
pip package manager
Virtual environment (recommended: venv or virtualenv)
Git for version control
Docker (optional, for containerized deployment)

Step 1: Clone the Repository
bashgit clone https://github.com/YOUR_USERNAME/studysync-backend.git
cd studysync-backend

Step 2: Set Up Python Environment
bash# Create virtual environment
python -m venv venv

# Activate virtual environment

# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate

Step 3: Install Dependencies

bashpip install -r requirements.txt

Note: The first time you run the application, Sentence Transformers will download the BERT model (all-MiniLM-L6-v2, ~90MB). This is a one-time download.

Step 4: Run the Application

bashpython app.py

The server will start on http://localhost:5000
Verify it's running:

bashcurl http://localhost:5000/api/health

# Expected response: {"status":"healthy","ai_model":"loaded"}

you know should have

# Web framework
Flask==2.3.3
flask-cors==4.0.0

# Data manipulation
pandas==2.0.3
numpy==1.24.3

# Machine Learning
scikit-learn==1.3.0

# Transformers & Sentence-BERT (compatible versions)
torch==2.0.1
transformers==4.33.2
sentence-transformers==2.2.2
huggingface_hub==0.15.1

# Database
SQLAlchemy==2.0.21
psycopg2-binary==2.9.7

# Utilities
python-dotenv==1.0.0
gunicorn==21.2.0

Type in the following

GET /api/health

you shoud see

{
  "status": "healthy",
  "ai_model": "loaded"
}

when you create a profile the terminal should show

{
  "id": "user_123",
  "name": "John Doe",
  "email": "john@university.edu",
  "university": "State University",
  "major": "Computer Science",
  "year": "Junior",
  "learningStyle": "I learn best with visual aids and hands-on practice",
  "subjects": ["Mathematics", "Computer Science", "Physics"],
  "studyEnvironments": ["Quiet Library", "Study Room"],
  "studyMethods": ["Flashcards", "Group Discussion"],
  "schedule": {
    "Monday": ["Evening (5-9 PM)"],
    "Wednesday": ["Evening (5-9 PM)"],
    "Friday": ["Afternoon (12-5 PM)"]
  },
  "performanceLevel": 4,
  "groupPreferences": {
    "groupSize": 4,
    "sessionDuration": 2,
    "studyGoals": ["Exam Preparation", "Concept Review"]
  }
}

then when getting a group recommends a group you should see

{
  "success": true,
  "recommendations": [
    {
      "id": 1,
      "title": "Computer Science Study Group",
      "matchPercentage": 92,
      "memberInfo": "3-5 members, actively seeking",
      "schedule": "Mon/Wed evenings",
      "focus": "Mathematics, Computer Science",
      "location": "Campus Study Areas",
      "action": "Request to Join",
      "suggested": false,
      "explanation": "High compatibility: Similar subjects, Compatible schedule, Similar learning style",
      "compatibility": {
        "subject": 0.85,
        "schedule": 0.78,
        "learningStyle": 0.89,
        "performance": 0.95
      }
    }
  ]
}


then when searching

{
  "results": [
    {
      "id": 1,
      "title": "Mathematics Group",
      "matchPercentage": 87,
      "memberInfo": "Actively seeking members",
      "schedule": "Mon/Wed evenings",
      "focus": "Calculus, Linear Algebra",
      "location": "Campus Study Areas",
      "action": "Request to Join",
      "suggested": false
    }
  ]
}


This project is licensed by apache 2.0 

author is by me, Dillon Opperman. I would like to acknowledge 

HuggingFace for pre-trained BERT models
Microsoft Recommenders team for collaborative filtering algorithms
Sentence-Transformers library for semantic similarity tools

This is not the full readme for the finished application, once this project is finsihed, I will give a updated version. 


