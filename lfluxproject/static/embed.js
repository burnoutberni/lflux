$(document).ready(function() {
    if(document.cookie.length==0) {
        $('body').addClass('noSession');
        $('#mark_as_read').html('Luminous Flux usually saves when you last read each article, to highlight any changes when you next read it. Your browser does not allow this for embedded content.<br />Read the full version if you\'d like to use this feature!');
    }
});
