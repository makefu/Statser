#!/usr/bin/python

import platform
import socket
import psutil
from time import time

class Statser:
    def __init__(self,prefix="retiolum."+platform.node(),graphite_host="localhost",graphite_port=2003,retry_limit=3):
        """
        default prefix is `hostname`
        default retry_limit is unlimited
        """
        self.db = []
        self.prefix = prefix
        self.graphite_host=graphite_host
        self.graphite_port=graphite_port
        self.retry_limit=retry_limit


    def add_data(self,name,data):
        """
        appends data to the current database to be written.

        this database needs to be cleared after every `to_x` command

        """
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

    def connect_graphite(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.graphite_host,self.graphite_port))

    def _write_graphite_msg(self,db):
        """
        db is the object to be written into the buffer
        """
        msg = ""
        for e in db:
            line = "%s.%s %s %s\r\n" %(self.prefix,e["name"],e["data"],e["time"])
            msg=msg + line
        return msg
        
    def to_graphite(self):
        """
        write the collected entries to the graphite server
        """
        msg = self._write_graphite_msg(self.db)
        tries = 0
        while msg and tries < self.retry_limit:
            try:
                l = self.sock.send(msg)
                msg = msg[l:]
            except: 
                print("Cannot send message, reconnecting...")
                try:
                    self.sock.connect((self.graphite_host,self.graphite_port))
                except:
                    print("Cannot connect to host, retrying (%d/%d)"
                            %(tries,self.retry_limit))
                    tries+=1
    def clean_db(self):
        """
        reset the database, needs to be done after every to_x
        """
        del (self.db)
        self.db = []

if __name__ == "__main__":
    a = Statser(prefix="balls",graphite_host="no_omo")
    a.connect_graphite()
    a.collect_iostat(["sda2"])
    a.to_graphite()
    print( a._write_graphite_msg(a.db))
    a.clean_db()
    a.collect_iostat()
    print(a._write_graphite_msg(a.db))
