'use strict';

const fichaArticulo = (() => {

$(() => $('.ask-art-date').datetimepicker({
    format:'d-M-Y, H:i'
}));

jQuery.datetimepicker.setLocale('es');

$('#edit_admin_click').click(function(){
    $('#f-art-form-modify').toggleClass('f-art-modify-default');
    $('#f-art-form-modify').toggleClass('f-art-modify-active');
    //console.log($('.f-art-modify-default').classList)
});

const notifyIfRequestDone = (shouldNotify, msg) => {
  if (!shouldNotify){
      return;
  }
  $.notify({
     message: msg
  }, {
      type: 'success'
  });
};

const notifyIfError = (error_msg) => {
    if(!error_msg || error_msg.length === 0){
        return;
    }

    $.notify({
       message: error_msg
    }, {
        type: 'danger'
    });
};


return {
    notifyIfRequestDone: notifyIfRequestDone,
    notifyIfError: notifyIfError
};
})();
