from flask import render_template, flash


from app.main import main
from app.main.forms import GenerateDataForm

from utils.fake_users.db_manager import main as write_fake_profiles


@main.route('/', methods=['GET', 'POST'])
def index():

    form = GenerateDataForm()
    if form.validate_on_submit():
        qty = int(form.qty.data)
        write_fake_profiles(qty)

        flash('Database filled with test data', 'success')

    title = "Home"
    return render_template('main/index.html',
                           title=title,
                           form=form)
