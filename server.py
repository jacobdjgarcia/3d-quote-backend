from flask import Flask, request, jsonify
import tempfile
import os
import trimesh

app = Flask(__name__)

@app.route("/quote", methods=["POST"])
def quote():
    file = request.files.get('model')
    if not file:
        return jsonify({'error': 'No file uploaded'}), 400

    with tempfile.NamedTemporaryFile(delete=False, suffix=".glb") as tmp:
        file.save(tmp.name)
        try:
            mesh = trimesh.load(tmp.name, force='mesh')
            volume_cm3 = mesh.volume / 1000  # Convert mm³ to cm³ if units are in mm
            base_price = 5.0
            rate_per_cm3 = 0.25
            price = base_price + (volume_cm3 * rate_per_cm3)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        finally:
            os.remove(tmp.name)

    return jsonify({'price': price})
