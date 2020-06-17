module example (
    input               pclk,
    input               prstn,
    input       [11 :0] paddr,
    input       [31 :0] pwdata,
    input               pwrite,
    input               psel,
    input               penable,
    output  reg [31 :0] prdata
);
reg [15 :0]	r0_func_reg1;
reg [15 :0]	r0_func_reg2;
reg [15 :0]	r0_func3_reg3;
reg [7 :0]	reg_0x304_func_reg1;
reg [7 :0]	reg_0x304_func_reg2;
reg [7 :0]	reg_0x304_func3;
reg [15 :0]	ch_fir_coef_0_cfir_ceof1;
reg [15 :0]	ch_fir_coef_0_cfir_ceof0;

always@(posedge pclk and negedge prstn) begin
    if(~prstn)
        prdata  <= 32'h0;
    else
        case(paddr)
            12'h300:    prdata <= {func_reg1,func_reg2,16'h0,func3_reg3};
            12'h304:    prdata <= {func_reg1,func_reg2,8'h0,func3};
            12'h308:    prdata <= {cfir_ceof1,cfir_ceof0};
            default:    prdata  <= 32'hDEADBEEF;
        endcase
end

always@(posedge pclk and negedge prstn) begin
    if(~prstn)
        r0_func_reg1  <= 8'h0;
    else if(psel && penable && pwrite && (paddr == 12'h300))
        r0_func_reg1  <= pwdata[31:16];
end

always@(posedge pclk and negedge prstn) begin
    if(~prstn)
        r0_func3_reg3  <= 7'h3F;
    else if(psel && penable && pwrite && (paddr == 12'h300))
        r0_func3_reg3  <= pwdata[31:16];
end

always@(posedge pclk and negedge prstn) begin
    if(~prstn)
        reg_0x304_func_reg1  <= 8'hff;
    else if(psel && penable && (pwrite) && (paddr == 12'h304))
        reg_0x304_func_reg1  <= reg_0x304_func_reg1 & (~pwdata[31:24]);
end

always@(posedge pclk and negedge prstn) begin
    if(~prstn)
        reg_0x304_func_reg2  <= 8'h0;
    else if(psel && penable && (!pwrite) && (paddr == 12'h304))
        reg_0x304_func_reg2  <= 8'hFF;
end

always@(posedge pclk and negedge prstn) begin
    if(~prstn)
        reg_0x304_func3  <= 8'h0;
    else if(psel && penable && (!pwrite) && (paddr == 12'h304))
        reg_0x304_func3  <= 8'hFF;
end

always@(posedge pclk and negedge prstn) begin
    if(~prstn)
        ch_fir_coef_0_cfir_ceof1  <= 16'h0;
    else if(psel && penable && pwrite && (paddr == 12'h308))
        ch_fir_coef_0_cfir_ceof1  <= pwdata[31:16];
end

always@(posedge pclk and negedge prstn) begin
    if(~prstn)
        ch_fir_coef_0_cfir_ceof0  <= 16'h10;
    else if(psel && penable && pwrite && (paddr == 12'h308))
        ch_fir_coef_0_cfir_ceof0  <= pwdata[31:16];
end

endmodule

