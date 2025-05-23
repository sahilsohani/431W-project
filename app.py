from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector
import hashlib
from role_required import buyer_required, seller_required, helpdesk_required, login_required
import uuid
from datetime import datetime
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secure key

# Database configuration (Update this with your MySQL credentials)
config = {
    'host': 'localhost',    
    'user': 'root',         
    'password': 'password', 
    'database': 'NittanyBusiness'
}

def generate_request_id():
    return random.randint(100000, 999999)  # 6-digit safe number

def update_profile_logic(current_role):
    if 'user' not in session:
        return redirect(url_for('login'))

    email = session['user']

    if request.method == 'POST':
        new_password = request.form.get('new_password')
        requested_role = request.form.get('new_role')

        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        try:
            # Update password
            if new_password:
                hashed_password = hash_password(new_password)
                cursor.execute("UPDATE User SET password = %s WHERE email = %s", (hashed_password, email))
                flash("Password updated.", "success")

            # Request role change
            if requested_role and requested_role != current_role:
                request_desc = f"Request to change role from {current_role} to {requested_role}"
                cursor.execute("""
                    INSERT INTO Request (request_id, sender_email, helpdesk_staff_email, request_type, request_desc, request_status)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (
                    generate_request_id(),
                    email,
                    'helpdeskteam@nittybiz.com',
                    'role_change',
                    request_desc,
                    0
                ))
                flash("Role change request submitted to HelpDesk.", "info")

            conn.commit()
        except mysql.connector.Error as err:
            flash(f"MySQL Error: {err}", "danger")
        finally:
            cursor.close()
            conn.close()

    user = {'email': email}
    if current_role == 'buyer':
        return render_template('buyer_profile.html', user=user)
    else:
        return render_template('seller_profile.html', user=user)

def get_user_role(email):
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        cursor.execute("SELECT 1 FROM Buyer WHERE email = %s", (email,))
        if cursor.fetchone():
            return 'buyer'

        cursor.execute("SELECT 1 FROM Seller WHERE email = %s", (email,))
        if cursor.fetchone():
            return 'seller'

        cursor.execute("SELECT 1 FROM HelpDesk WHERE email = %s", (email,))
        if cursor.fetchone():
            return 'helpdesk'

        return None
    except mysql.connector.Error as err:
        print(f"Error detecting role: {err}")
        return None
    finally:
        cursor.close()
        conn.close()


# Function to hash passwords using SHA-256
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to verify user credentials
def verify_user(email, password):
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        hashed_password = hash_password(password)
        query = "SELECT * FROM user WHERE email = %s AND password = %s"
        cursor.execute(query, (email, hashed_password))
        result = cursor.fetchone()

        cursor.close()
        conn.close()

        return result is not None  # Return True if credentials are correct

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return False

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return redirect(url_for('register'))

        hashed_password = hash_password(password)

        try:
            conn = mysql.connector.connect(**config)
            cursor = conn.cursor()

            # Check if user already exists
            cursor.execute("SELECT * FROM user WHERE email = %s", (email,))
            if cursor.fetchone():
                flash('User already exists with that email.', 'warning')
                return redirect(url_for('register'))

            # Insert new user
            cursor.execute("INSERT INTO user (email, password) VALUES (%s, %s)", (email, hashed_password))
            conn.commit()
            session['user'] = email
            flash('Registration successful! Please select your role.', 'info')
            return redirect(url_for('choose_role'))

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            flash('An error occurred. Please try again later.', 'danger')

        finally:
            cursor.close()
            conn.close()

    return render_template('register.html')

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['username']
        password = request.form['password']
        hashed_password = hash_password(password)

        try:
            conn = mysql.connector.connect(**config)
            cursor = conn.cursor(dictionary=True)

            # Verify credentials
            cursor.execute("SELECT * FROM User WHERE email = %s AND password = %s", (email, hashed_password))
            user = cursor.fetchone()

            if user:
                session['user'] = email

                # Check for role
                role = None
                cursor.execute("SELECT * FROM Seller WHERE email = %s", (email,))
                if cursor.fetchone():
                    role = 'seller'

                cursor.execute("SELECT * FROM Buyer WHERE email = %s", (email,))
                if cursor.fetchone():
                    role = 'buyer'

                cursor.execute("SELECT * FROM HelpDesk WHERE email = %s", (email,))
                if cursor.fetchone():
                    role = 'helpdesk'

                if role:
                    session['role'] = role
                    flash("Login successful!", "success")
                    return redirect(url_for(f'{role}_dashboard'))
                else:
                    flash("Please select a role to complete your setup.", "info")
                    return redirect(url_for('choose_role'))

            else:
                flash('Invalid email or password.', 'danger')

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            flash('Database error.', 'danger')

        finally:
            cursor.close()
            conn.close()

    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if verify_user(username, password):
            session['user'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password. Please try again.', 'danger')

    return render_template('login.html')


@app.route('/choose-role', methods=['GET', 'POST'])
def choose_role():
    if 'user' not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for('login'))

    if request.method == 'POST':
        selected_role = request.form.get('role')
        email = session['user']

        try:
            conn = mysql.connector.connect(**config)
            cursor = conn.cursor()

            # Generate a unique address ID
            address_id = str(uuid.uuid4())[:8].upper()  # e.g., 'A1B2C3D4'

            # Common function to insert address
            def insert_address(building_number, street_name, zip_code):
                cursor.execute("""
                    INSERT INTO Address (business_address_id, zip_code, building_number, street_name)
                    VALUES (%s, %s, %s, %s)
                """, (address_id, zip_code, building_number, street_name))

            if selected_role == 'buyer':
                business_name = request.form['buyer_business_name']
                insert_address(
                    request.form['buyer_building_number'],
                    request.form['buyer_street_name'],
                    request.form['buyer_zip_code']
                )
                cursor.execute("""
                    INSERT INTO Buyer (email, business_name, business_address_id)
                    VALUES (%s, %s, %s)
                """, (email, business_name, address_id))

            elif selected_role == 'seller':
                business_name = request.form['seller_business_name']
                insert_address(
                    request.form['seller_building_number'],
                    request.form['seller_street_name'],
                    request.form['seller_zip_code']
                )
                cursor.execute("""
                    INSERT INTO Seller (email, business_name, business_address_id, bank_routing_number, bank_account_number, balance)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (
                    email, business_name, address_id,
                    request.form['bank_routing_number'],
                    request.form['bank_account_number'],
                    0
                ))

            elif selected_role == 'helpdesk':
                cursor.execute("INSERT INTO HelpDesk (email, position) VALUES (%s, %s)", (email, 'Staff'))

            conn.commit()
            session['role'] = selected_role
            flash("Role assigned successfully!", "success")
            return redirect(url_for(f'{selected_role}_dashboard'))

        except mysql.connector.Error as err:
            print(f"Error assigning role: {err}")
            flash("Database error during role assignment.", "danger")

        finally:
            cursor.close()
            conn.close()

    return render_template('choose_role.html')

@app.route('/buyer/dashboard')
@login_required
def buyer_dashboard():
    return render_template('buyer_dashboard.html')

@app.route('/seller/dashboard')
@login_required
def seller_dashboard():
    return render_template('seller_dashboard.html')

@app.route('/helpdesk/dashboard')
@login_required
def helpdesk_dashboard():
    return render_template('helpdesk_dashboard.html')

@app.route('/categories')
@app.route('/categories/<string:category_name>')
@login_required
@buyer_required
def view_categories(category_name=None):
    if category_name is None:
        category_name = 'root'  # Always begin with the root category

    conn = mysql.connector.connect(**config)
    cursor = conn.cursor(dictionary=True)

    try:
        # Subcategories of the current category
        cursor.execute("SELECT * FROM Category WHERE parent_category = %s", (category_name,))
        subcategories = cursor.fetchall()

        # Products in the current category
        cursor.execute("""
            SELECT * FROM Product_Listing
            WHERE category = %s AND status = 1
        """, (category_name,))
        products = cursor.fetchall()

    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")
        flash("Error loading category data.", "danger")
        subcategories, products = [], []

    finally:
        cursor.close()
        conn.close()

    return render_template('buyer_view_categories.html',
                           subcategories=subcategories,
                           products=products,
                           current_category=category_name)

@app.route('/category/<string:category_name>/products')
@login_required
@buyer_required
def view_products_by_category(category_name):
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT * FROM Product_Listing
            WHERE category = %s AND status = 1
        """, (category_name,))
        products = cursor.fetchall()

    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")
        flash("Unable to load products for this category.", "danger")
        products = []

    finally:
        cursor.close()
        conn.close()

    return render_template('buyer_products.html', products=products, category_name=category_name)

@app.route('/cart')
@login_required
@buyer_required
def view_cart():
    cart = session.get('cart', {})  # {product_id: quantity}
    items = []
    total = 0

    if cart:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor(dictionary=True)
        for product_id, quantity in cart.items():
            cursor.execute("SELECT * FROM Product_Listing WHERE product_id = %s", (product_id,))
            product = cursor.fetchone()
            if product:
                subtotal = product['price'] * quantity
                product['quantity'] = quantity
                product['subtotal'] = subtotal
                items.append(product)
                total += subtotal
        cursor.close()
        conn.close()

    return render_template('buyer_view_cart.html', cart_items=items, total=total)

@app.route('/cart/remove/<int:product_id>', methods=['POST'])
@login_required
@buyer_required
def remove_from_cart(product_id):
    cart = session.get('cart', {})
    if str(product_id) in cart:
        cart.pop(str(product_id))
        session['cart'] = cart
        flash("Item removed from cart.", "info")
    return redirect(url_for('view_cart'))

@app.route('/checkout', methods=['GET', 'POST'])
@login_required
@buyer_required
def checkout():
    cart = session.get('cart', {})
    cart_items = []
    total = 0

    conn = mysql.connector.connect(**config)
    cursor = conn.cursor(dictionary=True)

    try:
        if request.method == 'GET':
            if not cart:
                flash("Your cart is empty.", "warning")
                return redirect(url_for('view_cart'))

            for product_id, quantity in cart.items():
                cursor.execute("SELECT * FROM Product_Listing WHERE product_id = %s", (product_id,))
                product = cursor.fetchone()
                if product:
                    product['quantity'] = quantity
                    total += product['price'] * quantity
                    cart_items.append(product)

            # Load buyer's saved credit cards
            cursor.execute("SELECT * FROM Credit_Card WHERE owner_email = %s", (session['user'],))
            credit_cards = cursor.fetchall()

            return render_template('checkout.html', cart_items=cart_items, total=total, credit_cards=credit_cards)

        # POST (Placing the order)
        selected_card = request.form.get('payment_method')

        if not selected_card:
            # No card selected — assume buyer is entering new card
            new_card_num = request.form.get('new_card_num')
            new_card_type = request.form.get('new_card_type')
            new_expire_month = request.form.get('new_expire_month')
            new_expire_year = request.form.get('new_expire_year')
            new_security_code = request.form.get('new_security_code')

            if not (new_card_num and new_card_type and new_expire_month and new_expire_year and new_security_code):
                flash("Please fill out all new card fields.", "danger")
                return redirect(url_for('checkout'))

            # Save new card to Credit_Card table
            cursor.execute("""
                INSERT INTO Credit_Card (credit_card_num, card_type, expire_month, expire_year, security_code, owner_email)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                new_card_num,
                new_card_type,
                new_expire_month,
                new_expire_year,
                new_security_code,
                session['user']
            ))
            conn.commit()

            payment_card = new_card_num
        else:
            # Buyer selected a saved card
            payment_card = selected_card

        for product_id, quantity in cart.items():
            # Fetch product again to get seller and price
            cursor.execute("SELECT * FROM Product_Listing WHERE product_id = %s", (product_id,))
            product = cursor.fetchone()

            if not product or quantity > product['stock']:
                flash(f"Product {product['name']} is out of stock or invalid quantity.", "danger")
                return redirect(url_for('view_cart'))

            # Generate a unique order ID
            order_id = random.randint(100000, 999999)
            cursor.execute("SELECT 1 FROM Orders WHERE order_id = %s", (order_id,))
            while cursor.fetchone():
                order_id = random.randint(100000, 999999)

            # Insert into Orders table
            cursor.execute("""
                INSERT INTO Orders (order_id, seller_email, product_id, buyer_email, date, amount, payment)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                order_id,
                product['seller_email'],
                product_id,
                session['user'],
                datetime.now().strftime('%Y-%m-%d'),
                quantity,
                product['price'] * quantity
            ))

            # Decrease stock
            cursor.execute("""
                UPDATE Product_Listing
                SET stock = stock - %s
                WHERE product_id = %s AND stock >= %s
            """, (quantity, product_id, quantity))

            if cursor.rowcount == 0:
                flash(f"Failed to update stock for {product['name']} due to concurrent order.", "danger")
                return redirect(url_for('view_cart'))

        conn.commit()
        session['cart'] = {}
        flash("Your order was placed successfully!", "success")
        return redirect(url_for('view_orders'))

    except mysql.connector.Error as err:
        conn.rollback()
        print(f"MySQL Error: {err}")
        flash("Order failed due to a database error.", "danger")

    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('view_orders'))


@app.route('/orders')
@login_required
@buyer_required
def view_orders():
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT o.*, p.name AS product_name
        FROM Orders o
        JOIN Product_Listing p ON o.product_id = p.product_id
        WHERE o.buyer_email = %s
    """, (session['user'],))
    orders = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('buyer_view_orders.html', orders=orders)

@app.route('/cart/add/<int:product_id>', methods=['POST'])
@login_required
@buyer_required
def add_to_cart(product_id):
    quantity = int(request.form.get('quantity', 1))
    if quantity < 1:
        flash("Invalid quantity.", "warning")
        return redirect(request.referrer)

    # Get current cart or create a new one
    cart = session.get('cart', {})

    # Update quantity if product already in cart
    if str(product_id) in cart:
        cart[str(product_id)] += quantity
    else:
        cart[str(product_id)] = quantity

    session['cart'] = cart
    flash("Product added to cart!", "success")
    return redirect(request.referrer or url_for('view_cart'))

@app.route('/seller/product/new', methods=['GET', 'POST'])
@login_required
@seller_required
def list_product():
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        category = request.form['category_id']
        price = float(request.form['price'])
        quantity = int(request.form['quantity'])

        try:
            product_id = random.randint(100000, 999999)

            # Ensure uniqueness
            cursor.execute("SELECT 1 FROM Product_Listing WHERE product_id = %s", (product_id,))
            while cursor.fetchone():
                product_id = random.randint(100000, 999999)

            cursor.execute("""
                INSERT INTO Product_Listing (seller_email, product_id, category, title, name, detail, stock, price, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                session['user'], product_id, category,
                title, title, description, quantity, price, 1
            ))
            conn.commit()
            flash('Product listed successfully.', 'success')
            return redirect(url_for('manage_products'))

        except mysql.connector.Error as err:
            flash(f'Error: {err}', 'danger')

    cursor.execute("SELECT * FROM Category")
    categories = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('seller_list_product.html', categories=categories)

@app.route('/seller/products')
@login_required
@seller_required
def manage_products():
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT * FROM Product_Listing
        WHERE seller_email = %s
    """, (session['user'],))
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('seller_manage_products.html', products=products)

@app.route('/seller/product/edit/<int:product_id>', methods=['GET', 'POST'])
@login_required
@seller_required
def edit_product(product_id):
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        price = float(request.form['price'])
        stock = int(request.form['stock'])
        status = int(request.form['status'])

        cursor.execute("""
            UPDATE Product_Listing
            SET title=%s, name=%s, detail=%s, price=%s, stock=%s, status=%s
            WHERE product_id=%s AND seller_email=%s
        """, (title, title, description, price, stock, status, product_id, session['user']))
        conn.commit()
        flash("Product updated successfully.", "success")
        return redirect(url_for('manage_products'))

    cursor.execute("SELECT * FROM Product_Listing WHERE product_id = %s AND seller_email = %s",
                   (product_id, session['user']))
    product = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('seller_edit_product.html', product=product)

@app.route('/seller/product/delete/<int:product_id>', methods=['POST'])
@login_required
@seller_required
def delete_product(product_id):
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM Product_Listing
        WHERE product_id = %s AND seller_email = %s
    """, (product_id, session['user']))
    conn.commit()
    cursor.close()
    conn.close()
    flash("Product deleted.", "info")
    return redirect(url_for('manage_products'))

@app.route('/seller/feedback')
@login_required
@seller_required
def view_feedback():
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT r.order_id, r.rating, r.text
        FROM Review r
        JOIN Orders o ON r.order_id = o.order_id
        WHERE o.seller_email = %s
    """, (session['user'],))
    reviews = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('seller_view_feedback.html', reviews=reviews)

@app.route('/search')
@login_required
@buyer_required
def search_products():
    query = request.args.get('q', '').strip()
    selected_category = request.args.get('category', '').strip()
    min_price = request.args.get('min_price')
    max_price = request.args.get('max_price')

    if not query:
        flash("Please enter a search term.", "warning")
        return redirect(url_for('buyer_dashboard'))

    filters = []
    values = []

    # Base query
    sql = "SELECT * FROM Product_Listing WHERE (title LIKE %s OR name LIKE %s) AND status = 1"
    values.extend([f'%{query}%', f'%{query}%'])

    # Optional category filter
    if selected_category:
        sql += " AND category = %s"
        values.append(selected_category)

    # Optional price filters
    if min_price:
        sql += " AND price >= %s"
        values.append(min_price)
    if max_price:
        sql += " AND price <= %s"
        values.append(max_price)

    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor(dictionary=True)

        cursor.execute(sql, tuple(values))
        results = cursor.fetchall()

        # Load categories for the filter dropdown
        cursor.execute("SELECT category_name FROM Category")
        categories = cursor.fetchall()

    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")
        flash("Could not perform search.", "danger")
        results = []
        categories = []

    finally:
        cursor.close()
        conn.close()

    return render_template('buyer_search_results.html', results=results, query=query,
                           categories=categories, selected_category=selected_category,
                           min_price=min_price, max_price=max_price)


@app.route('/helpdesk/resolve', methods=['GET', 'POST'])
@login_required
@helpdesk_required
def resolve_requests():
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor(dictionary=True)

    try:
        if request.method == 'POST':
            # Assign unassigned request
            if 'assign' in request.form:
                request_id = request.form['assign']
                cursor.execute("""
                    UPDATE Request
                    SET helpdesk_staff_email = %s
                    WHERE request_id = %s AND (helpdesk_staff_email IS NULL OR helpdesk_staff_email = 'helpdeskteam@nittybiz.com')
                """, (session['user'], request_id))
                conn.commit()
                flash("Request assigned to you.", "info")
                return redirect(url_for('resolve_requests'))

            elif 'resolve' in request.form:
                request_id = request.form['resolve']
                cursor.execute("""
                    UPDATE Request
                    SET request_status = 1, helpdesk_staff_email = %s
                    WHERE request_id = %s AND (
                        helpdesk_staff_email = %s OR helpdesk_staff_email = 'helpdeskteam@nittybiz.com'
                    )
                """, (session['user'], request_id, session['user']))
                conn.commit()
                flash("Request marked as resolved.", "success")
                return redirect(url_for('resolve_requests'))

        # Load all requests
        cursor.execute("SELECT * FROM Request ORDER BY request_status ASC, request_id DESC")
        requests = cursor.fetchall()

    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")
        flash("Error processing requests.", "danger")
        requests = []

    finally:
        cursor.close()
        conn.close()

    return render_template('helpdesk_resolve_requests.html',
                           requests=requests,
                           current_user=session['user'])

@app.route('/helpdesk/requests', methods=['GET', 'POST'])
@login_required
@helpdesk_required
def view_requests():
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor(dictionary=True)

    try:
        if request.method == 'POST':
            request_id = request.form.get('request_id')
            action = request.form.get('action')

            cursor.execute("SELECT * FROM Request WHERE request_id = %s", (request_id,))
            req = cursor.fetchone()

            if not req:
                flash("Request not found.", "danger")
                return redirect(url_for('view_requests'))

            if req['request_status'] != 0:
                flash("Request already processed.", "warning")
                return redirect(url_for('view_requests'))

            sender = req['sender_email']
            desc = req['request_desc']

            if action == 'accept':
                # Determine new role from description
                new_role = 'seller' if 'to seller' in desc else 'buyer'
                old_role = 'buyer' if new_role == 'seller' else 'seller'

                # Move user from old role table to new role table
                cursor.execute(f"DELETE FROM {old_role.capitalize()} WHERE email = %s", (sender,))
                cursor.execute(f"INSERT INTO {new_role.capitalize()} (email) VALUES (%s)", (sender,))

                cursor.execute("""
                    UPDATE Request
                    SET request_status = 1, helpdesk_staff_email = %s
                    WHERE request_id = %s
                """, (session['user'], request_id))
                flash(f"Accepted request: {sender} is now a {new_role}.", "success")

            elif action == 'deny':
                cursor.execute("""
                    UPDATE Request
                    SET request_status = 2, helpdesk_staff_email = %s
                    WHERE request_id = %s
                """, (session['user'], request_id))
                flash("Denied role switch request.", "info")

            conn.commit()
            return redirect(url_for('view_requests'))

        # Load all requests
        cursor.execute("""
            SELECT * FROM Request
            ORDER BY request_status ASC, request_id DESC
        """)
        requests = cursor.fetchall()

    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")
        flash("Unable to load requests.", "danger")
        requests = []

    finally:
        cursor.close()
        conn.close()

    return render_template('helpdesk_view_requests.html', requests=requests, current_user=session['user'])


@app.route('/admin/system')
@login_required
@helpdesk_required
def system_dashboard():
    return render_template('helpdesk/system_dashboard.html')

@app.route('/helpdesk/approve/<int:request_id>', methods=['POST'])
@login_required
@helpdesk_required
def approve_request(request_id):
    if session.get('role') != 'helpdesk':
        return redirect(url_for('login'))

    conn = mysql.connector.connect(**config)
    cursor = conn.cursor(dictionary=True)

    # Get request details
    cursor.execute("SELECT * FROM Request WHERE request_id = %s", (request_id,))
    req = cursor.fetchone()

    if req and req['request_status'] == 0:
        sender = req['sender_email']
        desc = req['request_desc']

        new_role = 'seller' if 'to seller' in desc else 'buyer'
        old_role = 'buyer' if new_role == 'seller' else 'seller'

        # Update user role
        cursor.execute("UPDATE User SET role = %s WHERE email = %s", (new_role, sender))

        # Remove from old role table and insert into new
        cursor.execute(f"DELETE FROM {old_role.capitalize()} WHERE email = %s", (sender,))
        cursor.execute(f"INSERT INTO {new_role.capitalize()} (email) VALUES (%s)", (sender,))

        # Update request status
        cursor.execute("UPDATE Request SET request_status = 1 WHERE request_id = %s", (request_id,))
        conn.commit()
        flash(f"Role updated to {new_role} for {sender}", "success")

    cursor.close()
    conn.close()
    return redirect(url_for('view_requests'))

@app.route('/orders/delete/<int:order_id>', methods=['POST'])
@login_required
@buyer_required
def delete_order(order_id):
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        # Only delete the order if it belongs to the current user
        cursor.execute("""
            DELETE FROM Orders
            WHERE order_id = %s AND buyer_email = %s
        """, (order_id, session['user']))

        if cursor.rowcount:
            flash("Order canceled and deleted successfully.", "success")
        else:
            flash("Unable to delete this order.", "warning")

        conn.commit()
    except mysql.connector.Error as err:
        flash(f"MySQL Error: {err}", "danger")
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('view_orders'))

@app.route('/buyer/profile', methods=['GET', 'POST'])
@login_required
@buyer_required
def buyer_update_profile():
    return update_profile_logic('buyer')

@app.route('/seller/profile', methods=['GET', 'POST'])
@login_required
@seller_required
def seller_update_profile():
    return update_profile_logic('seller')

if __name__ == '__main__':
    app.run(debug=True)
