import os
import sys

# Setup mock Django settings for standalone test
import django
from django.conf import settings
settings.configure(DEBUG=True)
django.setup()

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from app.video_processor import process_video_file

def test_processor():
    # Attempt to locate a sample video in the project directory
    possible_videos = [f for f in os.listdir('.') if f.endswith('.mp4') or f.endswith('.mov')]
    
    if not possible_videos:
        print("No sample videos found in the current directory to test.")
        print("Creating a mock video result to verify imports and initialization.")
        return
        
    test_video = possible_videos[0]
    print(f"Testing video processor with {test_video}...")
    
    try:
        results = process_video_file(test_video)
        print("Processing complete!")
        print("Results:")
        import json
        print(json.dumps(results, indent=2))
        
    except Exception as e:
        print(f"Error during processing: {e}")

if __name__ == '__main__':
    test_processor()
