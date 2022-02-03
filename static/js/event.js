$('#add_event').click(function (e) {  
    // new changes
    alert("ccccccclkdddss")
        $('#add_event').prop('disabled', true);
    // end
        console.log("ha ah a123123")
        e.preventDefault();
        $('.custom-loader').show();
        var form = $(this).parents('form');
        console.log(form);
        var data = new FormData($(this).parents('form').get(0));
        console.log(data);
        // $.each($('#id_image')[0].files, function(i, file) {
        //     data.append('image', file);
        // });
        var method = form.attr('method');
        var action = form.attr('action');
    
        $.ajax({
            url: action,
            type: method,
            data: data,
            cache: false,
            contentType: false,
            processData: false,
            beforeSend: function (xhr) {
                xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
            },
            success: function (data) {
            // new changes
                $('#add_event').prop('disabled', true);
                form.find('button').prop("disabled", true);
            // end
                $('.custom-loader').hide();
                if (data.status == true) {
                   window.location.reload();
                }else{
                    $('.action-bar-content').html(data.rendered);
    // new changes
                    $('#add_event').prop('disabled', false);
    // end
                }
            }
        });
    // new changes
        //document.getElementById(add_event).disabled = true;
    // end
        
    