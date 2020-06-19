#!/usr/bin/python3 -B
import  sys, getopt
from    parse_csv   import *
from    gen_rtl     import *

def print_usage():
    print('./csv2rtl.py -i <csv file> -o <rtl file> -b <delimiter> -d <data_bw> -a <addr_bw>')

def main(argv):
    # Get Arguments
    fcsv        = ''
    frtl        = ''
    data_bw     = 32
    addr_bw     = 12
    delimiter   = ','

    try:
        opts, args    = getopt.getopt(argv,"hi:o:d:a:b:")
    except getopt.GetoptError:
        print_usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print_usage()
            sys.exit()
        elif opt in ("-i"):
            fcsv       = arg
        elif opt in ("-o"):
            frtl       = arg
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
    module_name = fcsv.split('.')[0]

    ## Main Flow
    with open(fcsv, 'r', encoding = 'utf-8-sig') as fp:
        regmap  = parse_csv(fp, data_bw, delimiter)
    
    rtl_txt = gen_rtl(regmap, module_name, data_bw, addr_bw)
    
    with open(frtl, 'w') as fp:
        print(rtl_txt, file=fp)

if __name__ == "__main__":
    main(sys.argv[1:])

