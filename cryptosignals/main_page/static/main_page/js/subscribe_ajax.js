$(function() {
  var form = $('#form_subscribe');

  $(form).submit(function(event) {

    event.preventDefault();

    var formData = $(form).serialize();

    $.ajax({
      type: 'POST',
      url: $(form).attr('action'),
      data: formData,
      dataType: 'json',
      success: function(response) {
        if (response.is_ok == true) {
          console.log('subscribe');
          var btnSubscribe = $('#btn-subscribe');
          // btnSubscribe.attr('data-toggle', 'modal');
          // btnSubscribe.attr('data-target', '#exampleModal');
          // btnSubscribe.click();
          $(btnSubscribe.attr('data-target')).modal('show');
        }
      }
    })
  });
});