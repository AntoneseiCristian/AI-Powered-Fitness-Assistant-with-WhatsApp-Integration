from flask import Flask, render_template, request, session, redirect, url_for
from flask_babel import Babel, _

app = Flask(__name__)
app.secret_key = 'secret_key'
babel = Babel()

def get_locale():
    return session.get('lang', 'en')

babel.init_app(app, locale_selector=get_locale)

@app.route('/setlang/<lang>')
def setlang(lang):
    session['lang'] = lang
    return redirect(url_for('index'))

@app.route('/', methods=['GET', 'POST'])
def index():
    bmi = ''
    recommendation = ''
    if request.method == 'POST' and 'weight' in request.form and 'height' in request.form:
        weight = float(request.form.get('weight'))
        height = float(request.form.get('height'))
        bmi = calculate_bmi(weight, height)
        recommendation = get_recommendation(bmi)
    return render_template('index.html', bmi=bmi, recommendation=recommendation)

def calculate_bmi(weight, height):
    return round(weight / ((height / 100) ** 2), 2)

def get_recommendation(bmi):
    if bmi < 18.5:
        return _("You are underweight. It's recommended to consult a nutritionist for a balanced diet plan.")
    elif 18.5 <= bmi < 25:
        return _("You have a normal weight. Keep maintaining a balanced diet and regular physical activity.")
    elif 25 <= bmi < 30:
        return _("You are overweight. Consider a balanced diet and regular physical activity. Consult a healthcare professional if needed.")
    else:
        return _("You are in the obesity range. It's highly recommended to consult a healthcare professional for guidance and support.")

if __name__ == "__main__":
    app.run(debug=True)
