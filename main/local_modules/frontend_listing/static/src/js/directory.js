function bootstrap_table_ajax(search, status) {
    $.ajax({
        type: "post",
        url: "/directory/get_partners",
        data: {search: search, company_status: status},

        complete: function(){
            $('#loading-image').hide();
        },

        success: function (response) {
            var data = JSON.parse(response);
            $('table').bootstrapTable({
                classes: 'table table-no-bordered table-hover',
				height: getHeight(),
                striped: true,
                iconsPrefix: 'fa',
                iconSize: 'md',
                icons: {
                    paginationSwitchDown: 'glyphicon-collapse-down icon-chevron-down',
                    paginationSwitchUp: 'glyphicon-collapse-up icon-chevron-up',
                    refresh: 'glyphicon-refresh icon-refresh',
                    toggle: 'glyphicon-list-alt icon-list-alt',
                    columns: 'glyphicon-th icon-th',
                    detailOpen: 'glyphicon-plus icon-plus',
                    detailClose: 'glyphicon-minus icon-minus'
                },
                cache: true,
                pageSize: 25,

                pagination: true,
                onlyInfoPagination: false,
                showHeader: true,
                paginationVAlign: 'bottom',

                align: 'left',
                halign: 'center',
                falign: 'right',
                valign: 'middle',
                sortable: true,
                showColumns: false,

                locale: 'en-US',
                columns: [
                    {
                        field: 'logo',
                        title: 'Logo'

                    },
                    {
                        field: 'name',
                        title: 'Name'
                    },
                    {
                        field: 'email',
                        title: 'Email'
                    },
                    {
                        field: 'industries',
                        title: 'Industries'
                    },
                    {
                        field: 'location',
                        title: 'Location'
                    }
                ],
                data: data
            });

        }
    });
}

function getHeight() {
    return $(window).height() - $('.navbar').outerHeight(true) - $('footer').outerHeight(true) -122;
}


(function ($) {
    'use strict';
    $.fn.bootstrapTable.locales['en-US'] = {
        formatLoadingMessage: function () {
            return 'Loading, please wait...';
        },
        formatRecordsPerPage: function (pageNumber) {
            return pageNumber + ' studios per page';
        },
        formatShowingRows: function (pageFrom, pageTo, totalRows) {
            return '';
        },
        formatSearch: function () {
            return 'Search';
        },
        formatNoMatches: function () {
            return 'No matching records found';
        },
        formatPaginationSwitch: function () {
            return 'Hide/Show pagination';
        },
        formatRefresh: function () {
            return 'Refresh';
        },
        formatToggle: function () {
            return 'Toggle';
        },
        formatColumns: function () {
            return 'Columns';
        },
        formatAllRows: function () {
            return 'All';
        }
    };

    $.extend($.fn.bootstrapTable.defaults, $.fn.bootstrapTable.locales['en-US']);

})(jQuery);