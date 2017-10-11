/**
 * Created by Web Zoomer on 5/16/17.
 */

jQuery(document).ready(function ($) {

    // start search code
    $("#search-icon").on('click', function () {
        $("#search-button").css("display", "block");
        $("#search-input").removeClass('hide');
        $("#search-icon").on('click', function () {
            var text = $("#search-icon").on('change', function (data) {
                return data;
            });
            console.log(text)
        });
    });

    // share menu start
    $("#share-parent").on('mouseover', function () {
        $("#share-container").toggle("slow");
    }).on('click', function () {
        $("#share-container").toggle("slow");

    });

});

function getName (str){
    var slash = '';
    if (str.lastIndexOf('\\')) slash = '\\';
    else slash = '/';
    var img = str.slice(str.lastIndexOf(slash) + 1);
    if (img.length > 30) img = img.substr(0,15) + '.....' + img.substr(img.length - 7,img.length);
    jQuery('#file-form-label').text(img);
}