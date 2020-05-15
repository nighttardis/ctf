### Solution to SecDSM's minictf from 5/2020: `Project: AlienFS`
### Author: nighttardis

import base64

def fix_string(string: str) -> str:
    try:
        return bytes.fromhex(string).decode('utf-8')
    except:
        return string.strip('\x00')

data = list()
data1 = dict()
with open(file='alien.fs', mode='rb') as alien:
    # The 'while' loop can be simplified to
    # while (line := alien.read(16)):
    # if using python 3.8, would need to remove line 18 and 44
    line = alien.read(16)
    temp = dict()
    count = 0
    first = True
    while line:
        line = line.decode('utf-8').strip('\n')
        if 'BLKHDR' in line:
            if not first:
                if temp['BLKNUM'] == '':
                    data.append(temp)
                else:
                    data1[temp['BLKNUM']] = {'data': temp['data'], 'BLKNEXT': temp['BLKNEXT']}
            temp = dict()
            count += 1
            previous = ""
            first = False
        if previous == 'BLKTYPE':
            temp['data'] = fix_string(string=line)
        else:
            line = line.split('\n')
            if len(line[0]) == 6:
                value = fix_string(string=line[2])
            elif len(line[0]) == 7:
                value = fix_string(string=line[1])
            temp[line[0]] = value.strip()
            previous = line[0]
        line = alien.read(16)

for line in data:
    s = ''
    # Don't care if there isn't another piece of the puzzle
    if line['BLKNEXT'] != '':
        s = line['data']
        next_value = data1[line['BLKNEXT']]
        while True:
            s += next_value['data']
            # we've hit the end of the road
            if next_value['BLKNEXT'] == '': break
            next_value = data1[next_value['BLKNEXT']]
    print(base64.b64decode(s))
