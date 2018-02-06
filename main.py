import argparse
import my_loging
import models_pack.db_access


def hello():
    print('Hello')


map = {'hello': hello}
parser = argparse.ArgumentParser()
parser.add_argument('-command', choices=map)
namespace = parser.parse_args()
func = map[namespace.command]
func()
my_loging.info(str(namespace.name) + ' ввел свое имя')
print('Привет, ' + str(namespace.name))
# TODO: дописать парсер
