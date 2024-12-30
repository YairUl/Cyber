from flask import Flask, request

app = Flask(__name__)

@app.route('/sum', methods=['GET'])
def sum_numbers():
    try:
        a = float(request.args.get('a', 0))
        b = float(request.args.get('b', 0))
    except ValueError:
        return "Invalid numbers for a \ b.", 400

    c = a + b

    return f"""
    <html>
        <body>
            <h1>The result of {a} + {b} is: {c}</h1>
        </body>
    </html>
    """

@app.route('/average', methods=['GET'])
def average_numbers():
    try:
        a = float(request.args.get('a', 0))
        b = float(request.args.get('b', 0))
    except ValueError:
        return "Invalid numbers for a \ b.", 400

    c = (a + b)/2

    return f"""
    <html>
        <body>
            <h1>The average of {a} + {b} is: {c}</h1>
        </body>
    </html>
    """

@app.errorhandler(404)
def not_found_error(error):
    return f"""
    <html>
        <body>
            <h1>404 Not Found</h1>
            <p>The requested URL was not found on the server.</p>
        </body>
    </html>
    """, 404

if __name__ == '__main__':
    app.run(debug=True)
