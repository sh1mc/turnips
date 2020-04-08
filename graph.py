import numpy
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import datetime
import json

# x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
# y = [97, 80, 78, 72, 68, 65, 60, 102, 153, 184, 210, 100, 111]

# plt.plot(x, y)

# plt.savefig("./img/a.png")

def graph():
    today = datetime.date.today()
    data = []
    days = (datetime.date.today().weekday() + 1) % 7 + 1
    for i in range(days):
        td = datetime.timedelta(days=i)
        with open('./data/' + (str)(today - td) + '.json') as f:
            data.append(json.load(f))
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
        plt.plot(x, y, label=n)
        
    plt.legend()
    plt.savefig("./img/a.png")
    