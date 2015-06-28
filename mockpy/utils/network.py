#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import subprocess
import os
import re
import atexit
from .config import *


class NetworkConfig(object):

    def __init__(self, port):
        self.port = str(port)
        self.proxy_settings = {}

        self.previous_port = ""
        self.previous_proxy_settings = {}

        self.previous_http_proxy = ()
        self.previous_https_proxy = ()

    def apply(self):
        self.previous_proxy_settings = get_proxy_settings()

        self.previous_http_proxy = self.get_previous_proxy("http")
        self.previous_https_proxy = self.get_previous_proxy("https")

        self.proxy_settings = self.update_proxy_settings()

        apply_proxy_settings(self.proxy_settings)

        self.log_old_proxy_if_needed()

        restore_on_exit(self.previous_proxy_settings)

    def update_proxy_settings(self):
        new_settings = {}
        dict = {"http": ("127.0.0.1", self.port, True), "https": ("127.0.0.1", self.port, True)}
        for network_name in self.previous_proxy_settings.keys():
            new_settings[network_name] = dict

        return new_settings

    def get_previous_proxy(self, proxy_type):
        try:
            first_network = self.previous_proxy_settings.keys()[0]
            ip, port, enabled = self.previous_proxy_settings[first_network][proxy_type]
            if (port == self.port and ip == "127.0.0.1") or not enabled:
                return None

            return ip, port, enabled
        except Exception as ex:
            error(str(ex))
            return None

    def log_old_proxy_if_needed(self):
        self.log_proxy(self.previous_http_proxy, "HTTP")
        self.log_proxy(self.previous_http_proxy, "HTTPS")

    @staticmethod
    def log_proxy(proxy, title):
        if proxy is None:
            return

        info("Saving old %s proxy settings %s:%s" % (title, proxy[0], proxy[1]))


"""
    Getting the network settings
"""


def get_proxy_settings():
        networks = get_networks()
        dict = {}
        for network in networks:
            http = get_web_proxy(network)
            https = get_web_proxy(network, secure=True)
            dict[network] = {"http": http, "https": https}

        return dict


def get_networks():
    networks = os.popen("networksetup -listallnetworkservices").read().split("\n")
    return filter(is_valid_network, networks)


def is_valid_network(network_name):
    cmd = "networksetup -getinfo '{0}'".format(network_name)
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    ret_val = p.wait()
    return ret_val == 0


def get_web_proxy(network_name, secure=False):
    proxy = ["-getwebproxy", "-getsecurewebproxy"][secure]
    cmd = "networksetup {0} '{1}'".format(proxy, network_name)

    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    lines = p.stdout.read()
    server, port, enabled = "", "", True

    for line in lines.split("\n"):
        capture = re.match("Server:(.*)", line)
        if capture:
            server = capture.group(1).strip()

        capture = re.match("Port:(.*)", line)
        if capture:
            port = capture.group(1).strip()

        capture = re.match("Enabled:(.*)", line)
        if capture:
            enabled = capture.group(1).strip() == "Yes"

    return server, port, enabled


"""
    Changing proxy settings
"""


def apply_proxy_settings(settings):
    try:
        for network_name in settings.keys():
            set_proxy(network_name, settings[network_name])
            set_proxy(network_name, settings[network_name], secure=True)
    except KeyboardInterrupt:
        error("Exiting...")
        exit(0)


def set_proxy(network_name, values, secure=False):
    proxy = ["-setwebproxy", "-setsecurewebproxy"][secure]
    key = ["http", "https"][secure]
    server, port, enabled = values[key]

    cmd = "sudo networksetup {0} '{1}' {2} {3}".format(proxy, network_name, server, port)

    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    p.wait()

    if not enabled:
        turn_off_proxy_for_network(network_name, secure)


def turn_off_proxy_for_network(network_name, secure=False):
    proxy = ["-setwebproxystate", "-setsecurewebproxystate"][secure]
    cmd = "sudo networksetup {0} '{1}' off".format(proxy, network_name)
    subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).wait()


"""
    Restore old settings on exit
"""


def restore_on_exit(proxy_settings):
    def exit_handler():
        print("Restoring network proxy")
        warn("Note: sudo password may be asked to restore previous network http/https proxies\n")
        apply_proxy_settings(proxy_settings)

    atexit.register(exit_handler)
