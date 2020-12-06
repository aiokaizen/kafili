
function delete_instance(message, action_name='delete', id=null) {
    swal({
        title: "تحذير",
        text: message,
        icon: "error",
        buttons: ['إلغاء', 'تأكيد'],
        dangerMode: true,
    }).then((willDelete) => {
        if (willDelete) {
            let form_str = '<form method="POST" id="delete_form">' + csrf_token;
            if (id !== null) {
                form_str = form_str + '<input type="hidden" name="id" value="' + id + '">'
            }
            form_str = form_str + '<input type="hidden" name="action" value="' + action_name + '"></form>'
            $('body').append(form_str);
            let form = $("#delete_form");
            form.append($(".item_select").clone());
            form.submit();
        }
    });
}


function delete_selected_items(message) {
    
    if ($('.item_select:checked').length == 0) {
        swal({
            title: "تحذير",
            text: "لم تقم بإختيار أي عنصر من القائمة",
            icon: "warning",
            button: {
                text: "حسنا",
                value: true,
                visible: true,
                className: "",
                closeModal: true,
            }
        });
    }
    else {
        swal({
            title: "تحذير",
            text: message,
            icon: "error",
            buttons: ['إلغاء', 'تأكيد'],
            dangerMode: true,
        }).then((willDelete) => {
            if (willDelete) {
                $('body').append(`
                    <form method="POST" id="delete_form">
                    ` + csrf_token + `
                        <input type="hidden" name="action" value="delete_multiple">
                    </form>
                `);
                let form = $("#delete_form");
                form.append($(".item_select").clone());
                form.submit();
            }
        });
    }
}
