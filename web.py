from matplotlib.pyplot import text
from numpy import imag
from flask import Flask, request, render_template
import os

app = Flask(__name__)


@app.route('/')
def home(text_size="24px"):
    img = ['https://img.cpcdn.com/steps/12151953/m/e4ead46bfd61daa8f1655c006518fb29?u=4038599&p=1376194319']
    text = '4、次に、鍋につゆの材料を入れて沸騰したら、うどんを入れて再沸騰させる。その後、具を全部入れて煮立ったら火を止める。'
    if "text_size" in request.args:
        text_size = request.args["text_size"]
    return render_template('step.html', img=img, text=text, text_size=text_size)



if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0',  port=port)

    