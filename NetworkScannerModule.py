import scapy.all as scapy
import argparse
import BasicScannerModule
import FTPmodule
import time
import json
import HTTPmodule


def network_scan_func(_network):
    _network.print_network_scanning_information()


def port_func(_ip, _port):
    print("IP: " + _ip)
    targetIp = BasicScannerModule.PortScanFunc(_ip)
    targetIp.ip_ports_scan([_port])
    targetIp.port_status_print()


def default_ports_func(_ip):
    print("IP: " + _ip)
    default_ports_list = BasicScannerModule.default_ports
    targetIp = BasicScannerModule.PortScanFunc(_ip)
    targetIp.ip_ports_scan(default_ports_list)
    targetIp.port_status_print()


def full_tcp_func(_network, details_mode):
    data_base = {}
    ip_data = {}
    print(_network)
    for ip in _network:
        print(ip["ip"])

        single_ip_ports = []
        ports_data = {}

        default_ports_list = BasicScannerModule.default_ports
        targetIp = BasicScannerModule.PortScanFunc(ip["ip"])
        targetIp.ip_ports_scan(default_ports_list)

        for elem in targetIp.ports_banners.keys():
            info = {"port_info": "Banner: " + targetIp.ports_banners[elem], "danger_level": "High risk"}
            port_info = {elem: info}
            single_ip_ports.append(port_info)
            print(port_info)

        for elem in targetIp.ports_services.keys():
            info = {"port_info": "Service: " + targetIp.ports_services[elem], "danger_level": "Medium risk"}
            port_info = {elem: info}
            single_ip_ports.append(port_info)
            print(port_info)

        if not details_mode:
            ports_data["ports"] = single_ip_ports

            if len(ports_data["ports"]) == 0:
                ip_data[ip["ip"]] = "No open ports"
            else:
                ip_data[ip["ip"]] = ports_data

        else:
            for elem in targetIp.closed_ports.keys():
                info = {"danger_level": "low risk"}
                port_info = {elem: info}
                single_ip_ports.append(port_info)
                print(port_info)

            ports_data["ports"] = single_ip_ports
            ip_data[ip["ip"]] = ports_data

    data_base["ip"] = ip_data
    """print(data_base)"""
    with open("full_tcp.json", "w") as file:
        json.dump(data_base, file, indent=3)


def http_scan(ip):
    target = HTTPmodule.httpModule(ip)
    target.unitScan()
    target.getMassage()
    target.toJson()
    print(f"HTTP Module")
    print(f"HOST: {ip}")
    print(f"Status: {target.status}")
    print(f"Banner: {target.banner}")


def auth_ftp(ip, login, password):
    target = FTPmodule.ftpModule(ip, login, password)
    print(f"HTTP Module")
    print(f"HOST: {target.host_ip}")
    print(f"PORT: {target.port}/tcp")
    print("FTP login with authentication")
    print("---------------------------------------------")
    target.getFtpBanner()
    target.authLogin()
    print("---------------------------------------------")
    print(f"Banner: {target.banner}")
    print("---------------------------------------------")
    print()
    target.toJson()


def anon_ftp(ip):
    target = FTPmodule.ftpModule(ip)
    print(f"HTTP Module")
    print(f"HOST: {target.host_ip}")
    print(f"PORT: {target.port}/tcp")
    print("Anonymous FTP login")
    print("---------------------------------------------")
    target.getFtpBanner()
    target.anonLogin()
    print("---------------------------------------------")
    print(f"Banner: {target.banner}")
    print("---------------------------------------------")
    print()
    target.toJson()
