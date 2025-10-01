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
        return max(0, similarity)  # Ensure non-negative
    
    def generate_recommendations(self, target_student):
        recommendations = []
        
        for i, student in enumerate(self.students):
            if student['id'] == target_student['id']:
                continue
            
            # Calculate compatibility scores
            subject_score = self.calculate_subject_similarity(target_student, student)
            schedule_score = self.calculate_schedule_overlap(
                target_student.get('schedule', {}), 
                student.get('schedule', {})
            )
            learning_style_score = self.calculate_learning_style_similarity(target_student, student)
            
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
            
            # Convert to percentage
            match_percentage = int(composite_score * 100)
            
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
                        'subject': subject_score,
                        'schedule': schedule_score,
                        'learningStyle': learning_style_score,
                        'performance': performance_score
                    }
                })
        
        # Sort by match percentage
        recommendations.sort(key=lambda x: x['matchPercentage'], reverse=True)
        
        # Add "create your own group" suggestion
        recommendations.append({
            'id': len(recommendations) + 1,
            'title': 'Create Your Own Group',
            'matchPercentage': None,
            'memberInfo': f"Based on your profile, you could lead a {target_student.get('major', 'study')} group.",
            'schedule': f"{len([s for s in self.students if s.get('major') == target_student.get('major')])} similar students are available!",
            'focus': '',
            'location': '',
            'action': 'Start Group',
            'suggested': True,
            'explanation': 'Perfect opportunity to start your own study group based on your preferences',
            'compatibility': {'subject': 1.0, 'schedule': 1.0, 'learningStyle': 1.0, 'performance': 1.0}
        })
        
        return recommendations[:5]  # Return top 5
    
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
        print(f"Received student data: {student_data}")
        
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
        
        print(f"Generating recommendations for: {student_data.get('name', 'Unknown')}")
        
        # Generate AI-powered recommendations
        recommendations = matcher.generate_recommendations(student_data)
        
        print(f"Generated {len(recommendations)} recommendations")
        
        return jsonify({
            'success': True,
            'recommendations': recommendations
        })
    except Exception as e:
        print(f"Error generating recommendations: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

def _build_group_corpus():
	corpus = []
	for student in matcher.students:
		text_parts = []
		name = student.get('name', '')
		major = student.get('major', '')
		subjects = ", ".join(student.get('subjects', []))
		learning_style = student.get('learningStyle', '')
		description = student.get('description', '') or student.get('bio', '')
		if name:
			text_parts.append(name)
		if major:
			text_parts.append(major)
		if subjects:
			text_parts.append(subjects)
		if learning_style:
			text_parts.append(learning_style)
		if description:
			text_parts.append(description)
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
	texts = [item['text'] or (item['student'].get('major', '') + ' ' + ', '.join(item['student'].get('subjects', []))) for item in corpus]
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
	query_embedding = model.encode([query])
	results = semantic_search_groups(query_embedding)
	return jsonify({'results': results})

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'ai_model': 'loaded'})

import os

# At the bottom of your app.py, change:
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)