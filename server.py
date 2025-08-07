from flask import Flask, request, jsonify
from stl import mesh
import tempfile
import os

app = Flask(__name__)

def calculate_volume(file_path):
    your_mesh = mesh.Mesh.from_file(file_path)
    return abs(your_mesh.get_mass_properties()[0]) / 1000  # Convert mm³ to cm³

@app.route("/quote", methods=["POST"])
def quote():
    file = request.files.get('model')
    if not file:
        return jsonify({'error': 'No file uploaded'}), 400

    with tempfile.NamedTemporaryFile(delete=False, suffix=".stl") as tmp:
        file.save(tmp.name)
        try:
            volume_cm3 = calculate_volume(tmp.name)
            base_price = 5.0
            rate_per_cm3 = 0.25
            price = base_price + (volume_cm3 * rate_per_cm3)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        finally:
            os.remove(tmp.name)

    return jsonify({'price': price})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
