from flask import Blueprint, render_template, request, url_for, session, redirect, flash
from models import *

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/')
def home():
    return render_template('index.html')