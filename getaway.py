from flask import Flask, request, send_from_directory 
from flask_cors import CORS

from kafka import KafkaProducer
import json

app = Flask(__name__)
CORS(app)

# Root url
@app.route('/')
def root():    
    print("root")    
    return staticContent('index.html')
    
# Serve static content    
@app.route('/<path>')
def staticContent(path):    
    return send_from_directory('www', path)
    
# Receive events
@app.route('/events', methods=['POST'])
def addEvent():    
    event = request.get_json()   
    producer.send('sensors', json.dumps(event).encode()) 
    print(json.dumps(event))            
    return '', 204

if __name__ == '__main__':    
    producer = KafkaProducer(bootstrap_servers='localhost:9092')
    app.run(debug=True,ssl_context='adhoc', host='0.0.0.0', port=8080)