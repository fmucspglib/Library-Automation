from flask import Flask, render_template, request, redirect, send_file
from firebase_config import db
from qr_generator import generate_qr
from firebase_auth import auth

app = Flask(__name__)


# ----------------HOME PAGE---------------


# ---------------- DASHBOARD ----------------

@app.route('/dashboard')
def dashboard():

    # ---------------- BOOKS ----------------

    books = db.collection('books').stream()

    books_data = []

    total_books = 0


    for book in books:

        data = book.to_dict()

        books_data.append(data)

        total_books += int(data['quantity'])


    # ---------------- STUDENTS ----------------

    students = db.collection('students').stream()

    students_data = []


    for student in students:

        students_data.append(student.to_dict())


    total_students = len(students_data)


    # ---------------- TRANSACTIONS ----------------

    transactions = db.collection('transactions').stream()


    issued_count = 0

    returned_count = 0

    total_transactions = 0


    for transaction in transactions:

        data = transaction.to_dict()

        status = data.get('status', '')

        total_transactions += 1


        if status == "Issued":

            issued_count += 1


        elif status == "Returned":

            returned_count += 1


    # ---------------- ACTIVE ISSUED BOOKS ----------------

    issued_books = issued_count - returned_count


    if issued_books < 0:

        issued_books = 0


    return render_template(

        'dashboard.html',

        total_books=total_books,

        total_students=total_students,

        issued_books=issued_books,

        returned_books=returned_count,

        total_transactions=total_transactions,

        books=books_data[:5]
    )
# ---------------- BOOKS PAGE ----------------

@app.route('/books')
def books():

    books_data = []

    books = db.collection('books').stream()

    for book in books:
        books_data.append(book.to_dict())

    return render_template('books.html', books=books_data)


# ---------------- ADD BOOK ----------------

# ---------------- ADD BOOK ----------------

@app.route('/add_book', methods=['POST'])
def add_book():

    # Get Form Data
    book_id = request.form['book_id']

    title = request.form['title']

    author = request.form['author']

    edition = request.form['edition']

    publisher = request.form['publisher']

    price = request.form['price']

    quantity = request.form['quantity']


    # Generate QR
    qr_path = generate_qr(book_id)


    # Book Data
    data = {

        "book_id": book_id,

        "title": title,

        "author": author,

        "edition": edition,

        "publisher": publisher,

        "price": price,

        "quantity": quantity,

        "qr_code": qr_path
    }


    # Save To Firebase
    db.collection('books')\
      .document(book_id)\
      .set(data)


    return redirect('/books')


# ---------------- QR SCANNER PAGE ----------------

@app.route('/scanner')
def scanner():

    return render_template('scanner.html')


# ---------------- ISSUE PAGE ----------------

@app.route('/issue')
def issue():

    return render_template('issue.html')


# ---------------- ISSUE BOOK ----------------

@app.route('/issue_book', methods=['POST'])
def issue_book():

    book_id = request.form['book_id']

    student_id = request.form['student_id']


    # ---------------- GET STUDENT ----------------

    student_ref = db.collection('students')\
                    .document(student_id)

    student = student_ref.get()

    if not student.exists:

        return """
        <h2>
        Student Not Found
        </h2>
        """

    student_data = student.to_dict()


    # ---------------- GET BOOK ----------------

    book_ref = db.collection('books')\
                 .document(book_id)

    book = book_ref.get()


    if book.exists:

        data = book.to_dict()

        quantity = int(data['quantity'])


        # ---------------- CHECK STOCK ----------------

        if quantity > 0:

            quantity -= 1


            # Update Quantity
            book_ref.update({

                "quantity": quantity
            })


            # ---------------- SAVE TRANSACTION ----------------

            issue_data = {

                "student_id": student_id,

                "student_name": student_data['name'],

                "book_id": book_id,

                "book_title": data['title'],

                "status": "Issued"
            }


            db.collection('transactions')\
              .add(issue_data)


            return """
            <h2>
            Book Issued Successfully
            </h2>
            """


        else:

            return """
            <h2>
            Book Out Of Stock
            </h2>
            """


    return """
    <h2>
    Book Not Found
    </h2>
    """


# ---------------- RETURN PAGE ----------------

@app.route('/return')
def return_page():

    return render_template('return.html')


# ---------------- RETURN BOOK ----------------

@app.route('/return_book', methods=['POST'])
def return_book():

    book_id = request.form['book_id']

    student_id = request.form['student_id']


    # ---------------- GET STUDENT ----------------

    student_ref = db.collection('students')\
                    .document(student_id)

    student = student_ref.get()

    if not student.exists:

        return """
        <h2>
        Student Not Found
        </h2>
        """

    student_data = student.to_dict()


    # ---------------- GET BOOK ----------------

    book_ref = db.collection('books')\
                 .document(book_id)

    book = book_ref.get()


    if book.exists:

        data = book.to_dict()

        quantity = int(data['quantity'])


        # ---------------- INCREASE QUANTITY ----------------

        quantity += 1


        # Update Firebase
        book_ref.update({

            "quantity": quantity
        })


        # ---------------- SAVE TRANSACTION ----------------

        return_data = {

            "student_id": student_id,

            "student_name": student_data['name'],

            "book_id": book_id,

            "book_title": data['title'],

            "status": "Returned"
        }


        db.collection('transactions')\
          .add(return_data)


        return """
        <h2>
        Book Returned Successfully
        </h2>
        """


    return """
    <h2>
    Book Not Found
    </h2>
    """


#------------------HISTOTY PAGE-----------------
@app.route('/history')
def history():

    transactions_data = []

    transactions = db.collection('transactions').stream()

    for transaction in transactions:

        transactions_data.append(
            transaction.to_dict()
        )

    return render_template(
        'history.html',
        transactions=transactions_data
    )

#-----------------STUDENT DATABASE-----------------
# ---------------- STUDENTS PAGE ----------------

from student_qr import generate_student_qr


# ---------------- STUDENTS PAGE ----------------

@app.route('/students')
def students():

    students_data = []

    students = db.collection('students').stream()

    for student in students:

        students_data.append(
            student.to_dict()
        )

    return render_template(
        'students.html',
        students=students_data
    )


# ---------------- ADD STUDENT ----------------

@app.route('/add_student', methods=['POST'])
def add_student():

    student_id = request.form['student_id']

    name = request.form['name']

    department = request.form['department']

    semester = request.form['semester']

    # Generate Student QR
    qr_path = generate_student_qr(student_id)

    # Student Data
    data = {

        "student_id": student_id,

        "name": name,

        "department": department,

        "semester": semester,

        "qr_code": qr_path
    }

    # Store In Firebase
    db.collection('students')\
      .document(student_id)\
      .set(data)

    return redirect('/students')


# ---------------- SEARCH BOOK ----------------

@app.route('/search', methods=['GET', 'POST'])
def search():

    books_data = []

    if request.method == 'POST':

        search_text = request.form['search'].lower().strip()

        books = db.collection('books').stream()

        for book in books:

            data = book.to_dict()

            book_id= data.get('book_id', '').lower()

            title = data.get('title', '').lower()

            author = data.get('author', '').lower()


            # Partial Search
            if (

                search_text in book_id

                or

                search_text in title

                or

                search_text in author

            ):

                books_data.append(data)


    return render_template(

        'search.html',

        books=books_data
    )
# ---------------- SMART SCANNER ----------------

@app.route('/smart_scanner')
def smart_scanner():
    return render_template(
        'smart_scanner.html'
    )
# ---------------- QR ISSUE SYSTEM ----------------

@app.route('/issue_qr_book', methods=['POST'])
def issue_qr_book():

    data = request.get_json()

    student_id = data['student_id']

    book_id = data['book_id']


    # ---------------- GET STUDENT ----------------

    student_ref = db.collection('students')\
                    .document(student_id)

    student = student_ref.get()

    if not student.exists:

        return "Student Not Found"

    student_data = student.to_dict()


    # ---------------- GET BOOK ----------------

    book_ref = db.collection('books')\
                 .document(book_id)

    book = book_ref.get()

    if book.exists:

        book_data = book.to_dict()

        quantity = int(book_data['quantity'])


        # ---------------- CHECK STOCK ----------------

        if quantity > 0:

            quantity -= 1


            # Update Quantity
            book_ref.update({

                "quantity": quantity
            })


            # ---------------- SAVE TRANSACTION ----------------

            transaction = {

                "student_id": student_id,

                "student_name": student_data['name'],

                "book_id": book_id,

                "book_title": book_data ['title'],

                "status": "Issued"
            }


            db.collection('transactions')\
              .add(transaction)


            return "Book Issued Successfully"


        return "Book Out Of Stock"


    return "Book Not Found"
# ---------------- SMART RETURN PAGE ----------------

@app.route('/smart_return')
def smart_return():

    return render_template(
        'smart_return.html'
    )


# ---------------- QR RETURN SYSTEM ----------------

@app.route('/return_qr_book', methods=['POST'])
def return_qr_book():

    data = request.get_json()

    student_id = data['student_id']

    book_id = data['book_id']


    # ---------------- GET STUDENT ----------------

    student_ref = db.collection('students')\
                    .document(student_id)

    student = student_ref.get()

    if not student.exists:

        return "Student Not Found"

    student_data = student.to_dict()


    # ---------------- GET BOOK ----------------

    book_ref = db.collection('books')\
                 .document(book_id)

    book = book_ref.get()

    if book.exists:

        book_data = book.to_dict()

        quantity = int(book_data['quantity'])


        # ---------------- INCREASE QUANTITY ----------------

        quantity += 1


        # Update Quantity
        book_ref.update({

            "quantity": quantity
        })


        # ---------------- SAVE TRANSACTION ----------------

        transaction = {

            "student_id": student_id,

            "student_name": student_data['name'],

            "book_id": book_id,

            "book_title": book_data['title'],

            "status": "Returned"
        }


        db.collection('transactions')\
          .add(transaction)


        return "Book Returned Successfully"


    return "Book Not Found"
# ---------------- DELETE BOOK ----------------

@app.route('/delete_book/<book_id>')
def delete_book(book_id):

    db.collection('books')\
      .document(book_id)\
      .delete()

    return redirect('/books')
# ---------------- DELETE STUDENT ----------------

@app.route('/delete_student/<student_id>')
def delete_student(student_id):

    db.collection('students')\
      .document(student_id)\
      .delete()

    return redirect('/students')

# ---------------- SIGNUP PAGE ----------------

@app.route('/signup')
def signup():
    return render_template('signup.html')


# ---------------- CREATE ACCOUNT ----------------

@app.route('/create_account', methods=['POST'])
def create_account():

    email = request.form['email']

    password = request.form['password']

    try:

        # Maximum 4 users
        users = auth.get_account_info

        auth.create_user_with_email_and_password(
            email,
            password
        )

        return redirect('/')

    except:

        return """
        <h2>
        Account Already Exists
        </h2>
        """
# ---------------- LOGIN PAGE ----------------

@app.route('/')
def login():
    return render_template('login.html')


# ---------------- LOGIN SYSTEM ----------------

@app.route('/login', methods=['POST'])
def login_system():

    email = request.form['email']

    password = request.form['password']

    try:

        auth.sign_in_with_email_and_password(
            email,
            password
        )

        return redirect('/dashboard')

    except:

        return """
        <h2>
        Invalid Email or Password
        </h2>
        """
# ---------------- FORGOT PASSWORD ----------------

@app.route('/forgot_password')
def forgot_password():
    return render_template(
        'forgot_password.html'
    )


# ---------------- RESET PASSWORD ----------------

@app.route('/reset_password', methods=['POST'])
def reset_password():

    email = request.form['email']

    try:

        auth.send_password_reset_email(email)

        return """
        <h2>
        Password Reset Email Sent
        </h2>
        """

    except:

        return """
        <h2>
        Invalid Email Address
        </h2>
        """
# ---------------- EXPORT BOOKS EXCEL ----------------

@app.route('/export_books')
def export_books():

    import pandas as pd

    from openpyxl import load_workbook

    from openpyxl.drawing.image import Image


    books = db.collection('books').stream()

    books_data = []


    # Collect Book Data
    for book in books:

        data = book.to_dict()

        books_data.append({

            "book_id": data.get("book_id"),

            "Title": data.get("title"),

            "Author": data.get("author"),

            "Edition": data.get("edition"),

            "Publisher": data.get("publisher"),

            "Price": data.get("price"),

            "Quantity": data.get("quantity")
        })


    # Create Excel File
    df = pd.DataFrame(books_data)

    file_name = "books.xlsx"

    df.to_excel(file_name, index=False)


    # Open Workbook
    workbook = load_workbook(file_name)

    sheet = workbook.active


    # Add QR Column
    sheet["H1"] = "QR Code"


    # Insert QR Images
    row = 2

    for book in books_data:

        book_id = book["book_id"]

        qr_path = f"static/qr/{book_id}.png"

        try:

            img = Image(qr_path)

            img.width = 70

            img.height = 70

            sheet.add_image(img, f"H{row}")

            sheet.row_dimensions[row].height = 60

        except:

            pass

        row += 1


    # Column Width
    sheet.column_dimensions["H"].width = 18


    # Save Workbook
    workbook.save(file_name)


    return send_file(

        file_name,

        as_attachment=True
    )
# ---------------- RUN FLASK APP ----------------


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    app.run(host="0.0.0.0", port=port)


