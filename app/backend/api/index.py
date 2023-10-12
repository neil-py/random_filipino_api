from flask import Blueprint, render_template

index_bp = Blueprint('documentation', __name__, template_folder='app/templates')

@index_bp.route('/')
def index():
    return render_template('index.html')
