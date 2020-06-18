#!/usr/bin/python3
import csv, sys, getopt, json

def print_usage():
    print('./parse_csv.py -i <csv file> -o <json file> -d <delimiter> -b <data_bw>')

def get_addr_lst(s, step):
    # s="xx; xx-xx"
    addr_lst    = []
    s           = s.replace(' ', '').replace('\t', '')
    for ele in s.split(';'):
        addr    = ele.split('-')
        if len(addr) == 1:
            addr_lst.append(int(addr[0], 16))
        elif len(addr) == 2:
            addr_lst    += list(range(int(addr[0], 16), int(addr[1], 16) + step, step))
        else:
            print('[ERROR] Format of Address is wrong!')
    return addr_lst

def pre_proc(fcsv, delimiter = ','):
    with open(fcsv, 'r', encoding='UTF-8-sig') as fp:
        lines   = []
        for line in fp:
            # Delete spaces
            line    = line.strip()
            # Delete comments
            if line.startswith('#'):
                continue
            # Delete empty rows
            if line.replace(delimiter, '').strip() == '':
                continue
            lines.append(line)
        dict_csv    = csv.DictReader(lines)
        return dict_csv

def parse_csv(fcsv, data_bw, delimiter = ','):
    dict_csv    = pre_proc(fcsv, delimiter)
    regmap      = []
    for row in dict_csv:
        if row['Address'].strip()!= '':
            address_lst = get_addr_lst(row['Address'].strip(), int(data_bw/8))
            for idx in range(len(address_lst)):
                address = address_lst[idx]
                if row['Register'].strip() != '':
                    register    = row['Register'].strip() if len(address_lst) == 1 else row['Register'].strip() + '_' + str(idx)
                else:
                    register    = 'reg_' + hex(address)
                regmap.append({
                        'Name'      : register,
                        'Address'   : address,
                        'Field'     : []
                        })

        bits    = row['Bits'].strip().replace('[','').replace(']','').split(':')
        for idx in range(len(address_lst)):
            regmap[0-idx]['Field'].append({
                    'Name'  : row['Field'].strip(),
                    'Msb'   : int(bits[0]),
                    'Lsb'   : int(bits[1]) if len(bits) == 2 else bits[0],
                    'Length': (int(bits[0]) - int(bits[1]) + 1) if len(bits) == 2 else 1,
                    'Access': row['Access'].strip().upper(),
                    'Reset' : row['Reset'].strip(),
                    'Doc'   : row['Doc']
                    })
    return regmap

    
def main(argv):
    # Get Arguments
    fcsv        = ''
    fjson       = ''
    delimiter   = ','
    data_bw     = 32

    try:
        opts, args    = getopt.getopt(argv,"hi:o:d:b:")
    except getopt.GetoptError:
        print_usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print_usage()
            sys.exit()
        elif opt in ("-i"):
            fcsv        = arg
        elif opt in ("-o"):
            fjson       = arg
        elif opt in ("-d"):
            delimiter   = arg
        elif opt in ("-b"):
            data_bw     = arg
    
    if fcsv == '':
        fcsv    = 'default.csv'
    if fjson == '':
        fjson   = fcsv.split('.')[0] + '.json'

    ## Main Flow
    regmap  = parse_csv(fcsv, data_bw, delimiter)
    with open(fjson, 'w') as fp:
        json.dump(regmap, fp)

if __name__ == "__main__":
    main(sys.argv[1:])

