from flask import Flask, request, jsonify, send_file, render_template_string
from PIL import Image
from fpdf import FPDF
import io

app = Flask(__name__)

# HTML template for the web interface
html_template = """
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Image to PDF Converter</title>
</head>
<body>
    <h1>Image to PDF Converter</h1>
    <form action="/convert" method="post" enctype="multipart/form-data">
        <label for="image">Choose an image to convert:</label>
        <input type="file" id="image" name="image" accept="image/*">
        <button type="submit">Convert to PDF</button>
    </form>
    {% if pdf_url %}
    <h2>Download your PDF:</h2>
    <a href="{{ pdf_url }}">Download PDF</a>
    {% endif %}
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(html_template)

@app.route('/convert', methods=['POST'])
def convert_image_to_pdf():
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400
    
    image_file = request.files['image']
    image = Image.open(image_file)
    
    pdf = FPDF()
    pdf.add_page()
    pdf.image(image_file, 10, 10, 190, 0)  # fit image to A4 size
    
    output = io.BytesIO()
    pdf.output(output)
    
    output.seek(0)
    if request.headers.get('Content-Type') == 'application/json':
        return send_file(output, mimetype='application/pdf', as_attachment=True, attachment_filename='output.pdf')
    else:
        pdf_url = "/download_pdf"
        return render_template_string(html_template, pdf_url=pdf_url)

@app.route('/download_pdf')
def download_pdf():
    return send_file(output, mimetype='application/pdf', as_attachment=True, attachment_filename='output.pdf')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
