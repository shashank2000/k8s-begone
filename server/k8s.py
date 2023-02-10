import argparse
import yaml
import openai
import os 

openai.api_key = os.getenv("OPENAI_API_KEY", "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")

def construct_prompt(query_str, config):
    prompt = '''
    You are a Kubernetes debugging assistant.
    Given the following config object, and a question, suggest what actions can be taken with references ("SOURCES").
    ALWAYS return a "SOURCES" part in your answer.

    QUESTION: My cluster has 72 pods, a large chunk of which are the blenderbot pod. How do I prevent there from being so many replicas of the blenderbot?
    =========
    Config: apiVersion: apps/v1\nkind: Deployment\nmetadata:\n  name: blenderbot\n  namespace: chirpy\nspec:\n  selector:\n    matchLabels:\n      app: blenderbot\n  template:\n    metadata:\n      labels:\n        app: blenderbot\n    spec:\n      containers:\n      - image: 742352046111.dkr.ecr.us-east-1.amazonaws.com/chirpy/blenderbot:latest\n        name: main\n        ports:\n        - containerPort: 80\n          name: main\n        readinessProbe:\n          httpGet:\n            path: /\n            port: 80\n          initialDelaySeconds: 120\n      tolerations:\n      - effect: NoSchedule\n        key: node_type\n        operator: Equal\n        value: gpu\napiVersion: v1\nkind: Service\nmetadata:\n  name: blenderbot\n  namespace: chirpy\nspec:\n  ports:\n  - port: 80\n    protocol: TCP\n    targetPort: 80\n  selector:\n    app: blenderbot\n
    =========
    FINAL ANSWER: Check your node groups, its possible the pod isn't being able to get scheduled on any node and so is constantly respawning. 
    SOURCES: https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/

    QUESTION: How to eat vegetables using kubectl?
    =========
    Config: apiVersion: apps/v1\nkind: Deployment\nmetadata:\n  name: blenderbot\n  namespace: chirpy\nspec:\n  selector:\n    matchLabels:\n      app: blenderbot\n  template:\n    metadata:\n      labels:\n        app: blenderbot\n    spec:\n      containers:\n      - image: 742352046111.dkr.ecr.us-east-1.amazonaws.com/chirpy/blenderbot:latest\n        name: main\n        ports:\n        - containerPort: 80\n          name: main\n        readinessProbe:\n          httpGet:\n            path: /\n            port: 80\n          initialDelaySeconds: 120\n      tolerations:\n      - effect: NoSchedule\n        key: node_type\n        operator: Equal\n        value: gpu\napiVersion: v1\nkind: Service\nmetadata:\n  name: blenderbot\n  namespace: chirpy\nspec:\n  ports:\n  - port: 80\n    protocol: TCP\n    targetPort: 80\n  selector:\n    app: blenderbot\n

    =========
    FINAL ANSWER: You can't eat vegetables using kubernetes. You can only eat them using your mouth.
    SOURCES:

    QUESTION: {query_str}
    =========
    {config}
    =========
    FINAL ANSWER:

    '''
    return prompt.format(query_str=query_str, config=config)

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