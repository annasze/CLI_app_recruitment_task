from adapters.repository import Repository, SQLAlchemyRepository
from domain.models import PersonUser


class NotAuthenticated(Exception):
    pass


class NotAuthorized(Exception):
    pass


class System:
    def __init__(self, repository: Repository, user: PersonUser):
        self.repository = repository
        self.user = user

    def _admin_required(func):
        def wrapper(self, *args, **kwargs):
            if self.user.role != 'admin':
                raise NotAuthorized(
                    'You are not authorized to perform this action '
                    '(admin account required).')
            return func(self, *args, **kwargs)

        return wrapper

    def get_children_str(self):
        res = ""
        for child in self.user.children:
            res += f"{child.name}, {child.age}\n"

        return res.strip("\n")

    def get_similar_children_str(self):
        similar_people = self.repository.get_similar_users(self.user)
        res = ""
        for person in similar_people:
            children_part = "; ".join(
                f"{child.name}, {child.age}"
                for child in person.children
            )
            res += f"{person.firstname}, {person.telephone_number}: {children_part}\n"

        return res.strip("\n")

    @_admin_required
    def get_children_grouped_by_age_str(self):
        res = ""
        for age, count in self.repository.group_children_by_age():
            res += f"age: {age}, count: {count}\n"

        return res.strip("\n")

    @_admin_required
    def get_oldest_account_str(self):
        oldest_account = self.repository.get_oldest_account()
        return (
            f"name: {oldest_account.firstname}\n"
            f"email_address: {oldest_account.email}\n"
            f"created_at: {oldest_account.created_at}"
        )

    @_admin_required
    def get_accounts_count_str(self):
        return str(self.repository.get_accounts_count())


def get_access_to_system(
        login: str,
        password: str,
        repository: Repository = SQLAlchemyRepository()
):
    if login.isdigit():
        user = repository.get_person_by_telephone_number(
            login, with_children=True
        )
    else:
        user = repository.get_person_by_email(
            login, with_children=True
        )
    if user is None:
        raise NotAuthenticated("Invalid login")
    elif password != user.password:
        raise NotAuthenticated("Invalid login")

    return System(repository, user)
