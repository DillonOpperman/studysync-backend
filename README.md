# StudySync Backend

This repository contains the backend service for **StudySync**, an AI-powered study group matching and management application. It utilizes machine learning and semantic similarity techniques to match students based on their academic profiles, schedules, and learning preferences.

---

##  Table of Contents

- [Overview](#overview)
- [Key Technologies](#key-technologies)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation and Setup](#installation-and-setup)
- [Database Setup](#database-setup)
- [Environment Configuration](#environment-configuration)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [AI Matching Algorithm](#ai-matching-algorithm)
- [Project Structure](#project-structure)
- [Troubleshooting](#troubleshooting)
- [License](#license)
- [Author](#author)
- [Acknowledgements](#acknowledgements)
- [YouTube Video](#youtube-video)
  [Model Documentation](#model-documentation)
---

##  Overview

StudySync Backend is a Flask-based REST API that provides:
- **User authentication** with JWT tokens and bcrypt password hashing
- **AI-powered student matching** using BERT semantic embeddings
- **Study group management** with MySQL database persistence
- **Real-time messaging** and group chat functionality
- **Intelligent recommendations** based on subjects, schedules, learning styles, and performance levels

The matching algorithm uses a multi-factor approach combining:
- Subject similarity (Jaccard index)
- Schedule overlap detection
- Learning style semantic similarity (BERT embeddings)
- Performance level compatibility

---

##  Key Technologies

### Backend Stack

* **Web Framework:** Flask 2.3.3
* **Database:** MySQL with SQLAlchemy 2.0.21 ORM
* **Authentication:** JWT tokens with PyJWT 2.8.0, bcrypt 4.1.1
* **Database Driver:** PyMySQL 1.1.0
* **Deployment:** Gunicorn 21.2.0 (production WSGI server)
* **APIs:** Flask-CORS 4.0.0 (Cross-Origin Resource Sharing)

### AI/ML Components

* **Embeddings/Semantic Similarity:** Sentence Transformers 2.2.2 (utilizing BERT models)
* **Deep Learning Framework:** PyTorch 2.0.1
* **Model Utilities:** Transformers 4.33.2
* **ML Algorithms:** scikit-learn 1.3.0 (for cosine similarity and compatibility scoring)
* **Pre-trained Model:** all-MiniLM-L6-v2 (~90MB, auto-downloaded on first run)

### Data Processing

* **Data Manipulation:** pandas 2.0.3, numpy 1.24.3
* **Configuration Management:** python-dotenv 1.0.0

---

##  Features

### Authentication & Security
-  User registration with email validation (.edu domain required)
-  Secure password hashing with bcrypt
-  JWT token-based authentication
-  Protected API endpoints with @token_required decorator
-  7-day token expiration

### AI-Powered Matching
-  BERT semantic embeddings for learning style similarity
-  Multi-factor compatibility scoring (subjects, schedule, learning style, performance)
-  Configurable match threshold (default: 50%)
-  Fallback recommendations when no matches found

### Study Group Management
-  Create and manage study groups
-  User-specific group isolation (each user sees only their groups)
-  Group membership tracking (leader/member roles)
-  Maximum member limits
-  Active/pending status management

### Messaging & Chat
-  Real-time group messaging
-  Message reactions (emoji support)
-  Image sharing capability
-  Message persistence in MySQL database
-  Announcement-type messages for study sessions

### Search & Discovery
-  Semantic search across all users using BERT embeddings
-  Subject-based filtering
-  Relevance ranking
-  Protected search endpoint (authentication required)

---

##  Prerequisites

Ensure you have the following installed on your system before proceeding:

* **Python 3.8 - 3.10** (recommended: Python 3.9)
* **pip** package manager
* **MySQL Server 8.0+** (or MySQL Workbench)
* **Virtual Environment Tool** (recommended: `venv` or `virtualenv`)
* **Git** for version control

> ** Compatibility Note:** This project uses PyTorch 2.0.1 and Flask 2.3.3, which have specific Python version requirements. Python 3.11+ may cause dependency conflicts. **Python 3.9 is recommended for best compatibility.**

---

##  Installation and Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/study-group-matcher-backend.git
cd study-group-matcher-backend
```

### Step 2: Set Up Python Virtual Environment

It is **highly recommended** to use a virtual environment to isolate project dependencies.

#### Windows (Git Bash):
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/Scripts/activate

# You should now see (venv) in your prompt
```

#### macOS/Linux:
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

### Step 3: Install Python Dependencies

Install all required packages listed in `requirements.txt`.

```bash
pip install -r requirements.txt
```

**What gets installed:**
- Flask web framework and extensions
- SQLAlchemy for database ORM
- PyMySQL for MySQL connectivity
- PyTorch and Transformers for AI models
- Sentence Transformers for BERT embeddings
- Authentication libraries (PyJWT, bcrypt)

> ** First-Time Download:** The first time you run the application, Sentence Transformers will automatically download the pre-trained BERT model (`all-MiniLM-L6-v2`, approximately 90MB). This is a one-time download and will be cached locally.

---

##  Database Setup

### Step 1: Install MySQL

Download and install MySQL Server:
- **Windows/Mac:** [MySQL Community Server](https://dev.mysql.com/downloads/mysql/)
- **Linux:** `sudo apt-get install mysql-server`

Or use **MySQL Workbench** for a GUI interface.

### Step 2: Create Database

Open MySQL command line or MySQL Workbench and run:

```sql
CREATE DATABASE studysync;
```

### Step 3: Run Database Schema

The application will automatically create tables on first run using SQLAlchemy's `init_db()` function. However, you can also manually run the schema if needed.

**Tables created:**
- `users` - User accounts and profiles
- `study_groups` - Study group information
- `group_members` - Group membership tracking
- `messages` - Chat messages
- `message_reactions` - Message reactions (emojis)
- `study_sessions` - Scheduled study sessions
- `session_attendees` - Session attendance tracking

---

##  Environment Configuration

### Step 1: Create .env File

Create a `.env` file in the backend root directory:

```bash
# In your project folder
touch .env
```

### Step 2: Add Configuration

Copy and paste the following into your `.env` file:

```env
# Database Configuration
DB_USER=root
DB_PASSWORD=your_mysql_password_here
DB_HOST=localhost
DB_PORT=3306
DB_NAME=studysync

# JWT Configuration
JWT_SECRET_KEY=your_secret_key_change_in_production

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
```

** Important:**
- Replace `your_mysql_password_here` with your actual MySQL root password
- Replace `your_secret_key_change_in_production` with a secure random string (use at least 32 characters)
- **Never commit the `.env` file to GitHub!** Add it to `.gitignore`

---

##  Running the Application

### Step 1: Activate Virtual Environment

```bash
# Windows (Git Bash)
source venv/Scripts/activate

# macOS/Linux
source venv/bin/activate
```

### Step 2: Start the Server

```bash
python app.py
```

**Expected Output:**

```
Database initialized successfully!
============================================================
StudySync Backend - AI Study Group Matcher with Authentication
============================================================
Starting server on http://0.0.0.0:5000
Database: MySQL (studysync)
BERT Model: sentence-transformers/all-MiniLM-L6-v2
============================================================
 * Running on http://127.0.0.1:5000
 * Running on http://192.168.0.XXX:5000
```

The server will be accessible at:
- **Localhost:** `http://localhost:5000`
- **Android Emulator:** `http://10.0.2.2:5000`
- **Network:** `http://YOUR_LOCAL_IP:5000`

---

##  API Endpoints

### Health Check

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `GET` | `/api/health` | No | Check server status and AI model loading |

**Example:**
```bash
curl http://localhost:5000/api/health
```

**Response:**
```json
{
  "status": "healthy",
  "database": "connected",
  "ai_model": "loaded",
  "model_name": "sentence-transformers/all-MiniLM-L6-v2"
}
```

### Authentication Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `POST` | `/api/auth/register` | No | Register new user account |
| `POST` | `/api/auth/login` | No | Login with email and password |
| `GET` | `/api/auth/me` | Yes | Get current user info |

**Register Example:**
```json
POST /api/auth/register
{
  "name": "John Doe",
  "email": "john.doe@university.edu",
  "password": "securePassword123",
  "university": "State University",
  "major": "Computer Science",
  "year": "Junior",
  "learningStyle": "I learn best with visual aids and hands-on practice",
  "subjects": ["Mathematics", "Computer Science"],
  "schedule": {
    "Monday": ["Evening (5-9 PM)"],
    "Wednesday": ["Evening (5-9 PM)"]
  },
  "performanceLevel": 4,
  "groupPreferences": {
    "groupSize": 4,
    "sessionDuration": 2,
    "studyGoals": ["Exam Preparation"]
  }
}
```

**Response:**
```json
{
  "success": true,
  "message": "Registration successful",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "user_1234567890.123",
    "name": "John Doe",
    "email": "john.doe@university.edu"
  }
}
```

### AI Recommendation Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `POST` | `/api/recommend` | Yes | Get AI-powered study group recommendations |
| `POST` | `/api/search` | Yes | Search for users/groups semantically |

**Recommendation Response Example:**
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
      "explanation": "High compatibility: Similar subjects (85%), Compatible schedule (78%), Similar learning style (89%)",
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

### Group Management Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `POST` | `/api/groups/create` | Yes | Create a new study group |
| `GET` | `/api/groups/mine` | Yes | Get all groups user is a member of |
| `POST` | `/api/groups/<group_id>/join` | Yes | Request to join a group |

### Chat/Messaging Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `GET` | `/api/chat/<group_id>/messages` | Yes | Get all messages for a group |
| `POST` | `/api/chat/<group_id>/send` | Yes | Send a message to a group |
| `POST` | `/api/chat/message/<message_id>/react` | Yes | Add/remove reaction to a message |

**Authentication Header Format:**
```
Authorization: Bearer <your_jwt_token>
```

---

##  AI Matching Algorithm

### Overview

The StudySync matching algorithm uses a **multi-factor compatibility scoring system** that combines:

1. **Subject Similarity (40% weight)**
   - Uses Jaccard similarity: `intersection / union` of subjects
   - Ensures students share common academic interests

2. **Schedule Overlap (30% weight)**
   - Counts matching time slots across all days
   - Normalizes by total available slots
   - Ensures students can meet at the same times

3. **Learning Style Similarity (20% weight)**
   - Uses BERT embeddings (all-MiniLM-L6-v2 model)
   - Calculates cosine similarity between learning style descriptions
   - Matches students with compatible study approaches

4. **Performance Level Compatibility (10% weight)**
   - Prefers students at similar academic performance levels (1-5 scale)
   - Uses normalized distance metric
   - Ensures balanced group dynamics

### Algorithm Flow

```python
1. For each student in database:
   a. Calculate subject_similarity using Jaccard index
   b. Calculate schedule_overlap by counting matching slots
   c. Generate BERT embeddings for learning styles
   d. Calculate cosine_similarity of embeddings
   e. Calculate performance_compatibility

2. Compute weighted composite score:
   composite_score = (0.4 × subject) + (0.3 × schedule) + 
                     (0.2 × learning_style) + (0.1 × performance)

3. Filter matches above threshold (50%)

4. Sort by composite score (descending)

5. Return top matches with explanations
```

### Match Threshold

The default match threshold is **50%**. Students below this threshold are not shown as matches. Instead, the system suggests "Create Your Own Group" as a recommendation.

### Example Compatibility Breakdown

```json
{
  "matchPercentage": 87,
  "compatibility": {
    "subject": 0.75,        // 75% shared subjects
    "schedule": 0.85,       // 85% schedule overlap
    "learningStyle": 0.92,  // 92% learning style similarity
    "performance": 0.95     // Similar performance levels
  },
  "explanation": "High compatibility: Strong subject overlap, Excellent schedule match, Very similar learning styles, Comparable performance levels"
}
```

---

##  Project Structure

```
study-group-matcher-backend/
├── app.py                 # Main Flask application and API routes
├── database.py            # Database configuration and session management
├── models.py              # SQLAlchemy ORM models (User, Group, Message, etc.)
├── auth.py                # Authentication utilities (JWT, bcrypt, decorators)
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (NOT committed to Git)
├── .gitignore            # Git ignore rules
├── README.md             # This file
└── venv/                 # Virtual environment (NOT committed to Git)
```

### Key Files Explained

**app.py**
- Flask app initialization
- All API route definitions
- AI matching algorithm implementation
- Request/response handling

**database.py**
- SQLAlchemy engine configuration
- Database session management
- Connection pooling
- Database initialization function

**models.py**
- User model (profiles, authentication)
- StudyGroup model (group information)
- GroupMember model (membership tracking)
- Message model (chat messages)
- MessageReaction model (reactions)
- StudySession model (scheduled sessions)

**auth.py**
- `hash_password()` - Bcrypt password hashing
- `verify_password()` - Password verification
- `generate_token()` - JWT token generation
- `decode_token()` - JWT token validation
- `@token_required` - Route protection decorator

---

##  Troubleshooting

### Common Issues and Solutions

#### 1. Database Connection Errors

**Error:** `Access denied for user 'root'@'localhost'`

**Solution:**
```bash
# Check your .env file has the correct password
# Test MySQL connection:
mysql -u root -p
# Enter your password to verify it works
```

#### 2. Module Not Found Errors

**Error:** `ModuleNotFoundError: No module named 'PyMySQL'`

**Solution:**
```bash
# Make sure virtual environment is activated
source venv/Scripts/activate  # Windows Git Bash
source venv/bin/activate       # macOS/Linux

# Reinstall dependencies
pip install -r requirements.txt
```

#### 3. Port Already in Use

**Error:** `Address already in use`

**Solution:**
```bash
# Windows
taskkill /F /IM python.exe

# macOS/Linux
lsof -ti:5000 | xargs kill -9
```

#### 4. BERT Model Download Issues

**Error:** Model download fails or hangs

**Solution:**
```bash
# Manually download the model
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"
```

#### 5. MySQL Database Not Found

**Error:** `Unknown database 'studysync'`

**Solution:**
```sql
-- Open MySQL and run:
CREATE DATABASE studysync;
```

#### 6. JWT Token Errors

**Error:** `Invalid or expired token`

**Solution:**
- Check that JWT_SECRET_KEY is set in `.env`
- Verify token is being sent in Authorization header
- Token expires after 7 days - re-login to get new token

---

##  License

This project is licensed under the **Apache License 2.0**.

---

##  Author

**Dillon Opperman**
- GitHub: [@DillonOpperman](https://github.com/DillonOpperman)
- Email: dlopper@ilstu.edu
- University: Illinois State University

**Project Information:**
- Originally a project for IT-244 taught by (https://github.com/elaheJ)
- Entered into 2026 Illinois State University Mobile Application Contest
- Institution: Illinois State University

---

##  Acknowledgements

This project was made possible thanks to the following open-source projects and resources:

### AI/ML Libraries
- **[HuggingFace](https://huggingface.co/)** - For providing pre-trained BERT models and the Transformers library
- **[Sentence-Transformers](https://www.sbert.net/)** - For the semantic similarity framework and embedding models
- **[PyTorch](https://pytorch.org/)** - For the deep learning framework
- **[scikit-learn](https://scikit-learn.org/)** - For machine learning utilities and similarity metrics

### Web Framework & Tools
- **[Flask](https://flask.palletsprojects.com/)** - For the lightweight and flexible web framework
- **[SQLAlchemy](https://www.sqlalchemy.org/)** - For the powerful ORM and database toolkit

### Security
- **[PyJWT](https://pyjwt.readthedocs.io/)** - For JWT token implementation
- **[bcrypt](https://github.com/pyca/bcrypt/)** - For secure password hashing

### Inspiration
- **Microsoft Recommenders** - For collaborative filtering algorithm inspiration
- **React Native Documentation** - For frontend integration guidance
- **Flask-RESTful Examples** - For API design patterns

### Special Thanks
- Illinois State University 
- MAD Contest Organizers
- Dr. Elahe Javadi - School of Information Technology 

---

##  Support

For questions, issues, or contributions:

1. **Issues:** Open an issue on [GitHub Issues](https://github.com/DillonOpperman/studysync-backend/issues)
2. **Email:** Contact dlopper@ilstu.edu
3. **Documentation:** Refer to the [API Documentation](#api-endpoints) section above

---

**Last Updated:** November 2025  
**Version:** 1.0.0  
**Status:** Active Development for MAD Contest

## Model Documentation 

# Database Models & Schema

This section documents the data models used in the StudySync application.

---

##  Database Architecture

StudySync uses **MySQL** with **SQLAlchemy ORM** to manage the following entities:

### Entity Relationship Diagram

```
Users (1) ──── (Many) GroupMembers (Many) ──── (1) StudyGroups
  │                                                     │
  │                                                     │
  └──── (Many) Messages (Many) ──────────────────────┘
           │
           └──── (Many) MessageReactions
```

---

##  Data Models

### 1. User Model

Stores student profile information and authentication data.

**Table:** `users`

| Field | Type | Description |
|-------|------|-------------|
| `id` | String(50) | Primary key, generated UUID |
| `name` | String(100) | Student's full name |
| `email` | String(100) | Unique .edu email address |
| `password_hash` | String(255) | Bcrypt hashed password |
| `university` | String(100) | University name |
| `major` | String(100) | Field of study |
| `year` | String(50) | Academic year (Freshman, Sophomore, etc.) |
| `learning_style` | Text | Description of how student learns best |
| `study_environments` | JSON | Preferred study locations |
| `study_methods` | JSON | Preferred study techniques |
| `subjects` | JSON | Array of subjects studying |
| `schedule` | JSON | Weekly availability schedule |
| `performance_level` | Integer | Academic performance (1-5 scale) |
| `group_preferences` | JSON | Study group preferences |
| `created_at` | Timestamp | Account creation date |

**Example User Data:**
```json
{
  "id": "user_1701234567.890_alice",
  "name": "Alice Johnson",
  "email": "alice@ilstu.edu",
  "university": "Illinois State University",
  "major": "Computer Science",
  "year": "Junior",
  "learning_style": "I learn best with visual aids and hands-on coding practice",
  "subjects": ["Computer Science", "Mathematics", "Data Structures"],
  "schedule": {
    "Monday": ["Evening (5-9 PM)"],
    "Wednesday": ["Evening (5-9 PM)"],
    "Friday": ["Afternoon (12-5 PM)"]
  },
  "performanceLevel": 4,
  "groupPreferences": {
    "groupSize": 4,
    "sessionDuration": 2,
    "studyGoals": ["Exam Preparation", "Project Work"]
  }
}
```

---

### 2. StudyGroup Model

Represents a study group created by a user.

**Table:** `study_groups`

| Field | Type | Description |
|-------|------|-------------|
| `id` | String(50) | Primary key, generated UUID |
| `title` | String(100) | Group name/title |
| `subject` | String(100) | Main subject focus |
| `leader_id` | String(50) | Foreign key to Users (group creator) |
| `schedule` | String(200) | Meeting schedule description |
| `location` | String(200) | Meeting location |
| `max_members` | Integer | Maximum group size |
| `description` | Text | Group description |
| `status` | String(20) | Group status (active/inactive) |
| `created_at` | Timestamp | Group creation date |

**Example Group Data:**
```json
{
  "id": "group_1701234567.890",
  "title": "CS 230 Data Structures Study Group",
  "subject": "Computer Science",
  "leaderId": "user_1701234567.890_alice",
  "schedule": "Mon/Wed 6-8pm",
  "location": "Milner Library Room 304",
  "maxMembers": 5,
  "description": "Focused on mastering algorithms and data structures for CS 230",
  "status": "active"
}
```

---

### 3. GroupMember Model

Tracks which users belong to which groups.

**Table:** `group_members`

| Field | Type | Description |
|-------|------|-------------|
| `id` | Integer | Primary key, auto-increment |
| `group_id` | String(50) | Foreign key to StudyGroups |
| `user_id` | String(50) | Foreign key to Users |
| `role` | String(20) | Member role (leader/member) |
| `status` | String(20) | Membership status (active/pending/removed) |
| `joined_at` | Timestamp | Date user joined group |

**Example Membership:**
```json
{
  "groupId": "group_1701234567.890",
  "userId": "user_1701234567.890_bob",
  "role": "member",
  "status": "active",
  "joinedAt": "2024-11-20T18:30:00Z"
}
```

---

### 4. Message Model

Stores all group chat messages.

**Table:** `messages`

| Field | Type | Description |
|-------|------|-------------|
| `id` | String(50) | Primary key, generated UUID |
| `group_id` | String(50) | Foreign key to StudyGroups |
| `user_id` | String(50) | Foreign key to Users (sender) |
| `content` | Text | Message text content |
| `message_type` | String(20) | Type: text/image/announcement |
| `image_url` | String(500) | URL if message contains image |
| `created_at` | Timestamp | Message timestamp |

**Example Message:**
```json
{
  "id": "msg_1701234567.890",
  "groupId": "group_1701234567.890",
  "userId": "user_1701234567.890_alice",
  "userName": "Alice Johnson",
  "content": "Hey everyone! Don't forget we're meeting tomorrow at 6pm in Milner 304",
  "messageType": "text",
  "timestamp": "2024-11-20T15:45:00Z",
  "reactions": []
}
```

---

### 5. MessageReaction Model

Stores emoji reactions to messages.

**Table:** `message_reactions`

| Field | Type | Description |
|-------|------|-------------|
| `id` | Integer | Primary key, auto-increment |
| `message_id` | String(50) | Foreign key to Messages |
| `user_id` | String(50) | Foreign key to Users |
| `emoji` | String(10) | Emoji character |
| `created_at` | Timestamp | Reaction timestamp |

**Example Reaction:**
```json
{
  "messageId": "msg_1701234567.890",
  "userId": "user_1701234567.890_bob",
  "emoji": "👍"
}
```

---

### 6. StudySession Model

Represents scheduled study sessions for groups.

**Table:** `study_sessions`

| Field | Type | Description |
|-------|------|-------------|
| `id` | String(50) | Primary key, generated UUID |
| `group_id` | String(50) | Foreign key to StudyGroups |
| `title` | String(100) | Session title |
| `scheduled_time` | Timestamp | When session occurs |
| `location` | String(200) | Session location |
| `description` | Text | Session description |
| `created_by` | String(50) | Foreign key to Users |
| `created_at` | Timestamp | Session creation date |

---

### 7. SessionAttendee Model

Tracks who's attending study sessions.

**Table:** `session_attendees`

| Field | Type | Description |
|-------|------|-------------|
| `id` | Integer | Primary key, auto-increment |
| `session_id` | String(50) | Foreign key to StudySessions |
| `user_id` | String(50) | Foreign key to Users |
| `status` | String(20) | Attendance status (going/maybe/not_going) |
| `created_at` | Timestamp | RSVP timestamp |

---

##  Key Relationships

### One-to-Many Relationships:
- **User → Messages:** One user can send many messages
- **User → GroupMembers:** One user can join many groups
- **StudyGroup → GroupMembers:** One group has many members
- **StudyGroup → Messages:** One group has many messages
- **Message → MessageReactions:** One message can have many reactions

### Many-to-Many Relationships:
- **Users ↔ StudyGroups:** Through `GroupMembers` junction table
- **Users ↔ StudySessions:** Through `SessionAttendees` junction table

---

##  Example Data Flow

### Creating an Account & Joining a Group:

1. **User Registration:**
   ```
   POST /api/auth/register
   → Creates User record
   → Returns JWT token
   ```

2. **AI Matching:**
   ```
   POST /api/recommend
   → Analyzes user's subjects, schedule, learning style
   → Returns compatible groups
   ```

3. **Creating a Group:**
   ```
   POST /api/groups/create
   → Creates StudyGroup record
   → Creates GroupMember record (leader)
   ```

4. **Joining a Group:**
   ```
   POST /api/groups/{id}/join
   → Creates GroupMember record (member)
   → Updates group member count
   ```

5. **Sending Messages:**
   ```
   POST /api/chat/{group_id}/send
   → Creates Message record
   → Broadcasts to group members
   ```

---

##  Data Security

- **Passwords:** Hashed using bcrypt (never stored in plain text)
- **Authentication:** JWT tokens with 7-day expiration
- **Authorization:** All endpoints (except register/login) require valid JWT
- **Data Isolation:** Users can only access their own groups and messages

---

##  Sample Database Queries

### Get all groups for a user:
```sql
SELECT g.* FROM study_groups g
JOIN group_members gm ON g.id = gm.group_id
WHERE gm.user_id = 'user_1701234567.890_alice'
AND gm.status = 'active';
```

### Get all messages in a group:
```sql
SELECT m.*, u.name as sender_name 
FROM messages m
JOIN users u ON m.user_id = u.id
WHERE m.group_id = 'group_1701234567.890'
ORDER BY m.created_at ASC;
```

### Get compatible study partners:
```sql
SELECT u.* FROM users u
WHERE u.subjects && ARRAY['Computer Science']  -- Shares subjects
AND u.id != 'current_user_id'
LIMIT 10;
```

---

This models documentation provides a complete overview of the StudySync database structure and relationships.

##  YouTube Video

Here is a link to a YouTube video just explaning some small details.

https://youtu.be/n0UL5QlW-M0

**Last Updated:** Dec 2nd, 2025  

