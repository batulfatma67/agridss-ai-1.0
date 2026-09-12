# agridss-ai-1.0
Generative AI-powered agricultural assistant using RAG to provide personalized, explainable, and practical farming guidance.

## OpenAI setup

Install the dependencies, then configure your OpenAI API key before starting
Streamlit:

```powershell
pip install -r requirements.txt
$env:OPENAI_API_KEY = "your-api-key"
streamlit run app.py
```

For Streamlit Community Cloud, add `OPENAI_API_KEY` under the app's Secrets
settings. The app uses `gpt-4o-mini` by default; set `OPENAI_MODEL` to use a
different available model.
