from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    code = request.form.get('code')
    
    if code.isdigit() and len(code) == 6:
        return jsonify({'redirect': '/bill'})
    else:
        message = f"Mã số {code} không hợp lệ. Vui lòng nhập một mã số gồm 6 chữ số."
        return jsonify({'message': message, 'status': 'error'})

@app.route('/bill')
def bill():
    bill_file = os.path.join(app.static_folder, 'bill.txt')
    total_amount = 0
    items = []

    if os.path.exists(bill_file):
        with open(bill_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            for line in lines:
                parts = line.strip().split('-')
                item_name = parts[0].split(':')[1].strip()
                item_price = int(parts[1].split(':')[1].strip())
                item_quantity = int(parts[2].split(':')[1].strip())
                total = item_price * item_quantity
                total_amount += total
                items.append({
                    'name': item_name,
                    'price': item_price,
                    'quantity': item_quantity,
                    'total': total
                })
    
    return render_template('bill.html', items=items, total_amount=total_amount)

@app.route('/payment')
def payment():
    return render_template('payment.html')

if __name__ == '__main__':
    app.run(debug=True)
