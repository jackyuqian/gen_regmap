#!/usr/bin/python3 -B
import json, sys, getopt

def gen_ver(regmap, module_name, data_bw, addr_bw):
    txt =  ""
    txt += "bit [%d :0] rdata;\n" % (data_bw - 1)
    txt += "bit         fail;\n"
    txt += "fail    = 1'b0;\n"
    txt =  "\n"

    ## Read Logic
    for register in regmap:
        txt += "    // %s\n" % (register['Name'])
        txt += "    if_ahblite.read(%d'h%x, value32);\n" % (addr_bw, register['Address'])
        idx_bit = data_bw - 1
        txt_dv  = "{" # Default Value
        while idx_bit >= 0:
            field_found = False
            for field in register['Field']:
                if idx_bit <= field['Msb'] and idx_bit >= field['Lsb']:
                    # regname =register['Name'] + '_' + field['Name']
                    regname = field['Name'] + ('' if register['GroupIdx'] == -1 else ('[' + str(register['GroupIdx']) + ']')) 
                    if field['Name'] in ['RSVD', 'Reserved']:
                        txt_dv += "%d'h0," % field['Length']
                    else:
                        txt_dv += field['Reset'] + ","
                    idx_bit = field['Lsb'] - 1
                    field_found = True
            if field_found is False:
                txt_dv += "1'b0,"
                idx_bit = idx_bit - 1
        txt_dv =    txt_dv[:-1] + '}'
        txt += "    if(value32 != %s) begin;\n" % txt_dv
        txt += '        pass_flag = "fail";\n'
        txt += '        $display("[ERROR] Rslt is wrong: ' + '0x%x!", value32);\n'
        txt += "    end;\n"
    txt += "\n"

    return txt

def print_usage():
    print('./gen_rtl.py -i <json file> -o <rtl file> -d <data_bw> -a <addr_bw>')
    
def main(argv):
    # Get Arguments
    fjson       = ''
    frtl        = ''
    data_bw     = 32
    addr_bw     = 12

    try:
        opts, args    = getopt.getopt(argv,"hi:o:d:a:")
    except getopt.GetoptError:
        print_usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print_usage()
            sys.exit()
        elif opt in ("-i"):
            fjson       = arg
        elif opt in ("-o"):
            frtl       = arg
        elif opt in ("-d"):
            data_bw     = int(arg)
        elif opt in ("-a"):
            addr_bw     = int(arg)
    
    if fjson == '':
        fjson   = 'default.json'
    if frtl == '':
        frtl    = fjson.split('.')[0] + '.v'
    module_name = fjson.split('.')[0]

    ## Main Flow
    with open(fjson, 'r') as fp:
        regmap  = json.load(fp)
    rtl_txt = gen_rtl(regmap, module_name, data_bw, addr_bw)
    with open(frtl, 'w') as fp:
        print(rtl_txt, file=fp)

if __name__ == "__main__":
    main(sys.argv[1:])

