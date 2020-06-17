#!/usr/bin/python3
import csv, sys, getopt

def read_csv(fcsv, delimiter=','):
    with open(fcsv, 'r', encoding='UTF-8-sig') as fp:
        ## Read CSV
        #### Pre-Process
        lines   = []
        for line in fp:
            line.strip()
            if line.startswith('#'):
                continue
            elif line.replace(delimiter, '').strip() == '':
                continue
            lines.append(line)

        #### Read CSV
        dict_csv    = csv.DictReader(lines)
        
        ## Build Data Structure
        ##  regmap  = [ 
        ##      {
        ##          'Name'      : 'xxx',    (str)
        ##          'Address'   : 'xxx',    (str) 
        ##          'Field'     : [{
        ##                      'Name'      : 'xxx',    (str)
        ##                      'Msb'       : xxx,      (int) 
        ##                      'Lsb'       : xxx,      (int)
        ##                      'Length'    : xxx,      (int)
        ##                      'Access'    : 'xxx',    (str)
        ##                      'Reset'     : 'xxx',    (str) 
        ##                      'Doc'       : 'xxx'     (str) 
        ##                      }, {...}, ...]
        ##      },
        ##      {...},
        ##      ...
        ##      {...}
        ##  ]
        ## 
        regmap  = []

        for row in dict_csv:
            print(row['Field'])
            if row['Address'].strip() != '':
                bits        = row['Bits'].strip().replace('[','').replace(']','').split(':')
                register    = {
                        'Name'      : (row['Register'].strip() if row['Register'].strip() != '' else 'reg_' + row['Address'].strip()),
                        'Address'   : row['Address'].strip(),
                        'Field'     : [{
                            'Name'  : row['Field'].strip(),
                            'Msb'   : int(bits[0]),
                            'Lsb'   : int(bits[1]),
                            'Length': (int(bits[0]) - int(bits[1]) + 1),
                            'Access': row['Access'].strip(),
                            'Reset' : row['Reset'].strip(),
                            'Doc'   : row['Doc']
                            }]
                        }
                regmap.append(register)
            else:
                field   = {
                        'Name'  : row['Field'].strip(),
                        'Msb'   : int(bits[0]),
                        'Lsb'   : int(bits[1]),
                        'Length': (int(bits[0]) - int(bits[1]) + 1),
                        'Access': row['Access'].strip(),
                        'Reset' : row['Reset'].strip(),
                        'Doc'   : row['Doc']
                        }
                regmap[-1]['Field'].append(field)
        return regmap


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
    regmap  = read_csv(fcsv)
    print(regmap)

if __name__ == "__main__":
    main(sys.argv[1:])

