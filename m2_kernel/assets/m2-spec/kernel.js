define([
    'base/js/namespace'
], function(Jupyter) {
    "use strict";

    // taken from https://jupyter-notebook.readthedocs.io/en/stable/extending/frontend_extensions.html

    return { onload: function() {
            var handler = function () {
                alert('testing !!!');
            };
            var action = {
                icon: 'fa-comment-o', // a font-awesome class used on buttons, etc
                help: 'Show an alert',
                help_index : 'zz',
                handler : handler
            };
            var prefix = 'my_extension';
            var action_name = 'show-alert';
            var full_action_name = Jupyter.actions.register(action, action_name, prefix); // returns 'my_extension:show-alert'

            Jupyter.toolbar.add_buttons_group([full_action_name]);
        }
    }
})