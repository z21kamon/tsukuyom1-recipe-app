# импорт Flask
from flask import Flask, render_template, redirect, request, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_restful import Api
from flask_admin import Admin

# импорт БД
from data import db_session
from data.users import User
from data.recipes import Recipe

# импорт модулей
from register_form import RegisterForm
from recipe_add_form import RecipeAddForm
from login_form import LoginForm
from search_form import SearchForm
from like_btn import LikeButton, DislikeButton
from admin_view import AdminModelView, CustomIndexView

# импорт API
import users_resource
import recipes_resource

# импорт прочих модулей
from datetime import datetime as dt
from json import loads, dumps
from werkzeug.utils import secure_filename
import os
from PIL import Image
from sqlalchemy import desc

# инициализация приложения
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(32)
UPLOAD_FOLDER = os.path.join('static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# инициализация менеджера авторизации
login_manager = LoginManager()
login_manager.init_app(app)

# инициализация API
api = Api(app)
api.add_resource(users_resource.UsersListResource, '/api/users')
api.add_resource(users_resource.UserResource, '/api/users/<int:user_id>')
api.add_resource(recipes_resource.RecipesListResource, '/api/recipes')
api.add_resource(recipes_resource.RecipesResource, '/api/recipes/<int:recipe_id>')

# инициализация админки
app.config['FLASK_ADMIN_SWATCH'] = 'journal'
admin = Admin(app, name='Yarik Recipe App', template_mode='bootstrap3', index_view=CustomIndexView())


# проверка разрешенного формата файла
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


# обработка ошибки 404
@app.errorhandler(404)
def not_found(error):
    form = SearchForm()
    return render_template('404.html', form=form)


@app.route('/index')
def index_redirect():
    return redirect('/')


# главная страница
@app.route('/', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    if form.query_field.data:
        return redirect(f'/search?query={form.query_field.data}')
    db_sess = db_session.create_session()
    cotw_list = db_sess.query(Recipe).filter(Recipe.cotw == True)
    hot_list = db_sess.query(Recipe).order_by(desc(Recipe.likes_count / Recipe.views_count))
    return render_template('index.html', form=form, cotw_list=cotw_list, hot_list=hot_list)


# поиск по названию и тегам
@app.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    if form.query_field.data:
        return redirect(f'/search?query={form.query_field.data}')
    keyword = request.args.get('query')
    db_sess = db_session.create_session()
    recipes_list = db_sess.query(Recipe).filter((Recipe.name.like(f"%{keyword}%")) |
                                                (Recipe.tags.like(f"%{keyword}%")))
    return render_template('recipes.html', recipes_list=recipes_list, form=form)


# вход
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


# выход
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


# регистрация пользователя
@app.route('/signup', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User()
        user.nickname = form.nickname.data
        user.email = form.email.data
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


# добавление рецепта
@app.route('/add-recipe', methods=['GET', 'POST'])
@login_required
def add_recipe():
    form = RecipeAddForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        recipe = Recipe()

        recipe.name = form.name.data
        recipe.author = current_user.id
        recipe.prep_time = form.prep_time.data
        recipe.tags = dumps(list(map(str.strip, form.tags.data.split(','))))
        recipe.date = dt.strftime(dt.now(), "%b %d, %Y")
        recipe.ingredients = dumps(list(map(str.strip, form.ingredients.data.split(','))))
        recipe.views_count = 0

        f = form.image.data
        filename = secure_filename(f.filename)
        path = os.path.join(UPLOAD_FOLDER, secure_filename(filename))
        f.save(path)

        im = Image.open(path)
        width, height = im.size

        left = (width - 1000) / 2
        top = (height - 450) / 2
        right = (width + 1000) / 2
        bottom = (height + 450) / 2

        im = im.crop((left, top, right, bottom))
        im.save(os.path.join(UPLOAD_FOLDER, 'cropped-' + secure_filename(filename)))

        recipe.image_url = path
        recipe.cropped_image_url = os.path.join(UPLOAD_FOLDER, 'cropped-' + secure_filename(filename))

        db_sess.add(recipe)
        db_sess.commit()
        return redirect('/')
    return render_template('recipe_add.html', title='Добавление работы', form=form)


# отображение рецепта
@app.route('/recipe-post/<int:recipe_id>', methods=['GET', 'POST'])
def recipe_post(recipe_id):
    form = SearchForm()
    db_sess = db_session.create_session()
    recipe = db_sess.query(Recipe).get(recipe_id)
    author = db_sess.query(User).get(recipe.author)
    lks = loads(recipe.likers)
    like_btn = LikeButton() if current_user.is_authenticated and current_user.id not in lks else DislikeButton()
    if form.query_field.data:
        return redirect(f'/search?query={form.query_field.data}')
    if current_user.is_authenticated and current_user.id in lks and like_btn.is_submitted():
        recipe.likes_count -= 1
        print('-')
        lks.remove(author.id)
    if current_user.is_authenticated and current_user.id not in lks and like_btn.is_submitted():
        recipe.likes_count += 1
        print('+')
        lks.append(author.id)
    if current_user.is_anonymous and like_btn.is_submitted():
        flash('You have to log in')
    recipe.likers = dumps(lks)
    db_sess.commit()
    recipe.views_count += 1
    return render_template('recipe_post.html',
                           form=form,
                           recipe=recipe,
                           author=author,
                           like_btn=like_btn,
                           json_ingredients=loads(recipe.ingredients),
                           json_tags=loads(recipe.tags))


# профиль пользователя
@app.route('/profile/<name>', methods=['GET', 'POST'])
def account(name):
    form = SearchForm()
    db_sess = db_session.create_session()
    profile = db_sess.query(User).filter(User.nickname == name).first()
    recipes_list = db_sess.query(Recipe).filter(Recipe.author == profile.id)
    return render_template('account.html',
                           profile=profile,
                           recipes_list=recipes_list,
                           form=form)


# список всех рецептов
@app.route('/all-recipes', methods=['GET', 'POST'])
def all_recipes():
    form = SearchForm()
    db_sess = db_session.create_session()
    recipes = db_sess.query(Recipe).all()
    return render_template('recipes.html', form=form, recipes_list=recipes)


# запуск приложения
if __name__ == '__main__':
    db_session.global_init("db/users.db")
    admin.add_view(AdminModelView(User, db_session.create_session()))
    admin.add_view(AdminModelView(Recipe, db_session.create_session()))
    app.run(port=8080, host='127.0.0.1', debug=True)
