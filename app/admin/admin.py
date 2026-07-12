
from starlette_admin.contrib.sqla import ModelView as SQLAlchemyModelView, Admin
from app.models import User, Book
from app.core.database import engine
from app.admin.auth import AdminAuthProvider


class UserAdmin(SQLAlchemyModelView):
    fields = [User.id, User.username, User.email, User.created_at, User.updated_at]
    exclude_fields_from_list = [User.updated_at]
    exclude_fields_from_create = [User.id, User.created_at, User.updated_at]
    exclude_fields_from_edit = [User.id, User.created_at, User.updated_at]
    # Кол-во пользователей на одной странице
    page_size = 20


class BookAdmin(SQLAlchemyModelView):
    fields = [Book.id, Book.title, Book.author, Book.genre, Book.user_id, Book.created_at, Book.updated_at]
    exclude_fields_from_list = [Book.updated_at]
    exclude_fields_from_create = [Book.id, Book.created_at, Book.updated_at]
    exclude_fields_from_edit = [Book.id, Book.created_at, Book.updated_at]
    page_size = 20



# Создает административное приложение, связанное с моей БД

admin = Admin(engine=engine,
              auth_provider=AdminAuthProvider())
admin.add_view(
    UserAdmin(
        User,
        name='User',
        label="Users",
    ))
admin.add_view(
    BookAdmin(
        Book,
        name="Book",
        label="Books",
    ))

