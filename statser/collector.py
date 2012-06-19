#!/usr/bin/python

import platform
import socket
import psutil
from time import time, sleep

class StatserPsutil:
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

    def collect_disk_io(self,whitelist=[]):
        """
        disks is a list of disk to be collected
        if disks is empty, collect all disk io stats

        TODO rewrite to avoid using private functions from psutil
        """
        stats=psutil.disk_io_counters(perdisk=True)
        for entry,stat in stats.iteritems():
            if not whitelist or entry in whitelist:
                for k,v in stat._asdict().iteritems():
                    self.add_data("disk-%s.%s"%(entry,k),v)

    def collect_network_io(self,whitelist=[]):
        """
        TODO refactor, as it is essentially copy-paste of disk_io
        """
        stats=psutil.network_io_counters(pernic=True)
        for entry,stat in stats.iteritems():
            if not whitelist or entry in whitelist:
                for k,v in stat._asdict().iteritems():
                    self.add_data("nic-%s.%s"%(entry.replace(" ","_"),k),v)
    def collect_cpu_times(self,whitelist=[]):
        """
        whitelist is a list of cpus to be used, must be integer
        """
        stats=psutil.cpu_times(percpu=True)
        for entry,stat in enumerate(stats):
            if not whitelist or entry in whitelist:
                for k,v in stat._asdict().iteritems():
                    self.add_data("cpu%d.%s"%(entry,k),v)
    def collect_phymem_usage(self):
        """
        TODO skip the percentage? it can be calculated by graphite, so...
        """
        stats = psutil.phymem_usage()
        for k,v in stats._asdict().iteritems():
            self.add_data("phymem.%s"%k,v)
    def collect_uptime(self):
        uptime = int(time()) - int(psutil.BOOT_TIME)
        self.add_data("uptime",uptime)

    def collect_virtmem_usage(self):
        """
        TODO skip the percentage? it can be calculated by graphite, so...
        """
        stats = psutil.virtmem_usage()
        for k,v in stats._asdict().iteritems():
            self.add_data("virtmem.%s"%k,v)

    def collect_disk_usage(self,whitelist=[]):
        """
        for free disk whitelist, both mountpoint (`/`) and device (`/dev/sda1`)
        is fine.
        Sys-fs will be ignored by default

        TODO implement the ability to get free Disk space for sysfs etc
        """
        for partition in psutil.disk_partitions():
            if not whitelist or partition.mountpoint in whitelist or partition.device in whitelist :
                usage = psutil.disk_usage(partition.mountpoint)
                if platform.system() == "Windows"  :
                  disk_name = "-"+partition.mountpoint.replace("\\","").replace(":","") 
                else:
                  disk_name= partition.mountpoint.replace("/","-")
                  if disk_name == "-":
                      disk_name="-root"
                self.add_data("df%s.total"%
                        disk_name, usage.total)
                self.add_data("df%s.used"%
                        disk_name, usage.used)
                self.add_data("df%s.free"%
                        disk_name, usage.free)
 
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

    def collect_all(self):
        """
        TODO automagically find functions for collector
        TODO add whitelisting feature in some cool way
        """
        self.collect_disk_io()
        self.collect_cpu_times()
        self.collect_uptime()
        self.collect_network_io()
        self.collect_phymem_usage()
        self.collect_virtmem_usage()
        self.collect_disk_usage()

if __name__ == "__main__":
    a = Statser(graphite_host="no_omo")
    #a.start()
    a.connect_graphite()
    #a.collect_disk_io(["sda2"])
    #a.collect_cpu_times([1])
    a.collect_all()
    #a.to_graphite()
    #print( a._write_graphite_msg(a.db))
    #print(a._write_graphite_msg(a.db))

