import requests

url = "https://symptom-checker4.p.rapidapi.com/analyze"

querystring = {"symptoms":"<REQUIRED>"}

payload = {"symptoms": "I have a red rash on my forearm that appeared suddenly last night. It does not itch or hurt."}
headers = {
	"content-type": "application/json",
	"X-RapidAPI-Key": "SIGN-UP-FOR-KEY",
	"X-RapidAPI-Host": "symptom-checker4.p.rapidapi.com"
}

response = requests.request("POST", url, json=payload, headers=headers, params=querystring)

print(response.text)