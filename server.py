import os
from flask import Flask, request, jsonify
import trimesh

app = Flask(__name__)

@app.route('/quote', methods=['POST'])
def quote():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']

    if not file.filename.endswith('.glb'):
        return jsonify({'error': 'Only .glb files are supported'}), 400

    try:
        mesh = trimesh.load(file, file_type='glb')
        volume = mesh.volume / 1000  # cm^3 if units are in mm^3
        price = round(0.20 * volume + 5, 2)  # Simple formula
        return jsonify({'volume_cm3': volume, 'price_usd': price})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)