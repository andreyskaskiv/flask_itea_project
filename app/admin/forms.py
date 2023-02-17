from flask_wtf import FlaskForm
from wtforms import SubmitField, HiddenField, StringField, SelectField
from wtforms.validators import DataRequired, Length, Regexp, Email


class EditUserForm(FlaskForm):
    id = HiddenField('id')
    username = StringField(
        'Edit username',
        validators=[
            DataRequired(),
            Length(3, 100),
            Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 'Username must contains only letters, underscores or digits')
        ],
        render_kw={'placeholder': 'Enter your name'}
    )

    email = StringField("Email: ",
                        validators=[DataRequired(), Length(10, 100), Email()],
                        render_kw={'placeholder': 'Enter email'})

    role = SelectField('Update role',
                       choices=[('1', 'user'), ('2', 'admin')])

    submit = SubmitField("Edit",
                         render_kw={'class': 'btn btn-success'})

    # def validate_email(self, email):
    #     if email.data != current_user.email:
    #         if User.select().where(User.email == email.data).first():
    #             raise ValidationError('That email is taken. Please choose a different one.')
