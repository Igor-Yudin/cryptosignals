$(function() {
  var form = $('#form_emit_signal');

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
          console.log('emit');
        }
      }
    })
  });
});