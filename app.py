## render_template -->to use html files present in templates
from flask import Flask,render_template,url_for 
import requests
from flask import request as flask_request

from src.hugging_face_text_summerizer.utils.common import read_yaml_file
from src.hugging_face_text_summerizer.constants import CONFIG_FILE_PATH

app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
#The below fuction is need in the app.py it is mandatory because when you run it flask run it automatically search for templates/index.html file in the give directory
#so you can keep "render_template('index.html')" or "hello world "->a string etc... if you keep a html file then thing get hosted accronding how there are decrible ther or else just shows the string
def Index():
    return render_template('index.html')


@app.route('/summarize', methods=['GET','POST'])
def summarize():
    if flask_request.method == 'POST':
        try:
            config = read_yaml_file(CONFIG_FILE_PATH)
            print("Config contents:", config)
            data = flask_request.form['data']
            maxL = int(flask_request.form['maxlength'])
            minL = maxL//4
            API_URL = config['hugging_face_pegasus_api_url']
            HF_TOKEN = config['huggging_face_pegasus_hf_key']
            
            headers = {"Authorization": f"Bearer {HF_TOKEN}"}
            


            def query(payload):
                response = requests.post(API_URL, headers=headers, json=payload)
                return response.json()
            
            output = query({
                "inputs": data,
                "parameters": {"min_length": minL, "max_length": maxL}
            })

            # Debug print
            print("Output:", output)
            summary = output[0].get('summary_text', '')
            # Check if output contains error
            if isinstance(output, list) and len(output) > 0:
                ## Hear the output is list we can acces it by output[0][summary_text] but this way help us to write safety code what if it is not there etc...
                return render_template('index.html', result=output[0].get('summary_text','No summary output[0][summary_text] not there'))
            
        except Exception as e:
            return render_template('index.html', result=f"Error: {str(e)}")
    return render_template('index.html')


if __name__ == '__main__':
    app.debug = True
    app.run()