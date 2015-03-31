#!/usr/bin/env python 
#-*- coding:utf-8 -*- 

import threading
import Queue
import time
import socket
import logging
import urllib2

from optparse import OptionParser

class MyThread(threading.Thread):
    def __init__(self, work_queue):
        threading.Thread.__init__(self)
        self.work_queue = work_queue
        self.start()

    def run(self):
        while True:
            try:
                do, args = self.work_queue.get(block=False)
                do(args)
            except:
                break


class threadpool(object):
    def __init__(self, thread_nums , ip_list, port_list):
        self.thread_nums = thread_nums
        self.ip_list = ip_list
        self.port_list = port_list
        self.threads = []
        self.work_queue = Queue.Queue()

        self.__init_work_queue()
        self.__init_thread_pool()

    def __init_thread_pool(self):
        for x in xrange(self.thread_nums):
            self.threads.append(MyThread(self.work_queue))

    def __init_work_queue(self):
        for ip in self.ip_list:
            for port in self.port_list:
                self.add_job(do_job, (ip, port ))

    def wait_thread_complete(self):
        for thread in self.threads:
            if thread.isAlive():
                thread.join()

    def add_job(self, func, *argv):
        self.work_queue.put((do_job, list(argv)))

logger = logging.getLogger('PortScan')
logger.setLevel(logging.DEBUG)
hd = logging.StreamHandler()
formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
hd.setFormatter(formatter)
logger.addHandler(hd)


scan_store_result = []

def http_banner(ip, port):
    u = urllib2.urlopen('http://%s:%d' % (ip, port))
    #print u.info()['Server'].split()
    if len(u.info()['Server'].split()) == 2:
        _service, _os = u.info()['Server'].split()
        _os = _os.strip('()')
        logger.warning('%s, %s' % (_service, _os))
        return u.info()['Server']
    if len(u.info()['Server'].split()) == 1:
        _service = u.info()['Server']
        logger.warning('%s' % (_service))
        return u.info()['Server']
    if len(u.info()['Server'].split()) == 3:
        _service, _os, x = u.info()['Server'].split()
        _os = _os.strip('()')
        logger.warning('IP:%s Port: %d %s %s' % (ip, port, _service, _os))
        return u.info()['Server']

def do_job(argv):
    args_tuple = argv[0]
    time.sleep(0.1)
    ip = args_tuple[0]
    port = int(args_tuple[1])
    if 80 == port:
        banner = http_banner(ip, port)
        scan_store_result.append ({"ip":ip, "port": port, "banner": banner})
        return

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)
    #logger.info('Scan IP %s, port %d' % (ip, port))
    try:
        sock.connect((ip, int(port)))
        sock.send('/GET')
        banner = sock.recv(1024)
        logger.warning('Server %s port %d : \n%s' % (ip, port))
        scan_store_result.append({"ip":ip, "port": port, "banner": banner})
    except Exception, e:
        logger.error('Server %s port %d is not connected' % (ip, port))
        pass
    sock.close()

def ip2num(ip):
    ip = [int(x) for x in ip.split('.')]
    return ip[0] << 24 | ip[1] << 16 | ip[2] << 8 | ip[3]

def num2ip(num):
    return '%s.%s.%s.%s' % ( (num & 0xff000000) >> 24,
                             (num & 0x00ff0000) >> 16,
                             (num & 0x0000ff00) >> 8,
                             num & 0x000000ff )

def main():
    opt_parse = OptionParser(usage="usage: %prog [options] host")
    opt_parse.add_option('-p', '--port',
                         action='store',
                         type='string',)

    opt_parse.add_option('-t', '--threads',
                         action='store',
                         type='int',
                         default=20)

    (options, args) = opt_parse.parse_args()
    if len(args) != 1:
        opt_parse.error('Please input host')
    if not options.port:
        port_list = [port for port in xrange(65535)]
    else:
        port_list = filter(None, options.port.split(','))

    thread_num = options.threads
    ips = args[0].split('-')
    iplist = ips
    if len(ips) == 2:
        start = ip2num(ips[0])
        end = ips[0].split('.')
        end[3] = ips[1]
        end = ip2num('.'.join(end))
        #print start,end
        iplist = [num2ip(num) for num in range(start, end+1) if num & 0xff]

    logger.info('PortScan starting...')

    t = threadpool(thread_num, iplist, port_list)
    t.wait_thread_complete()
    logger.info('PortScan complete...')
    print scan_store_result

if __name__ == '__main__':
    main()