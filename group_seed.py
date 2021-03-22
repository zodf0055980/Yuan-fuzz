import sys
import glob
import os
import matplotlib.pyplot as plt
import numpy as np
import subprocess
from collections import Counter
from sklearn import cluster, metrics
import socket
import signal

kmeans_group = 0
seed_group = []


def signal_handler(sig, frame):
    for i in range(kmeans_group):
        seed_group[i] = sorted(
            seed_group[i], key=lambda k: (k['fuzzcount'], k['skip']))
        print(f"group {i} : {seed_group[i]}")
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)
HOST = '127.0.0.1'
PORT = int(sys.argv[1])
print(f"[*] port = {PORT}")
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen(1)
conn, addr = sock.accept()
dirpath = conn.recv(250).decode("utf-8")
print(f"[*] dirpath = {dirpath}")

init_seed_count = int(conn.recv(8))
print(f"[*] init_seed_count = {init_seed_count}")

seed_list = [os.path.basename(x) for x in glob.glob(dirpath+'/queue/id*')]
seed_list.sort()

# initial seed group
kmeans_group = int(len(seed_list) ** 0.5)
print(f"[*] kmeans_group = {kmeans_group}")
for i in range(kmeans_group):
    seed_group.append([])

# obtain raw bitmaps
raw_bitmap = {}
tmp_cnt = []
out = ''

for filename in seed_list:
    f = open(dirpath+'/queue_info/queue/' + filename, 'r')
    argv = f.readline().split()
    argv_file_padding = 0
    for argv_search in argv:
        if argv_search.find('.cur_input') >= 0:
            argv[argv_file_padding] = dirpath+'/queue/' + filename
            break
        argv_file_padding = argv_file_padding + 1
    print(argv)
    tmp_list = []
    try:
        out = subprocess.check_output(
            ['./afl-showmap', '-q', '-e', '-o', '/dev/stdout', '-m', 'none', '-t', '500'] + argv)
    except subprocess.CalledProcessError:
        print("find a crash")
    for line in out.splitlines():
        edge = line.split(b':')[0]
        tmp_cnt.append(edge)
        tmp_list.append(edge)
    raw_bitmap[filename] = tmp_list
counter = Counter(tmp_cnt).most_common()

# save bitmaps to individual numpy label
label = [int(f[0]) for f in counter]
bitmap = np.zeros((len(seed_list), len(label)))
for idx, i in enumerate(seed_list):
    tmp = raw_bitmap[i]
    for j in tmp:
        if int(j) in label:
            bitmap[idx][label.index((int(j)))] = 1

fit_bitmap, indices = np.unique(bitmap, return_index=True, axis=1)
new_label = [label[f] for f in indices]

kmeans_fit = cluster.KMeans(n_clusters=kmeans_group).fit(fit_bitmap)

cluster_labels = kmeans_fit.labels_
print("[*] cluster_labels")
print(cluster_labels)
print("[*] show group")
for i in range(0, init_seed_count):
    seed_group[cluster_labels[i]].append({"id": i, "skip": 0, "fuzzcount": 1})
for i in range(init_seed_count, len(cluster_labels)):
    seed_group[cluster_labels[i]].append({"id": i, "skip": 0, "fuzzcount": 0})
for i in range(kmeans_group):
    seed_group[i] = sorted(seed_group[i], key=lambda k: k['fuzzcount'])
    print(f"group {i} : {', '.join(str(x['id'])for x in seed_group[i]) }")

print(f"[*] run rarget = {seed_group[0][0]['id']}")
conn.sendall(str(seed_group[0][0]['id']).encode(encoding="utf-8"))
run_group = 0
seed_count = len(cluster_labels)
re_group = seed_count + (seed_count // 2)
max_skip = 2
skip = max_skip
regroup = 0
while(1):
    require = conn.recv(5)
    print(f"[*] get {require}")

    # get current find path
    seed_list = [os.path.basename(x) for x in glob.glob(dirpath+'/queue/id*')]
    seed_list.sort()
    # regroup
    if(len(seed_list) > re_group):
        regroup = 1
        seed_group[run_group][0]['fuzzcount'] = seed_group[run_group][0]['fuzzcount'] + 1
        print(f"[*] re group")
        # update
        all_seed = []
        print(f"old group")
        for i in range(kmeans_group):
            print(f"group {i} : {seed_group[i]}")
            for s in seed_group[i]:
                all_seed.append(s)
        for i in range(seed_count, len(seed_list)):
            all_seed.append({"id": i, "skip": 0, "fuzzcount": 0})
        all_seed = sorted(all_seed, key=lambda k: k['id'])
        print(all_seed)

        seed_count = len(seed_list)
        re_group = seed_count + (seed_count // 2)

        raw_bitmap = {}
        tmp_cnt = []
        out = ''

        for filename in seed_list:
            f = open(dirpath+'/queue_info/queue/' + filename, 'r')
            argv = f.readline().split()
            argv_file_padding = 0
            for argv_search in argv:
                if argv_search.find('.cur_input') >= 0:
                    argv[argv_file_padding] = dirpath+'/queue/' + filename
                    break
                argv_file_padding = argv_file_padding + 1
            print(argv)
            tmp_list = []
            try:
                out = subprocess.check_output(
                    ['./afl-showmap', '-q', '-e', '-o', '/dev/stdout', '-m', 'none', '-t', '500'] + argv)
            except subprocess.CalledProcessError:
                print("This is a crash file")
            for line in out.splitlines():
                edge = line.split(b':')[0]
                tmp_cnt.append(edge)
                tmp_list.append(edge)
            raw_bitmap[filename] = tmp_list
        counter = Counter(tmp_cnt).most_common()

        # save bitmaps to individual numpy label
        label = [int(f[0]) for f in counter]
        bitmap = np.zeros((len(seed_list), len(label)))
        for idx, i in enumerate(seed_list):
            tmp = raw_bitmap[i]
            for j in tmp:
                if int(j) in label:
                    bitmap[idx][label.index((int(j)))] = 1

        fit_bitmap, indices = np.unique(
            bitmap, return_index=True, axis=1)
        new_label = [label[f] for f in indices]

        kmeans_group = int(len(seed_list) ** 0.5)
        print(f"[*] kmeans_group = {kmeans_group}")

        kmeans_fit = cluster.KMeans(
            n_clusters=kmeans_group).fit(fit_bitmap)

        cluster_labels = kmeans_fit.labels_
        print("[*] new cluster_labels")
        print(cluster_labels)

        # initial seed group
        seed_group = []
        for i in range(kmeans_group):
            seed_group.append([])

        for i in range(0, len(cluster_labels)):
            seed_group[cluster_labels[i]].append(all_seed[i])
        print("[*] show new group")
        for i in range(kmeans_group):
            seed_group[i] = sorted(
                seed_group[i], key=lambda k: (k['fuzzcount'], k['skip']), reverse=False)
            print(
                f"group {i} : {', '.join(str(x['id'])for x in seed_group[i]) }")
    # have new path, but maybe find from argv, so predict first.
    elif(seed_count < len(seed_list)):
        # predict
        print(f"[*] find new path {seed_count} to {len(seed_list)-1}")
        predic = []
        for i in range(seed_count, len(seed_list)):
            f = open(dirpath+'/queue_info/queue/' + seed_list[i], 'r')
            argv = f.readline().split()
            argv_file_padding = 0
            for argv_search in argv:
                if argv_search.find('.cur_input') >= 0:
                    argv[argv_file_padding] = dirpath+'/queue/' + seed_list[i]
                    break
                argv_file_padding = argv_file_padding + 1
            # print(argv)
            try:
                out = subprocess.check_output(
                    ['./afl-showmap', '-q', '-e', '-o', '/dev/stdout', '-m', 'none', '-t', '500'] + argv)
            except subprocess.CalledProcessError:
                print("find crash !!")
            tmp_list = []
            for line in out.splitlines():
                edge = line.split(b':')[0]
                tmp_list.append(edge)
            predict_bitmap = [int(i) for i in tmp_list]
            predicrt_label = []
            for i in new_label:
                if i in predict_bitmap:
                    predicrt_label.append(1)
                else:
                    predicrt_label.append(0)
            predic.append(predicrt_label)
        predict_list = kmeans_fit.predict(predic)

        for i in range(len(predict_list)):
            seed_group[predict_list[i]].append(
                {"id": seed_count + i, "skip": 0, "fuzzcount": 0})
            print(f"add {seed_count + i} in group {predict_list[i]}")
        # update seed count
        seed_count = len(seed_list)

    # find new path in fuzz_one
    if(require == b'next'):
        if (regroup == 1):
            run_group = 0
            print(f"[*] run rarget = {seed_group[0][0]['id']}")
            conn.sendall(str(seed_group[0][0]['id']).encode(encoding="utf-8"))
        else:
            seed_group[run_group][0]['fuzzcount'] = seed_group[run_group][0]['fuzzcount'] + 1
            # sort first
            seed_group[run_group] = sorted(
                seed_group[run_group], key=lambda k: (k['fuzzcount'], k['skip']), reverse=False)
            # send next seed
            conn.sendall(str(seed_group[run_group]
                             [0]['id']).encode(encoding="utf-8"))

    elif(require == b'notf'):
        # no new path
        seed_group[run_group][0]['fuzzcount'] = seed_group[run_group][0]['fuzzcount'] + 1
        # sort first
        seed_group[run_group] = sorted(
            seed_group[run_group], key=lambda k: (k['fuzzcount'], k['skip']), reverse=False)
        # run next group
        run_group = (run_group + 1) % kmeans_group
        # prevent seed_group is null
        while not seed_group[run_group]:
            run_group = (run_group + 1) % kmeans_group
        seed_group[run_group] = sorted(
            seed_group[run_group], key=lambda k: (k['fuzzcount'], k['skip']), reverse=False)
        conn.sendall(str(seed_group[run_group][0]
                         ['id']).encode(encoding="utf-8"))
        # fuzz count ++
        print(f"[*] next group {run_group}")
        print(f"[*] run target = {seed_group[run_group][0]['id']}")

    elif(require == b'skip'):
        seed_group[run_group][0]['skip'] = seed_group[run_group][0]['skip'] + 1
        if(skip == 0):
            # run bext group and reset skip
            skip = max_skip
            run_group = (run_group + 1) % kmeans_group
            while not seed_group[run_group]:
                run_group = (run_group + 1) % kmeans_group
            seed_group[run_group] = sorted(
                seed_group[run_group], key=lambda k: (k['fuzzcount'], k['skip']), reverse=False)
            conn.sendall(str(seed_group[run_group][0]
                             ['id']).encode(encoding="utf-8"))
            print(f"[*] next group {run_group}")
            print(f"[*] run target = {seed_group[run_group][0]['id']}")
        else:
            skip = skip - 1
            seed_group[run_group] = sorted(
                seed_group[run_group], key=lambda k: (k['fuzzcount'], k['skip']), reverse=False)
            # this group is fuzz already
            if(seed_group[run_group][0]['skip'] > 0 or seed_group[run_group][0]['fuzzcount'] > 0):
                print(f"[*] group {run_group} is all skip or been fuzz")
                run_group = (run_group + 1) % kmeans_group
                while not seed_group[run_group]:
                    run_group = (run_group + 1) % kmeans_group
            conn.sendall(str(seed_group[run_group][0]
                             ['id']).encode(encoding="utf-8"))
            print(f"[*] run target = {seed_group[run_group][0]['id']}")
