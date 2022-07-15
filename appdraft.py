

from crypt import methods
from datetime import datetime

from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)

#sklite store database locally in file  /// slash is is current dir but //// is in behind just like absolute path
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///post.db'  #this is the best one in development mode so if you want to use mysql put here mysql or postgresql#app.config['SQLAlchemy_DATABASE_URI'] = 'mysql://username:password#@xxxxxx.hostedresource.com/dbname'

db=SQLAlchemy(app)


class BlogPosts(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(100),nullable=False)
    content=db.Column(db.Text,nullable=False)
    author=db.Column(db.String(20),nullable=False,default='N/A')
    date_posted=db.Column(db.DateTime,default=datetime.utcnow);

    def __repr__(self):
        return 'Blog post'+str(self.id)
    




@app.route('/')
def index():
    return render_template("index.html")   #alwayz point on template folder


@app.route('/posts',methods=['GET','POST'])
def posts():

    if request.method == 'POST':
        post_title=request.form['title']
        post_content=request.form['content']
        author=request.form['author']
        new_post=BlogPosts(title=post_title,content=post_content,author=author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        all_posts=BlogPosts.query.all()
        return render_template('posts.html', posts=all_posts)

@app.route('/posts/delete/<int:id>')
def delete(id):
    post=BlogPosts.query.get_or_404(id)   #  get_or_404 meanbecause because if data not dfound we don't want to break
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts')



@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    post=BlogPosts.query.get_or_404(id)
    if request.method == 'POST':
        post.title=request.form['title']
        post.author=request.form['author']
        post.content=request.form['content']
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template("edit.html",post=post) 



@app.route('/posts/new', methods=['GET', 'POST'])
def new_post():
     if request.method == 'POST':
        post_title=request.form['title']
        post_content=request.form['content']
        author=request.form['author']
        new_post=BlogPosts(title=post_title,content=post_content,author=author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
     else:
        return render_template('new_post.html')
   





@app.route('/home/users/<string:name>/posts/<int:id>')  #forexample for integer    /<int:id> {% this one its called jinja syntax %}
def hello(name,id):
    return "Hello, " + name + ", your id is: " + str(id)


@app.route("/onlyget",methods=['GET'])

def get_req():
    return "you get get only this webpage"

if __name__ == "__main__":
    app.run(debug=True)
#app.run()


