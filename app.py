from flask import Flask, render_template,request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Use DATABASE_URL from environment variable (Vercel will set this automatically)
# Falls back to SQLite for local development if DATABASE_URL is not set
database_url = os.getenv('DATABASE_URL', 'sqlite:///todo.db')

# Fix for SQLAlchemy 2.0+: Convert postgres:// to postgresql://
# Vercel/Neon sometimes provides postgres:// but SQLAlchemy 2.0+ requires postgresql://
if database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configure connection pool for Neon PostgreSQL (important for serverless)
if database_url.startswith('postgresql://'):
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_pre_ping': True,  # Verify connections before using them
        'pool_recycle': 300,    # Recycle connections after 5 minutes
        'pool_size': 10,        # Connection pool size
        'max_overflow': 5       # Allow up to 5 extra connections
    }

db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False) 
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

# Helper function to ensure tables exist (Flask 3.x compatible)
def ensure_tables_exist():
    try:
        db.create_all()
    except Exception as e:
        print(f"Error creating tables: {e}")

@app.route('/',methods=['GET', 'POST'])
def hello_world():
    ensure_tables_exist()  # Ensure tables exist before querying
    if request.method=='POST':
        title=request.form['title']
        desc=request.form['desc']
        todo = Todo(title=title, desc=desc)  
        db.session.add(todo)
        db.session.commit()
        
    allTodo=Todo.query.all()
    return render_template('index.html', allTodo=allTodo)

@app.route('/show')  
def products():
    allTodo=Todo.query.all()
    print(allTodo)
    return 'This is the products page'

@app.route('/update/<int:sno>', methods=['GET', 'POST'])  
def update(sno):
    ensure_tables_exist()  # Ensure tables exist before querying
    if request.method=='POST':
        title=request.form['title']
        desc=request.form['desc']
        todo=Todo.query.filter_by(sno=sno).first() 
        todo.title=title
        todo.desc=desc
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
    todo=Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo=todo)

@app.route('/delete/<int:sno>')  
def delete(sno):
    todo=Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True, port=8000)
