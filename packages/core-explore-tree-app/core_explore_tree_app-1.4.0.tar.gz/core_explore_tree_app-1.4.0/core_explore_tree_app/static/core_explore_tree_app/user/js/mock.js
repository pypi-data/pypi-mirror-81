$(document).ready( function() {
    var waitingTime = 500;
    setTimeout(function() {
        $('#tree-details').removeClass('hide');
        $('#tree-loading').hide();
        $('#explore-panel-loading').hide();
    }, waitingTime);
});

