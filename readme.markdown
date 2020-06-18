# Usage

* Start with "#" for comments.

# Internal Data Structure
```
regmap  = [ 
    {
        "Name"      : "xxx",    			(str)
        "Address"   : xxx,      			(int) 
        "Field"     : [{
                    "Name"      : "xxx",    (str)
                    "Msb"       : xxx,      (int) 
                    "Lsb"       : xxx,      (int)
                    "Length"    : xxx,      (int)
                    "Access"    : "xxx",    (str, upper case)
                    "Reset"     : "xxx",    (str) 
                    "Doc"       : "xxx"     (str) 
                    }, 
                    {...},
                    ...
                    {...},
                    ]
    },
    {...},
    ...
    {...}
]
```
# Access Attribute
Supported	Access  Write                                                           Read
v       	RO	    no effect                                                       no effect
v       	RW	    as-is                                                           no effect
v       	RC	    no effect                                                       clears all bits
v       	RS	    no effect                                                       sets all bits
        	RU	                                                           
        	WRC	    as-is                                                           clears all bits
        	WRS	    as-is                                                           sets all bits
        	WC	    clears all bits                                                 no effect
        	WS	    sets all bits                                                   no effect
        	WSRC	sets all bits                                                   clears all bits
        	WCRS	clears all bits                                                 sets all bits
v       	W1C	    1/0 clears/no effect on matching bit                            no effect
v       	W1S	    1/0 sets/no effect on matching bit                              no effect
        	W1T	    1/0 toggles/no effect on matching bit                           no effect
        	W0C	    1/0 no effect on/clears matching bit                            no effect
        	W0S	    1/0 no effect on/sets matching bit                              no effect
        	W0T	    1/0 no effect on/toggles matching bit                           no effect
        	W1SRC	1/0 sets/no effect on matching bit                              clears all bits
        	W1CRS	1/0 clears/no effect on matching bit                            sets all bits
        	W0SRC	1/0 no effect on/sets matching bit                              clears all bits
        	W0CRS	1/0 no effect on/clears matching bit                            sets all bits
        	WO	    as-is                                                           error
        	WOC	    clears all bits                                                 error
        	WOS	    sets all bits                                                   error
        	W1	    first one after HARD reset is as-is other W have no effects     no effect
        	WO1	    first one after HARD reset is as-is other W have no effects     error
        	A0
        	A1
