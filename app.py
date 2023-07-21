from flask import Flask
from SEND_DATA_TO_THINGSPEAK import run

app = Flask(__name__)

@app.route('/')
def run_script():
    run()
    import SEND_DATA_TO_THINGSPEAK
    SEND_DATA_TO_THINGSPEAK.your_function()
    return "Script has been run!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
