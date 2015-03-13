import random
from multiprocessing import Pool, Manager

class Tester(object):
    def __init__(self, num=0.0, name='none'):
        self.num  = num
        self.name = name

    def __repr__(self):
        return '%s(%r, %r)' % (self.__class__.__name__, self.num, self.name)

def init(L):
    global tests
    tests = L

def modify(i_t_nn):
    i, t, nn = i_t_nn
    t.num += random.normalvariate(mu=0, sigma=1) # modify private copy
    t.name = nn
    tests[i] = t # copy back
    return i

def main():
    num_processes = num = 10 #note: num_processes and num may differ
    manager = Manager()
    tests = manager.list([Tester(num=i) for i in range(num)])
    print(tests[:2])

    args = ((i, t, 'some') for i, t in enumerate(tests))
    pool = Pool(processes=num_processes, initializer=init, initargs=(tests,))
    for i in pool.imap_unordered(modify, args):
        print("done %d" % i)
    pool.close()
    pool.join()
    print(tests[:2])

if __name__ == '__main__':
    main()