#!/usr/bin/python3
import csv, sys, getopt

def read_csv(fcsv):
    with open(fcsv, 'r', encoding='UTF-8-sig') as fp:
        ## Read CSV
        dict_csv    = csv.DictReader(fp)
        
        ## Build Data Structure
        ##  Regmap  = [ 
        ##      {
        ##          'Name'      : 'xxx',    (str)
        ##          'Address'   : xxx,      (int) 
        ##          'Field'     : {
        ##                      'Name'      : 'xxx',    (str)
        ##                      'Msb'       : xxx,      (int) 
        ##                      'Lsb'       : xxx,      (int)
        ##                      'Length'    : xxx,      (int)
        ##                      'Access'    : 'xxx',    (str)
        ##                      'Reset'     : xxx       (int) 
        ##                      }
        ##      },
        ##      {...},
        ##      ...
        ##      {...}
        ##  ]
        ## 
        for row in dict_csv:
            print(row['Address'])

def print_help():
    print('Oh!')
    
def main(argv):
    fcsv    = 'default.csv'
    frtl    = 'default.v'

    ## Read Arguments
    try:
        opts, args    = getopt.getopt(argv,"hi:o:",["csv=","rtl="])
    except getopt.GetoptError:
        print_help()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print_help()
            sys.exit()
        elif opt in ("-i", "--csv"):
            fcsv    = arg
        elif opt in ("-o", "--rtl"):
            frtl    = arg
    
    ## Main Flow
    read_csv(fcsv)

if __name__ == "__main__":
    main(sys.argv[1:])

