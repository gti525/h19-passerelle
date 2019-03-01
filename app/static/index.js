$('select').material_select();

function hidee() {
  if ($("#userType option:selected").val() == 'admin'){
$("#username").css("display","none");
}
else{
$("#username").css("display","block");
}
}