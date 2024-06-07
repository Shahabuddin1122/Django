from flask import Flask
import spacy

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    image_processing()
    return {
        'message': 'Hello World!',
        'id': 1
    }


@app.route('/user/<name>')
def user(name):
    return 'Hello %s!' % name


if __name__ == '__main__':
    app.run(debug=True)


def image_processing():
    nlp = spacy.load('en_core_web_sm')
    with open("data.txt", "r") as f:
        text = f.read()
        print(nlp(text))
    return "Hello World!"
