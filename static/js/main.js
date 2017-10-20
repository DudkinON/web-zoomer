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

    //tooltip
    $(function () {
        $('[data-toggle="tooltip"]').tooltip()
    });

    // image button show
    $('#img-field').on('change', function () {
        $('#img-btn').show()
    });

    // share menu start
    $("#share-parent").on('mouseover', function () {
        $("#share-container").toggle("slow");
    }).on('click', function () {
        $("#share-container").toggle("slow");
    });

    // delete tag
    $('.delete-tag').on('click', function () {
        updateTags(this);
    });

    // like
    $('.like').on('click', function () {
        var like = $('.like');
        var dislike = $('.dislike');
        if (!like.hasClass('liked')) {
            if ($(this).data()['uid'] !== 'None') {
                var url = $(location).attr('href');
                var data = {
                    'csrfmiddlewaretoken': $(this).data()['csrf'],
                    'like': 1
                };
                $.post(url, data, function (r) {
                    if (dislike.hasClass('disliked')) dislike.removeClass('disliked');
                    if (!like.hasClass('liked')) like.addClass('liked');
                    like.data()['csrf'] = r['csrf'];
                    dislike.data()['csrf'] = r['csrf'];
                    $('#likes').text(r['likes']);
                    $('#dislikes').text(r['dislikes']);
                })
            }
        }

    });

    // dislike
    $('.dislike').on('click', function () {
        var like = $('.like');
        var dislike = $('.dislike');
        if (!dislike.hasClass('disliked')) {
            if ($(this).data()['uid'] !== 'None') {
                var url = $(location).attr('href');
                var data = {
                    'csrfmiddlewaretoken': $(this).data()['csrf'],
                    'like': 0
                };
                $.post(url, data, function (r) {
                    if (!dislike.hasClass('disliked')) dislike.addClass('disliked');
                    if (like.hasClass('liked')) like.removeClass('liked');
                    like.data()['csrf'] = r['csrf'];
                    dislike.data()['csrf'] = r['csrf'];
                    $('#likes').text(r['likes']);
                    $('#dislikes').text(r['dislikes']);
                })
            }
        }
    })

}).ajaxComplete(function () {
    // update DOM delete tag
    jQuery('.delete-tag').on('click', function () {
        updateTags(this);
    });
});