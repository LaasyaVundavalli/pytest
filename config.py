import yaml
import os

CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'config.yaml')
with open(CONFIG_PATH, 'r') as f:
	config = yaml.safe_load(f)

BASE_URL = config.get('base_url')
USERNAME = config.get('username')
PASSWORD = config.get('password')
