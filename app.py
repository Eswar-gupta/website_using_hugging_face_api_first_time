from flask import Flask, render_template, request
import requests
from src.hugging_face_text_summerizer.utils.common import read_yaml_file
from src.hugging_face_text_summerizer.constants import CONFIG_FILE_PATH

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/TextSummerizer', methods=['GET', 'POST'])
def TextSummerizer():
    if request.method == 'POST':
        try:
            config = read_yaml_file(CONFIG_FILE_PATH)
            data = request.form['data']
            maxL = int(request.form['maxlength'])
            minL = maxL // 4

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

            summary = output[0].get('summary_text', 'Error: Unable to generate summary.')
            return render_template('TextSummerizer.html', result=summary)

        except Exception as e:
            return render_template('TextSummerizer.html', result=f"Error: {str(e)}")
    return render_template('TextSummerizer.html', result="")

@app.route('/MovieReview')
def MovieReview():
    return render_template('MovieReview.html')

if __name__ == '__main__':
    app.debug = True
    app.run()
