# Flask server that accepts a prompt and config.yaml file for the deployment in question
# makes a request to the OpenAI API with a well-formed prompt
# returns the response from the API to the caller 


from flask import Flask, request, jsonify
from k8s import handler
import os

app = Flask(__name__)


@app.route('/api', methods=['POST'])
def api():
    # get the prompt and config objects from the request
    prompt = request.form['prompt']
    config = request.form['config']


    # prompt = request.form.get('prompt')
    # config = request.form.get('config')
    
    # make request to OpenAI API with prompt and config
    # return response from API to caller
    final_prompt = handler(prompt, config)
    

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)