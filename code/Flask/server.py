from flask import Flask, request, jsonify, Response, render_template


app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({})

if __name__ == "__main__":
    app.run(debug=True)


