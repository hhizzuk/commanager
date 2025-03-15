"""
Payment processing route.

URLs include:
/process_payment
"""
import flask
import commanager

@commanager.app.route('/process_payment', methods=['POST'])
def process_payment():
    """Handle PayPal payment processing."""
    data = flask.request.json
    print("Payment received:", data)

    # could Store payment details in database (DNE right now)
    return flask.jsonify({"message": "Payment successful"}), 200
