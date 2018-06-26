define([
    'base/js/namespace',
    './macaulay2'
  ], function (Jupyter) {
    "use strict";

    return {
      load_ipython_extension: function () {
        console.log('Loading Macaulay2 Mode...');
      }
    };

  });
