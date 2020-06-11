import time as time

from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from flask_celery import make_celery

app = Flask(__name__)
app.config['SECRET_KEY'] = 'there is no secret'

app.config.update(
    CELERY_BROKER_URL='amqp://localhost//',
    CELERY_RESULT_BACKEND='rpc://'
)

socketio = SocketIO(app, message_queue='amqp://')


celery = make_celery(app)


@app.route('/', methods=['GET', 'POST'])
def main():
    message = 'first'
    if request.method == 'POST':
        text = request.values.get('text')
        message = text
    return render_template('main.html', message=message)


@socketio.on('connection', namespace='/')
def confirmation_message(message):
    print('confirmation', {'connection_confirmation': message['connection_confirmation']})

@socketio.on('submit_result', namespace='/')
def text_handler(message):
	text = message['text']
	when_will_result.delay(text)


# # using this method with the ajax request
# @app.route('/task', methods=['GET', 'POST'])

@celery.task(name="task.message")
def when_will_result(text):
    socketio = SocketIO(message_queue='amqp://')
    condition = True
    while condition:
        for val in range(101):
            time.sleep(0.05)
            socketio.emit('progress_update', {'ratio': val})
        condition = False

    socketio.emit('progress_update', {'data_text': exampleresult()})
    return('when_will_result() -> ok; update_complete;')


def exampleresult():
    # JSON format for reading JS on the client
    preproc = []
    for i in range(5):
        preproc.append({"fieldtext": "{this_text}"
                       .format(this_text='Глокая куздра штеко будланула бокра и курдячит бокрёнка ' + str(i))
                        })
    return preproc

if __name__ == '__main__':
    socketio.run(app)
