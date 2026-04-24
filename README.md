# ResearchMind AI

A Multi-Agent Research System built with LangChain, Google Gemini, Tavily, and Streamlit. This application uses four specialized AI agents collaborating (searching, reading/scraping, writing, and critiquing) to deliver a polished research report on any topic.

## Features
- **Search Agent:** Uses Tavily Search API to gather recent web information.
- **Reader Agent:** Scrapes and extracts deep content from web sources.
- **Writer Chain:** Drafts a full research report based on search and reading.
- **Critic Chain:** Reviews and scores the report.

## Setup Instructions

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd Multi-agent-research-system
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Environment Variables
Create a `.env` file in the root directory and add your API keys:
```env
GOOGLE_API_KEY=your_google_gemini_api_key
TAVILY_API_KEY=your_tavily_api_key
```

### 4. Run the Application
```bash
streamlit run app1.py
```
*(Note: You can also use `app.py` for an alternative UI layout).*

## Deployment to Render

This repository is ready to be hosted on [Render](https://render.com). 

**Option 1: Using render.yaml (Blueprint)**
1. Connect your GitHub repository to Render.
2. Render will automatically detect the `render.yaml` Blueprint.
3. Once the service is created, go to the Environment settings and add your actual `GOOGLE_API_KEY` and `TAVILY_API_KEY`.

**Option 2: Manual Web Service**
1. Create a New Web Service on Render.
2. Connect your GitHub repository.
3. Configure the following:
   - **Environment:** Python
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `streamlit run app1.py --server.port $PORT --server.address 0.0.0.0`
4. Add Environment Variables:
   - `PYTHON_VERSION`: `3.10.0` (or your preferred version)
   - `GOOGLE_API_KEY`: `<your-key>`
   - `TAVILY_API_KEY`: `<your-key>`
5. Click **Create Web Service**.
