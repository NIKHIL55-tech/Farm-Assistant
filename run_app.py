from app import app
import logging
import os

# Make sure templates directory exists
templates_dir = 'templates'
if not os.path.exists(templates_dir):
    os.makedirs(templates_dir)
    logging.warning(f"Created missing {templates_dir} directory")

# Make sure models directory exists for yield prediction models
models_dir = 'models'
if not os.path.exists(models_dir):
    os.makedirs(models_dir)
    logging.warning(f"Created missing {models_dir} directory")

if __name__ == '__main__':
    # Run the Flask application
    app.run(debug=True, host='0.0.0.0', port=5000) 