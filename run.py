from dotenv import load_dotenv
from src.app import app as flask_app
import os

load_dotenv(os.path.join(os.getcwd(), ".env"))

flask_app.run(debug=True)
