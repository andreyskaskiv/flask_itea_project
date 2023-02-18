from flask import render_template, current_app, flash

from app.auth.models import Role, Profile, Post, User
from app.generate_data.main import  create_data
from app.main import main
from app.main.forms import GenerateDataForm


@main.route('/', methods=['GET', 'POST'])
def index():
    db = current_app.config['db']
    db.create_tables([Role, Profile, Post, User])

    if not Role.select().where(Role.name == 'user').first():
        roles = [
            ('user',),
            ('admin',)
        ]
        Role.insert_many(roles, fields=[Role.name]).execute()

    form = GenerateDataForm()
    if form.validate_on_submit():
        email_admin, password_admin = create_data()

        flash(f'{email_admin}  |  {password_admin}', 'success')
        flash('Database filled with test data', 'success')

    title = "Home"
    return render_template('main/index.html',
                           title=title,
                           form=form)
