from pygraphviz import AGraph

ip_dict = {}  # maps source-destination IP pairs to their number of occurrences

trace_path = '/var/log/syslog'
trace_file = open(trace_path, newline='')

for line in trace_file.readlines():
    split_line = line.split('|')

    if len(split_line) == 4:
        src_dst_pair = (split_line[1], split_line[2])

        if src_dst_pair in ip_dict.keys():
            ip_dict[src_dst_pair] = ip_dict[src_dst_pair] + 1
        else:
            ip_dict[src_dst_pair] = 1

ip_graph = AGraph(directed=True)

for (src_ip, dst_ip), packet_count in ip_dict.items():
    ip_graph.add_edge(
        src_ip, dst_ip, color='brown', label=packet_count, labelangle=45, len=1.75)

ip_graph.layout()

ip_graph.draw('graph.png')