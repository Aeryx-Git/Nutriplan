# 🥗 NutriPlan Agent

**NutriPlan Agent** is an end-to-end AI data pipeline and agent workflow designed to intelligently extract and structure complex recipe datasets from Instagram videos. Built as a Kaggle 5-Day Vibe Coding Final Project.

## Features
- **Multimodal Video Processing**: Uses Gemini 3.6 Flash's native multimodal capabilities to "watch" and "listen" to Instagram reels to extract recipes even when they aren't written in the caption.
- **Automated Scraping**: Uses yt-dlp to automatically download the highest quality video stream from public Instagram posts.
- **Data Structuring**: Enforces strict JSON output schemas (Recipe Name, Ingredients, Instructions) using Pydantic.
- **Local Storage**: Automatically saves extracted recipes to a local database (saved_recipes.json) for later reference.
- **Beautiful Web UI**: A clean, interactive Streamlit interface for easy operation.

## Setup Instructions

1. **Clone the repository**
   \\\Bash
   git clone https://github.com/Aeryx-Git/Nutriplan.git
   cd Nutriplan

2. **Install Dependencies**
   Ensure you have Python installed, then run:
   \\\Bash
   
   pip install -r requirements.txt

4. **Configure Environment**
   Create a .env file in the root directory and add your Google Gemini API key:
   
   \\\env
   GEMINI_API_KEY=your_actual_api_key_here

5. **Install Playwright Browsers**

   \\\Bash
   playwright install chromium

## Usage

Run the web interface locally using Streamlit:

\\\Bash 
streamlit run app.py


1. Paste a public Instagram Reel URL into the input field.
2. Click **Download & Extract**.
3. Watch as the AI downloads the video, processes it, and generates a structured recipe.
4. Download the extracted JSON or browse your previously saved recipes in the sidebar!

## 🛠️ Architecture
- app.py: Main Streamlit Web UI.
- downloader.py: Handles Instagram video downloads via yt-dlp.
- gemini_extractor.py: Interfaces with the Gemini API to process the video and extract the structured data.
- validator.py: Contains the Pydantic schema enforcing the JSON structure.
