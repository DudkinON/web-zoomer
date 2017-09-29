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
    });
    $("#share-parent").on('click', function () {
        $("#share-container").toggle("slow");

    });
});