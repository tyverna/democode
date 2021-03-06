#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import threading
import random
import datetime

import crc
import memorymapping
import concatenate
import devices


class MainThread(threading.Thread):
    def __init__(self):
        super().__init__()

        self.invgroup = []
        for id in range(1, 3):
            inv = devices.Inverter(id)
            print(inv)
            self.invgroup.append(inv)

        self.imeter = devices.DCBoxIlluMeter(11)
        self.tmeter = devices.DCBoxTempMeter(10)
            
        self.concatthread = concatenate.ConcatThread(self.invgroup, self.imeter, self.tmeter)


    def run(self):
        refresh_timestamp = time.time()
        self.concatthread.start()
        while True:
            now = time.time()
            if now - refresh_timestamp > 3:
                for inv in self.invgroup:
                    inv.refresh()

                self.imeter.refresh()
                self.tmeter.refresh()

                #dt = datetime.datetime.fromtimestamp(now)
                #print('Refresh at {}'.format(dt))
                refresh_timestamp = now


def main():
    print('PV Inverter simulator')
    mainthread = MainThread()
    mainthread.start()


if __name__ == '__main__':

    main()
