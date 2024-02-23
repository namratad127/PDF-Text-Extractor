from flask import Flask, render_template, request
import os  # Import the os module
import pdftotext
import re

app = Flask(__name__)

# Ensure the 'uploads' directory exists
uploads_dir = os.path.join(app.root_path, 'uploads')
os.makedirs(uploads_dir, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    uploaded_file = request.files['file']

    if uploaded_file.filename != '':
        # Save the uploaded PDF
        pdf_path = os.path.join(uploads_dir, 'uploaded_file.pdf')
        uploaded_file.save(pdf_path)

        # Run the script from Part 1 to extract data
        with open(pdf_path, 'rb') as f:
            pdf = pdftotext.PDF(f)
            text = '\n\n'.join(pdf)

        # Using regular expressions to match the text on invoices
        invoice_number_match = re.search(r'Invoice\s*No\s*:\s*(.+?)\s*', text, re.IGNORECASE)
        total_amount_due_match = re.search(r'Total\s*CHF\s*:\s*(.+?)\s*', text, re.IGNORECASE)
        invoice_date_match = re.search(r'Payment\s*Date\s*:\s*(.+?)\s*', text, re.IGNORECASE)

        # Extracting data with error handling
        invoice_number = invoice_number_match.group(1).strip() if invoice_number_match else None
        total_amount_due = total_amount_due_match.group(1).strip() if total_amount_due_match else None
        invoice_date = invoice_date_match.group(1).strip() if invoice_date_match else None

        return render_template('result.html', invoice_number=invoice_number, total_amount_due=total_amount_due, invoice_date=invoice_date)
    else:
        return render_template('index.html', error='Please upload a PDF file.')

if __name__ == '__main__':
    app.run(debug=True)
