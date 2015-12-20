$('table').bootstrapTable({
    classes: 'table table-hover',
    height: getHeight(),
    striped: false,
    iconsPrefix: 'fa',
    iconSize: 'sm',
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
    pagination: true,
    onlyInfoPagination: false,
    showHeader: true,
    paginationVAlign: 'bottom',

    align: 'left',
    halign: 'center',
    falign: 'right',
    valign: 'middle',
    sortable: true,
    showColumns: true,
    
    locale:'en-US'

});
    
function getHeight() {
    return $(window).height() - $('.navbar').outerHeight(true) - $('h2').outerHeight(true) - $('footer').outerHeight(true);
}
