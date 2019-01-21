define([
    'base/js/namespace',
    './macaulay2'
  ], function (Jupyter) {
    "use strict";

    return {
      load_ipython_extension: function () {
        // Jupyter.keyboard_manager.command_shortcuts.remove_shortcut('0,0');
        // Jupyter.keyboard_manager.command_shortcuts.add_shortcut('7,8,9', 'jupyter-notebook:restart-kernel');

        console.log('Loading Macaulay2 mode...');
      }
    };

  });
