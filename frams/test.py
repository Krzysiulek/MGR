import os
from multiprocessing import Process


def info(title):
    print(title)
    print('module name:', __name__)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())


def f(name):
    info('function f')
    print('hello', name)


def haploid():
    pass


def diploid():
    pass


if __name__ == '__main__':
    info('main line')
    h = Process(target=haploid)
    d = Process(target=diploid)

    h.start()
    d.start()

    h.join()
    d.join()
