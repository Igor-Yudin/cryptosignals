$(function() {
  var form = $('#form_subscribe');

  $(form).submit(function(event) {

    event.preventDefault();

    var formData = $(form).serialize();

    var email = $('#input_email').val();

    if (email == "")
      return;

    $.ajax({
      type: 'POST',
      url: $(form).attr('action'),
      data: formData,
      dataType: 'json',
      success: function(response) {
        if (response.is_ok == true) {
          console.log('subscribe');
          var btnSubscribe = $('#btn-subscribe');
          $('#modal_message').text(email + ", you've subscribed!");
          $('#input_email').val("");
          $(btnSubscribe.attr('data-target')).modal('show');
        }
      }
    })
  });
});