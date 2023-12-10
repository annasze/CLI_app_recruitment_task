from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from domain.system import get_access_to_system, NotAuthorized, NotAuthenticated

__all__ = [
    'print_all_accounts',
    'print_oldest_account',
    'group_by_age',
    'print_children',
    'find_similar_children_by_age',
    'create_database'
]


def authenticate(func):
    def wrapper(args, **kwargs):
        try:
            system = get_access_to_system(
                login=args.login,
                password=args.password
            )
            return func(system, **kwargs)
        except NotAuthenticated as exc:
            print(exc)
        except SQLAlchemyError:
            print("The database hasn't been created yet. "
                  "Please run: 'python script.py create-database' first.")
    return wrapper


@authenticate
def print_all_accounts(system):
    try:
        print(system.get_accounts_count_str())
    except NotAuthorized as exc:
        print(exc)


@authenticate
def print_oldest_account(system):
    try:
        print(system.get_oldest_account_str())
    except NotAuthorized as exc:
        print(exc)


@authenticate
def group_by_age(system):
    try:
        print(system.get_children_grouped_by_age_str())
    except NotAuthorized as exc:
        print(exc)


@authenticate
def print_children(system):
    print(system.get_children_str())


@authenticate
def find_similar_children_by_age(system):
    print(system.get_similar_children_str())


def create_database(*args, data):
    from adapters.orm import create_sqlite_db
    try:
        create_sqlite_db(data=data)
        print("The database has been created.")
    except IntegrityError:
        print("The database already exists.\n"
              "Run 'python script.py --help' to see available commands.")

