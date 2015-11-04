/**
 * controller.js: listeners and controllers for DNAinfo crime map
 * Author: NiJeL
 */


$( document ).ready(function() {

    $('#introduction').modal('show');
    $('#closeIntroModal').click(function() {
      $('#introduction').modal('hide');
    });

    $('#help').click(function() {
      $('#introduction').modal('show');
    });


    $('#imFinished').click(function() {
      OrgDraw.imFinished();
    });

    $('#startOver').click(function() {
      OrgDraw.startOver();
    });

});
