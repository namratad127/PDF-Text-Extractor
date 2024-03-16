from flask import Flask, request, render_template
import pdfplumber

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        pdf_text = extract_text_from_pdf(uploaded_file)
        return pdf_text
    else:
        return 'No file uploaded'

def extract_text_from_pdf(file):
    with pdfplumber.open(file) as pdf:
        text = ''
        for page in pdf.pages:
            text += page.extract_text()
    return text

if __name__ == '__main__':
    app.run(debug=True)
