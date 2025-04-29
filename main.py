import requests

def extract_token_from_cookie(cookie):
    # Facebook Graph API URL for user information
    url = 'https://graph.facebook.com/v15.0/me?access_token={cookie}'

    headers = {
        'cookie': cookie,
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36'
    }

    # Send GET request to Facebook Graph API
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        # If response is OK, extract the token
        result = response.json()
        if 'id' in result:
            print("Token extraction successful!")
            return result
        else:
            print("Error: Token extraction failed.")
            return None
    else:
        # If error occurs (invalid session, expired cookie etc.)
        print(f"Error: {response.status_code} - {response.text}")
        return None

# Example of how to use this
cookie = input("Paste your Facebook cookie: ")
token_info = extract_token_from_cookie(cookie)
if token_info:
    print(f"Extracted Token Info: {token_info}")
