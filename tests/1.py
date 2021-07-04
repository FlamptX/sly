import requests

url = "https://nsfw-image-classification1.p.rapidapi.com/img/nsfw"

# Don't go on the link below as it might be NSFW. It is here for testing the API
payload = "{\"url\": \"https://images-ext-2.discordapp.net/external/O5Oxq_bx4rQvfFoe05k836o3fq0aV_tSJiWlp1uQJeg/https/i.redd.it/1vaasl5xk6871.png?width=676&height=556\"}"
headers = {
    'content-type': "application/json",
    'x-rapidapi-key': "",
    'x-rapidapi-host': "nsfw-image-classification1.p.rapidapi.com"
    }

response = requests.request("POST", url, data=payload, headers=headers)

json = response.json()
print(round(json['NSFW_Prob']))