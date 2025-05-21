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

`content_tool.py` provides a sample workflow for generating local SEO content. The script
fetches a trending news article, rewrites it with basic replacements and produces
text for a podcast episode and YouTube short. Network calls to news APIs,
YouTube, podcast hosts and Wordpress are represented as placeholders.

Run the workflow with:

```bash
python content_tool.py
```

Replace the API key and location inside the script with your own values.
