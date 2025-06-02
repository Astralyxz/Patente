
from flask import Flask, request, render_template_string
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import smtplib
from email.message import EmailMessage
import os

app = Flask(__name__)

FONT_PATH = "5x5dotso.ttf"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
  <head><title>Generador de Patentes</title></head>
  <body>
    <h2>Generar y Enviar Patente</h2>
    <form method="POST">
      <input name="patente" type="text" required placeholder="Ej: HLPT47">
      <input name="email" type="email" required placeholder="Correo destino">
      <input type="submit" value="Enviar PDF por correo">
    </form>
  </body>
</html>
"""

def crear_pdf(patente):
    pdf_path = f"{patente}.pdf"
    c = canvas.Canvas(pdf_path, pagesize=A4)
    c.setFont("Dots", 36)
    y = 750
    for _ in range(10):
        c.drawString(100, y, patente)
        c.drawString(350, y, patente)
        y -= 60
    c.save()
    return pdf_path

def enviar_email(destinatario, archivo_pdf, nombre_patente):
    msg = EmailMessage()
    msg['Subject'] = f"Patente {nombre_patente} en PDF"
    msg['From'] = '8ea29e002@smtp-brevo.com'
    msg['To'] = destinatario
    msg.set_content(f"Hola,\n\nAquí tienes el archivo PDF de la patente {nombre_patente}.\n\nGracias por usar la app.")

    with open(archivo_pdf, 'rb') as f:
        msg.add_attachment(f.read(), maintype='application', subtype='pdf', filename=f"{nombre_patente}.pdf")

    with smtplib.SMTP('smtp-relay.brevo.com', 587) as smtp:
        smtp.starttls()
        smtp.login('8ea29e002@smtp-brevo.com', '75UrzyN6RXObI4BM')
        smtp.send_message(msg)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        patente = request.form['patente'].strip().upper()
        email = request.form['email'].strip()
        path = crear_pdf(patente)
        enviar_email(email, path, patente)
        return f"<h3> PDF enviado a {email}</h3>"
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    pdfmetrics.registerFont(TTFont("Dots", FONT_PATH))
    app.run(debug=True)

