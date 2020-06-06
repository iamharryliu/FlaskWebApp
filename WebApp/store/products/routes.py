from flask import Blueprint, render_template, redirect, url_for, abort, request, flash
from flask_login import current_user
from WebApp.store.forms import ItemForm
from WebApp.store.utils import (
    get_all_products,
    get_product,
    search_products,
    add_item_to_cart,
)


products_blueprint = Blueprint(
    "products", __name__, url_prefix="/store/products", template_folder="templates"
)


@products_blueprint.route("/search/", methods=["GET", "POST"])
def search():
    search = request.form["search"]
    products = search_products(search)
    return render_template("products/products.html", title="Store", products=products)


@products_blueprint.route("")
def products():
    products = get_all_products()
    return render_template("products/products.html", title="Store", products=products)


@products_blueprint.route("/<int:product_id>", methods=["GET", "POST"])
def product(product_id):
    product = get_product(product_id)
    form = ItemForm()
    if form.validate_on_submit():
        add_item_to_cart(product)
        flash(
            f"{form.quantity.data} x {product.name} ({form.size.data}) added to your cart.",
            "success",
        )
        return redirect(url_for("products.products", product_id=product_id))
    return render_template(
        "products/product-item.html", title=product.name, product=product, form=form
    )
