from flask import Flask, request, jsonify
from gradio_client import Client, handle_file
import tempfile

app = Flask(__name__)
client = Client("jamesliu1217/EasyControl_Ghibli")

@app.route("/convert", methods=["POST"])
def convert():
    if 'image' not in request.files:
        return jsonify({"error": "Image not provided"}), 400

    file = request.files['image']

    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
        file.save(tmp.name)
        result = client.predict(
            prompt="Ghibli Studio style, Charming hand-drawn anime-style illustration",
            spatial_img=handle_file(tmp.name),
            height=768,
            width=768,
            seed=42,
            control_type="Ghibli",
            use_zero_init=False,
            zero_steps=1,
            api_name="/single_condition_generate_image"
        )
    return jsonify(result)
