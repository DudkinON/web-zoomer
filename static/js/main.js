/**
 * Created by Web Zoomer on 5/16/17.
 */

function updateTags(obj) {

    var url = $(location).attr('href');

    var data = {
        'remove_tag': $(obj).data()['tagId'],
        'csrfmiddlewaretoken': $(obj).data()['csrf']
    };
    $.post(url, data, function (r) {
        console.log(r['csrf']);
        var tags = $('#tags-container');

        tags.html(function () {
            var block = '';
            for (var tag in r['data']) {
                block += '<div class="tag-container inline">' + r['data'][tag] + '\n' +
                    '       <i class="fa fa-times cursor-pointer close-button delete-tag"\n' +
                    '           aria-hidden="true" data-tag-id="' + tag + '"\n' +
                    '           data-csrf="' + r['csrf'] + '"></i>\n</div>';
            }
            return block;
        })
    });
}

jQuery(document).ready(function ($) {

    // start search code
    $("#search-icon").on('click', function () {
        $("#search-button").css("display", "block");
        $("#search-input").removeClass('hide');
        $("#search-icon").on('click', function () {
            var text = $("#search-icon").on('change', function (data) {
                return data;
            });
        });
    });
    $('#img-field').on('change', function () {
        $('#img-btn').show()
    });
    // share menu start
    $("#share-parent").on('mouseover', function () {
        $("#share-container").toggle("slow");
    }).on('click', function () {
        $("#share-container").toggle("slow");
    });
    $('.delete-tag').on('click', function () {
            var obj = this;
            updateTags(obj);
        });
}).ajaxComplete(function () {
        jQuery('.delete-tag').on('click', function () {
            var obj = this;
            updateTags(obj);
        });
    });