define([
    'base/js/namespace',
    'jquery',
    'base/js/utils',
    'base/js/dialog',
    'base/js/events'
], function (Jupyter, $, utils, dialog, events) {

    var spinner = $('<p/>').html('<svg width="38" height="38" viewBox="0 0 38 38" xmlns="http://www.w3.org/2000/svg" stroke="#fff"> <g fill="none" fill-rule="evenodd"> <g transform="translate(1 1)" stroke-width="2"> <circle stroke-opacity=".5" cx="18" cy="18" r="18"/> <path d="M36 18c0-9.94-8.06-18-18-18"> <animateTransform attributeName="transform" type="rotate" from="0 18 18" to="360 18 18" dur="1s" repeatCount="indefinite"/> </path> </g> </g></svg>').css({
        'display': 'table-cell',
        'vertical-align': 'middle'
    });
    var spinner_overlay = $('<div/>').append(spinner).css({
        display: 'table',
        position: 'fixed',
        top: 0,
        left: 0,
        width: '100%',
        height: '100%',
        background: 'rgba(0,0,0,0.5)',
        'text-align': 'center',
        'z-index': '999'
    });

    var getCookie = function(name) {
      var match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
      if (match) return match[2];
    };

    var loader = function (action) {

        if (action === 'show' && !$('body').find(spinner_overlay).length)
            $('body').append(spinner_overlay);
        else
            spinner_overlay.remove();
    };

    var nbresetall = function () {
        dialog.modal({
            title: "Reset all notebooks to original",
            keyboard_manager: IPython.notebook.keyboard_manager,
            body: "This will undo all your modifications",
            buttons : {
                "Cancel": {},
                "OK": {
                    class: "btn-primary",
                    click: function () {
                        loader('show');

                        var data = {
                            _xsrf : getCookie('_xsrf')
                        };

                        var nbresetAllUrl = utils.url_path_join(utils.get_body_data('baseUrl'), 'nbresetall');
                        $.post(nbresetAllUrl, data, function () {
                            window.onbeforeunload = function (e) {
                              console.log('reload after reset');
                            };
                            window.location.reload(true)
                        })
                    }
                }
            },
            open : function (event, ui) {
                var that = $(this);
                // Upon ENTER, click the OK button.
                that.find('input[type="text"]').keydown(function (event, ui) {
                    if (event.which === 13) {
                        that.find('.btn-primary').first().click();
                        return false;
                    }
                });
                that.find('input[type="text"]').focus().select();
            }
        });
    };

    var nbreset = function () {
        dialog.modal({
            title: "Reset notebook to original",
            keyboard_manager: IPython.notebook.keyboard_manager,
            body: "This will undo all your modifications",
            buttons : {
                "Cancel": {},
                "OK": {
                    class: "btn-primary",
                    click: function () {
                        loader('show');

                        var data = {
                            nburl : Jupyter.notebook.metadata.nbreset,
                            nbpath : Jupyter.notebook.notebook_path,
                            _xsrf : getCookie('_xsrf')
                        };

                        var nbresetUrl = utils.url_path_join(utils.get_body_data('baseUrl'), 'nbreset');
                        $.post(nbresetUrl, data, function (data) {
                            window.onbeforeunload = function (e) {
                              console.log('reload afetr reset');
                            };
                            window.location.reload(true)
                        })
                    }
                }
            },
            open : function (event, ui) {
                var that = $(this);
                // Upon ENTER, click the OK button.
                that.find('input[type="text"]').keydown(function (event, ui) {
                    if (event.which === 13) {
                        that.find('.btn-primary').first().click();
                        return false;
                    }
                });
                that.find('input[type="text"]').focus().select();
            }
        });
    };

    var init_buttons = function () {
        var $running_notebooks_button = $('' +
            '<li id="running_notebooks" role="none" title="See all running notebooks">' +
            '  <a href="../../../tree#running" role="menuitem">Running notebooks</a>' +
            '</li>'
        );
        var $reset_all_button = $('' +
            '<li id="reset_all_to_original" role="none" title="Reset all notebooks to their original content">' +
            '  <a href="#" role="menuitem">Reset all to original</a>' +
            '</li>'
        );
        var $reset_button = $('' +
            '<li id="reset_to_original" role="none" title="Reset this notebook to its original content">' +
            '  <a href="#" role="menuitem">Reset to original</a>' +
            '</li>'
        );
        $reset_all_button.insertAfter('#restore_checkpoint');
        $reset_button.insertAfter('#restore_checkpoint');
        $running_notebooks_button.insertAfter('#restore_checkpoint');

        $reset_all_button.click(nbresetall);
        $reset_button.click(nbreset);
    };

    var load_ipython_extension = function () {
        init_buttons();
    };

    return {
        load_ipython_extension: load_ipython_extension,
    };

});