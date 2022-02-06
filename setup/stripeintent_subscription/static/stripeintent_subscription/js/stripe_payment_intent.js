// A reference to Stripe.js
//https://stripe.com/docs/payments/payment-intents
//https://stripe.com/docs/payments/accept-a-payment
//https://stripe.com/docs/api/payment_methods/list
if (!$.isFunction(window.getCookie)) {
  function getCookie(cname) {
       var name = cname + "=";
       var ca = document.cookie.split(';');
       for(var i=0; i<ca.length; i++) {
          var c = ca[i];
          while (c.charAt(0)==' ') c = c.substring(1);
          if(c.indexOf(name) == 0)
             return c.substring(name.length,c.length);
       }
       return "";
  }
}

$(document).keypress(function(e){
  var keycode = (event.keyCode ? event.keyCode : event.which);
  if(keycode == '13'){
      alert('Please use pay now');
      e.preventDefault();
      return false;    
  }
});
$('#stripe-intent-form').submit(function(e){
  
  if ( typeof( e.isTrigger ) == 'undefined' ) {
    e.preventDefault();           
  }
});
var stripe;

var orderData = {
};
alert($("button[type='submit']").attr('initial-url'))
fetch($("button[type='submit']").attr('initial-url'))
  .then(function(result) {
    return result.json();
  })
  .then(function(data) {
    return setupElements(data);
  })
  .then(function({ stripe, card, clientSecret }) {

    //document.querySelector("#submit").addEventListener("click", function(evt) {
    $("button[type='submit']").on("click", function(evt){
      evt.preventDefault();
      // optionsval = $('input[name="payment_id"]').val()
      
      pay(stripe, card, clientSecret);
      
    });
  });

var setupElements = function(data) {
  stripe = Stripe(data.publicKey);
  /* ------- Set up Stripe Elements to use in checkout form ------- */
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

  var card = elements.create("card", { style: style,hidePostalCode: true });
  card.mount("#card-element");

  return {
    stripe,
    card,
    clientSecret: data.clientSecret
  };
};

var handleAction = function(clientSecret) {
  // Show the authentication modal if the PaymentIntent has a status of "requires_action"
  stripe.handleCardAction(clientSecret).then(function(data) {
    if (data.error) {
      // showError("Your card was not authenticated, please try again");
      fetch($("button[type='submit']").attr('pay-url'), {
        method: "POST",
        headers: new Headers({
          'X-CSRFToken': getCookie("csrftoken"),
          'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
          'X-Requested-With': 'XMLHttpRequest'
        }),
        body: JSON.stringify({
          'cancel': true,
        })
      })
        .then(function(result) {
          return result.json();
        })
        .then(function(json) {
          if (json.error) {
            showError(json.error);
          } else {
            orderComplete(clientSecret);
          }
        });
    } else if (data.paymentIntent.status === "requires_confirmation") {
      // Card was properly authenticated, we can attempt to confirm the payment again with the same PaymentIntent
      fetch($("button[type='submit']").attr('pay-url'), {
        method: "POST",
        headers: new Headers({
          'X-CSRFToken': getCookie("csrftoken"),
          'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
          'X-Requested-With': 'XMLHttpRequest'
        }),
        body: JSON.stringify({
          paymentIntentId: data.paymentIntent.id,
          payment_id:$('input[name="payment_id"]').val()
        })
      })
        .then(function(result) {
          return result.json();
        })
        .then(function(json) {
          if (json.error) {
            showError(json.error);
          } else {
            orderComplete(clientSecret);
          }
        });
    }
  });
};

/*
 * Collect card details and pay for the order 
 */
var pay = function(stripe, card) {
  // var cardholderName = document.querySelector("#name").value;
  var data = {
    billing_details: {}
  };

  // if (cardholderName) {
  //   data["billing_details"]["name"] = cardholderName;
  // }

  changeLoadingState(true);

  // Collect card details
  stripe
    .createPaymentMethod("card", card, data)
    .then(function(result) {
      if (result.error) {
        showError(result.error.message);
      } else {
        orderData.paymentMethodId = result.paymentMethod.id;
        
        //orderData.isSavingCard = document.querySelector("#save-card").checked;
        orderData.isSavingCard = true;
        orderData.exp_month = result.paymentMethod.card.exp_month;
        orderData.exp_year = result.paymentMethod.card.exp_year;
        orderData.last4 = result.paymentMethod.card.last4;
        orderData.payment_id = $('input[name="payment_id"]').val()
        var myHeaders = new Headers();
        myHeaders.append('Accept', 'application/json');
        myHeaders.append('Content-Type', 'application/json');
        myHeaders.append("X-CSRFToken", getCookie("csrftoken"));
        // return fetch($("button[type='submit']").attr('pay-url'), {
        //   method: "POST",
        //   headers: myHeaders,
        //   mode: 'cors',
        //   cache: 'default',
        //   body: JSON.stringify(orderData)
        // });
        return fetch($("button[type='submit']").attr('pay-url'), {
          method: 'POST',
          credentials: 'include',
          headers: new Headers({
            'X-CSRFToken': getCookie("csrftoken"),
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest'
          }),
          body: JSON.stringify(orderData),
        });
        // $.ajax({
        //   type: 'POST', url: $("button[type='submit']").attr('pay-url'), data: orderData,
        // }).done(function(res) {
        //   console.log(res);
        // });
      }
    })
    .then(function(result) {
      return result.json();
    })
    .then(function(paymentData) {
      if (paymentData.requiresAction) {
        // Request authentication
        handleAction(paymentData.clientSecret);
      } else if (paymentData.error) {
        showError(paymentData.error);
        console.log('*************paymentData.error*********8',paymentData.error)
        if(paymentData.redirect_url){
          window.location.href = paymentData.redirect_url;
        }
      } else {
        orderComplete(paymentData.clientSecret);
      }
    });
};

/* ------- Post-payment helpers ------- */

/* Shows a success / error message when the payment is complete */
var orderComplete = function(clientSecret) {
  stripe.retrievePaymentIntent(clientSecret).then(function(result) {
    var paymentIntent = result.paymentIntent;
    var paymentIntentJson = JSON.stringify(paymentIntent, null, 2);
    document.querySelectorAll(".payment-view").forEach(function(view) {
      view.classList.add("hidden");
    });
    document.querySelectorAll(".completed-view").forEach(function(view) {
      view.classList.remove("hidden");
    });
    // document.querySelector(".status").textContent =
    //   paymentIntent.status === "succeeded" ? "succeeded" : "failed";
    // document.querySelector("pre").textContent = paymentIntentJson;
    $('input[name="payment_intent"]').val(paymentIntent.id)
    $('input[name="status"]').val("confirmed")
    
    var form = $('button[type="submit"]').parents('form');
    form.submit()
  });
};

var showError = function(errorMsgText) {
  changeLoadingState(false);
  toastr.error('', errorMsgText);
};

// Show a spinner on payment submission
var changeLoadingState = function(isLoading) {
  
  old_html = $('button[type="submit"]').attr('label')
  if (isLoading) {
    document.querySelector("button").disabled = true;
    $("button[type='submit']").prop('disabled', true);
    // document.querySelector("#spinner").classList.remove("hidden");
    // document.querySelector("#button-text").classList.add("hidden");
    $('button[type="submit"]').html($('button[type="submit"]').attr("data-loading-text"))
    // $('button[type="submit"]').closest('form').hide()
    $('button[type="submit"]').closest('.stripe-card-container').prepend('<div class="stripe-loader"><div class="spinner01"><div class="spinner-flex"><div class="spinner-border" role="status"><span class="sr-only">Loading...</span></div></div></div><p class="text-center">Processing payment... please wait</p></div>');
  } else {
    $("button[type='submit']").prop('disabled', false);
    $('button[type="submit"]').html(old_html)
    // $('button[type="submit"]').closest('form').show()
    $('.stripe-loader').remove()
    
    // document.querySelector("#spinner").classList.add("hidden");
    // document.querySelector("#button-text").classList.remove("hidden");
  }
};



$(document).ready(function() {
  $(jQuery("body").find("[stripeintentsubscriptionoption-js]")).each(
      function() { // use . for class selectors
        stripeintentsubscriptionoption(this); // pass this from here
      }
  ); 
});

function stripeintentsubscriptionoption(obj){
  var obj_id = $(obj).attr('id');
  var obj_name = $(obj).attr('name');
  availableVal2 =  $('input[name='+obj_name+']:checked').val();
  $('input[name='+obj_name+']').unbind('change');
  $('input[name='+obj_name+']').change(function() {
      availableVal =  $('input[name='+obj_name+']:checked').val();
      if(availableVal ==0){
          $(obj).closest('form').find('.new-card-details').closest('div').fadeIn();

      } else {
         
          $(obj).closest('form').find('.new-card-details').closest('div').fadeOut();
      }
  });
  if(availableVal2 ==0){
    $(obj).closest('form').find('.new-card-details').closest('div').show();
 } else if(availableVal2 !=''){
    $(obj).closest('form').find('.new-card-details').closest('div').fadeOut();
 }

}
