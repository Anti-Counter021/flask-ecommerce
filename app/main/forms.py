from datetime import date

from flask_wtf import FlaskForm

from wtforms import (
    StringField,
    DateField,
    SelectField,
    SubmitField
)
from wtforms.validators import (
    DataRequired,
    ValidationError
)


class OrderForm(FlaskForm):
    """ Order form """
    first_name = StringField('Name', validators=[DataRequired()])
    last_name = StringField('Surname', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    buying_type = SelectField('Buying type', choices=[('self', 'self'), ('delivery', 'delivery')])
    comment = StringField('Comment')
    order_date = DateField('Order date', format="%d-%b-%Y")
    submit = SubmitField('Create order')

    def validate_order_date(self, order_date):
        today = date.today()
        if order_date.data < today:
            raise ValidationError('Please use correct date.')


class TestimonialForm(FlaskForm):
    """ Testimonial """
    APPRAISAL_CHOICES = [
        ('very bad', 'very bad'), ('bad', 'bad'), ('normal', 'normal'), ('good', 'good'), ('excellent', 'excellent')
    ]
    appraisal = SelectField('Appraisal', validators=[DataRequired()], choices=APPRAISAL_CHOICES)
    comment = StringField('Comment')
    submit = SubmitField('Create testimonial')
