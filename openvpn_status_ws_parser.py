#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""File that contains OpenvpnStatusWsParser class."""


class OpenvpnStatusWsParser():
    log_path = None
    log_type = None
    raw_data = None

    def __init__(self, status_log_path):
        self.log_path = status_log_path
        self.fetch_raw_data()
        self.fetch_log_type()

    def fetch_raw_data(self):
        with open(self.log_path, 'r') as file_handle:
            self.raw_data = file_handle.read().strip()

    def fetch_log_type(self):
        pass

    @property
    def data(self):
        data = dict()
        data['raw_data'] = self.raw_data

        return data
