'use strict';

const fichaArticulo = (() => {

$(() => $('.ask-art-date').datetimepicker({
    format:'Y-m-d H:m'
}));

jQuery.datetimepicker.setLocale('es');

let notifyIfRequestDone = (shouldNotify) => {
  if (!shouldNotify){
      return;
  }
  $.notify({
     message: 'Reserva solicitada!'
  }, {
      type: 'success'
  });
};


return {
    notifyIfRequestDone: notifyIfRequestDone
};
})();
