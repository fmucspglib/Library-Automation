import qrcode


def generate_student_qr(student_id):

    data = f"Student ID: {student_id}"

    qr = qrcode.make(data)

    path = f"static/student_qr/{student_id}.png"

    qr.save(path)

    return "/" + path