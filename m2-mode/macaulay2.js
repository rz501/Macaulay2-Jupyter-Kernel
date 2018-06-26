define([
    'codemirror/lib/codemirror',
    'codemirror/addon/mode/simple'
], function (CodeMirror) {
    'use strict';

    var keyword = RegExp(['(?:for|from|to|superhui|apply|break|breakpoint|continue|else|export|exportto|for|if|importfrom|',
        'keepring|load|quit|return|while)\\b'].join(''))

    CodeMirror.defineSimpleMode("macaulay2", {
        start: [
            {regex: keyword, token: "keyword"},
            {regex: /--.*/, token: "comment"},
        ]
    });
    CodeMirror.defineMIME('text/x-macaulay2', 'macaulay2');
});
