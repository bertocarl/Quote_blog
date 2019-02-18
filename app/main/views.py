from flask import render_template,request,redirect,url_for,abort
from . import main
from .forms import BlogForm,UpdateProfile,CommentForm
from ..import db,photos
from ..models import User,Blog,Comment
from flask_login import login_required,current_user
import markdown2

#Views
@main.route("/")
def index():
    """
    View root page function that return the index page and its data
    """
    blogs = Blog.query.all()

    title = "Bloggers Paradise"
    return render_template('index.html',title=title,blogs=blogs)

@main.route("/post",methods=['GET','POST'])
@login_required
def post():
    form = BlogForm()
    if form.validate_on_submit():
        title = form.title.data
        blog = form.blog.data
        category= form.category.data
        like=0
        dislike=0

        # Updated blog instance
        new_blog = Blog(blog_title=title,blog_body=blog,category=category,like=like,dislike=dislike,user=current_user)

        # save blog method
        new_blog.save_blog()
        return redirect(url_for('main.post'))

    title="Post your blog"
    return render_template('post.html',title=title,blog_form=form)

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

        new_comment = Comment(id=id,comment=comment,user_id=current_user.id)

        new_comment.save_comment()
        new_comment.append_comment()
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
def subscribe():
    form=SubscribeForm()

    if form.validate_on_submit():
        subscriber = Subscribe(email=form.email.data)

        db.session.add(subscriber)
        db.session.commit()

        
        return redirect(url_for('main.index'))

        title = 'Subscribe Now'

    return render_template('subscribe.html',subscribe_form = form)
# @main.route('/getBlogById',methods=['POST'])
# def getBlogById():
#     try:
#         if session.get('user'):
 
#             _id = request.form['id']
#             _user = session.get('user')
 
#             conn = psql.connect()
#             cursor = conn.cursor()
#             cursor.callproc('sp_GetBlogById',(_id,_user))
#             result = cursor.fetchall()
 
#             blog = []
#             blog.append({'Id':result[0][0],'Title':result[0][1],'Description':result[0][2]})
 
#             return json.dumps(blog)
#         else:
#             return render_template('error.html', error = 'Unauthorized Access')
#     except Exception as e:
#         return render_template('error.html',error = str(e))
