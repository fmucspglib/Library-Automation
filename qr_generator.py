import qrcode
import os

print("QR Generator Loaded")


def generate_qr(book_id):

    print("Generating QR for:", book_id)

    folder = "static/qr"

    # Create folder if not exists
    if not os.path.exists(folder):
        os.makedirs(folder)

    # QR Data
    data = f"book_id: {book_id}"

    # Generate QR
    img = qrcode.make(data)

    # File path
    file_path = f"{folder}/{book_id}.png"

    # Save QR
    img.save(file_path)

    print("QR Saved:", file_path)

    return file_path