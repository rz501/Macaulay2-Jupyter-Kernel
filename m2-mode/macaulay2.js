define([
    'codemirror/lib/codemirror',
    'codemirror/addon/mode/simple'
], function (CodeMirror) {
    'use strict';

    // var m2keyword = RegExp(['(?:)\\b'].join(''))

    CodeMirror.defineSimpleMode("macaulay2", {
        start: [
            {regex: /"(?:[^\\]|\\.)*?(?:"|$)/,
             token: "string"},
            {regex: /(?:for|while|if|and|or|not)\b/,
             token: "keyword"},
            {regex: /(?:then|do|list|else)\b/,
             token: "keyword", indent: true},
            {regex: /true|false|null/,
             token: "atom"},
            {regex: /0x[a-f\d]+|[-+]?(?:\.\d+|\d+\.?\d*)(?:e[-+]?\d+)?/i,
             token: "number"},
            {regex: /(?:from|to)/,
             token: "number"},
            {regex: /[\{\[\(]/, indent: true},
            {regex: /[\}\]\);]/, dedent: true},
            {regex: /[a-z$][\w$]*/, token: "variable"},
            {regex: /(?:builtin|rern)\b/,
             token: "builtin"},
            {regex: /(?:property|twoproperty)\b/,
             token: "property"},
            {regex: /(?:property|Matrix)\b/,
             token: "string-2"},
            {regex: /(?:property|twotag)\b/,
             token: "tag"},
            {regex: /(?:Matrix|twolink)\b/,
             token: "atom"},
            {regex: /(?:property|twoerror)\b/,
             token: "error"},
            {regex: /(?:three|twovar2)\b/,
             token: 'string-2'}, // link
            {regex: /(?:three|twovar3)\b/,
             token: 'variable'},
            {regex: /--.*/,
             token: "comment"},
        ]
    });
    CodeMirror.defineMIME('text/x-macaulay2', 'macaulay2');
});
