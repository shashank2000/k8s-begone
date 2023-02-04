# make requests to Flask endpoint
import requests
import argparse
import yaml


def make_request(yaml_path, prompt):
    with open(yaml_path, "r") as stream:
        yaml_data = yaml.safe_load(stream)

    # Convert the Python object to a string
    yaml_string = yaml.dump(yaml_data)
    
    url = "http://localhost:5000/api"
    payload = {'prompt': prompt, 'config': yaml_string}
    headers = {'Content-Type': 'application/json'}
    response = requests.request("POST", url, headers=headers, data=payload)
    return response

if __name__ == "__main__":
    args = parse_args()
    prompt = args.prompt
    yaml_path = args.yaml_path
    response = make_request(yaml_path, prompt)
    print(response.text)
