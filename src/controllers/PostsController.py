from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from src.models.UsersModel import User
import boto3
from src.models.PostsModel import Post, db
import os, random

def upload_file(file_name, bucket, post_filename):
    object_name = file_name
    s3client = boto3.client('s3')
    extra_args = {'ContentDisposition': 'inline'}
    response = s3client.upload_file(file_name, bucket, post_filename, ExtraArgs=extra_args)
    os.remove(file_name)
    return response

def delete_file(bucket, post_filename):
    s3client = boto3.client('s3')
    response = s3client.delete_object(Bucket=bucket, Key=post_filename)
    return response

@login_required
def create():
    ALLOWED_EXTENSION = {"png", "jpg", "jpeg", "gif"}
    UPLOAD_FOLDER = "/static/temp/"
    BUCKET = "jiquephotoblog"
    if request.method == 'POST':
        description = request.form['description']
        file = request.files['file']
        filename, file_extension = os.path.splitext(file.filename) 
        file_extension = file_extension.replace(".", "")

        if file_extension.lower() in ALLOWED_EXTENSION:
            file.save(file.filename)
            post_filename = str(current_user.id) + "-" + str(file.filename)
            upload_file(f"{file.filename}", BUCKET, post_filename)

            post = Post(user_id = current_user.id,
                        post_description=description,
                        post_mediatype=file_extension,
                        post_mediapath="https://jiquephotoblog.s3.us-east-2.amazonaws.com/",
                        post_filename=post_filename)
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('app_routes.profile', user_account=current_user.user_account))
        
    return render_template('posts/create.html', current_user=current_user)

def read(user_account, post_id):
    if User.query.filter_by(user_account=user_account).count() == 0 or Post.query.filter_by(id=post_id).count() == 0:
        return "conta ou post nao existe"
    else:
        user = db.one_or_404(db.select(User).filter_by(user_account=user_account))
        post = db.one_or_404(db.select(Post).filter_by(id=post_id))
        return render_template('posts/read.html', user=user, post=post, current_user=current_user)

@login_required
def update(user_account, post_id):
    if User.query.filter_by(user_account=user_account).count() == 0 or Post.query.filter_by(id=post_id).count() == 0:
        return "conta ou post nao existe"
    else:
        if request.method == 'POST':
            if current_user.user_account == user_account:
                post = db.one_or_404(db.select(Post).filter_by(id=post_id))
                post.post_description = request.form['description']
                db.session.commit()
                return redirect(url_for('app_routes.profile', user_account=user_account))
            else:
                return "sem permissao"
        else:
            user = db.one_or_404(db.select(User).filter_by(user_account=user_account))
            post = db.one_or_404(db.select(Post).filter_by(id=post_id))
            return render_template('posts/update.html', user=user, post=post, current_user=current_user)

@login_required
def delete(user_account, post_id):
    BUCKET = "jiquephotoblog"
    if User.query.filter_by(user_account=user_account).count() == 0 or Post.query.filter_by(id=post_id).count() == 0:
        return "conta ou post nao existe"
    else:
        if current_user.user_account == user_account:
            post = db.one_or_404(db.select(Post).filter_by(id=post_id))
            post_filename = db.session.query(Post.post_filename).filter_by(id=post_id).scalar()
            delete_file(BUCKET, post_filename=post_filename)
            db.session.delete(post)
            db.session.commit()
            return redirect(url_for('app_routes.profile', user_account=user_account))
        else:
            return "sem permissao"