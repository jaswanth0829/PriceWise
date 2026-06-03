from flask_mail import Mail
from flask_mail import Message

mail = Mail()

def send_price_alert(
    app,
    recipient,
    product_name,
    current_price
):

    with app.app_context():

        msg = Message(

            subject="Price Drop Alert!",

            sender=app.config[
                "MAIL_USERNAME"
            ],

            recipients=[recipient]
        )

        msg.body = f"""

Good news!

Price dropped for:

{product_name}

Current Price:
₹ {current_price}

- PriceWise
"""

        mail.send(msg)