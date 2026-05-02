
"""
CareerIQ Backend - app.py
Main Flask application entry point
"""
 
from flask import Flask
from flask_cors import CORS
from routes.resume_routes import resume_bp
 
app = Flask(__name__)
 
# Allow requests from your Next.js frontend (adjust origin as needed)
CORS(app)
 
# Register blueprints
app.register_blueprint(resume_bp)
 
 
@app.route("/")
def home():
    return {"message": "CareerIQ Backend Running!", "status": "ok"}
 
 
if __name__ == "__main__":
    app.run(debug=True, port=5000)