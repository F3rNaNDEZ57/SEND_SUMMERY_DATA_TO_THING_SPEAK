from flask import Flask

app = Flask(__name__)

@app.route('/run-script')
def run_script():
    # Your existing script here.
    # ...

    if response.status_code == 200:
        return 'Data sent to ThingSpeak successfully'
    else:
        return 'Failed to send data to ThingSpeak'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
