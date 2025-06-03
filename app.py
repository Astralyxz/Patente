from flask import Flask, request, render_template_string, send_file
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import smtplib
from email.message import EmailMessage
import os

app = Flask(__name__)

# Registrar fuente personalizada
FONT_PATH = "5x5dotso.ttf"
if not os.path.exists(FONT_PATH):
    raise FileNotFoundError("No se encontró el archivo de fuente 5x5dotso.ttf")
pdfmetrics.registerFont(TTFont("5x5DotsOutline", FONT_PATH))

# HTML
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="UTF-8">
    <title>Generador de Patentes</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
  </head>
  <body class="bg-light">
    <div class="container py-5">
      <div class="row justify-content-center">
        <div class="col-md-6">
          <div class="card shadow rounded-4">
            <div class="card-body">
              <h3 class="card-title text-center mb-4"><i class="bi bi-file-earmark-pdf"></i> Generador de Patentes</h3>
              <form method="POST">
                <div class="mb-3">
                  <label for="patente" class="form-label">Patente</label>
                  <input name="patente" type="text" class="form-control" placeholder="Ej: JJSP45" required>
                </div>
                <div class="mb-3">
                  <label for="email" class="form-label">Correo destino</label>
                  <input name="email" type="email" class="form-control" placeholder="ejemplo@correo.com" required>
                </div>
                <div class="d-grid">
                  <button type="submit" class="btn btn-primary"><i class="bi bi-download"></i>Enviar PDF por correo</button>
                </div>
              </form>
            </div>
          </div>
          <div class="text-center mt-3 text-muted">
            <small>Desarrollado por Astralyxz - Proyecto de patente PDF</small>
          </div>
        </div>
      </div>
    </div>
  </body>
</html>
"""


# Crear PDF

def crear_pdf(patente):
    font_size = 36
    page_width, _ = letter
    x_left = 100
    start_y = 700
    line_spacing = 60
    text_width = pdfmetrics.stringWidth(patente, "5x5DotsOutline", font_size)
    x_right = page_width - text_width - 80

    filename = f"{patente}.pdf"
    path = os.path.join("/tmp", filename)
    c = canvas.Canvas(path, pagesize=letter)
    c.setFont("5x5DotsOutline", font_size)

    for i in range(10):
        y = start_y - (i * line_spacing)
        c.drawString(x_left, y, patente)
        c.drawString(x_right, y, patente)

    c.save()
    return path

# Enviar PDF por correo
def enviar_email(destinatario, archivo_pdf, nombre_patente):
    msg = EmailMessage()
    msg['Subject'] = f"Patente {nombre_patente} en PDF"
    msg['From'] = 'parramartinalejandro690@gmail.com'
    msg['To'] = destinatario
    msg.set_content(f"Archivo PDF de la patente a imprimir {nombre_patente}")

    try:
        with open(archivo_pdf, 'rb') as f:
            msg.add_attachment(f.read(), maintype='application', subtype='pdf', filename=f"{nombre_patente}.pdf")

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login('parramartinalejandro690@gmail.com', 'danmqxiyigoytkgi')  # Tu contraseña de app
            smtp.send_message(msg)

        return True

    except Exception as e:
        print(f"Error al enviar correo: {e}")
        return False

# Ruta web
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        patente = request.form['patente'].strip().upper()
        email = request.form['email'].strip()
        path = crear_pdf(patente)
        enviado = enviar_email(email, path, patente)
        if enviado:
            return render_template_string("""
            <p>PDF de la patente <b>{{ patente }}</b> enviado a <b>{{ email }}</b></p>
            <a href="/">Volver a enviar otra patente</a>
            """, patente=patente, email=email)
        else:
            return "<p>Hubo un error al enviar el correo.</p><a href='/'>Volver a intentar</a>"
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    app.run(debug=True)
