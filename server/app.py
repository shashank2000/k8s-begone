# Flask server that accepts a prompt and config.yaml file for the deployment in question
# makes a request to the OpenAI API with a well-formed prompt
# returns the response from the API to the caller 


from flask import Flask, request, jsonify
from k8s import handler
import os

app = Flask(__name__)


@app.route('/api', methods=['GET'])
def api():
    # get prompt, exception_msg from request
    prompt = request.args.get('prompt')
    exception_msg = request.args.get('exception_msg')

    # make request to OpenAI API with prompt and config
    # return response from API to caller
    return handler(prompt, exception_msg)
    

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)