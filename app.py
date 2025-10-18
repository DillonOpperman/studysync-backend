from flask import Flask, request, jsonify
from flask_cors import CORS
from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import json

app = Flask(__name__)
CORS(app)

# Initialize the BERT model (this will download on first run)
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

class AIStudentMatcher:
    def __init__(self):
        self.model = model
        self.students = []
    
    def add_student(self, student_data):
        self.students.append(student_data)
        print(f"Added student: {student_data.get('name')}. Total students: {len(self.students)}")
        return len(self.students) - 1
    
    def calculate_subject_similarity(self, student1, student2):
        subjects1 = set(student1.get('subjects', []))
        subjects2 = set(student2.get('subjects', []))
        if not subjects1 or not subjects2:
            return 0
        intersection = len(subjects1.intersection(subjects2))
        union = len(subjects1.union(subjects2))
        return intersection / union if union > 0 else 0
    
    def calculate_schedule_overlap(self, schedule1, schedule2):
        if not schedule1 or not schedule2:
            return 0
        
        overlap_count = 0
        total_slots = 0
        
        for day in schedule1:
            if day in schedule2:
                slots1 = set(schedule1[day])
                slots2 = set(schedule2[day])
                overlap_count += len(slots1.intersection(slots2))
                total_slots += len(slots1.union(slots2))
        
        return overlap_count / max(total_slots, 1)
    
    def calculate_learning_style_similarity(self, student1, student2):
        style1 = student1.get('learningStyle', '')
        style2 = student2.get('learningStyle', '')
        
        if not style1 or not style2:
            return 0
        
        # Use BERT embeddings for semantic similarity
        embeddings = self.model.encode([style1, style2])
        similarity = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
        return max(0, float(similarity))  # Convert to float and ensure non-negative
    
    def generate_recommendations(self, target_student):
        print(f"\n=== Generating recommendations for: {target_student.get('name')} ===")
        print(f"Total students in database: {len(self.students)}")
        print(f"Target student subjects: {target_student.get('subjects')}")
        
        recommendations = []
        
        # Only match with OTHER students (not yourself)
        for i, student in enumerate(self.students):
            if student['id'] == target_student['id']:
                print(f"Skipping self: {student.get('name')}")
                continue
            
            print(f"\nComparing with: {student.get('name')}")
            
            # Calculate compatibility scores
            subject_score = float(self.calculate_subject_similarity(target_student, student))
            schedule_score = float(self.calculate_schedule_overlap(
                target_student.get('schedule', {}), 
                student.get('schedule', {})
            ))
            learning_style_score = float(self.calculate_learning_style_similarity(target_student, student))
            
            print(f"  Subject similarity: {subject_score:.2f}")
            print(f"  Schedule overlap: {schedule_score:.2f}")
            print(f"  Learning style similarity: {learning_style_score:.2f}")
            
            # Performance balance (prefer similar levels)
            perf1 = target_student.get('performanceLevel', 3)
            perf2 = student.get('performanceLevel', 3)
            performance_score = 1 - abs(perf1 - perf2) / 4  # Normalize to 0-1
            
            # Weighted composite score
            weights = {
                'subject': 0.4,
                'schedule': 0.3,
                'learning_style': 0.2,
                'performance': 0.1
            }
            
            composite_score = (
                subject_score * weights['subject'] +
                schedule_score * weights['schedule'] +
                learning_style_score * weights['learning_style'] +
                performance_score * weights['performance']
            )
            
            # Convert to percentage - IMPORTANT: use int() to avoid float32 serialization error
            match_percentage = int(composite_score * 100)
            print(f"  COMPOSITE MATCH: {match_percentage}%")
            
            if match_percentage > 50:  # Only include decent matches
                recommendations.append({
                    'id': len(recommendations) + 1,
                    'title': f"{student.get('major', 'Study')} Group",
                    'matchPercentage': match_percentage,
                    'memberInfo': '3-5 members, actively seeking',
                    'schedule': self.format_schedule(student.get('schedule', {})),
                    'focus': ', '.join(student.get('subjects', [])[:2]),
                    'location': 'Campus Study Areas',
                    'action': 'Request to Join',
                    'suggested': False,
                    'explanation': self.generate_explanation(
                        subject_score, schedule_score, learning_style_score, performance_score
                    ),
                    'compatibility': {
                        'subject': float(subject_score),
                        'schedule': float(schedule_score),
                        'learningStyle': float(learning_style_score),
                        'performance': float(performance_score)
                    }
                })
        
        # Sort by match percentage
        recommendations.sort(key=lambda x: x['matchPercentage'], reverse=True)
        
        print(f"\nFound {len(recommendations)} matches above 50%")
        
        # LOGIC: If matches found, show matches + create option
        # If NO matches found, ONLY show create option
        if len(recommendations) == 0:
            print("No matches found - suggesting to create own group")
            recommendations.append({
                'id': 1,
                'title': 'Create Your Own Study Group',
                'matchPercentage': None,
                'memberInfo': f"No existing groups match your profile yet.",
                'schedule': f"Set your own schedule based on your availability",
                'focus': ', '.join(target_student.get('subjects', [])[:3]),
                'location': 'Choose your preferred study location',
                'action': 'Start Group',
                'suggested': True,
                'explanation': f"Be the first to start a {target_student.get('major', 'study')} group! Other students studying {', '.join(target_student.get('subjects', [])[:2])} are looking for groups to join.",
                'compatibility': {'subject': 1.0, 'schedule': 1.0, 'learningStyle': 1.0, 'performance': 1.0}
            })
        else:
            print(f"Matches found - adding create option as additional choice")
            # Add create group as an ADDITIONAL option when matches exist
            recommendations.append({
                'id': len(recommendations) + 1,
                'title': 'Create Your Own Group',
                'matchPercentage': None,
                'memberInfo': f"Or start your own {target_student.get('major', 'study')} group",
                'schedule': f"Lead a group based on your preferences",
                'focus': ', '.join(target_student.get('subjects', [])[:2]),
                'location': 'Your preferred location',
                'action': 'Start Group',
                'suggested': True,
                'explanation': 'Perfect opportunity to lead your own study group based on your preferences',
                'compatibility': {'subject': 1.0, 'schedule': 1.0, 'learningStyle': 1.0, 'performance': 1.0}
            })
        
        print(f"=== Returning {len(recommendations)} total recommendations ===\n")
        return recommendations
    
    def format_schedule(self, schedule):
        available_days = [day for day, slots in schedule.items() if slots]
        if len(available_days) >= 2:
            return f"{available_days[0][:3]}/{available_days[1][:3]} evenings"
        elif len(available_days) == 1:
            return f"{available_days[0][:3]} evenings"
        return "Flexible schedule"
    
    def generate_explanation(self, subject_score, schedule_score, learning_style_score, performance_score):
        explanations = []
        if subject_score > 0.5:
            explanations.append("Similar subjects")
        if schedule_score > 0.3:
            explanations.append("Compatible schedule")
        if learning_style_score > 0.6:
            explanations.append("Similar learning style")
        if performance_score > 0.7:
            explanations.append("Similar academic level")
        
        return "High compatibility: " + ", ".join(explanations) if explanations else "Basic compatibility match"

# Initialize matcher
matcher = AIStudentMatcher()

@app.route('/api/student', methods=['POST'])
def create_student():
    try:
        student_data = request.json
        print(f"\n=== New student registration ===")
        print(f"Name: {student_data.get('name')}")
        print(f"Major: {student_data.get('major')}")
        print(f"Subjects: {student_data.get('subjects')}")
        
        # Add to our matcher
        matcher.add_student(student_data)
        
        return jsonify({
            'success': True,
            'message': f"Welcome {student_data.get('name', 'Student')}! Profile created successfully."
        })
    except Exception as e:
        print(f"Error creating student: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/recommend', methods=['POST'])
def get_recommendations():
    try:
        data = request.json
        student_data = data.get('student_data')
        
        # Generate AI-powered recommendations
        recommendations = matcher.generate_recommendations(student_data)
        
        return jsonify({
            'success': True,
            'recommendations': recommendations
        })
    except Exception as e:
        print(f"Error generating recommendations: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500

def _build_group_corpus():
    corpus = []
    for student in matcher.students:
        text_parts = []
        name = student.get('name', '')
        major = student.get('major', '')
        subjects = ", ".join(student.get('subjects', []))
        learning_style = student.get('learningStyle', '')
        if name:
            text_parts.append(name)
        if major:
            text_parts.append(major)
        if subjects:
            text_parts.append(subjects)
        if learning_style:
            text_parts.append(learning_style)
        corpus.append({
            'id': student.get('id', len(corpus) + 1),
            'title': f"{major or 'Study'} Group",
            'text': ' '.join(text_parts).strip(),
            'student': student
        })
    return corpus

def semantic_search_groups(query_embedding, top_k: int = 5):
    corpus = _build_group_corpus()
    if not corpus:
        return []
    texts = [item['text'] for item in corpus]
    corpus_embeddings = model.encode(texts)
    scores = cosine_similarity(query_embedding, corpus_embeddings)[0]
    indices = np.argsort(scores)[::-1][:top_k]
    results = []
    for rank, idx in enumerate(indices, start=1):
        item = corpus[idx]
        student = item['student']
        results.append({
            'id': item['id'],
            'title': item['title'],
            'matchPercentage': int(max(0.0, min(1.0, float(scores[idx]))) * 100),
            'memberInfo': 'Actively seeking members',
            'schedule': AIStudentMatcher().format_schedule(student.get('schedule', {})),
            'focus': ', '.join(student.get('subjects', [])[:2]),
            'location': 'Campus Study Areas',
            'action': 'Request to Join',
            'suggested': False
        })
    return results

@app.route('/api/search', methods=['POST'])
def search_groups():
    data = request.json
    query = data.get('query', '')
    print(f"Search query: {query}")
    query_embedding = model.encode([query])
    results = semantic_search_groups(query_embedding)
    print(f"Found {len(results)} results")
    return jsonify({'results': results})

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'ai_model': 'loaded',
        'total_students': len(matcher.students),
        'timestamp': str(__import__('datetime').datetime.now())
    })

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    print(f"\n{'='*60}")
    print("StudySync Backend - AI Study Group Matcher")
    print(f"{'='*60}")
    print(f"Starting server on http://0.0.0.0:{port}")
    print(f"BERT Model: sentence-transformers/all-MiniLM-L6-v2")
    print(f"{'='*60}\n")
    
    # Optional demo/test students (only loaded when running this file directly)
    test_students = [
        {
            'id': 'test_lisa',
            'name': 'Lisa Martinez',
            'email': 'lisa@university.edu',
            'university': 'State University',
            'major': 'Mathematics',
            'year': 'Junior',
            'learningStyle': 'I prefer visual learning with diagrams and practice problems',
            'subjects': ['Mathematics', 'Physics'],
            'studyEnvironments': ['Quiet Library', 'Study Room'],
            'studyMethods': ['Flashcards', 'Practice Tests'],
            'schedule': {
                'Monday': ['Evening (5-9 PM)'],
                'Wednesday': ['Evening (5-9 PM)']
            },
            'performanceLevel': 4,
            'groupPreferences': {
                'groupSize': 4,
                'sessionDuration': 2,
                'studyGoals': ['Exam Preparation']
            }
        },
        {
            'id': 'test_mike',
            'name': 'Mike Rodriguez',
            'email': 'mike@university.edu',
            'university': 'State University',
            'major': 'Computer Science',
            'year': 'Sophomore',
            'learningStyle': 'Hands-on coding practice with peer discussions',
            'subjects': ['Computer Science', 'Mathematics'],
            'studyEnvironments': ['Study Room', 'Coffee Shop'],
            'studyMethods': ['Group Discussion', 'Hands-on Practice'],
            'schedule': {
                'Tuesday': ['Afternoon (12-5 PM)'],
                'Thursday': ['Afternoon (12-5 PM)']
            },
            'performanceLevel': 3,
            'groupPreferences': {
                'groupSize': 3,
                'sessionDuration': 3,
                'studyGoals': ['Project Collaboration']
            }
        }
    ]

    for student in test_students:
        matcher.add_student(student)
        print(f"Pre-loaded test student: {student['name']}")
    
    print(f"Initial students loaded: {len(matcher.students)}")
    print(f"{'='*60}\n")

    app.run(debug=False, host='0.0.0.0', port=port)