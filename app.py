
import os
import json
from flask import Flask, render_template, request, redirect, url_for, session
from flask import Flask, render_template, redirect, url_for, request, session

app = Flask(__name__)
app.secret_key = 'everest_secret_key'


def load_products():
    with open("products.json", "r", encoding="utf-8") as f:
        return json.load(f)


# دیتابیس ساده (در حافظه)
products = [
    {'id': 1, 'name': 'Laptop',
        'price': 500, 'image': 'https://via.placeholder.com/100'},
    {'id': 2, 'name': 'Shoes',
        'price': 70, 'image': 'https://via.placeholder.com/100'},
    {'id': 3, 'name': 'Watch',         'price': 120,
        'image': 'https://via.placeholder.com/100'}
]


# صفحه Scarfs


@app.route('/scarfs')
def scarfs():
    return render_template('scarfs.html')


@app.route('/beauty')
def beauty():
    return render_template('beauty.html')


@app.route('/toys')
def toys():
    return render_template('toys.html')


# صفحه Tools

@app.route('/tools')
def tools():
    return render_template('tools.html')


@app.route("/search")
def search():
    query = request.args.get("query", "").lower()
    products = load_products()
    matched = [p for p in products if query in p["name"].lower()]
    return render_template("search.html", results=matched, query=query)


# صفحه اصلی


@app.route('/')
def index():
    products = load_products()
    clothes_products = [p for p in products if p["category"] == "index"]
    return render_template('index.html', products=clothes_products)


@app.route('/shoes')
def shoes():
    products = load_products()
    shoes_products = [p for p in products if p.get(
        "category", "").lower() == "shoes"]
    print("Shoes Products Found:", shoes_products)
    return render_template('shoes.html', products=shoes_products)


@app.route('/tops')
def tops():
    products = load_products()
    tops_products = [p for p in products if p.get(
        "category", "").lower() == "tops"]
    print("tops Products Found:", tops_products)
    return render_template('tops.html', products=tops_products)


@app.route('/skirts')
def skirts():
    products = load_products()
    skirts_products = [p for p in products if p.get(
        "category", "").lower() == "skirts"]
    print("Skirts Products Found:", skirts_products)
    return render_template('skirts.html', products=skirts_products)


# صفحه محصول


@app.route('/product/<int:product_id>')
def product(product_id):
    products = load_products()
    product_details = next(
        (p for p in products if p["id"] == product_id), None)

    if product_details:
        return render_template('product.html', product=product_details)
    else:
        return "Product not found", 404

# افزودن به سبد خرید


@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    products = load_products()
    product = next(
        (p for p in products if p["id"] == product_id), None)
    if product is None:
        return "Product not found", 404
    session["cart"] = [product]
    session.modified = True
    return redirect(url_for('cart'))

# صفحه سبد خرید


@app.route('/cart')
def cart():
    cart_items = session.get('cart', [])
    total = sum(float(item['price']) for item in cart_items)
    return render_template('cart.html', cart=cart_items, total=total)

# صفحه تأیید سفارش


@app.route('/confirmation')
def confirmation():
    session.pop('cart', None)
    return render_template('confirmation.html')

# صفحه پرداخت


@app.route('/payment')
def payment():
    return render_template('payment.html')

# پنل مدیریت


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        new_product = {
            'id': len(products) + 1,
            'name': request.form['name'],
            'description': request.form['description'],
            'price': float(request.form['price']),
            'image': request.form['image']
        }
        products.append(new_product)
        return redirect(url_for('index'))
    return render_template('admin.html', products=products)


# اجرای سرور

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
