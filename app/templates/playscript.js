<script type=text/javascript>
  $(function() {
    $('a#calculate').bind('click', function() {
      $.getJSON($SCRIPT_ROOT + '/_add_numbers', {
        player1: $('getCurrentUserId()').val(),
      }, function(data) {
        $("#result").text(data.result);
      });
      return false;
    });
  });

</script>