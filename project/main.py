from flask import Blueprint, render_template
from . import db
from flask_login import login_required, current_user
from .models import ApiKey

main = Blueprint('main', __name__)
@main.route('/')
def index():
	print(current_user)
	if current_user.is_authenticated:
		return render_template('index.html', name=current_user.name)
	else:
		return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
	active_keys = ApiKey.query.filter_by(email=current_user.email).with_entities(ApiKey.name, ApiKey.api_key, ApiKey.email)
	dictrows = [dict(row) for row in active_keys]
	print(dictrows)
	for r in dictrows:
		r['api_key'] = r['api_key'].decode('utf-8')
	return render_template('profile.html', name=current_user.name,api_keys=dictrows)
