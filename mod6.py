import os
import argparse
import requests
import json


def do_ping_sweep(ip, num_of_host, op_sys):
    ip_parts = ip.split('.')
    network_ip = ip_parts[0] + '.' + ip_parts[1] + '.' + ip_parts[2] + '.'
    scanned_ip = network_ip + str(int(ip_parts[3]) + num_of_host)
    if op_sys == 'w':
        response = os.popen(f'ping -n 1 -w 2000 {scanned_ip}')
    elif op_sys == 'l':
        response = os.popen(f'ping -n 1 -c 1 -w 2 {scanned_ip}')
    res = response.readlines()
    print()
    if op_sys == 'w':
        print(f"[#] Result of scanning: {scanned_ip} [#]\n{res[2].encode('cp1251').decode('cp866')}", end='\n\n')
    elif op_sys == 'l':
        lost_pack = res[3].split(',')
        print(f"[#] Result of scanning: {scanned_ip} [#]\n{res[2]}{lost_pack[2]}", end='\n\n')


def sent_http_request(target, method, headers=None, payload=None):
    headers_dict = dict()
    if headers:
        for header in headers:
            header_name = header.split(':')[0]
            header_value = header.split(':')[1:]
            headers_dict[header_name] = ':'.join(header_value)
    if method == "GET":
        response = requests.get(target, headers=headers_dict)
    elif method == "POST":
        response = requests.post(target, headers=headers_dict, data=payload)
    print(
        f"[#] Response status code: {response.status_code}\n"
        f"[#] Response headers: {json.dumps(dict(response.headers), indent=4, sort_keys=True)}\n"
        f"[#] Response content:\n {response.text}"
    )


parser = argparse.ArgumentParser(description='Network scanner')

parser.add_argument('task', choices=['scan', 'send_http'], help='Network scan or send HTTP request')
parser.add_argument('-os', type=str, help='Group of system: Windows(w) or Linux(l)')
parser.add_argument('-i', '--ip', type=str, help='IP address')
parser.add_argument('-n', '--num_of_hosts', type=int, help='Number of hosts')
parser.add_argument('-t', '--target', type=str, help='target for sending an HTTP request')
parser.add_argument('-m', '--method', choices=['GET', 'POST'], help='type of request method: POST or GET')
parser.add_argument('-hd', '--headers', nargs='*', type=str, help='Request headers')
parser.add_argument('-p', '--payload', type=str, help='Payload data')

args = parser.parse_args()

if args.task == 'scan':
    for host_num in range(args.num_of_hosts):
        do_ping_sweep(args.ip, host_num, args.os)
elif args.task == 'send_http':
    sent_http_request(args.target, args.method, args.headers, args.payload)
