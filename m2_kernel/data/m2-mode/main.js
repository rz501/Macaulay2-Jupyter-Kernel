define([
    'base/js/namespace',
    './macaulay2'
  ], function (Jupyter) {
    "use strict";

    return {
      load_ipython_extension: function () {
        // Jupyter.keyboard_manager.command_shortcuts.remove_shortcut('9,0');
        Jupyter.keyboard_manager.command_shortcuts.add_shortcut('9,0', 'jupyter-notebook:restart-kernel-and-clear-output');
        console.log('Loading Macaulay2 mode...');

      }
    };

  });
