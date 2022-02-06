$(document).ready(function () {
    
   
    // update taxtypes
    $('.stripeintent-approve-btn').click(function () { 
       var loader_alert ="Payment approval proccessing... ";
       obj =  $('.stripeintent-approve-btn')
       stripeintent_submit(obj,'approve',loader_alert) 
    });
    $('.stripeintent-cancel-btn').click(function () {  
        var loader_alert ="Payment decline proccessing... ";
        obj =  $('.stripeintent-cancel-btn')
        stripeintent_submit(obj,'cancel',loader_alert);
     });
    // $('.stripeintent-submit-btn').click(function () {  
    //     var loader_alert ="Payment submit proccessing... ";
    //     obj =  $('.stripeintent-submit-btn')
    //     stripeintent_submit(obj,'submit',loader_alert);
    // });
    $('[data-toggle="m-tooltip"]').popover(
        {
            placement : 'top',
            trigger : 'hover'
            
        }
    ); 

    
});
function stripeintent_submit(obj,type="submit",loader_alert="Payment submit proccessing... "){
    var form = $(obj).parents('form');
    
    var method = form.attr('method');
    var action = form.attr('action');
    //$('input[name="stripeintent-awaiting_timer_count"]').val(parseInt($('input[name="stripeintent-awaiting_timer_count"]').val())+1)
    // var data = form.serialize()+ '&go=ok'+'&attr_id='+attr_id;
    var loading ='<div class="d-flex align-items-center"><strong>'+loader_alert+'</strong><div class="spinner-border ml-auto" role="status" aria-hidden="true"></div></div>'
    var data = new FormData(form.get(0));  
    data.append('go', 'ok'); 
    data.append('type',type); 
    message ='Are you sure?';
    var message_body = "You won't be able to revert this!"
    if (typeof $(obj).attr('message') !== typeof undefined && $(obj).attr('message') !== false) {
       message_body = $(obj).attr('message');
    }  
    if(data){
        swal({
            title: message,
            text: message_body,
            type: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Yes, Proceed it!',
            buttons:true,//The right way
            buttons: ["No", "Yes"] //The right way to do it in Swal1
        }).then((result) => {
            if (result.value || result === true) {
                $.ajax({
                    type: method,
                    url: action, 
                    data: data,
                    cache: false,
                    contentType: false,
                    processData: false,
                    beforeSend: function(xhr) {
                        xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
                        $('.custom-loader').show();
                        $("button[type='button']").attr("disabled", true);
                        $('.action-bar-content').children().html(loading);
                    },
                    success: function (data2) {
                        $('.custom-loader').hide();
                        if(data2.success){
                            $('#action-sidebar').css(
                                {
                                    'width': '0px',
                                
                                }
                            );
                            $('#action-sidebar').removeClass('show-menu');
                        
                            if(data2.message){
                                toastr.success(data2.message, 'Success');
                            }
                            if(data2.page_refresh){
                                location.reload();
                            }
                        }else{
                            $('.action-bar-content').html(data2);
                        }
                        $("button[type='button']").attr("disabled", false);
                    }
                });
            }
        });
    }
}
