import requests
def getAccessToken():
  url = "https://id.twitch.tv/oauth2/token"

  payload='grant_type=refresh_token&refresh_token=ygwjdynkiz6f7blo0qrjn5444f7a4vkgvxo2nlobdjgvtx94lz&client_id=dopdpg77hpbj960fjqvvg6pocyk0cp&client_secret=tfd22bxozj8q2schorcenf2ickqs9e'
  headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Cookie': 'twitch.lohp.countryCode=US; server_session_id=39c40b58db2f4db9b08a97e49a60c5f1; unique_id=zpsXp7lsLValOEHcQd16yBaOAQyajksz; unique_id_durable=zpsXp7lsLValOEHcQd16yBaOAQyajksz'
  }

  response = requests.request("POST", url, headers=headers, data=payload)
  return "oauth:" + response.json()["access_token"]
