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
        ##          'Address'   : xxx,      (int) 
        ##          'Field'     : [{
        ##                      'Name'      : 'xxx',    (str)
        ##                      'Msb'       : xxx,      (int) 
        ##                      'Lsb'       : xxx,      (int)
        ##                      'Length'    : xxx,      (int)
        ##                      'Access'    : 'xxx',    (str, lower case)
        ##                      'Reset'     : 'xxx',    (str) 
        ##                      'Doc'       : 'xxx'     (str) 
        ##                      }, 
        ##                      {...},
        ##                      ...
        ##                      {...},
        ##                      ]
        ##      },
        ##      {...},
        ##      ...
        ##      {...}
        ##  ]
        ## 
        regmap  = []

        for row in dict_csv:
            if row['Address'].strip() != '':
                bits        = row['Bits'].strip().replace('[','').replace(']','').split(':')
                reg_name    = row['Register'].strip() if row['Register'].strip() != '' else 'reg_' + row['Address'].strip()
                register    = {
                        'Name'      : reg_name,
                        'Address'   : int(row['Address'].strip(), 16),
                        'Field'     : [{
                            'Name'  : row['Field'].strip(),
                            'Msb'   : int(bits[0]),
                            'Lsb'   : int(bits[1]),
                            'Length': (int(bits[0]) - int(bits[1]) + 1),
                            'Access': row['Access'].strip().lower(),
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
                        'Access': row['Access'].strip().lower(),
                        'Reset' : row['Reset'].strip(),
                        'Doc'   : row['Doc']
                        }
                regmap[-1]['Field'].append(field)
        return regmap

def write_verilog(regmap, frtl, data_bw, addr_bw):
    ## Head
    txt =  "module " + frtl.split('.')[0] + " (\n"
    txt += "    input               pclk,\n"
    txt += "    input               prstn,\n"
    txt += "    input       [11 :0] paddr,\n"
    txt += "    input       [31 :0] pwdata,\n"
    txt += "    input               pwrite,\n"
    txt += "    input               psel,\n"
    txt += "    input               penable,\n"
    txt += "    output  reg [31 :0] prdata\n"
    txt += ");\n"

    ## Declaration
    for register in regmap:
        for field in register['Field']:
            if field['Name'] not in ['RSVD', 'Reserved']:
                txt += "reg [%d :0]\t%s;\n" % (field['Length'] - 1, register['Name'] + '_' + field['Name'])
    txt += "\n"

    ## Read Logic
    txt += "always@(posedge pclk and negedge prstn) begin\n"
    txt += "    if(~prstn)\n"
    txt += "        prdata  <= 'h0;\n"
    txt += "    else\n"
    txt += "        case(paddr)\n"
    for register in regmap:
        txt += "            %d'h%x:    prdata <= {" % (addr_bw, register['Address'])
        for field in register['Field']:
            if field['Name'] in ['RSVD', 'Reserved']:
                txt += "%d'h0," % field['Length']
            else:
                txt += field['Name'] + ","
        txt = txt[:-1]
        txt += "};\n"
    txt += "            default:    prdata  <= %d'hDEADBEEF;\n" % data_bw
    txt += "        endcase\n"
    txt += "end\n"
    txt += "\n"

    ## Modified Logic
    for register in regmap:
        for field in register['Field']:
            if field['Access'] == 'rw':
                txt += "always@(posedge pclk and negedge prstn) begin\n"
                txt += "    if(~prstn)\n"
                txt += "        %s  <= %s;\n" % (register['Name'] + '_' + field['Name'], field['Reset'])
                txt += "    else if(psel && penable && pwrite && (paddr == %d'h%x))\n" % (addr_bw, register['Address'])
                txt += "        %s  <= pwdata;\n" % (register['Name'] + '_' + field['Name'])
                txt += "end\n\n"

    ## Tail
    txt += 'endmodule\n'

    with open(frtl, 'w') as fp:
        print(txt, file=fp)
        print(txt)

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
    write_verilog(regmap, frtl, 32, 12)

if __name__ == "__main__":
    main(sys.argv[1:])

