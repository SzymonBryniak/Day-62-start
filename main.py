from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import csv
import pandas as pd

'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)
# https://docs.sqlalchemy.org/en/20/orm/quickstart.html


# class User(Base):
#     __tablename__ = 'users'
#     id = Column(Integer, primary_key=True)
#     first_name = Column(Text)
#     last_name = Column(Text, nullable=True)

dataframe = pd.read_csv('./cafe-data.csv', index_col=False, on_bad_lines="skip") #on_bad_lines="skip" to fix the error
ratings = dataframe.iloc[:,4:6]
unique = pd.unique(ratings['Coffee'])  # to try unique length. Just unique doesn't work.



# ratings_coffee = dataframe.iloc[:,4:5].to_dict() # worse version of unique
# ratings_coffee_list = []
# for key, value in ratings_coffee['Coffee'].items():
#     print(value)
#     ratings_coffee_list.append(value)

print(unique)

class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    url = StringField('Cafe Location', validators=[DataRequired(), URL()])
    opening_times = StringField('Opening Times', validators=[DataRequired()])
    closing_times = StringField('Closing Times', validators=[DataRequired()])
    coffee_rating = SelectField(u'Coffee Rating', choices=[i for i in unique])
    wifi_stregth = SelectField(u'WiFi Strength', choices=["💪","💪💪","💪💪💪","💪💪💪💪"])
    power = SelectField(u'WiFi Strength', choices=["🔌","🔌🔌","🔌🔌🔌","🔌🔌🔌🔌"])
    submit = SubmitField('Submit')

# Exercise:
# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
#e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------

# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['GET', 'POST'])
def add_cafe(): 
    form = CafeForm()
    if form.validate_on_submit():
        print('True')
        print(form.wifi_stregth.data, form.cafe.data)
        with open('./cafe-data.csv', mode="a", encoding="utf-8") as file:
            file.write(f"\n{form.cafe.data},{form.url.data},{form.opening_times.data},{form.closing_times.data}, {form.coffee_rating.data},{form.wifi_stregth.data},{form.power.data}")
            
    # Make the form write a new row into cafe-data.csv
    # with   if form.validate_on_submit()
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    dict_Test = {0: "value1"}
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        # cafes = pd.read_csv('./cafe-data.csv')
        for row in csv_data:
            list_of_rows.append(row)
        # print(cafes)
        # cafes = pd.DataFrame(list_of_rows)
        # print(cafes)
    return render_template('cafes.html',cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
