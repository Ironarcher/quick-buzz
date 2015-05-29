<script type=text/javascript>
  var status = ""
  var error = "none"
  $(function() {
    var start_game = function(e){
      $.getJSON($SCRIPT_ROOT + '/startlobby', {
        player1: ""
        set_id: $("#set_select").val()
      }, function(data) {
        $("#creator").text(data.result["creator"]);
        $("#category").text(data.result["category"]);
        $("#lobby_id").text(data.result["lobby_id"]);
        error = d
      });
      return false;
    };

    var next_question = function(e){

      $('#startgame').bind('click', function() {
        $.getJSON($SCRIPT_ROOT + '/nextquestion', {

        }, function(data){
          
      });
      return false; 
    };

    $('#startgame').bind('click', start_game);
    $('#startgame').bind('click', next_question)
  });

</script>