import argparse

from src.crud import get_user, get_all_todos, create_todo, update_todo, remove_todo, get_student_load, get_teachers
from src.models import Student, Teacher


parser = argparse.ArgumentParser(description='Todo APP')
parser.add_argument('--action', '-a' help='Command: create, remove, update, delete, list')
parser.add_argument('--id')
parser.add_argument('--title')
parser.add_argument('--desc')
parser.add_argument('--login')
parser.add_argument('--model', '-m')
parser.add_argument('--name', '-n')


arguments = parser.parse_args()
print(arguments)
my_arg = vars(arguments)
print(my_arg)

action = my_arg.get('action')
title = my_arg.get('title')
description = my_arg.get('desc')
_id = my_arg.get('id')
login = my_arg.get('login')


def main(user):
    match action:
        case 'create':
            create_todo(title=title, description=description, user=user)
        case 'list':
            todos = get_all_todos(user)
            for t in todos:
                print(t.id, t.title, t.description, t.user.login)
        case 'update':
            t = update_todo(_id=_id, title=title,
                            description=description, user=user)
            if t:
                print(t.id, t.title, t.description, t.user.login)
            else:
                print('Not found id')
        case 'remove':
            r = remove_todo(_id=_id, user=user)
            print(f'Remove {r}')
        case 'student':
            print(get_student_load())
        case _:
            print('Nothing?')


if __name__ == "__main__":
    # get_student_load()
    get_teachers()
    # user = get_user(login)
    # password = input('Password: ')
    # if password == user.password:
    #     main(user)
    # else:
    #     print('Wrong password')
