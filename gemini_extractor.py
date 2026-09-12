import os
import time
from google import genai
from validator import Recipe

def extract_recipe_from_video(video_path: str, caption_text: str = "") -> Recipe:
    """
    Uploads a video to Gemini and extracts structured recipe information.
    """
    # Requires GEMINI_API_KEY environment variable to be set
    client = genai.Client()
    
    prompt = f"""
    You are an expert AI nutrition planner. Your task is to extract a recipe from the provided video and caption.
    Pay close attention to what is shown on screen and what is spoken in the video audio.
    
    Caption Text (if any):
    {caption_text}
    """
    
    print(f"Uploading video {video_path} to Gemini API...")
    # Upload the video file
    video_file = client.files.upload(file=video_path)
    
    print(f"Uploaded as {video_file.name}. Waiting for processing...")
    # Wait for the file to be processed (video processing takes a few seconds)
    while True:
        file_info = client.files.get(name=video_file.name)
        if file_info.state.name == "ACTIVE":
            break
        elif file_info.state.name == "FAILED":
            raise Exception("Video processing failed in Gemini.")
        time.sleep(2)
        
    print("Video processed. Generating content...")
    response = client.models.generate_content(
        model='gemini-3.6-flash',
        contents=[video_file, prompt],
        config=genai.types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=Recipe,
            temperature=0.1
        ),
    )
    
    # Optionally delete the file from Gemini to save space (since we are done with it)
    try:
        client.files.delete(name=video_file.name)
    except:
        pass
        
    return response.parsed
