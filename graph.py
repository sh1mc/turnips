import numpy
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import datetime
import json
import os

# x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
# y = [97, 80, 78, 72, 68, 65, 60, 102, 153, 184, 210, 100, 111]

# plt.plot(x, y)

# plt.savefig("./img/a.png")

def graph():
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_xticks(numpy.linspace(1, 15, 8))
    ax.set_xticklabels(['SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT'])
    ax.set_xlim(0.5, 14.5)
    
    today = datetime.date.today()
    data = []
    days = (datetime.date.today().weekday() + 1) % 7 + 1
    for i in range(days):
        td = datetime.timedelta(days=i)
        path = './data/' + (str)(today - td) + '.json'
        if os.path.exists(path):
            with open(path) as f:
                data.append(json.load(f))
        else:
            d = {}
            path = [
                '../../turnips/data/' + (str)(today - td) + '.json',
                '../../bei/turnips/data/' + (str)(today - td) + '.json',
                '../../shim/turnips/data/' + (str)(today - td) + '.json'
            ]
            if os.path.exists(path[0]):
                with open(path[0]) as f:
                    d.update(json.load(f))
            if os.path.exists(path[1]):
                with open(path[1]) as f:
                    d.update(json.load(f))
            if os.path.exists(path[2]):
                with open(path[2]) as f:
                    d.update(json.load(f))
            with open(path, 'w') as f:
                json.dump(d, f, indent=4, ensure_ascii=False)
            data.append(d)
    data.reverse()
    print(data)
    names = set()
    for d in data:
        for k in d:
            names.add(k)
    names.discard('day')
    for n in names:
        i = 0
        y = []
        x = []
        for d in data:
            if n in d:
                i += 1
                if 'am' in d[n]:
                    y.append(d[n]['am'])
                    x.append(i)
                i += 1
                if 'pm' in d[n]:
                    y.append(d[n]['pm'])
                    x.append(i)
            else:
                i += 2
        print(y)
        ax.plot(x, y, label=n, marker='o') 
    ax.legend()
    plt.savefig("./img/a.png", dpi=300)
    plt.clf()
    