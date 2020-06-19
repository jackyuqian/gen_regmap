#!/usr/bin/python3 -B
import json, sys, getopt

def gen_rtl(regmap, module_name, data_bw, addr_bw):
    ## Head
    txt =  "module %s (\n" % module_name
    txt += "    input               pclk,\n"
    txt += "    input               prstn,\n"
    txt += "    input       [%d :0] paddr,\n"   % (addr_bw - 1)
    txt += "    input       [%d :0] pwdata,\n"  % (data_bw - 1)
    txt += "    input               pwrite,\n"
    txt += "    input               psel,\n"
    txt += "    input               penable,\n"
    txt += "    output              pready,\n"
    txt += "    input       [%d :0] pstrb,\n"   % int(data_bw / 8 - 1)
    txt += "    output  reg [%d :0] prdata\n"   % (data_bw - 1)
    txt += ");\n"

    ## Declaration
    for register in regmap:
        for field in register['Field']:
            if field['Name'] not in ['RSVD', 'Reserved']:
                txt += "reg [%d :0]\t%s;\n" % (field['Length'] - 1, register['Name'] + '_' + field['Name'])
    txt += "\n"
    
    ## Misc Logic
    mask_str    = "{"
    for i in range(int(data_bw / 8))[::-1]:
        mask_str    += "{8{pstrb[%d]}}," % i
    mask_str    = mask_str[:-1] + "}"
    txt += "assign  pready      = 1'b1;\n"
    txt += "wire    pwdata_msk  = %s;\n" % mask_str
    txt += "wire    write_en    = psel && penable && pwrite;\n"
    txt += "wire    read_en     = psel && penable && (!pwrite);\n\n"

    ## Read Logic
    txt += "always@(posedge pclk and negedge prstn) begin\n"
    txt += "    if(~prstn)\n"
    txt += "        prdata  <= %d'h0;\n" % data_bw
    txt += "    else\n"
    txt += "        case(paddr)\n"
    for register in regmap:
        txt += "            %d'h%x:    prdata <= {" % (addr_bw, register['Address'])
        for field in register['Field']:
            regname =register['Name'] + '_' + field['Name']
            if field['Name'] in ['RSVD', 'Reserved']:
                txt += "%d'h0," % field['Length']
            else:
                txt += regname + ","
        txt = txt[:-1]
        txt += "};\n"
    txt += "            default:    prdata  <= %d'hDEADBEEF;\n" % data_bw
    txt += "        endcase\n"
    txt += "end\n"
    txt += "\n"

    ## Modified Logic
    for register in regmap:
        for field in register['Field']:
            if field['Name'] in ['RSVD', 'Reserved']:
                continue
            if field['Access'] in ['RO']:
                continue
            if field['Access'] not in ['RW', 'WO', 'RC', 'RS', 'W1C', 'W1S']:
                print('[ERROR] Unrecognized Access Code: %s!' % field['Access'])
                sys.exit()
            regname =register['Name'] + '_' + field['Name']

            txt     += "always@(posedge pclk and negedge prstn) begin\n"
            txt     += "    if(~prstn)\n"
            txt     += "        %s  <= %s;\n" % (regname, field['Reset'])
            if field['Access'] in ['RW', 'WO']:
                txt += "    else if(write_en && (paddr == %d'h%x) && (&(pwdata_msk[%d:%d])))\n" % (addr_bw, register['Address'], field['Msb'], field['Lsb'])
                txt += "        %s  <= pwdata[%d:%d];\n" % (regname, field['Msb'], field['Lsb'])
                txt += "end\n\n"
            elif field['Access'] == 'RC':
                txt += "    else if(read_en && (paddr == %d'h%x))\n" % (addr_bw, register['Address'])
                txt += "        %s  <= %d'h0;\n" % (regname, field['Length'])
                txt += "end\n\n"
            elif field['Access'] == 'RS':
                txt += "    else if(read_en && (paddr == %d'h%x))\n" % (addr_bw, register['Address'])
                txt += "        %s  <= %d'h%s;\n" % (regname, field['Length'], hex(2**field['Length']-1)[2:].upper())
                txt += "end\n\n"
            elif field['Access'] == 'W1C':
                txt += "    else if(write_en && (paddr == %d'h%x) && (&(pwdata_msk[%d:%d])))\n" % (addr_bw, register['Address'], field['Msb'], field['Lsb'])
                txt += "        %s  <= %s & (~pwdata[%d:%d]);\n" % (regname, regname, field['Msb'], field['Lsb'])
                txt += "end\n\n"
            elif field['Access'] == 'W1S':
                txt += "    else if(write_en && (paddr == %d'h%x) && (&(pwdata_msk[%d:%d])))\n" % (addr_bw, register['Address'], field['Msb'], field['Lsb'])
                txt += "        %s  <= %s | pwdata[%d:%d];\n" % (regname, regname, field['Msb'], field['Lsb'])
                txt += "end\n\n"

    ## Tail
    txt += 'endmodule\n'
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
            data_bw     = arg
        elif opt in ("-a"):
            addr_bw     = arg
    
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

