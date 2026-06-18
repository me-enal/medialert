import json
import os

# Path to our saved data file
DATA_FILE = "data/hospitals_data.json"

def save_hospitals(hospitals):
    """
    Concept: JSON serialization — converts Python
    dictionary/list into a JSON file on disk
    """
    with open(DATA_FILE, 'w') as f:
        json.dump(hospitals, f, indent=4)

def load_hospitals():
    """
    Concept: JSON deserialization — reads JSON file
    and converts it back into Python list of dicts
    """
    # If saved file exists, load from it
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    
    # Otherwise load from original hospitals.py
    from data.hospitals import hospitals
    return hospitals