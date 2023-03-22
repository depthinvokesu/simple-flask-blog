from flask import Blueprint, render_template, abort, request, url_for, redirect, flash
from flask_login import login_required
from application.models.model import *
from application.forms import CreatePostForm

blog_bp = Blueprint('blog', __name__, template_folder='templates')


@blog_bp.route('/')
@login_required
def blog():
    page_number = request.args.get("p", "1") # if p is None, return 1
    if page_number.isdigit():
        page_number = int(page_number)
        pgntn_obj = db.paginate(db.select(Post).order_by(Post.created.desc()), page=page_number, per_page=3)
        return render_template('blog/blog.html.jinja2', pgntn=pgntn_obj)
    abort(404)


@blog_bp.route("/search")
@login_required
def search():
    query = request.args.get("q")
    page_number = request.args.get("p", "1") # if p is None, return 1
    if query and page_number.isdigit():
        page_number = int(page_number)
        pgntn_obj = db.paginate(
            select=
                db.select(Post).where(
                    db.or_(
                    Post.title.contains(query),
                    Post.body.contains(query)
                    )
                ),
            page=page_number,
            per_page=5
        )
        return render_template('blog/blog.html.jinja2', pgntn=pgntn_obj, search_query = query)
    abort(404)


@blog_bp.route("/create", methods = ['POST', 'GET'])
@login_required
def create():
    tags_db = set(db.session.scalars(db.select(Tag.name)).all())
    form_create = CreatePostForm(formdata=request.form)

    if request.method == 'POST' and form_create.validate():
        title = form_create.title.data
        body = form_create.body.data
        tags_form = set(form_create.tag.raw_data)

        tags_new = tags_form.difference(tags_db)
        tags_exist = tags_form.intersection(tags_db)

        tags_new_db = [Tag(name=tag) for tag in tags_new if tag != '']
        tags_exist_db = [db.session.scalars(db.select(Tag).where(Tag.name == tag)).first() for tag in tags_exist]

        try:
            post = Post(title=title, body=body)
            post.tags.extend([*tags_new_db, *tags_exist_db])
            db.session.add(post)
            db.session.commit()
        except:
            flash("An error occured while persisting chages to the database")
            return redirect(url_for('blog.create'))
        
        flash("Your post has been succesfully created!", category='success')
        return redirect(url_for('blog.blog'))

    # if request.method == 'GET' or form is invalid (form.errors is not empty)
    return render_template("blog/create.html.jinja2", form=form_create, tags=tags_db)


@blog_bp.route("/<slug>")
@login_required
def view_post(slug):
    post = db.session.scalars(db.select(Post).where(Post.slug==slug)).first()
    if post:
        tags = getattr(post, 'tags', None)
        return render_template("blog/post.html.jinja2", post=post, tags=tags)
    abort(404)


@blog_bp.route("/<slug>/edit", methods = ['POST', 'GET'])
@login_required
def edit_post(slug):
    post = db.session.scalars(db.select(Post).where(Post.slug==slug)).first()
    if post:
        form_edit = CreatePostForm(formdata=request.form, obj=post) # obj only used if formdata is not passed
        if request.method == 'POST' and form_edit.validate():
            form_edit.populate_obj(obj=post)
            # populate_obj method modifies its parameter (post) according to a form (form_post) based on common attributes
            # alternatively this opearation could be also done manually, e.g.:
                # post.title = form.title.data
                # post.body = from.body.data
                # post.tags = form.body.tag            
            db.session.commit()
            return redirect(url_for('blog.blog'))
        
        # if request.method == 'GET' or form is invalid (form.errors is not empty)
        return render_template('blog/edit.html.jinja2', form=form_edit)

    # if post wasn't found
    return redirect(url_for('blog.blog'))


@blog_bp.route("/tag/<slug>")
@login_required
def view_tag(slug):
    tag = db.session.scalars(db.select(Tag).where(Tag.slug == slug)).first()
    if tag:
        posts = getattr(tag, 'posts', None)
        return render_template("blog/tag.html.jinja2", tag=tag, posts=posts, slug=slug)
    abort(404)