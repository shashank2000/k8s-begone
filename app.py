# Flask server that accepts a prompt and config.yaml file for the deployment in question
# makes a request to the OpenAI API with a well-formed prompt
# returns the response from the API to the caller 


from flask import Flask, request, jsonify
from k8s import handler
import os

app = Flask(__name__)

simple_in_memory_db = {}

@app.route('/api', methods=['POST'])
def api(error_message, prompt, config):
    # get user id
    user_id = request.headers.get('user_id')

    # get the prompt and config objects from the request
    prompt = request.form['prompt']
    config = request.form['config']
    
    # make request to OpenAI API with prompt and config
    # return response from API to caller
    suggestion = handler(prompt, config)
    simple_in_memory_db[user_id].append((suggestion,))
    # server remembers what we suggested to the caller so we can use it in the next request
    return jsonify(suggestion)

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)