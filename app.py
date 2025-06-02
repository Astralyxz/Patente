from flask import Flask, request, send_file, render_template_string
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

app = Flask(__name__)
pdfmetrics.registerFont(TTFont("5x5DotsOutline", "5x5dotso.ttf"))

HTML_TEMPLATE = '''
<!doctype html>
<title>Generador de Patentes</title>
<h2>Ingresa tu patente:</h2>
<form method="post">
  <input name="patente" type="text" maxlength="10" required>
  <input type="submit" value="Generar PDF">
</form>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        patente = request.form['patente'].upper()
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
        return send_file(path, as_attachment=True)

    return HTML_TEMPLATE

if __name__ == '__main__':
    app.run()
