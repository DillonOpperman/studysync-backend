Here is the complete and final Markdown code for your **`README.md`** file, incorporating all the clean formatting, correct code blocks, and structured sections. You can copy this entire block and paste it directly into your file.

````markdown
# StudySync Backend 

This repository contains the backend service for **StudySync**, a study group recommendation and management application. It utilizes machine learning and semantic similarity techniques to match users based on their academic profiles and study preferences.

---

##  Key Technologies

The core of the application is built using the **Flask** web framework, with a heavy emphasis on **AI/ML** components for its recommendation engine.

### Backend Stack

* **Web Framework:** Flask 2.3.3
* **Database:** PostgreSQL (via **SQLAlchemy** and **psycopg2-binary**)
* **Deployment:** **Gunicorn** (production WSGI server)
* **APIs:** **Flask-CORS** (Cross-Origin Resource Sharing)

### AI/ML Components

* **Embeddings/Semantic Similarity:** **Sentence Transformers** (utilizing **BERT** models)
* **Deep Learning Framework:** **PyTorch 2.0.1**
* **Model Utilities:** **Transformers 4.33.2**
* **ML Algorithms:** **scikit-learn** (for similarity calculations and ML utilities)
    * *Note: This architecture uses **cosine similarity** on BERT embeddings for core matching.*

---

##  Prerequisites

Ensure you have the following installed on your system before proceeding:

* **Python 3.8+**
* **pip** package manager
* **Virtual Environment Tool** (recommended: `venv` or `virtualenv`)
* **Git** for version control
* **Docker** (Optional, for containerized deployment)

> **Compatibility Note:** Be aware that the specified versions of **PyTorch** (`torch==2.0.1`) and **Flask** (`Flask==2.3.3`) have specific compatibility requirements. Using newer Python versions (e.g., Python 3.11+) may lead to dependency issues with these packages.

---

##  Installation and Setup

Follow these steps to get the backend running locally.

### Step 1: Clone the Repository

```bash
git clone [https://github.com/YOUR_USERNAME/studysync-backend.git](https://github.com/YOUR_USERNAME/studysync-backend.git)
cd studysync-backend
````

### Step 2: Set Up Python Environment

It is highly recommended to use a virtual environment to isolate project dependencies.

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

Install all required packages listed in `requirements.txt`.

```bash
pip install -r requirements.txt
```

> **Note:** The first time you run the application, the **Sentence Transformers** library will automatically download the pre-trained **BERT model** (`all-MiniLM-L6-v2`, approximately 90MB). This is a one-time download.

### Step 4: Run the Application

Execute the main application file:

```bash
python app.py
```

The server will start and be accessible at **`http://localhost:5000`**.

-----

##  Verification and API Endpoints

### Health Check

Verify the server is running and the AI model has loaded successfully.

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/health` | Checks application status and AI model loading. |

**Example Verification (using `curl`):**

```bash
curl http://localhost:5000/api/health
```

**Expected Response:**

```json
{
  "status": "healthy",
  "ai_model": "loaded"
}
```

### Example AI Endpoint Responses

The following examples demonstrate the JSON structure for key AI-powered endpoints:

#### User Profile Creation (Example)

```json
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
```

#### Group Recommendation (Example)

```json
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
```

#### Group Search (Example)

```json
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
```

-----

##  Docker Deployment (Optional)

For containerized deployment, we suggest testing the build process.

> **Note on Dependencies:** When building into Docker, the most common issues encountered were related to version conflicts among **PyTorch**, **Transformers**, and **Flask**. Building the container is the best way to ensure the current `requirements.txt` is fully functional in an isolated environment.

-----

##  License and Acknowledgements

### License

This project is licensed under the **Apache License 2.0**.

### Author

  * Dillon Opperman

### Acknowledgements

We acknowledge the significant contributions of the following projects and teams:

  * **HuggingFace** for providing pre-trained BERT models.
  * **Sentence-Transformers library** for the semantic similarity tools.
  * **Microsoft Recommenders team** for inspiration on collaborative filtering algorithms.

<!-- end list -->

```
```
