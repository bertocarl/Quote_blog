from flask import render_template,request,redirect,url_for,abort,flash
from . import main
from flask_login import login_required,current_user
from ..models import User,Blog,Comment,Subscribe
from .forms import UpdateProfile,BlogForm,CommentForm,SubscribeForm
from .. import db
from ..email import mail_message
import markdown2

@main.route('/')
def index():
    '''
    View root page function that returns the index page and its data
    '''
    
    title = 'Blogger Application'

    return render_template('index.html',title=title)

@main.route('/user/<uname>')
def profile(uname):
    user=User.query.filter_by(username=uname).first()

    if user is None:
        abort(404)

    title = "Profile Page"

    return render_template("profile/profile.html",title = title,user = user)

@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username=uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()
    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))
    return render_template('profile/update.html',form=form)

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))

@main.route('/blog/new',methods=['GET','POST'])
@login_required
def new_blog():
    form = BlogForm()
    if form.validate_on_submit():
        title=form.title.data
        post=form.post.data
        new_blog=Blog(title=title,post=post,user=current_user)
        new_blog.save_blog()
        subscribers= Subscribe.query.all()
        print(subscribers)
        for subscriber in subscribers:
            print(subscriber.email)
            # mail_message("New Blog Alert!!", "email/new_blog", subscriber.email)
        #     mail_message("New Blog Notice!!","email/new_blog",subscriber.email, subscriber=subscriber)
        return redirect(url_for('main.index'))
    return render_template('new_blog.html',blog_form = form)
    
@main.route('/blog/<int:id>')
def see_blogs(id):
    form=BlogForm()
    user=User.query.filter_by(id=id).first()
    blog= Blog.query.filter_by(id=id).first()

    comments = Comment.get_blog_comments(id)


    title = 'Blogger Application'
    return render_template('blog.html',comments = comments,title = title,blog = blog,blog_form = form,user = user)

@main.route('/comment/new/<int:id>',methods=['GET','POST'])
def new_comment(id):
    blog=Blog.query.filter_by(id=id).first()

    if blog is None:
        abort(404)
    form = CommentForm()

    if form.validate_on_submit():
        name = form.name.data
        comment_itself = form.comment_itself.data
        new_comment = Comment(comment_itself = comment_itself,name = name,blog = blog)
        new_comment.save_comment()

        return redirect(url_for('main.see_blogs',id = blog.id))

    title='Comment Section'

    return render_template('new_comment.html',title = title,comment_form = form)

@main.route('/subscribe',methods=["GET","POST"])
def subscribe():
    form=SubscribeForm()

    if form.validate_on_submit():
        subscriber = Subscribe(email=form.email.data)

        db.session.add(subscriber)
        db.session.commit()

        
        return redirect(url_for('main.index'))

        title = 'Subscribe Now'

    return render_template('subscription.html',subscribe_form = form)

