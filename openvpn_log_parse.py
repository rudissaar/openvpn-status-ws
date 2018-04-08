#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def parse(log_path):
    with open(log_path, 'r') as log_handle:
        print(log_handle.read())
