setInterval(function (){
    $(document).ready(function() {
        $('#divMain').load('complete_cmd.html #divMain', function () {
            $('#divMain .child').slice(0 , -6).remove()
        });});},1000)