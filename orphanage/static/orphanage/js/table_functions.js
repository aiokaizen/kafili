
// select all checkboxes
$('#select_all').click(function() {
    let check_boxes = $('.item_select');
    if ($(this).is(':checked')) {
        check_boxes.attr('checked', true);
    } else {
        check_boxes.attr('checked', false);
    }
});