from flask import Blueprint, render_template, redirect, url_for, flash, request, session
# from flask_login import login_user, login_required, current_user
from . import db

views = Blueprint('views', __name__)


@views.route('/')
def home():

    return "server is running"
