import random

from flask import *
from Dbconnection import Db

app = Flask(__name__)
app.secret_key = "abc"


@app.route('/')
def index():
    c = Db()
    qry = "select * from addpost"
    r = c.select(qry)
    return render_template("index.html",data=r)


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/rating/<postname>')
def rating(postname):
    c = Db()
    qry = "select postname,username from addpost where postname='"+str(postname)+"'"
    r=c.selectOne(qry)
    return render_template('rating.html', data=r)


@app.route('/reg')
def reg():
    return render_template('reg.html')

@app.route('/add')
def add():
    return render_template('addpost.html')

@app.route('/adminhome')
def adminhome():
    return render_template('adminhome.html')

@app.route('/userhome')
def userhome():
    return render_template('userhome.html')


@app.route('/login_post',methods=['post'])
def login_post():
    c=Db()
    uname=request.form['username']
    password=request.form['password']
    qry = "select * from login where username='"+uname+"' and `password`='"+password+"'"
    res = c.selectOne(qry)
    if res is not None:
        type=res['type']
        if type=='admin':
            return adminhome()
        elif type=='user':
            session['username'] = res['username']
            return userhome()
        else:
            return '''<script>alert('invalid username or password');window.location='/login'</script>'''
    else:
        return '''<script>alert('invalid username or password');window.location='/login'</script>'''


@app.route('/reg_post', methods=['post'])
def reg_post():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    qry = "insert into register(username,email,password)values('" + username + "','" + email + "','" + password + "')"
    c = Db()
    c.insert(qry)
    qry1 = "insert into login(username,password,type)values('" + username + "','" + password + "','user')"
    d=Db()
    d.insert(qry1)
    return '''<script>alert("added successfully");window.location="/"</script>'''


@app.route('/addpost1', methods=['post'])
def addpost1():
    username = session['username']
    pname = request.form['poname']
    category = request.form['category']
    type = request.form['type']
    photo = request.files['file']
    # date = request.form['date']
    content = request.form['content']
    photo.save("C:\\Users\\sneha\\PycharmProjects\\stories in your hand\\static\\images"+photo.filename)
    path = "static/images/"+photo.filename
    qry = "insert into addpost(username,postname,category,type,image,date,content)values('" + username + "','" + pname + "','" + category + "','" + type + "','" + path + "',curdate(),'" + content + "')"
    c = Db()
    c.insert(qry)
    return '''<script>alert("added successfully");window.location="/add"</script>'''

@app.route('/viewpost')
def viewpost():
    c = Db()
    qry = "select * from addpost"
    r = c.select(qry)
    return render_template("user_view_all_post.html", data=r)

@app.route('/userviewallpost')
def userviewallpost():
    c = Db()
    qry = "select * from addpost"
    r = c.select(qry)
    return render_template("user_view_all_post.html", data=r)




@app.route('/<postname>')
def specpost(postname):
    c = Db()
    qry="select * from addpost where postname='"+str(postname)+"'"
    qry1="select * from rating_review where postname='"+str(postname)+"'"
    r = c.selectOne(qry)
    r1=c.select(qry1)
    session['postname'] = postname
    return render_template("specific_post.html", data=r,data1=r1)

# @app.route('v/<postname>')
# def v(postname):
#     c = Db()
#     qry="select * from addpost where postname='"+str(postname)+"'"
#     r = c.selectOne(qry)
#     session['postname'] = postname
#     return render_template("specific_post.html", data=r)



@app.route('/viewmyposts')
def viewmyposts():
    username=session['username']
    c = Db()
    qry = "select * from addpost where username='"+str(username)+"'"
    r = c.select(qry)
    return render_template("view_my_post.html", data=r)

@app.route('/viewposts')
def viewposts():
    c = Db()
    qry = "select * from addpost"
    r = c.select(qry)
    return render_template("user_view_all_post.html", data=r)

@app.route('/adminviewposts')
def adminviewposts():
    c = Db()
    qry = "select * from addpost"
    r = c.select(qry)
    return render_template("adminviewpost.html", data=r)


@app.route('/viewcomment')
def viewcomment():
    c = Db()
    qry = "select * from feedback"
    r = c.select(qry)
    return render_template("feedback.html", data=r)

@app.route('/userviewcomment')
def userviewcomment():
    c = Db()
    qry = "select * from feedback"
    r = c.select(qry)
    return render_template("user_view_comment.html", data=r)


@app.route('/delete_post/<username>')
def delete_post(username):
    db = Db()
    qry = "delete from addpost where username='" + str(username) + "'"
    db.delete(qry)
    return '''<script>alert("deleted successfully");window.location="/adminviewposts"</script>'''

@app.route('/user_delete_post/<username>')
def user_delete_post(username):
    db = Db()
    qry = "delete from addpost where username='" + str(username) + "'"
    db.delete(qry)
    return '''<script>alert("deleted successfully");window.location="/viewpost"</script>'''

@app.route('/edit_post/<postname>')
def edit_post(postname):
    qry="select * from addpost WHERE postname='"+str(postname)+"'"
    db=Db()
    res=db.selectOne(qry)
    session['postname'] = res['postname']
    return render_template("edit_post.html",data=res)

@app.route('/edit_my_post',methods=['post'])
def edit_my_post():
    db=Db()
    x = session['postname']
    category = request.form['category']
    type = request.form['type']
    content = request.form['content']
    qry = "update  addpost  set  category='"+category+"',type='"+type+"',content='"+content+"' where postname='" + str(x) + "'"
    db.update(qry)
    return '''<script>alert("edited successfully");window.location="/viewposts"</script>'''


@app.route("/add_rating", methods=['POST'])
def add_review():
    review = request.form["review"]
    rating = request.form["rating"]
    email = request.form["email"]
    postname = request.form["postname"]
    username = request.form["username"]
    qry = "insert into rating_review(username,review,email,rating,postname,date) values('" + username + "','" + review + "','" + email + "','" + rating + "','" + postname + "',curdate())"
    c = Db()
    c.insert(qry)
    return '''<script>alert("added successfully");window.location="/"</script>'''

@app.route('/view_rating')
def view_rating():
    c = Db()
    qry = "select * from rating_review"
    r = c.select(qry)
    return render_template("view_rating_and_review.html", data=r)

@app.route('/user_view_rating')
def user_view_rating():
    username = session['username']
    c = Db()
    qry = "select * from rating_review where username='"+str(username)+"'"
    r = c.select(qry)
    return render_template("userview_rating.html", data=r)

@app.route('/search',methods=['post'])
def search():
    c=Db()
    name=request.form['nn']
    qry="select * from addpost where postname like '%"+name+"%'"
    r=c.select(qry)
    return render_template("search_view.html",data=r)

@app.route('/admin_delete_comment/<username>')
def admin_delete_comment(username):
    db = Db()
    qry = "delete from rating_review where username='" + str(username) + "'"
    db.delete(qry)
    return '''<script>alert("deleted successfully");window.location="/view_rating"</script>'''

@app.route('/logout')
def logout():
    session.pop('username',None)
    return redirect('/')

@app.route('/checkusername', methods=['POST'])
def checkusername():
    c = Db()
    print(request.form)
    email=request.form['un']
    qr="SELECT * FROM `register` WHERE `username`='"+email+"' "
    res=c.selectOne(qr)
    print(res)
    if res is None:
        resp = make_response(json.dumps(""))
        resp.status_code = 200
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    else:
        resp = make_response(json.dumps("Username Existing"))
        resp.status_code = 200
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp


@app.route('/checkemail1', methods=['POST'])
def checkemail1():
    c = Db()
    print(request.form)
    email=request.form['em']
    qr="SELECT * FROM `register` WHERE `email`='"+email+"'"
    res=c.selectOne(qr)
    print(res)
    if res is None:
        resp = make_response(json.dumps(""))
        resp.status_code = 200
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    else:
        resp = make_response(json.dumps("Email Existing"))
        resp.status_code = 200
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp

@app.route('/checkpost', methods=['POST'])
def checkpost():
    c = Db()
    print(request.form)
    email=request.form['po']
    qr="SELECT * FROM `addpost` WHERE `postname`='"+email+"'"
    res=c.selectOne(qr)
    print(res)
    if res is None:
        resp = make_response(json.dumps(""))
        resp.status_code = 200
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    else:
        resp = make_response(json.dumps("Post exist"))
        resp.status_code = 200
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp



if __name__ == '__main__':
   app.run(debug=True, host='0.0.0.0')
