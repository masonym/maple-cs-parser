from flask import Flask, jsonify, send_from_directory
import os
import item_matcher # type: ignore

app = Flask(__name__, static_folder='./upcoming-sales-website/build', static_url_path='/')
app.config["JSON_SORT_KEYS"] = False


item_data = item_matcher.main()

@app.route('/api/items', methods=['GET'])
def get_items():
    return jsonify(item_data)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_react_app(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run()