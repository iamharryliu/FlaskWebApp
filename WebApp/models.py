from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from WebApp import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="default.jpg")
    password = db.Column(db.String(60), nullable=False)
    confirmed_email = db.Column(db.Boolean, default=False)
    subscription_status = db.Column(db.Boolean, default=True)
    posts = db.relationship("Post", backref="author", cascade="all,delete", lazy=True)
    carts = db.relationship("Cart", backref="customer", cascade="all,delete", lazy=True)

    def get_confirm_email_token(self):
        s = Serializer(current_app.config["SECRET_KEY"])
        return s.dumps({"user_id": self.id}).decode("utf-8")

    @staticmethod
    def verify_confirm_email_token(token):
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            user_id = s.loads(token)["user_id"]
        except:
            return None
        return User.query.get(user_id)

    def get_reset_password_token(self, expires_sec=1800):
        s = Serializer(current_app.config["SECRET_KEY"], expires_sec)
        return s.dumps({"user_id": self.id}).decode("utf-8")

    @staticmethod
    def verify_reset_password_token(token):
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            user_id = s.loads(token)["user_id"]
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}', '{self.subscription_status}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    price = db.Column(db.Float, nullable=False)
    code = db.Column(db.Text, unique=True, nullable=False, default="")
    color = db.Column(db.Text, nullable=False, default="")
    description = db.Column(db.Text, nullable=False, default="")
    image_file = db.Column(db.String(20), nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    cart_item = db.relationship("CartItem", backref="product", lazy=True)

    def __repr__(self):
        return f"Product Item('{self.name}', '{self.price}')"


class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    cart_items = db.relationship(
        "CartItem", backref="cart", cascade="all,delete", lazy=True
    )
    # quantity = db.Column(db.Integer, default=0)
    # total = db.Column(db.Float, default=0)


class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey("cart.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    size = db.Column(db.Text, nullable=False)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # user = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    email = db.Column(db.String(120), nullable=False)

    shipping_first_name = db.Column(db.String(20))
    shipping_last_name = db.Column(db.String(20), nullable=False)
    shipping_address = db.Column(db.String(20), nullable=False)
    shipping_address_unit = db.Column(db.String(20))
    shipping_city = db.Column(db.String(20), nullable=False)
    shipping_region = db.Column(db.String(20), nullable=False)
    shipping_country = db.Column(db.String(20), nullable=False)
    shipping_postal_code = db.Column(db.String(20), nullable=False)
    shipping_phone_number = db.Column(db.String(20), nullable=False)
    shipping_method = db.Column(db.String(20))

    card_number = db.Column(db.String(20), nullable=False)
    card_name = db.Column(db.String(40), nullable=False)
    card_expiration_month = db.Column(db.String(2), nullable=False)
    card_expiration_year = db.Column(db.String(2), nullable=False)

    billing_first_name = db.Column(db.String(20))
    billing_last_name = db.Column(db.String(20), nullable=False)
    billing_address = db.Column(db.String(20), nullable=False)
    billing_address_unit = db.Column(db.String(20))
    billing_city = db.Column(db.String(20), nullable=False)
    billing_region = db.Column(db.String(20), nullable=False)
    billing_country = db.Column(db.String(20), nullable=False)
    billing_postal_code = db.Column(db.String(20), nullable=False)
    billing_phone_number = db.Column(db.String(120), nullable=False)
