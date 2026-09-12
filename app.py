import streamlit as st
import os
import json
from dotenv import load_dotenv
from downloader import download_video
from gemini_extractor import extract_recipe_from_video

# Load environment variables
load_dotenv()

st.set_page_config(page_title="NutriPlan Agent", page_icon="🥗", layout="wide")

# ---- Database Setup ----
DB_FILE = "saved_recipes.json"

def load_saved_recipes():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def save_recipe(recipe_data):
    recipes = load_saved_recipes()
    # Check if it already exists (basic check by name)
    if not any(r.get("recipe_name") == recipe_data.recipe_name for r in recipes):
        recipes.insert(0, recipe_data.model_dump())
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(recipes, f, indent=2)

# ---- Sidebar for Saved Recipes ----
st.sidebar.title("📚 Saved Recipes")
saved_recipes = load_saved_recipes()

if not saved_recipes:
    st.sidebar.info("No recipes saved yet. Extract one to get started!")
else:
    for idx, r in enumerate(saved_recipes):
        with st.sidebar.expander(f"🍲 {r.get('recipe_name', 'Unknown Recipe')}"):
            st.markdown("**Ingredients**")
            for item in r.get('ingredients', []):
                st.markdown(f"- {item}")
            st.markdown("**Instructions**")
            for i, step in enumerate(r.get('instructions', []), 1):
                st.markdown(f"**Step {i}:** {step}")

# ---- Main Content ----
st.title("🥗 NutriPlan Agent")
st.markdown("Extract structured recipes from Instagram videos/reels using Gemini's native Video AI!")

# Check for API key
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    st.error("⚠️ GEMINI_API_KEY is not set in the environment or .env file.")
    st.stop()

# Input section
url = st.text_input("Enter Instagram Post URL:", placeholder="https://www.instagram.com/p/...")

if st.button("Download & Extract", type="primary"):
    if not url:
        st.warning("Please enter a valid URL.")
    else:
        # Step 1: Download Video
        with st.spinner("Downloading video using yt-dlp... This might take a bit."):
            video_path = download_video(url)
            
        if not video_path or not os.path.exists(video_path):
            st.error("Failed to download video from the URL. The post might be private or unavailable.")
        else:
            st.success(f"Successfully downloaded video!")
            
            # Step 2: Extract using Video Model
            with st.spinner("Uploading video to Gemini and extracting recipe data..."):
                try:
                    recipe_data = extract_recipe_from_video(video_path)
                    
                    # Save to local database
                    save_recipe(recipe_data)
                    
                    st.divider()
                    st.subheader(f"🍲 {recipe_data.recipe_name}")
                    
                    col1, col2 = st.columns([1, 2])
                    
                    with col1:
                        st.markdown("### Ingredients")
                        for item in recipe_data.ingredients:
                            st.markdown(f"- {item}")
                            
                    with col2:
                        st.markdown("### Instructions")
                        for i, step in enumerate(recipe_data.instructions, 1):
                            st.markdown(f"**Step {i}:** {step}")
                            
                    # Provide JSON download
                    st.divider()
                    st.download_button(
                        label="Download Recipe JSON",
                        data=recipe_data.model_dump_json(indent=2),
                        file_name=f"{recipe_data.recipe_name.replace(' ', '_')}.json",
                        mime="application/json"
                    )
                    
                    st.success("Recipe extracted and saved to your library!")
                    
                except Exception as e:
                    st.error(f"Error during AI extraction: {e}")
                finally:
                    # Clean up the local video file to save space
                    try:
                        if os.path.exists(video_path):
                            os.remove(video_path)
                    except:
                        pass
