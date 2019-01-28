saveStandardPrint = Thing#{Standard,Print}
--saveStandardAfterPrint = Thing#{Standard,AfterPrint}
saveTeXmacsPrint = Thing#{TeXmacs,Print}
--saveTeXmacsAfterPrint = Thing#{TeXmacs,AfterPrint}

sentinelStandardPrint = x -> ( << "--VAL\n"; saveStandardPrint(x); << "--CLS\n"; )
--sentinelStandardAfterPrint = x -> ( << "--CLS\n"; saveStandardAfterPrint(x); << "--CLR\n"; )
sentinelTeXmacsPrint = x -> ( << "--VAL\n"; saveTeXmacsPrint(x); << "--CLS\n"; )
--sentinelTeXmacsAfterPrint = x -> ( << "--CLS\n"; saveTeXmacsAfterPrint(x); << "--CLR\n"; )

Thing#{Standard,Print} = sentinelStandardPrint
--Thing#{Standard,AfterPrint} = sentinelStandardAfterPrint
texmacsmode = false;

noop = (trigger) -> ( lineNumber=lineNumber-1; null )
mode = (usetexmacs) -> (
    if texmacsmode != usetexmacs then (
        texmacsmode = usetexmacs;
        if texmacsmode then (
            Thing#{Standard,Print} = sentinelTeXmacsPrint
            --Thing#{Standard,AfterPrint} = sentinelTeXmacsAfterPrint
        ) else (
            Thing#{Standard,Print} = sentinelStandardPrint
            --Thing#{Standard,AfterPrint} = sentinelStandardAfterPrint
        )
    );
    noop(mode);
)
