#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def parse_status_log(status_log_path):
    with open(status_log_path, 'r') as file_handle:
        print(file_handle.read())
