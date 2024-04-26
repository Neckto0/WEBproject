from flask import Blueprint, jsonify
from . import db_session
from .product import Products
from .turbo import Turbo

prod_bl_print = Blueprint(
    "product",
    __name__,
    template_folder='templates'
)


@prod_bl_print.route("/api/product")
def get_prod():
    db_sess = db_session.create_session()
    prods = db_sess.query(Products).all()
    types = db_sess.query(Turbo).all()
    return jsonify(
        {
            'products': [prod.to_dict(only=("id", "type", "name", "quality", "price", "about"))
                         for prod in prods],
            'types': [typ.to_dict(only=("id", "name")) for typ in types]
        }
    )
