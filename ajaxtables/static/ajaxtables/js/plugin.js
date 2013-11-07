$.fn.ajaxTable = function() {
    var option = arguments[0]
    
    function AjaxTable(el, options) {
        this.element = el
        this.url = el.data("ajaxsource");
        this.post = el.data("post")
        this.method = this.post == undefined ? 'get' : 'post'
        
        this.init = function() {
            page_size = $.cookie("page_size") || el.data("pagesize") || 10;
            $.cookie("page_size", page_size);
            this.reload();
        }
        
        this.reload = function(page) {
            var parent = this;
            page_size = $.cookie("page_size");
            act_page = page || $.cookie("act_page") || 1;
            $.ajax({
                url: parent.url + '?' + $.param({'pageSize': page_size, 'actPage': act_page}),
                type: parent.method,
                data: $(parent.post).serialize(),
                async: false,
                success: function (retval) {
                    if (retval.tbody && retval.tfoot) {
                        parent.element.find('tbody').html(retval.tbody)   
                        parent.element.find('tfoot').html(retval.tfoot)
                    }

                    $('ul.pagination > li > a').click(function (e) {
                        e.preventDefault();
                    });
                }
            });
            
            /* Set the act_page in the cookie */
            act_page = $('ul.pagination > li.active > a').text() || 1
            $.cookie('act_page', act_page);

            /* Bind the pagination links */
            $('ul.pagination > li:not(.active, .disabled) > a').click(function (e) {
                page = $(this).data('page')
                parent.reload(page);
            });
        }
    };
          
    this.each(function() {
        var element = $(this)
        var data = $(this).data('ajaxTable')
        allowedMethods = ["reload"]

        if (!data) {
            data = new AjaxTable(element, arguments)
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