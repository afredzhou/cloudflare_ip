import ipaddress
import subprocess
import re
import time
import socket


def test_speed(ip, port=80, packet_size=1024, packet_count=10):
    """
    测试指定IP地址和端口上的网速（以每秒字节数为单位）
    """
    start_time = time.time()
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    total_sent = 0

    for _ in range(packet_count):
        packet = b'x' * packet_size  # 创建一个指定大小的数据包
        sent = sock.sendto(packet, (ip, port))
        total_sent += sent

    end_time = time.time()
    total_time = end_time - start_time
    speed = total_sent / total_time  # 计算网速（字节/秒）
    speed_MB = speed / 10 ** 6
    return speed_MB


# ipv4_network = ipaddress.IPv4Network("108.162.210.0/24", strict=False)
networks = [
    # ipaddress.IPv4Network("8.10.148.0/24", strict=False),
    # ipaddress.IPv4Network("173.245.48.0/20", strict=False),
    # ipaddress.IPv4Network("103.21.244.0/22", strict=False),
    # ipaddress.IPv4Network("103.22.200.0/22", strict=False),
    # ipaddress.IPv4Network("103.31.4.0/22", strict=False),
    # ipaddress.IPv4Network("141.101.64.0/18", strict=False),
    ipaddress.IPv4Network("108.162.192.0/18", strict=False),
    # ipaddress.IPv4Network("190.93.240.0/20", strict=False),
    # ipaddress.IPv4Network("188.114.96.0/20", strict=False),
    # ipaddress.IPv4Network("197.234.240.0/22", strict=False),
    # ipaddress.IPv4Network("198.41.128.0/17", strict=False),
    # ipaddress.IPv4Network("162.158.0.0/15", strict=False),
    # ipaddress.IPv4Network("104.16.0.0/130", strict=False),
    # ipaddress.IPv4Network("104.24.0.0/14", strict=False),
    # ipaddress.IPv4Network("172.64.0.0/13", strict=False),
    # ipaddress.IPv4Network("131.0.72.0/22", strict=False),



]
response_data = {}
for ipv4_network in networks:
    print(f"Scanning network: {ipv4_network}")
for ipv4_address in ipv4_network.hosts():
    ipv4_address_str = str(ipv4_address)
    try:
        result = subprocess.run(['ping', '-W', '1', '-c', '1', ipv4_address_str], capture_output=True, text=True)
        print(ipv4_address_str, result)

        if result.returncode == 0:
            # 打印 stdout 字段

            lines = result.stdout.split('\n')
            # print("lines:")
            for line in lines:
                # print(line)
                avg_match = re.search(r'(\d+\.\d{3})/\d+\.\d{3}/\d+\.\d{3}/\d+\.\d{3}\s*ms', line)
                if avg_match:
                    avg_value = avg_match.group(1)
                    # print("Average round-trip time:", avg_value)
                    ping_values = avg_value  # 将找到的平均值赋给 ping_values
        else:
            with open('notong.txt', 'a') as f:
                f.write(str(ipv4_address) + '\n')
            print(f"{ipv4_address_str} is unreachable.")
            continue
        download_speed = test_speed(ipv4_address_str, port=80, packet_size=1024, packet_count=10)
        response_data[ipv4_address_str] = (ping_values, download_speed,)
        print(
            f"Node: {ipv4_address_str}, Ping: {ping_values} ms, Download Speed: {download_speed:.2f} MB/s,")
        with open('iplist.txt', 'a') as f:
            f.write(f"Node: {ipv4_address_str}, Ping: {ping_values} ms, Download Speed: {download_speed:.2f} MB/s\n")

    except Exception as e:
        print(f"Error processing node {ipv4_address_str}: {e}")

if response_data:
    fastest_node = min(response_data, key=lambda x: response_data[x][2])
    print(
        f"The fastest node is: {fastest_node} with ping value of {response_data[fastest_node][0]} ms and speed of {response_data[fastest_node][2]:.2f} Mbps")
else:
    print("No valid nodes found.")
