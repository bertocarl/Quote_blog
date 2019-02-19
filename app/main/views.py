from flask import render_template,request,redirect,url_for,abort
from . import main
from .forms import BlogForm,UpdateProfile,CommentForm
from ..import db,photos
from ..models import User,Blog,Comment
from flask_login import login_required,current_user
import markdown2
import requests
@main.route("/")
def index():
   
    response = requests.get('http://quotes.stormconsultancy.co.uk/random.json')

    quote = response.json()
       
    blogs = Blog.query.all()

    title = "Bloggers Paradise"
    return render_template("index.html", title = title, quote = quote, blogs = blogs)

@main.route("/post",methods=['GET','POST'])
@login_required
def post():

    response = requests.get('http://quotes.stormconsultancy.co.uk/random.json')

    quote = response.json()


    form = BlogForm()
    if form.validate_on_submit():
        title = form.title.data
        blog = form.blog.data
        category= form.category.data
        like=0
        dislike=0

        # New blog instance
        new_blog = Blog(blog_title=title,blog_body=blog,category=category,like=like,dislike=dislike,user=current_user)

        # save blog method
        new_blog.save_blog()
        
        return redirect(url_for('main.post'))

    title="New Post"
    return render_template('post.html',title=title,blog_form=form, quote = quote, div = "New Post")

@main.route('/blog_comment/<int:id>',methods=['GET','POST'])
def blog_comment(id):
    blog=Blog.query.get_or_404(id)
    comment= Comment.query.all()
    form=CommentForm()

    if request.args.get("like"):
        blog.like = blog.like+1

        db.session.add(blog)
        db.session.commit()

        return redirect("/blog_comment/{blog_id}".format(blog_id=blog.id))

    elif request.args.get("dislike"):
        blog.dislike=blog.dislike+1

        db.session.add(blog)
        db.session.commit()

        return redirect("/blog_comment/{blog_id}".format(blog_id=blog.id))

    if form.validate_on_submit():
        comment = form.comment.data

        new_comment = Comment(comment=comment)

        new_comment.save_comment()
        return redirect(url_for('main.blog_comment',id=id))
    comments = Comment.query.all()
    return render_template('blog_comment.html',comment=comment,blog=blog,comment_form=form,comments=comments)


@main.route('/user/<uname>')
def profile(uname):
    user=User.query.filter_by(username=uname).first()
    blogs = Blog.query.filter_by(user_id=user.id).all()

    if user is None:
        abort(404)

    return render_template("profile/profile.html",user=user,blogs=blogs)

@main.route('/user/<uname>/update',methods=['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form=form)

@main.route('/user/<uname>/update/pic',methods=['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename= photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()

    return redirect(url_for('main.profile',uname=uname))
@main.route('/subscribe',methods=['GET','POST'])
def subscribe():
    form = SubscribeForm()

    if form.validate_on_submit():
       subscriber = subscribe(email=form.email.data)

       db.session.add(subscriber)
       db.session.commit()

       
       return redirect(url_for('main.index', subscribe = subscribe))

       title = 'Subscribe Now'


    return render_template('subscribe.html',subscribe_form = form, tittle = title)


@main.route("/post/update",methods=['GET','POST'])
@login_required
def update_post(blog_id):
    blog =Blog.query.get_or_404(blog_id)
    if blog.author != current_user:
        abort (403)
    
    form = BlogForm()
    form.title.data = post.title
    form.content.data = post.content

    title="update Post"

    return render_template('post.html',title=title,blog_form=form, div ="Update Post")