#!/usr/bin/python

import platform
import socket
import psutil
from time import time

class Statser:
    def __init__(self,prefix="retiolum."+platform.node(),graphite_host="localhost",graphite_port="2003",retry_limit=-1):
        """
        default prefix is `hostname`
        default retry_limit is unlimited
        """
        self.db = []
        self.prefix = prefix
        self.graphite_host=graphite_host
        self.graphite_port=graphite_port
        self.retry_limit=retry_limit
        #self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.sock.connect((host,port))

    def add_data(self,name,data):
        self.db.append({"name":name,"data":data,"time":int(time())})

    def collect_iostat(self,disks=[]):
        """
        disks is a list of disk to be collected
        if disks is empty, collect all disk io stats
        """
        stats=psutil.disk_io_counters(perdisk=True)
        for disk,stat in stats.iteritems():
            if not disks or disk in disks:
                # TODO rewrite to avoid using private functions
                for k,v in stat._asdict().iteritems():
                    self.add_data("disk-%s.%s"%(disk,k),v)

    def _write_graphite_msg(self,db):
        """
        db is the object to be written into the buffer
        """
        msg = ""
        for e in db:
            line = "%s.%s %s %s\n" %(self.prefix,e["name"],e["data"],e["time"])
            msg=msg + line
        return msg
        
    def to_graphite(self):
        """
        write the collected entries to the graphite server
        """
        msg = self._write_graphite_msg(db)
        tries = 0
        while msg is "" or not tries == self.retry_limit:
            try:
                self.sock.send(msg)
            except: 
                print("Cannot send message, reconnecting...")
                try:
                    self.sock.connect((self.graphite_host,self.graphite_port))
                except:
                    print("Cannot connect to host, retrying (%d/%d)"
                            %(tries,RETRY_LIMIT))
                    tries+=1
            else:
                msg=""
    def clean_db(self):
        """
        reset the database
        """
        del (self.db)
        self.db = []

if __name__ == "__main__":
    a = Statser()
    a.collect_iostat(["sda2"])
    print( a._write_graphite_msg(a.db))
    a.clean_db()
    a.collect_iostat()
    print(a._write_graphite_msg(a.db))
