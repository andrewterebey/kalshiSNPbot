from dotenv import load_dotenv
import os

# Specify the path to your env file
from pathlib import Path
env_path = Path('.') / 'info.env'
load_dotenv(dotenv_path=env_path)

# Retrieve the email and password
username = os.getenv('EMAIL')
password = os.getenv('PASSWORD')

print(username, password)  # For testing purposes, remove this line in production
