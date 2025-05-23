# :earth_americas: GDP dashboard template

A simple Streamlit app showing the GDP of different countries in the world.

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://gdp-dashboard-template.streamlit.app/)

### How to run it on your own machine

1. Install the requirements

   ```
   $ pip install -r requirements.txt
   ```

2. Run the app

   ```
   $ streamlit run streamlit_app.py
   ```

## Content creation tool

`content_tool.py` demonstrates a basic workflow for generating local SEO content.
The script fetches trending news, rewrites it with OpenAI and generates at least
two images with DALL·E. These images are compiled into a short video with a QR
code watermark that links back to the article.
Network calls to news APIs, OpenAI, YouTube, podcast hosts and Wordpress are
still represented as placeholders.

Run the workflow with:

```bash
python content_tool.py
```

Replace the news and OpenAI API keys along with the location inside the script
with your own values.
