#!/usr/bin/python

import platform
import socket
import psutil

class Statser:
    def __init__(self,prefix="retiolum."+platform.node(),graphite_host="localhost",graphite_port="2003",retry_limit=-1):
        """
        default prefix is `hostname`
        default retry_limit is unlimited
        """
        self.msg = ""
        self.prefix = prefix
        self.host=graphite_host
        self.port=graphite_port
        self.retry_limit=retry_limit
        #self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.sock.connect((host,port))

    def add_data(self,name,data):
        from time import time
        line = "%s.%s %s %s\n" %(self.prefix,name,data,int(time()))
        self.msg=self.msg + line
    def collect_iostat(self,disks=[]):
        """
        disks is a list of disk to be collected
        if disks is empty, collect all disk io stats
        """
        stats=psutil.disk_io_counters(perdisk=True)
        for disk,stat in stats.iteritems():
            # TODO rewrite to avoid using private functions
            if not disks or disk in disks:
                for k,v in stat._asdict().iteritems():
                    self.add_data("disk-%s.%s"%(disk,k),v)


    def to_graphite(self):
        tries = 0
        while self.msg is "" or not tries == self.retry_limit:
            try:
                self.sock.send(self.msg)
            except: 
                print("Cannot send message, reconnecting...")
                try:
                    self.sock.connect((self.host,self.port))
                except:
                    print("Cannot connect to host, retrying (%d/%d)"
                            %(tries,RETRY_LIMIT))
                    tries+=1
            else:
                self.msg=""

if __name__ == "__main__":
    a = Statser()
    a.collect_iostat(["sda2"])
    print a.msg
