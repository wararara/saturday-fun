$(document).ready(function () {
	function checkIfValid (){
		err = 0;
		$('.form-control').each(function () {
			if($(this).val() == ''){
				$(this).addClass('is-invalid');
				err = 1
			}else{
				$(this).removeClass('is-invalid');
			}
		})
		if(window.location == '/'){

		}
		if($('#PASSWORDINPUT').val() != $('#PASSWORDREPEAT').val() && $('#PASSWORDINPUT').val() != ''){
			err = 1
			$('#PASSWORDINPUT').addClass('is-invalid');
			$('#PASSWORDREPEAT').addClass('is-invalid');
		}else{
			$('#PASSWORDINPUT').removeClass('is-invalid');
			$('#PASSWORDREPEAT').removeClass('is-invalid');
		}
		if (err){
			return false
		}else{
			return true
		}
	}
	$('#regBut').on('click',function(){
		alert(checkIfValid());
		if (checkIfValid()){
			$.ajax({
				method: "POST",
				url: "/ajax/registration",
				contentType: "application/json",
				dataType: "json",
				data: JSON.stringify({
					login: $('#LOGININPUT').val(),
					password: $('#PASSWORDINPUT').val(), 
					name: $('#NAMEINPUT').val(),
					surname: $('#SURNAMEINPUT').val(),
					phone: $('#NUMBERINPUT').val(),
					mail: $('#MAILINPUT').val(),
				})
			})
			.done(function(result) {
				window.location.href = '/login';
			});
		}
	});

	$('#logBut').on('click',function(){

			$.ajax({
				method: "POST",
				url: "/ajax/login",
				contentType: "application/json",
				dataType: "json",
				data: JSON.stringify({
					login: $('#LOGININPUT').val(),
					password: $('#PASSWORDINPUT').val(), 
					phone: $('#NUMBERINPUT').val(),
					mail: $('#MAILINPUT').val(),
				})
			})
			.done(function(result) {
				if(result.result)
				{
					window.location.href = '/mainpage';
				}
				else
				{
					$('#LOGININPUT').addClass('is-invalid');
					$('#PASSWORDINPUT').addClass('is-invalid');
					$('.invalid-feedback').html(result.error);
				}
			});
		
	})
})

$(document).keypress(function(e){
    if (e.which == 13){
        $("#logBut").click();
    }
});



