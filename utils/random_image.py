import requests
import config


def space():
    url = f"https://api.nasa.gov/planetary/apod?api_key={config.API_KEY}"
    response = requests.get(url)
    data = response.json()
    return data["title"], data["url"]


if __name__ == '__main__':
    title, url = space()
    print(title)
    print(url)