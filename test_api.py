import requests
import json


def make_api_get_call(url):
    response = requests.get(url)
    if response.status_code == 200:
        print("API Response:")
        print(response.json())
    else:
        print(f"Error: {response.status_code}, {response.text}")


def make_api_post_call(url, data=None, headers=None):
    response = requests.post(url, data=json.dumps(data), headers=headers)
    if response.status_code == 200:
        print("API Response:")
        print(response.json())
    else:
        print(f"Error: {response.status_code}, {response.text}")


def make_api_delete_call(url):
    response = requests.delete(url)
    if response.status_code == 200:
        print("API Response:")
        print(response.json())
    else:
        print(f"Error: {response.status_code}, {response.text}")


if __name__ == "__main__":
    # make_api_get_call("http://127.0.0.1:5000/api/baby/1/Hadar")
    make_api_post_call("http://127.0.0.1:5000/api/baby/1/Sharon",
                        data={"gender": "f", "dob": "2022-06-01"},
                        headers={"Content-Type": "application/json"})
    # make_api_delete_call("http://127.0.0.1:5000/api/baby/1/Shalom")
