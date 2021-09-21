import json
import os

from flask import Flask
from flask import request

app = Flask(__name__)

BASE_COMMMAND = "echo '{{ingr_string}}' | {phrase_tagger_bin_path}/parse-ingredients.py --model-file {model_file_path}"
COMMAND = BASE_COMMMAND.format(
    phrase_tagger_bin_path=os.environ['PHRASE_TAGGER_BIN_PATH'], model_file_path=os.environ['MODEL_FILE_PATH']
)


@app.route("/", methods=['POST'])
def parse_ingredients():
    post_data = request.get_json(force=True)
    ingr_strings = post_data['ingr_strings']
    ingr_data = []
    for ingr_string in ingr_strings:
        command = COMMAND.format(ingr_string=ingr_string)
        result = os.popen(command)
        output = result.read()
        ingr_data.append(json.loads(output)[0])
    return {'ingr_data': ingr_data}
