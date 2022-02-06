

$(window).keydown(function(event){
  if(event.keyCode == 13) {
      event.preventDefault();
      return false;
  }
});

$(document).ready(function () {
    
    componentWillUnmount()
    public_key = $('button[afl-operation="add"]').attr('public_key')
    ////alert(public_key)
    var stripe = Stripe(public_key);
    var elements = stripe.elements();
    var style = {
      base: {
        color: "#32325d",
        fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
        fontSmoothing: "antialiased",
        fontSize: "16px",
        "::placeholder": {
          color: "#aab7c4"
        }
      },
      invalid: {
        color: "#fa755a",
        iconColor: "#fa755a"
      }
    };
    var cardElement = elements.create('card', { style: style,hidePostalCode: true });
    cardElement.mount('#card-element');

    $('[data-toggle="m-tooltip"]').popover(
        {
            placement : 'top',
            trigger : 'hover'
            
        }
    ); 
    $('button[afl-operation="add"]').click(function (e) {
        e.preventDefault();
        clientSecret = $(this).attr('client_secret');
        var button = $(this)
        var form = $(this).parents('form');
        var method = form.attr('method');
        var action = form.attr('action');
        var data = form.serialize() + '&go=ok';
        stripe.confirmCardSetup(
            clientSecret,
            {
              payment_method: {
                card: cardElement,
                // billing_details: {
                //   name: cardholderName.value,
                // },
              },
            }
          ).then(function(result) {
            if (result.error) {
                //console.log('******************error*********************88')
                //console.log(result.error)
                showError(result.error.message)
            } else {
              //console.log('******************cardButtonsss*dddd*********************88')
              //console.log(result.setupIntent.id)
              // The setup has succeeded. Display a success message.
              $('input[name="setup_intent"]').val(result.setupIntent.id)
              //alert('selup intent')
              //alert($('input[name="setup_intent"]').val())
              //data2 = $.extend(form.serialize(), { setup_intent: result.id });
              data2 = form.serialize();
            //   data2 = form.serialize()
              //console.log(data2)
              $.ajax({
                  type: 'POST',
                  url: action,
                  data: data2,
                  beforeSend: function (xhr) {
                      xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
                      changeLoadingState(true);
                      
                  },
                  success: function (data2) {
                      //alert('success')
                      changeLoadingState(false);
                      if (data2.success) {
                          $('#action-sidebar').css(
                              {
                                  'width': '0px',
  
                              }
                          );
                          $('#action-sidebar').removeClass('show-menu');
                          if (data2.message) {
                              toastr.success(data2.message, 'Success');
                          }
                          if (data2.page_refresh) {
                              location.reload();
                          }
                      } else {
                          $('.action-bar-content').html(data2);
                      }
  
                  }
              });
            }
        });
    });
    


});

var showError = function(errorMsgText) {
    changeLoadingState(false);
    toastr.error(errorMsgText);
  };
  
// Show a spinner on payment submission
var changeLoadingState = function(isLoading) {
  
    old_html = $('button[afl-operation="add"]').attr('label')
    if (isLoading) {
      document.querySelector("button").disabled = true;
      $("button[afl-operation='add']").prop('disabled', true);
      // document.querySelector("#spinner").classList.remove("hidden");
      // document.querySelector("#button-text").classList.add("hidden");
      $('button[afl-operation="add"]').html($('button[afl-operation="add"]').attr("data-loading-text"))
      $('button[afl-operation="add"]').closest('form').hide()
      $('button[afl-operation="add"]').closest('.stripe-card-container').prepend('<div class="stripe-loader d-flex align-items-center"><strong>Saving card Processing... please wait.</strong><div class="spinner-border ml-auto" role="status" aria-hidden="true"></div></div>')
    } else {
      $('button[afl-operation="add"]').prop('disabled', false);
      $('button[afl-operation="add"]').html(old_html)
      $('button[afl-operation="add"]').closest('form').show()
      $('.stripe-loader').remove()
      // document.querySelector("#spinner").classList.add("hidden");
      // document.querySelector("#button-text").classList.remove("hidden");
    }
  };
function componentWillUnmount() {
    let ivan = document.getElementsByTagName("iframe");
    let i = 0;
    while (i < ivan.length) {
      if (ivan[i].name.startsWith("__privateStripeFrame")) {
        ivan[i].remove()
      }
      i += 1;
    }
    // this.state.prButton.destroy('#payment-request-button');
    // let dave = document.getElementById('payment-request-button');
    // dave.removeChild(dave.firstChild)
}
