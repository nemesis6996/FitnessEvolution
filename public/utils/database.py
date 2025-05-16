import sqlite3
import os
import pandas as pd
import json
import streamlit as st

# Database file path
DB_PATH = "fitness_app.db"

def get_connection():
    """Create a connection to the SQLite database"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # This enables column access by name
    return conn

def initialize_database():
    """Initialize the database with tables and sample data if it doesn't exist"""
    if not os.path.exists(DB_PATH):
        conn = get_connection()
        cursor = conn.cursor()
        
        # Create tables
        
        # Users table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT UNIQUE,
            first_name TEXT,
            last_name TEXT,
            height REAL,
            weight REAL,
            goals TEXT,
            experience_level TEXT,
            is_admin INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Exercise categories table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS exercise_categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            description TEXT
        )
        ''')
        
        # Exercises table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS exercises (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            category_id INTEGER,
            difficulty TEXT,
            equipment TEXT,
            muscles_targeted TEXT,
            description TEXT,
            short_description TEXT,
            instructions TEXT,
            tips TEXT,
            image_url TEXT,
            video_url TEXT,
            FOREIGN KEY (category_id) REFERENCES exercise_categories (id)
        )
        ''')
        
        # Workout templates table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS workout_templates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            description TEXT,
            difficulty TEXT,
            duration INTEGER,
            goal TEXT,
            created_by INTEGER,
            is_public INTEGER DEFAULT 1,
            FOREIGN KEY (created_by) REFERENCES users (id)
        )
        ''')
        
        # Workout exercises junction table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS workout_exercises (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            workout_id INTEGER,
            exercise_id INTEGER,
            sets INTEGER,
            reps TEXT,
            rest_time INTEGER,
            notes TEXT,
            order_num INTEGER,
            FOREIGN KEY (workout_id) REFERENCES workout_templates (id),
            FOREIGN KEY (exercise_id) REFERENCES exercises (id)
        )
        ''')
        
        # User workouts table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_workouts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            template_id INTEGER,
            name TEXT,
            is_completed INTEGER DEFAULT 0,
            scheduled_date TEXT,
            completed_date TEXT,
            notes TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (template_id) REFERENCES workout_templates (id)
        )
        ''')
        
        # User progress table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            date TEXT,
            weight REAL,
            body_fat REAL,
            chest REAL,
            waist REAL,
            hips REAL,
            arms REAL,
            thighs REAL,
            notes TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        ''')
        
        # Insert sample data
        
        # Exercise categories
        categories = [
            ("Strength", "Exercises focused on building muscular strength"),
            ("Cardio", "Exercises focused on cardiovascular fitness"),
            ("Flexibility", "Exercises focused on improving range of motion"),
            ("Functional", "Exercises that improve everyday movement"),
            ("Balance", "Exercises that improve stability and coordination"),
            ("Core", "Exercises focused on abdominal and back strength")
        ]
        
        cursor.executemany(
            "INSERT INTO exercise_categories (name, description) VALUES (?, ?)",
            categories
        )
        
        # Sample exercises
        exercises = [
            # Strength exercises
            (
                "Barbell Squat", 1, "Intermediate", "Barbell", "Quadriceps, Hamstrings, Glutes", 
                "The barbell squat is a compound exercise that primarily targets the quadriceps, hamstrings, and glutes.",
                "A fundamental lower body compound exercise",
                "1. Stand with feet shoulder-width apart\n2. Rest barbell on upper traps/rear delts\n3. Bend knees and lower until thighs are parallel to ground\n4. Push through heels to return to starting position",
                "Keep chest up, maintain neutral spine, drive through heels",
                "https://pixabay.com/get/g5d59f68517540751059ad4683209cf0a853bc413ea21466416f6f1006fabf4aecd7f5fd77130082ccae94996e13bb4f90787cfdeb85ad7da6d94939cafdf3664_1280.jpg",
                ""
            ),
            (
                "Bench Press", 1, "Intermediate", "Barbell, Bench", "Chest, Triceps, Shoulders",
                "The bench press is a compound exercise that primarily targets the chest, with secondary emphasis on the triceps and shoulders.",
                "The classic chest-building exercise",
                "1. Lie on bench with feet flat on floor\n2. Grip barbell slightly wider than shoulder width\n3. Lower bar to mid-chest\n4. Press bar up until arms are extended",
                "Keep wrists straight, shoulders retracted, and feet firmly planted",
                "https://pixabay.com/get/g170798a89223f827d49da57a0f41b7aeb3f00ea02954d7ea7938b60111e2b10892b983ec2386827a94f241581455e31c2fec1ec882a1fcfe43c305c21f4d4366_1280.jpg",
                ""
            ),
            (
                "Deadlift", 1, "Advanced", "Barbell", "Lower Back, Hamstrings, Glutes, Traps",
                "The deadlift is a compound exercise that works multiple muscle groups including the lower back, hamstrings, glutes, and traps.",
                "A powerful exercise for overall strength development",
                "1. Stand with feet hip-width apart, barbell over mid-foot\n2. Bend at hips and knees, grip barbell\n3. Flatten back and lift chest\n4. Drive through heels and stand up straight\n5. Lower bar by hinging at hips and bending knees",
                "Maintain neutral spine throughout, keep bar close to body",
                "https://pixabay.com/get/ga33d59d721dc445224e9e388def1d555b77e8cec6653016929a0f7ca8128a0e46016c28a5e607416cd5a9dda26ad7e34700d2bb5d41da6797a21e04c43e95860_1280.jpg",
                ""
            ),
            
            # Cardio exercises
            (
                "Running", 2, "Beginner", "None", "Heart, Legs, Core",
                "Running is a cardiovascular exercise that improves heart health, endurance, and burns calories effectively.",
                "The most accessible form of cardio",
                "1. Maintain good posture with slight forward lean\n2. Land midfoot with each step\n3. Keep arms at 90-degree angles\n4. Breathe rhythmically",
                "Start with walk/run intervals if you're a beginner",
                "https://pixabay.com/get/g7bbaf6544b35ae3c4487738e4a08b6f5ddb369406b0b48d2e6113fcc7a2738e9d0dc4f2c347e3ad677c71f22bc55569fa2bfc38fda23e5d37240d488695ac56a_1280.jpg",
                ""
            ),
            (
                "Jumping Rope", 2, "Beginner", "Jump Rope", "Calves, Shoulders, Heart",
                "Jumping rope is a high-intensity cardiovascular exercise that improves coordination and burns calories efficiently.",
                "A fun, portable cardio workout",
                "1. Hold handles with relaxed grip\n2. Keep elbows close to sides\n3. Jump just high enough to clear rope\n4. Land softly on balls of feet\n5. Maintain rhythm and breathing",
                "Start with short intervals and build up endurance",
                "https://pixabay.com/get/g1442a789e8b0d47ad70ca469db2457f7660f480578325f32cf40b2b2a982ee84794188f5194dde3f8b54cb0b1a467c5d8a6f7e585ee3e14a0ec8881de638b403_1280.jpg",
                ""
            ),
            
            # Flexibility exercises
            (
                "Standing Hamstring Stretch", 3, "Beginner", "None", "Hamstrings, Lower Back",
                "This stretch targets the hamstring muscles on the back of the thigh and can help prevent lower back pain.",
                "An essential stretch for lower body flexibility",
                "1. Stand tall with feet hip-width apart\n2. Extend one leg forward, heel on ground, toes up\n3. Hinge at hips and lean forward slightly\n4. Hold for 20-30 seconds\n5. Switch legs and repeat",
                "Keep back straight, don't bounce, breathe deeply",
                "https://pixabay.com/get/g52c9a21308956d592258ddb80b06b4d49f940403310696b8c730250331e951c1c35e79fe002ed7a99f6df039fd491930d022bc667c8e4c3776a67d47fe4ca672_1280.jpg",
                ""
            ),
            
            # Core exercises
            (
                "Plank", 6, "Beginner", "None", "Abs, Lower Back, Shoulders",
                "The plank is an isometric core exercise that strengthens the abdominals, back, and shoulders.",
                "A foundational core stability exercise",
                "1. Start in push-up position with arms straight\n2. Lower onto forearms, elbows under shoulders\n3. Form straight line from head to heels\n4. Engage core and hold position\n5. Hold for desired time (30-60 seconds for beginners)",
                "Don't let hips sag or lift too high, breathe normally",
                "https://pixabay.com/get/g3d5957a558b873a9d3130e2cdba71f1c30dc9f706890c083738b65d4ee9eb6c05dd2b238afb121b767adfed27a77c56fe77ab00c4202744b85daaf8f06f4d8ba_1280.jpg",
                ""
            ),
            (
                "Russian Twists", 6, "Intermediate", "Dumbbell (optional)", "Obliques, Abs",
                "Russian twists target the obliques and help develop rotational strength in the core.",
                "An effective exercise for the sides of your core",
                "1. Sit on floor with knees bent\n2. Lean back slightly, keeping back straight\n3. Lift feet slightly off ground (optional)\n4. Clasp hands together or hold weight\n5. Twist torso to right, then to left\n6. Continue alternating sides",
                "Focus on rotating from the core, not just the arms",
                "https://pixabay.com/get/g68598295d056a5d283cbf0cdea458bc04b57800066868db8b631d6447d5ef94d02fb492bbe3928ec04b7e386ce2bce8e8a569413107027c8a75f0a81bcba62b3_1280.jpg",
                ""
            ),
            
            # Functional exercises
            (
                "Kettlebell Swing", 4, "Intermediate", "Kettlebell", "Glutes, Hamstrings, Core, Shoulders",
                "The kettlebell swing is a dynamic exercise that builds power in the posterior chain while improving cardiovascular fitness.",
                "A powerful hip-hinge movement for overall athleticism",
                "1. Stand with feet shoulder-width apart\n2. Hold kettlebell with both hands\n3. Hinge at hips, swinging kettlebell between legs\n4. Thrust hips forward powerfully\n5. Let kettlebell swing up to chest height\n6. Control the descent and repeat",
                "Power comes from the hips, not the arms or shoulders",
                "https://pixabay.com/get/gadda681deecf85e99969770d111eddb10016b0a3f900d10efa341a260a4871900e828f0eb23a8b49f1e28785c3968a9f5aa27bf02dbc414c2f8b3f6cc3937768_1280.jpg",
                ""
            ),
            
            # Balance exercises
            (
                "Single-Leg Stand", 5, "Beginner", "None", "Ankles, Core, Legs",
                "The single-leg stand improves balance, stability, and proprioception.",
                "A simple but effective balance training exercise",
                "1. Stand tall with feet together\n2. Shift weight to one foot\n3. Lift other foot off ground\n4. Hold position for 30 seconds\n5. Switch legs and repeat",
                "Focus on a fixed point for better balance, engage core",
                "https://pixabay.com/get/gabbcb03880215068eebc4ba0f1e1ac95fb420bd6c74205212e4104a9706bef71098ee17e0ce1614e0785ec09a3ade7f0b3365a8f0af7e3df7a85cc50d3b602da_1280.jpg",
                ""
            )
        ]
        
        cursor.executemany(
            "INSERT INTO exercises (name, category_id, difficulty, equipment, muscles_targeted, description, short_description, instructions, tips, image_url, video_url) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            exercises
        )
        
        # Sample workout templates
        workouts = [
            (
                "Beginner Full Body", 
                "A complete full body workout ideal for beginners to build a foundation of strength",
                "Beginner", 
                45, 
                "Strength", 
                1,  # Admin user
                1   # Public
            ),
            (
                "Cardio Blast", 
                "High-intensity cardio workout to improve endurance and burn calories",
                "Intermediate", 
                30, 
                "Cardio", 
                1,  # Admin user
                1   # Public
            ),
            (
                "Core Crusher", 
                "Focused core workout to build abdominal strength and stability",
                "Intermediate", 
                20, 
                "Core Strength", 
                1,  # Admin user
                1   # Public
            )
        ]
        
        cursor.executemany(
            "INSERT INTO workout_templates (name, description, difficulty, duration, goal, created_by, is_public) VALUES (?, ?, ?, ?, ?, ?, ?)",
            workouts
        )
        
        # Sample workout exercises (linking exercises to workouts)
        workout_exercises = [
            # Beginner Full Body
            (1, 1, 3, "10-12", 60, "Focus on form", 1),  # Barbell Squat
            (1, 2, 3, "10-12", 60, "Keep back on bench", 2),  # Bench Press
            (1, 7, 3, "30 sec", 30, "Keep core tight", 3),  # Plank
            
            # Cardio Blast
            (2, 4, 1, "10 min", 0, "Moderate pace", 1),  # Running
            (2, 5, 3, "1 min", 30, "Keep rhythm", 2),  # Jumping Rope
            
            # Core Crusher
            (3, 7, 3, "30 sec", 30, "Maintain proper form", 1),  # Plank
            (3, 8, 3, "15 each side", 30, "Control the movement", 2)  # Russian Twists
        ]
        
        cursor.executemany(
            "INSERT INTO workout_exercises (workout_id, exercise_id, sets, reps, rest_time, notes, order_num) VALUES (?, ?, ?, ?, ?, ?, ?)",
            workout_exercises
        )
        
        # Admin user
        cursor.execute(
            "INSERT INTO users (username, password, email, first_name, last_name, height, weight, goals, experience_level, is_admin) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            ("admin", "admin123", "admin@nffitness.com", "Admin", "User", 180, 80, "Maintenance", "Advanced", 1)
        )
        
        # Sample user
        cursor.execute(
            "INSERT INTO users (username, password, email, first_name, last_name, height, weight, goals, experience_level, is_admin) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            ("user", "password123", "user@example.com", "Sample", "User", 175, 75, "Muscle gain", "Intermediate", 0)
        )
        
        # Sample progress data for the sample user
        progress_data = [
            (2, "2023-01-01", 80.5, 18.0, 95.0, 85.0, 100.0, 35.0, 55.0, "Starting measurements"),
            (2, "2023-02-01", 79.0, 17.5, 96.0, 84.0, 99.5, 35.5, 55.5, "Good progress"),
            (2, "2023-03-01", 78.0, 16.8, 97.0, 83.0, 99.0, 36.0, 56.0, "Consistent training"),
            (2, "2023-04-01", 77.5, 16.0, 98.0, 82.0, 98.5, 36.5, 56.5, "Increased protein intake")
        ]
        
        cursor.executemany(
            "INSERT INTO user_progress (user_id, date, weight, body_fat, chest, waist, hips, arms, thighs, notes) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            progress_data
        )
        
        conn.commit()
        conn.close()
        
        st.success("Database initialized successfully!")

def get_exercise_categories():
    """Get all exercise categories"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM exercise_categories ORDER BY name")
    categories = [row[0] for row in cursor.fetchall()]
    
    conn.close()
    return categories

def get_exercises_by_category(category_name):
    """Get exercises for a specific category"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT e.* FROM exercises e
        JOIN exercise_categories c ON e.category_id = c.id
        WHERE c.name = ?
        ORDER BY e.name
    """, (category_name,))
    
    exercises = []
    for row in cursor.fetchall():
        exercise = dict(row)
        exercises.append(exercise)
    
    conn.close()
    return exercises

def get_exercise_by_id(exercise_id):
    """Get a specific exercise by ID"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM exercises WHERE id = ?", (exercise_id,))
    exercise = dict(cursor.fetchone())
    
    conn.close()
    return exercise

def get_all_exercises():
    """Get all exercises"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT e.*, c.name as category_name 
        FROM exercises e
        JOIN exercise_categories c ON e.category_id = c.id
        ORDER BY e.name
    """)
    
    exercises = []
    for row in cursor.fetchall():
        exercise = dict(row)
        exercises.append(exercise)
    
    conn.close()
    return exercises

def get_workout_templates():
    """Get all workout templates"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT * FROM workout_templates
        WHERE is_public = 1
        ORDER BY name
    """)
    
    templates = []
    for row in cursor.fetchall():
        template = dict(row)
        templates.append(template)
    
    conn.close()
    return templates

def get_workout_exercises(workout_id):
    """Get exercises for a specific workout template"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT we.*, e.name as exercise_name, e.image_url, e.short_description, e.difficulty
        FROM workout_exercises we
        JOIN exercises e ON we.exercise_id = e.id
        WHERE we.workout_id = ?
        ORDER BY we.order_num
    """, (workout_id,))
    
    exercises = []
    for row in cursor.fetchall():
        exercise = dict(row)
        exercises.append(exercise)
    
    conn.close()
    return exercises

def get_workout_template(workout_id):
    """Get a specific workout template by ID"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM workout_templates WHERE id = ?", (workout_id,))
    template = dict(cursor.fetchone())
    
    conn.close()
    return template

def get_user_progress(user_id):
    """Get progress data for a specific user"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT * FROM user_progress
        WHERE user_id = ?
        ORDER BY date
    """, (user_id,))
    
    progress = []
    for row in cursor.fetchall():
        entry = dict(row)
        progress.append(entry)
    
    conn.close()
    return progress

def add_progress_entry(user_id, date, weight, body_fat, chest, waist, hips, arms, thighs, notes):
    """Add a new progress entry for a user"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO user_progress 
        (user_id, date, weight, body_fat, chest, waist, hips, arms, thighs, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (user_id, date, weight, body_fat, chest, waist, hips, arms, thighs, notes))
    
    conn.commit()
    conn.close()

def add_exercise(name, category_id, difficulty, equipment, muscles_targeted, 
               description, short_description, instructions, tips, image_url, video_url):
    """Add a new exercise to the database"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO exercises
        (name, category_id, difficulty, equipment, muscles_targeted, 
         description, short_description, instructions, tips, image_url, video_url)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (name, category_id, difficulty, equipment, muscles_targeted, 
          description, short_description, instructions, tips, image_url, video_url))
    
    conn.commit()
    conn.close()

def add_workout_template(name, description, difficulty, duration, goal, created_by, is_public):
    """Add a new workout template"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO workout_templates
        (name, description, difficulty, duration, goal, created_by, is_public)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (name, description, difficulty, duration, goal, created_by, is_public))
    
    last_id = cursor.lastrowid
    
    conn.commit()
    conn.close()
    
    return last_id

def add_workout_exercise(workout_id, exercise_id, sets, reps, rest_time, notes, order_num):
    """Add an exercise to a workout template"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO workout_exercises
        (workout_id, exercise_id, sets, reps, rest_time, notes, order_num)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (workout_id, exercise_id, sets, reps, rest_time, notes, order_num))
    
    conn.commit()
    conn.close()
