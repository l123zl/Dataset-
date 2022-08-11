import os
import shutil

train = 'annotation/labels/train'
test = 'annotation/labels/test'

trains = []
tests = []
for i in os.listdir(train):
    trains.append(int(i.split('.')[0]))
trains.sort()
for i in os.listdir(test):
    tests.append(int(i.split('.')[0]))
tests.sort()
print(trains, tests, len(trains), len(tests))
with open('train.txt', 'w') as f:
    for i in trains:
        f.write(str(i) + '\n')
f.close()
with open('test.txt', 'w') as f:
    for i in tests:
        f.write(str(i) + '\n')
f.close()
file = 'images'
for i in trains:
    shutil.copy(os.path.join(file, str(i) + '.jpg'), 'annotation/images/train')
for i in tests:
    shutil.copy(os.path.join(file, str(i) + '.jpg'), 'annotation/images/test')
print('finish')
