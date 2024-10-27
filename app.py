from flask import Flask, render_template, request, jsonify
from confluent_kafka import Producer

app = Flask(__name__)

# Configure Kafka producer
conf = {'bootstrap.servers': "localhost:9092",
        'group.id': "clicks_group",
        'auto.offset.reset': 'earliest'}

producer = Producer(conf)

@app.route('/')
def index():
    images = {
        1: 'https://logo.clearbit.com/amazon.com',
        3: 'https://logo.clearbit.com/facebook.com',
        5: 'https://logo.clearbit.com/twitter.com',
        7: 'https://logo.clearbit.com/youtube.com',
        9: 'https://logo.clearbit.com/google.com'
    }
    return render_template('index.html', images=images)
    #return render_template('index.html')

@app.route('/click', methods=['POST'])
def click():
    button_id = request.form.get('button_id')
    if button_id:
        # Send message to Kafka
        producer.produce('clicks_topic', key=button_id, value=button_id)
        producer.flush()
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'error', 'message': 'No button_id provided'})

if __name__ == '__main__':
    app.run(debug=True)
