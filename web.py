from flask import Flask, render_template, request, flash, redirect, url_for, get_flashed_messages
import asyncio
from app.__main__ import generate_and_print_barcode, print_text
from random import randbytes

app = Flask(__name__)
app.secret_key = randbytes(5).hex()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/print', methods=['POST'])
async def print_label():
    text_to_print = request.form['text']
    print_type = request.form['type']
    
    if print_type == 'barcode':
        await generate_and_print_barcode(text_to_print, should_print=True)
        flash("Printing barcode...")
    else:
        await print_text(text_to_print, should_print=True)
        flash("Printing text...")
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
