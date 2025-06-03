from flask import Flask, request, render_template_string
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import smtplib
from email.message import EmailMessage
import os

app = Flask(__name__)

# Ruta de la fuente TTF
FONT_PATH = "5x5dotso.ttf"
pdfmetrics.registerFont(TTFont("Dots", FONT_PATH))

# HTML simple para la interfaz
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
  <head><title>Generador de Patentes</title></head>
  <body>
    <h2>Generar y Enviar Patente</h2>
    <form method="POST">
      <input name="patente" type="text" required>
      <input name="email" type="email" required placeholder="Correo destino">
      <input type="submit" value="Enviar PDF por correo">
    </form>
  </body>
</html>
"""

# Crear PDF de patente con la fuente personalizada
def crear_pdf(patente):
    pdf_path = f"{patente}.pdf"
    c = canvas.Canvas(pdf_path, pagesize=A4)
    c.setFont("Dots", 36)
    y = 750
    for _ in range(10):
        c.drawString(100, y, patente)
        c.drawString(480, y, patente)
        y -= 60
    c.save()
    return pdf_path

# Enviar email con archivo PDF adjunto usando Gmail SMTP
def enviar_email(destinatario, archivo_pdf, nombre_patente):
    msg = EmailMessage()
    msg['Subject'] = f"Patente {nombre_patente} en PDF"
    msg['From'] = 'tucorreo@gmail.com'  # Reemplaza con tu correo
    msg['To'] = destinatario
    msg.set_content(f"Hola,\n\nAquí tienes el archivo PDF de la patente {nombre_patente}.\n\nGracias por usar la app.")

    with open(archivo_pdf, 'rb') as f:
        msg.add_attachment(f.read(), maintype='application', subtype='pdf', filename=f"{nombre_patente}.pdf")

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login('parramartin690@gmail.com', 'danmqxiyigoytkgi')  # Reemplaza con tu correo y contraseña de app
            smtp.send_message(msg)
    except Exception as e:
        print(f"Error al enviar correo: {e}")

# Rutas web
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        patente = request.form['patente'].strip().upper()
        email = request.form['email'].strip()
        path = crear_pdf(patente)
        enviar_email(email, path, patente)
        return f"<p>PDF de la patente <b>{patente}</b> enviado a <b>{email}</b></p>"
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    app.run(debug=True)
