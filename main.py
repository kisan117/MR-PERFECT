import requests
import re

def extract_token(cookie):
    try:
        headers = {
            'cookie': cookie,
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; Mobile) AppleWebKit/537.36 Chrome/120 Safari/537.36'
        }

        url = "https://m.facebook.com/composer/ocelot/async_loader/?publisher=feed"
        response = requests.get(url, headers=headers)

        if "for (;;);" in response.text or "login" in response.url:
            return 'Invalid or expired cookie.'

        match = re.search(r'"accessToken\\":\\"(EAA\w+)\\"', response.text)
        if match:
            return f"Access Token:\n{match.group(1)}"
        else:
            return "Token not found. Try with a fresh cookie."
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    print("=== Facebook Token Extractor ===")
    cookie_input = input("Paste your Facebook cookie:\n")
    result = extract_token(cookie_input.strip())
    print("\n" + result)
