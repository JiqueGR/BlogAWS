from flask import Blueprint

from src.controllers.PostsController import create, update, read, delete

PostsRoutes = Blueprint('posts_routes',__name__)

PostsRoutes.route('create/', methods=['GET','POST'])(create)
PostsRoutes.route('read/<user_account>/<post_id>', methods=['GET'])(read)
PostsRoutes.route('update/<user_account>/<post_id>', methods=['GET', 'POST'])(update)
PostsRoutes.route('delete/<user_account>/<post_id>', methods=['GET'])(delete)
