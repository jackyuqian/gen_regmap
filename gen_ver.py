#!/usr/bin/python3 -B
import json, sys, getopt

def gen_ver(regmap, fver, data_bw, addr_bw, addr_offset):
    ## Read Logic
    txt = '"%s": begin\n\n' % (fver.split('.')[0])
    txt += '    bit [31 :0] addr_offset;\n'
    txt += '    addr_offset = %s;\n' % addr_offset
    txt += '    pass_flag   = "pass";\n\n'
    
    txt += '    // Check Default Value\n'
    for register in regmap:
        skip    = False
        for field in register['Field']:
            if field['Access'] in ['RO', 'RC', 'RS', 'ro', 'rc', 'rs']:
                skip    = True
        if skip is True:
            continue

        txt += "    // %s\n" % (register['Name'])
        txt += "    if_ahblite.read(addr_offset + %d'h%x, value32);\n" % (addr_bw, register['Address'])
        idx_bit = data_bw - 1
        txt_dv  = "{" # Default Value
        while idx_bit >= 0:
            field_found = False
            for field in register['Field']:
                if idx_bit <= field['Msb'] and idx_bit >= field['Lsb']:
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
        txt += "    if(value32 != %s) begin\n" % txt_dv
        txt += '        pass_flag = "fail";\n'
        txt += '        $display("[ERROR] Rslt is wrong: ' + '0x%x!", value32);\n'
        txt += "    end\n\n"

    txt += '    // Check Bit Toggle\n'
    for register in regmap:
        skip    = False
        for field in register['Field']:
            if field['Access'] in ['RO', 'RC', 'RS', 'ro', 'rc', 'rs']:
                skip    = True
        if skip is True:
            continue

        idx_bit = data_bw - 1
        txt_mask= "{" # Mask
        while idx_bit >= 0:
            field_found = False
            for field in register['Field']:
                if idx_bit <= field['Msb'] and idx_bit >= field['Lsb']:
                    regname = field['Name'] + ('' if register['GroupIdx'] == -1 else ('[' + str(register['GroupIdx']) + ']')) 
                    if field['Name'] in ['RSVD', 'Reserved']:
                        txt_mask    += "%d'h0," % field['Length']
                    else:
                        txt_mask    += "{%d{1'b1}}," % (field['Msb'] - field['Lsb'] + 1)
                    idx_bit = field['Lsb'] - 1
                    field_found = True
            if field_found is False:
                txt_mask    += "1'b0,"
                idx_bit     = idx_bit - 1
        txt_mask    = txt_mask[:-1] + '}'
        txt += "    // %s\n" % (register['Name'])
        txt += "    if_ahblite.write(addr_offset + %d'h%x, 32'hAAAAAAAA);\n" % (addr_bw, register['Address'])
        txt += "    if_ahblite.read(addr_offset + %d'h%x, value32);\n" % (addr_bw, register['Address'])
        txt += "    if(value32 != (32'hAAAAAAAA & %s) begin\n" % txt_mask
        txt += '        pass_flag = "fail";\n'
        txt += '        $display("[ERROR] Rslt is wrong: ' + '0x%x!", value32);\n'
        txt += "    end\n\n"

        txt += "    // %s\n" % (register['Name'])
        txt += "    if_ahblite.write(addr_offset + %d'h%x, 32'h555555555);\n" % (addr_bw, register['Address'])
        txt += "    if_ahblite.read(addr_offset + %d'h%x, value32);\n" % (addr_bw, register['Address'])
        txt += "    if(value32 != (32'h55555555 & %s) begin\n" % txt_mask
        txt += '        pass_flag = "fail";\n'
        txt += '        $display("[ERROR] Rslt is wrong: ' + '0x%x!", value32);\n'
        txt += "    end\n\n"

    txt += "end\n"

    return txt

def print_usage():
    print('./gen_ver.py -i <json file> -o <ver file> -d <data_bw> -a <addr_bw>')
    
def main(argv):
    # Get Arguments
    fjson       = ''
    fver        = ''
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
            fver       = arg
        elif opt in ("-d"):
            data_bw     = int(arg)
        elif opt in ("-a"):
            addr_bw     = int(arg)
    
    if fjson == '':
        fjson   = 'default.json'
    if fver == '':
        ver    = fjson.split('.')[0] + '_default_value_case.v'

    ## Main Flow
    with open(fjson, 'r') as fp:
        regmap  = json.load(fp)
    ver_txt = gen_ver(regmap, fver, data_bw, addr_bw)
    with open(fver, 'w') as fp:
        print(ver_txt, file=fp)

if __name__ == "__main__":
    main(sys.argv[1:])

