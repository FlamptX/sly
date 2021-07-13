import requests

url = "https://memifyapi.herokuapp.com/api/meme/dank/1000"

headers = {
    'x-api-key': "qD3fmWSfwOoAIGzhtcB1AEWYMnLWveMTvzIymAXaOXRfvszhTV",
    }

response = requests.request("GET", url, headers=headers)
json = response.json()
print(json)