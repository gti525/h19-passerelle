$('select').material_select();

function hidee() {
  if ($("#userType option:selected").val() == 'admin'){
$("#username").prop('disabled', true);
$("#account_number").prop('disabled', true);
}
else{
$("#username").prop('disabled', false);
$("#account_number").prop('disabled', false);
}
}