$("#add-event").submit(function (e) {
    alert("addevnt d ")

    // preventing from page reload and default actions
    e.preventDefault();
    // serialize the data for sending the form data.
    var serializedData = $(this).serialize();
    // make POST ajax call
    $.ajax({
        type: 'POST',
        url: "{% url 'afl_events:add_event' %}",
        data: serializedData,
        success: function (response) {
            // on successfull creating object
            // 1. clear the form.
            $("#add-event").trigger('reset');
            // 2. focus to nickname input 
            
           
        },
        error: function (response) {
            // alert the error if any error occured
            alert(response["responseJSON"]["error"]);
        }
    })

    $(function () {
      $('#myModal').modal('toggle');
    });
    window.location.reload();
})