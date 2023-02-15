import argparse
import yaml
import openai
import os 

openai.api_key = os.getenv("OPENAI_API_KEY", "")

def construct_prompt(query_str, config):
    prompt=f"\"\"\"\nYou are a kubectl assistant. You return kubectl commands.\n\"\"\"\n\n# delete all deployments in the namespace 'chirpy'\nkubectl delete --all deployments --namespace=chirpy\n\n# get list of pods in the namespace 'shawn'\nkubectl -n chirpy get pods\n\n# {query_str}\n"
    return prompt

def get_code_block(original_prompt, response):
    return response["choices"][0]["text"]

def handler(prompt, config=None):
    unformatted_prompt = construct_prompt(prompt, config)
    
    # count the number of words in final_prompt
    prompt_str_words = unformatted_prompt.split()
    if len(prompt_str_words) > 2048:
        raise ValueError("Prompt is too long, must be less than 2048 words")
    print(len(prompt_str_words))
    final_prompt = " ".join(prompt_str_words[:2048])
   
    completion = openai.Completion.create(
        model="code-cushman-001",
        prompt=final_prompt,
        temperature=0.1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=["#"]
    )
    code_block = get_code_block(unformatted_prompt, completion)

    # dry run first - ask the user if the code_block is correct
    # if yes, then execute the code block
    # if no, then ask the user for a new prompt
    print(code_block + " is the command to execute. Is this correct? (y/n)")
    user_input = input()
    if user_input != "y":
        return "User input was not y, exiting"
    os.system(code_block)
    return "Success!"

if __name__=="__main__":
    # take in user arguments for prompt and config
    parser = argparse.ArgumentParser(description='Kubectl debugging assistant')
    parser.add_argument('--prompt', type=str, help='prompt for the debugging assistant')

    # TODO: add support for multiple config files, potentially have vector DB lookups
    parser.add_argument('--config', type=str, help='config file for the debugging assistant', required=False)
    args = parser.parse_args()
    prompt = args.prompt
    config = args.config
    
    yaml_string = ""

    if config:
        # read in the config file, possibly multiple documents to parse
        with open(config, 'r') as stream:
            documents = yaml.load_all(stream, Loader=yaml.FullLoader)
            for document in documents:
                yaml_string += yaml.dump(document)

    print(handler(prompt, yaml_string))