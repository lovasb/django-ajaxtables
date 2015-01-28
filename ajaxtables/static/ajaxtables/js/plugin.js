(function($) {
    function AjaxTable(el, options) {
        this.element = el;
        this.url = el.data("ajaxsource") || window.location.href.split('?')[0];
        this.post = el.data("post");
        this.method = this.post === undefined ? 'get' : 'post';
        this.onReload = options.onReload;
        this.onReload = options.onReload;

        this.displayFilters = {
            sort_by: {},
            hidden_cols: []
        };

        this.init = function() {
            page_size = $.cookie("page_size") || el.data("pagesize") || 10;
            $.cookie("page_size", page_size);

            var self = this;
            $.each($("th.at-sort", this.element), function(i, o){
                var elem = $(o);
                var elem_id = elem.attr('id');
                var sortButton = document.createElement('span');
                elem.prepend(sortButton);

                $(sortButton).addClass('at-btn at-sort-btn glyphicon glyphicon-sort')
                    .click(function(){
                        var elem = $(this);
                        if(elem.hasClass('glyphicon-sort')){
                            elem.removeClass('glyphicon-sort').addClass('glyphicon-sort-by-attributes at-btn-pressed');
                            delete self.displayFilters.sort_by[elem_id];
                            self.displayFilters.sort_by[elem_id] = {value: elem_id};

                            self.reload();
                        }
                        else if(elem.hasClass('glyphicon-sort-by-attributes')){
                            elem.removeClass('glyphicon-sort-by-attributes').
                                addClass('glyphicon-sort-by-attributes-alt at-btn-pressed');
                            delete self.displayFilters.sort_by[elem_id];
                            self.displayFilters.sort_by[elem_id] = {value: '-' + elem_id};

                            self.reload();
                        }
                        else if(elem.hasClass('glyphicon-sort-by-attributes-alt')){
                            elem.removeClass('glyphicon-sort-by-attributes-alt').addClass('glyphicon-sort');
                            elem.removeClass('at-btn-pressed');
                            delete self.displayFilters.sort_by[elem_id];

                            self.reload();
                        }
                    });
            });

            $.each($("th.at-hide", this.element), function(i, o) {
                var elem = $(o);
                var elem_id = elem.attr('id');
                var col_index = elem.index() + 1;

                var hideButton = document.createElement('span');
                elem.append(hideButton);
                $(hideButton).addClass('at-btn at-hide-btn glyphicon glyphicon-remove')
                    .click(function(){
                        self.displayFilters.hidden_cols.push({
                            'value': elem_id,
                            'col_index': col_index
                        });
                        $("thead th:nth-child(" + col_index + "), tbody td:nth-child(" + col_index + ")", self.element).hide();
                        self.showHidden.show();
                        self.reload();
                    });
            });

            $.each($('.at-show-hidden', this.element), function (i, o) {
                var elem = $(o);
                var showHidden = $(document.createElement('span'));
                showHidden.attr('title','Show hidden columns');
                showHidden.addClass('at-btn glyphicon glyphicon-eye-open').hide();
                elem.append(showHidden);

                showHidden.click(function(){
                    $.each(self.displayFilters.hidden_cols, function (i, col) {
                        $('thead th:hidden, tbody td:hidden', self.element).show();
                    });
                    self.displayFilters.hidden_cols = [];
                    self.showHidden.hide();
                    self.reload();
                });
                self.showHidden = showHidden;
            });

            this.reload();
        };
        
        this.reload = function(page) {
            var parent = this;
            page_size = $.cookie("page_size");
            act_page = page || $.cookie("act_page") || 1;

            $.ajax({
                url: parent.url + '?' + $.param($.extend($.QueryString, {'pageSize': page_size, 'page': act_page})),
                type: parent.method,
                data: (function(){
                    var serializedForm = $(parent.post).serializeArray();

                    $.each(parent.displayFilters, function (k, v) {
                        $.each(v, function (i, obj) {
                            serializedForm.push({
                                name: k,
                                value: obj.value
                            });
                        })
                    });

                    return serializedForm;
                    }()),
                async: false,
                success: function (retval) {
                    var html = $(retval);

                    $.each(parent.displayFilters.hidden_cols, function (i, o) {
                        $('tbody td:nth-child(' + o.col_index +')', html).hide();
                    });

                    var paginator = html.find('tfoot > tr > td[colspan]');
                    paginator.attr('colspan', paginator.attr('colspan') - parent.displayFilters.hidden_cols.length);

                    parent.element.find('tbody').html(html.find('tbody > tr'));
                    parent.element.find('tfoot').html(html.find('tfoot > tr'));
                    $('ul.pagination > li > a').click(function (e) {
                        e.preventDefault();
                    });
                }
            });
            
            /* Set the act_page in the cookie */
            act_page = $('ul.pagination > li.active > a').text() || 1;
            $.cookie('act_page', act_page);

            /* Bind the pagination links */
            $('ul.pagination > li:not(.active, .disabled) > a').click(function (e) {
                page = $(this).data('page');
                parent.reload(page);
            });

            /* Trigger onReload event */
            parent.onReload();
        };
    }

    $.fn.ajaxTable = function() {
        var option = arguments[0],
            args = arguments,
            allowedMethods = ["reload"];
         
        this.each(function() {
            var element = $(this);
            var data = $(this).data('ajaxTable');
            options = $.extend({}, $.fn.ajaxTable.defaults, typeof option === 'object' && option);

            if (!data) {
                data = new AjaxTable(element, options);
                $(this).data('ajaxTable', data);
            }
            if (typeof option === 'string') {
                if ($.inArray(option, allowedMethods) < 0) {
                    throw "Unknown method: " + option;
                }
                value = data[option]();
            } else {
                data.init();
            }
        });
    };

    $.fn.ajaxTable.defaults = {
        onReload: function() { return false;}
    };
})(jQuery);
