$('.a-submit').off('click').on('click', function () {
    console.log('a-submit');
    console.log(this);
    console.log($(this).closest('form'));
    $(this).closest('form').submit();
});
