from flask import render_template, request, Blueprint
from flaskblog.models import Post


main = Blueprint('main', __name__)  # similar to app = Flask(__name__)


@main.route('/home')
@main.route('/')
def home():
    page = request.args.get('page', 1, type=int)  # getting the page. Default page is 1
    # posts = Post.query.all()  # kept it here to show how I did it earlier
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=4)  # to prevent grabbing and loading all the posts at once
    return render_template("home.html", posts=posts)


@main.route('/about')
def about():
    return render_template("about.html", title='about')
