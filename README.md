# agridss-ai-1.0
Generative AI-powered agricultural assistant using RAG to provide personalized, explainable, and practical farming guidance.

## OpenAI setup

Install the dependencies, then configure your OpenAI API key before starting
Streamlit. For local development, copy `.streamlit/secrets.toml.example` to
`.streamlit/secrets.toml` and replace the placeholder with your key:

```powershell
pip install -r requirements.txt
streamlit run app.py
```

The app reads `OPENAI_API_KEY` and `OPENAI_MODEL` from Streamlit secrets. It
also accepts the `OPENAI_API_KEY` and `OPENAI_MODEL` environment variables. If
neither is configured, the sidebar provides a masked, session-only key field.
Groq keys beginning with `gsk_` are routed automatically to Groq's
OpenAI-compatible API and use `openai/gpt-oss-120b` by default.

For Streamlit Community Cloud, paste the contents of the template into the
app's **Settings > Secrets** panel and replace the placeholder. The app uses
`gpt-4o-mini` by default; set `OPENAI_MODEL` to use a different available
model.
