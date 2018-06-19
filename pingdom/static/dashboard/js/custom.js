/**
 * Created by faisal on 29/7/16.
 */
(function () {
    $(document).on('click', '#mail_sent', function (event) {
        site_id = $('#mail_sent').attr('name');
        jQuery.ajax({
            type: 'GET',
            url: "/email/" + site_id,
            data: "",
            success: function () {
                $('.alert-dismissable').css('display', 'block');
            },
            error: function () {
                console.log('Some Error has occurred');
            }
        });
        event.preventDefault();
    });

})();

function checknow(site) {
    $('#enter').attr('href', '/create_edit_site/?delete_site_id=' + site);

}

function site_update(site_id, id) {
    value = id
    if (value == 'True') {
        var auto_test_mode = 1

    }
    else {
        var auto_test_mode = 0
    }
    jQuery.ajax({
        type: 'GET',
        url: "/create_edit_site/?auto_test_mode",
        data: {'auto_test_mode': auto_test_mode, 'site_id': site_id},
        success: function (data) {
            location.reload()
        },
        error: function (data) {
        }

    });
}

function find() {
    if (event.key == "Enter") {
        var value = $('#search').val()
        if (!value) {
            $('#search').attr('placeholder', 'Please type Search Keyword');
            $('#search').css('border-color', 'red');
            return false;
        }
        jQuery.ajax({
            type: 'GET',
            url: "/dashboard",
            data: {'name': value},
            success: function (response) {
                $('.ajax-content').html(response)
            },
            error: function (data) {
            }

        });
    }


}
$(document).on('click', '.pagination li a', function (e) {
    e.preventDefault();
    var mypath = $(this).attr('href');
    mypath = mypath.replace('?', '');
    $.ajax({
        type: 'get',
        url: "/dashboard",
        data: mypath,
        success: function (response) {
            $('.ajax-content').html(response)
        },
        error: function () {
        }
    });
});
