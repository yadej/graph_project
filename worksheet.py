from modules.open_digraph import *
import inspect

d = open_digraph([1, 2, 3], [6], [node(0, 'a', [], [1])])
print(f'd = {d}\n')


print(f'methodes du module open_digraph = {dir(open_digraph)}')

