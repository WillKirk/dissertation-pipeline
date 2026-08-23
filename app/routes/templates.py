from flask import Blueprint, request, jsonify
from jinja2 import Environment

templates_bp = Blueprint("templates", __name__, url_prefix="/templates")


@templates_bp.route("/render", methods=["POST"])
def render_template_custom():
    data = request.get_json()
    template_str = data.get("template")
    context = data.get("context", {})

    env = Environment()
    template = env.from_string(template_str)
    rendered = template.render(**context)

    return jsonify({"rendered": rendered}), 200


@templates_bp.route("/preview", methods=["POST"])
def preview_template():
    data = request.get_json()
    template_str = data.get("template")

    safe_output = template_str.replace("{", "&#123;").replace("}", "&#125;")

    return jsonify({"preview": safe_output}), 200