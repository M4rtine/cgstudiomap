//Script to simulate a form submit on a <a>
$('.a-submit').off('click').on('click', function () {
    $(this).closest('form').submit();
});
