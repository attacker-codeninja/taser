import threading
from os import path
from time import sleep
from datetime import datetime, timedelta

class TaserTimeout(threading.Thread):
    '''
    Time class to send shutdown signal on max timeout
    or when self.running = False.
    '''
    def __init__(self, timeout):
        threading.Thread.__init__(self)
        self.timeout = timeout
        self.start_time = datetime.now()
        self.running = True

    def run(self):
        while self.running:
            if (datetime.now() - self.start_time) > timedelta(seconds=self.timeout):
                self.stop()
            sleep(0.05)

    def stop(self):
        self.running = False


def read_file_lines(file):
    return [line.strip() for line in open(file)]

def file_exists(parser, filename, contents=True):
    # Argparse support for accepting file
    if not path.exists(filename):
        parser.error("Input file not found: {}".format(filename))
    if contents:
        return read_file_lines(filename)
    else:
        return filename

def delimiter2list(value, delimiter=","):
    return (value).split(delimiter) if value else []

def delimiter2dict(value, delimiter1=";", delimiter2="="):
    x = {}
    for item in value.split(delimiter1):
        if item:
            k,v = item.split(delimiter2)
            x[k] = v
    return x

def ranger(size_input):
    '''
    Takes comma seperated or range of number inputs and
    returns a single list to iterate over.
    '''
    t = []
    for x in delimiter2list(size_input):
        if "-" in x:
            t += [y for y in range(int(x.split('-')[0]), int(x.split('-')[1])+1)]
        else:
            t.append(int(x))
    return t

