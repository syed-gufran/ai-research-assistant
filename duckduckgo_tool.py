# duckduckgo_tool.py
import requests

class DuckDuckGoSearchTool:
    def __init__(self):
        self.api_url = "https://api.duckduckgo.com/"

    def search(self, query):
        params = {
            'q': query,
            'format': 'json',
            't': 'ai-research-assistant'
        }
        try:
            response = requests.get(self.api_url, params=params, timeout=10)
            data = response.json()
            # Try to get a summary or first related topic
            result = data.get('Abstract', '')
            if not result and data.get('RelatedTopics'):
                result = data['RelatedTopics'][0].get('Text', '')
            return result or "No results found."
        except Exception as e:
            return f"Search error: {str(e)}"
