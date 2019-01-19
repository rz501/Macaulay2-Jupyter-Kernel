define([
    'codemirror/lib/codemirror',
    'codemirror/addon/mode/simple'
], function (CodeMirror) {
    'use strict';
    
    // see https://codemirror.net/demo/simplemode.html

    CodeMirror.defineSimpleMode("macaulay2", {
        start: [
            {regex: /example_keyword\b/, token: "keyword"},
            {regex: /example_atom\b/, token: "atom"},
            {regex: /example_number\b/, token: "number"},
            {regex: /example_def\b/, token: "def"},
            {regex: /example_variable\b/, token: "variable"},
            {regex: /example_variable2\b/, token: "variable-2"},
            {regex: /example_variable3\b/, token: "variable-3"},
            {regex: /example_puntuation\b/, token: "puntuation"},
            {regex: /example_operator\b/, token: "operator"},
            {regex: /example_comment\b/, token: "comment"},
            {regex: /example_string\b/, token: "string"},
            {regex: /example_meta\b/, token: "meta"},
            {regex: /example_qualifier\b/, token: "qualifier"},
            {regex: /(ZZ|QQ|RR|PP|CC|Matrix|List)\b/, token: "tag"},
            {regex: /example_builtin\b/, token: "builtin"},
            {regex: /example_bracket\b/, token: "bracket"},
            {regex: /example_tag\b/, token: "tag"},
            {regex: /example_attribute\b/, token: "attribute"},
            {regex: /example_link\b/, token: "link"},
            {regex: /example_error\b/, token: "error"},

            {regex: /"(?:[^\\]|\\.)*?(?:"|$)/, token: "string"},
            {regex: /(?:for|while|if|and|or|not)\b/, token: "keyword"},
            {regex: /(?:then|do|list|else)\b/, token: "keyword", indent: true},
            {regex: /(true|false|null)\b/, token: "atom"},
            {regex: /0x[a-f\d]+|[-+]?(?:\.\d+|\d+\.?\d*)(?:e[-+]?\d+)?/i, token: "number"},
            {regex: /(?:from|to)\b/, token: "number"},
            {regex: /[\{\[\(]/, indent: true},
            {regex: /[\}\]\);]/, dedent: true},
            {regex: /[a-z$][\w$]*/, token: "variable"},
            {regex: /^\s*--\s*%.*/, token: "comment meta"},
            {regex: /--.*/, token: "comment"},
        ]
    });
    CodeMirror.defineMIME('text/x-macaulay2', 'macaulay2');
});
