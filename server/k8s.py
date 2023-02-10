import argparse
import yaml
import openai
import os 

openai.api_key = os.getenv("OPENAI_API_KEY", "")

def construct_prompt(query_str, config):
    prompt = f'''
        You are a Kubernetes debugging assistant. I've tried the following commands on my cluster, and the outputs are below. 
        Give me another command to try, with no English text, only kubectl commands. Make the command's output minimal so it's just enough to triage. 
        {query_str}
    '''
    return prompt

def handler(prompt, config):
    # TODO: only get the relevant parts of the config
    # TODO: decide what the relevant parts of the config are
    unformatted_prompt = construct_prompt(prompt, config)
    # count the number of words in final_prompt
    prompt_str_words = unformatted_prompt.split()
    if len(prompt_str_words) > 2048:
        raise ValueError("Prompt is too long, must be less than 2048 words")
    final_prompt = " ".join(prompt_str_words[:2048])

    completion = openai.Completion.create(
        engine="davinci",
        prompt=final_prompt,
        max_tokens=1000,
        temperature=0.4,
        frequency_penalty=1.9,
    )

    return completion["choices"][0]["text"]

if __name__=="__main__":
    # take in user arguments for prompt and config
    parser = argparse.ArgumentParser(description='Kubectl debugging assistant')
    parser.add_argument('--prompt', type=str, help='prompt for the debugging assistant')
    parser.add_argument('--config', type=str, help='config file for the debugging assistant')
    args = parser.parse_args()
    prompt = args.prompt
    config = args.config
    
    yaml_string = ""

    # read in the config file, possibly multiple documents to parse
    with open(config, 'r') as stream:
        documents = yaml.load_all(stream, Loader=yaml.FullLoader)
        for document in documents:
            yaml_string += yaml.dump(document)

    print(handler(prompt, yaml_string))