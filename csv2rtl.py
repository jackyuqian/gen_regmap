#!/usr/bin/python3 -B
import  sys, getopt
from    parse_csv   import *
from    gen_rtl     import *
from    gen_ver     import *

def print_usage():
    print('./csv2rtl.py -i <csv file> -r <rtl file> -v <ver file> -b <delimiter> -d <data_bw> -a <addr_bw>')

def main(argv):
    # Get Arguments
    fcsv        = ''
    frtl        = ''
    fver        = ''
    data_bw     = 32
    addr_bw     = 12
    delimiter   = ','

    try:
        opts, args    = getopt.getopt(argv,"hi:r:v:d:a:b:")
    except getopt.GetoptError:
        print_usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print_usage()
            sys.exit()
        elif opt in ("-i"):
            fcsv       = arg
        elif opt in ("-r"):
            frtl       = arg
        elif opt in ("-v"):
            fver       = arg
        elif opt in ("-d"):
            data_bw     = int(arg)
        elif opt in ("-a"):
            addr_bw     = int(arg)
        elif opt in ("-b"):
            delimiter   = arg
    
    if fcsv == '':
        fcsv    = 'default.csv'
    if frtl == '':
        frtl    = fcsv.split('.')[0] + '.v'
    if fver == '':
        fver    = fcsv.split('.')[0] + '_ver.v'
    module_name = fcsv.split('.')[0]

    ## Main Flow
    with open(fcsv, 'r', encoding = 'utf-8-sig') as fp:
        regmap  = parse_csv(fp, data_bw, delimiter)
    
    rtl_txt = gen_rtl(regmap, module_name, data_bw, addr_bw)
    ver_txt = gen_ver(regmap, module_name, data_bw, addr_bw)
    
    with open(frtl, 'w') as fp:
        print(rtl_txt, file=fp)
    
    with open(fver, 'w') as fp:
        print(ver_txt, file=fp)

if __name__ == "__main__":
    main(sys.argv[1:])

