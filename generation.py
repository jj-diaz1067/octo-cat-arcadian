__author__ = 'JuanJose'

import datetime
import time
import threading
import copy
import configparser
class OctoCat:

    def __init__(self):
        full = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
                'S', 'T', 'U', 'V', 'X', 'Y', 'Z',
                'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r'
                's', 't', 'u', 'v', 'x', 'y', 'z'
                '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
        my = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
              'S', 'T', 'U', 'V', 'X', 'Y', 'Z']
        mn = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
              's', 't', 'u', 'v', 'x', 'y', 'z']
        nm = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']

        self.dist = []
        self.iterations = [0]
        self.finish = [0]
        self.threads = []
        self.words = {}
        self.lock = threading.Lock()
        self.time = [0]
        self.section = ''
        for i in range(0, 8):
            self.dist.append([])

        self.dist[0] = my
        self.dist[1] = mn
        self.dist[2] = mn
        self.dist[3] = mn
        self.dist[4] = mn
        self.dist[5] = mn
        self.dist[6] = mn
        self.dist[7] = nm
        self.time[0] = datetime.datetime.now()

        cases = 1

        for k in self.dist:
            cases *= len(k)

        print 'the number of cases are: ', cases

    def gen(self):
        current_time = datetime.datetime.now()
        print 'Generating: '
        for i in self.dist[0]:
            for j in self.dist[1]:
                n = ''.join([i, j])
                n_word = copy.deepcopy(n)
                t = Worker()
                t = Worker(target=self.rec, name=n_word, index=2, word=n_word, thread=t)
                self.words[n_word] = n_word
                self.threads.append(t)
                t.start()
        print 'Done --  it took: ', datetime.datetime.now() - current_time

    def rec(self, index, word, name):
        if len(word) == 8:
            self.found(word)
        if self.finish[0] == 0:
            # Add other letter
            if index < len(self.dist):
                for j in self.dist[index]:
                    n = ''.join([word, j])
                    n_word = copy.deepcopy(n)
                    self.words[name] = n_word
                    self.rec(index+1, n_word, name)

    def found(self, word):
        # lock.acquire()
        # self.iterations[0] += 1
        # if self.iterations[0] % 1000000 == 0:
        #    print self.iterations[0] / 1000000, 'M'
        # lock.release()
        if word == 'Megaman5':
            self.finish[0] = 1
            print 'found it'
            print 'iteration: ', self.iterations[0]
            time2 = datetime.datetime.now() - self.time[0]
            print 'Completion time: ', time2

class Worker(threading.Thread):
    def __init__(self, target=None, index=None, word=None, name=None, thread=None):
        threading.Thread.__init__(self, target=target, args=(index, word, name), name=name)
        self.name = name
        self.word = word

    def new_word(self, word):
        self.word = word

obj = OctoCat()
obj.gen()
time1 = datetime.datetime.now() - obj.time[0]
print 'First Thread time: ', time1

def printing():
    config = configparser.RawConfigParser()
    config.add_section('data')
    for t in obj.words.keys():
        # print t.word[0]+t.word[1], ' = ', t.word
        # print t.word[0:2], ' = ', t.word
        config.set('data', t, obj.words[t])
    config_file = open('octoConfig.ini', 'wb')
    config.write(config_file)
    config_file.close()

# threading.Thread(target=printing)
while obj.finish[0] == 0:
    printing_date = datetime.datetime.now()
    print 'Printing -- time: ', printing_date - obj.time[0]
    printing()
    print 'Printing -- done, it took: ', datetime.datetime.now() - printing_date
    time.sleep(60)
