module example (
    input               pclk,
    input               prstn,
    input       [11 :0] paddr,
    input       [31 :0] pwdata,
    input               pwrite,
    input               psel,
    input               penable,
    output              pready,
    input       [3 :0] pstrb,
    output  reg [31 :0] prdata
);
reg [15 :0]	r0_func_reg1;
reg [6 :0]	r0_func_reg2;
reg [5 :0]	r0_func3_reg3;
reg [7 :0]	reg_0x304_func_reg1;
reg [7 :0]	reg_0x304_func_reg2;
reg [7 :0]	reg_0x304_func3;
reg [15 :0]	ch_fir_coef_0_0_cfir_ceof1;
reg [15 :0]	ch_fir_coef_0_0_cfir_ceof0;
reg [15 :0]	ch_fir_coef_0_1_cfir_ceof1;
reg [15 :0]	ch_fir_coef_0_1_cfir_ceof0;
reg [15 :0]	ch_fir_coef_0_2_cfir_ceof1;
reg [15 :0]	ch_fir_coef_0_2_cfir_ceof0;
reg [15 :0]	ch_fir_coef_0_3_cfir_ceof1;
reg [15 :0]	ch_fir_coef_0_3_cfir_ceof0;
reg [15 :0]	ch_fir_coef_0_4_cfir_ceof1;
reg [15 :0]	ch_fir_coef_0_4_cfir_ceof0;
reg [15 :0]	ch_fir_coef_0_5_cfir_ceof1;
reg [15 :0]	ch_fir_coef_0_5_cfir_ceof0;
reg [15 :0]	ch_fir_coef_0_6_cfir_ceof1;
reg [15 :0]	ch_fir_coef_0_6_cfir_ceof0;

assign  pready      = 1'b1;
wire    pwdata_msk  = {{8{pstrb[3]}},{8{pstrb[2]}},{8{pstrb[1]}},{8{pstrb[0]}}};
wire    write_en    = psel && penable && pwrite;
wire    read_en     = psel && penable && (!pwrite);

always@(posedge pclk and negedge prstn) begin
    if(~prstn)
        prdata  <= 32'h0;
    else
        case(paddr)
            12'h300:    prdata <= {r0_func_reg1,r0_func_reg2,4'h0,r0_func3_reg3};
            12'h304:    prdata <= {reg_0x304_func_reg1,reg_0x304_func_reg2,8'h0,reg_0x304_func3};
            12'h308:    prdata <= {ch_fir_coef_0_0_cfir_ceof1,ch_fir_coef_0_0_cfir_ceof0};
            12'h400:    prdata <= {ch_fir_coef_0_1_cfir_ceof1,ch_fir_coef_0_1_cfir_ceof0};
            12'h404:    prdata <= {ch_fir_coef_0_2_cfir_ceof1,ch_fir_coef_0_2_cfir_ceof0};
            12'h408:    prdata <= {ch_fir_coef_0_3_cfir_ceof1,ch_fir_coef_0_3_cfir_ceof0};
            12'h40c:    prdata <= {ch_fir_coef_0_4_cfir_ceof1,ch_fir_coef_0_4_cfir_ceof0};
            12'h410:    prdata <= {ch_fir_coef_0_5_cfir_ceof1,ch_fir_coef_0_5_cfir_ceof0};
            12'h500:    prdata <= {ch_fir_coef_0_6_cfir_ceof1,ch_fir_coef_0_6_cfir_ceof0};
            default:    prdata  <= 32'hDEADBEEF;
        endcase
end

always@(posedge pclk and negedge prstn) begin
    if(~prstn)
        r0_func_reg1  <= 8'h0;
    else if(write_en && (paddr == 12'h300) && (&(pwdata_msk[31:16])))
        r0_func_reg1  <= pwdata[31:16];
end

always@(posedge pclk and negedge prstn) begin
    if(~prstn)
        r0_func3_reg3  <= 7'h3F;
    else if(write_en && (paddr == 12'h300) && (&(pwdata_msk[5:0])))
        r0_func3_reg3  <= pwdata[5:0];
end

always@(posedge pclk and negedge prstn) begin
    if(~prstn)
        reg_0x304_func_reg1  <= 8'hff;
    else if(write_en && (paddr == 12'h304) && (&(pwdata_msk[31:24])))
        reg_0x304_func_reg1  <= reg_0x304_func_reg1 & (~pwdata[31:24]);
end

always@(posedge pclk and negedge prstn) begin
    if(~prstn)
        reg_0x304_func_reg2  <= 8'h0;
    else if(read_en && (paddr == 12'h304))
        reg_0x304_func_reg2  <= 8'hFF;
end

always@(posedge pclk and negedge prstn) begin
    if(~prstn)
        reg_0x304_func3  <= 8'h0;
    else if(read_en && (paddr == 12'h304))
        reg_0x304_func3  <= 8'hFF;
end

always@(posedge pclk and negedge prstn) begin
    if(~prstn)
        ch_fir_coef_0_0_cfir_ceof1  <= 16'h0;
    else if(write_en && (paddr == 12'h308) && (&(pwdata_msk[31:16])))
        ch_fir_coef_0_0_cfir_ceof1  <= pwdata[31:16];
end

always@(posedge pclk and negedge prstn) begin
    if(~prstn)
        ch_fir_coef_0_0_cfir_ceof0  <= 16'h10;
    else if(write_en && (paddr == 12'h308) && (&(pwdata_msk[15:0])))
        ch_fir_coef_0_0_cfir_ceof0  <= pwdata[15:0];
end

always@(posedge pclk and negedge prstn) begin
    if(~prstn)
        ch_fir_coef_0_1_cfir_ceof1  <= 16'h0;
    else if(write_en && (paddr == 12'h400) && (&(pwdata_msk[31:16])))
        ch_fir_coef_0_1_cfir_ceof1  <= pwdata[31:16];
end

always@(posedge pclk and negedge prstn) begin
    if(~prstn)
        ch_fir_coef_0_1_cfir_ceof0  <= 16'h10;
    else if(write_en && (paddr == 12'h400) && (&(pwdata_msk[15:0])))
        ch_fir_coef_0_1_cfir_ceof0  <= pwdata[15:0];
end

always@(posedge pclk and negedge prstn) begin
    if(~prstn)
        ch_fir_coef_0_2_cfir_ceof1  <= 16'h0;
    else if(write_en && (paddr == 12'h404) && (&(pwdata_msk[31:16])))
        ch_fir_coef_0_2_cfir_ceof1  <= pwdata[31:16];
end

always@(posedge pclk and negedge prstn) begin
    if(~prstn)
        ch_fir_coef_0_2_cfir_ceof0  <= 16'h10;
    else if(write_en && (paddr == 12'h404) && (&(pwdata_msk[15:0])))
        ch_fir_coef_0_2_cfir_ceof0  <= pwdata[15:0];
end

always@(posedge pclk and negedge prstn) begin
    if(~prstn)
        ch_fir_coef_0_3_cfir_ceof1  <= 16'h0;
    else if(write_en && (paddr == 12'h408) && (&(pwdata_msk[31:16])))
        ch_fir_coef_0_3_cfir_ceof1  <= pwdata[31:16];
end

always@(posedge pclk and negedge prstn) begin
    if(~prstn)
        ch_fir_coef_0_3_cfir_ceof0  <= 16'h10;
    else if(write_en && (paddr == 12'h408) && (&(pwdata_msk[15:0])))
        ch_fir_coef_0_3_cfir_ceof0  <= pwdata[15:0];
end

always@(posedge pclk and negedge prstn) begin
    if(~prstn)
        ch_fir_coef_0_4_cfir_ceof1  <= 16'h0;
    else if(write_en && (paddr == 12'h40c) && (&(pwdata_msk[31:16])))
        ch_fir_coef_0_4_cfir_ceof1  <= pwdata[31:16];
end

always@(posedge pclk and negedge prstn) begin
    if(~prstn)
        ch_fir_coef_0_4_cfir_ceof0  <= 16'h10;
    else if(write_en && (paddr == 12'h40c) && (&(pwdata_msk[15:0])))
        ch_fir_coef_0_4_cfir_ceof0  <= pwdata[15:0];
end

always@(posedge pclk and negedge prstn) begin
    if(~prstn)
        ch_fir_coef_0_5_cfir_ceof1  <= 16'h0;
    else if(write_en && (paddr == 12'h410) && (&(pwdata_msk[31:16])))
        ch_fir_coef_0_5_cfir_ceof1  <= pwdata[31:16];
end

always@(posedge pclk and negedge prstn) begin
    if(~prstn)
        ch_fir_coef_0_5_cfir_ceof0  <= 16'h10;
    else if(write_en && (paddr == 12'h410) && (&(pwdata_msk[15:0])))
        ch_fir_coef_0_5_cfir_ceof0  <= pwdata[15:0];
end

always@(posedge pclk and negedge prstn) begin
    if(~prstn)
        ch_fir_coef_0_6_cfir_ceof1  <= 16'h0;
    else if(write_en && (paddr == 12'h500) && (&(pwdata_msk[31:16])))
        ch_fir_coef_0_6_cfir_ceof1  <= pwdata[31:16];
end

always@(posedge pclk and negedge prstn) begin
    if(~prstn)
        ch_fir_coef_0_6_cfir_ceof0  <= 16'h10;
    else if(write_en && (paddr == 12'h500) && (&(pwdata_msk[15:0])))
        ch_fir_coef_0_6_cfir_ceof0  <= pwdata[15:0];
end

endmodule

