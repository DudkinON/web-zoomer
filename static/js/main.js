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

function bookmark(obj) {
    var e = obj;
    var url = $(location).attr('href');
    var bookmark;
    if ($(e).data("bookmark") === 0) bookmark = 1;
    else bookmark = 0;
    var data = {
        "csrfmiddlewaretoken": $(e).data("csrf"),
        "article_id": $(e).data("article-id"),
        "bookmark": bookmark
    };
    $.post(url, data, function (callback) {
        console.log(callback['title']);
        $(e).attr('data-csrf', callback['csrf']);
        $(e).attr('data-bookmark', callback['bookmark']);
        $(e).tooltip('dispose');
        $(e).attr('title', callback['title']);
        $(e).tooltip('show');
        if ($(e).hasClass('green')) {$(e).removeClass('green');}
        else {$(e).addClass('green');}
    });
}

jQuery(document).ready(function ($) {

    //search focus
    $('#search-input').focus();

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

    // edit profile control
    $('.edit-name').on('click', function () {
        $('#user-full-name').toggle();
        $('#first-name').toggle().focus();
        $('#last-name').toggle();
    });

    // edit first and last name user
    $('#first-name').on('change', function () {
        var firstName = $(this).val();
        $('#first-name-output').text(firstName);
    });
    $('#last-name').on('change', function () {
        var lastName = $(this).val();
        $('#last-name-output').text(lastName);
    });

    // add/remove bookmark
    $('.bookmark-article').on('click', function () {
        bookmark(this);
    });


    // like
    $('.like').on('click', function () {
        var like = $('.like');
        var dislike = $('.dislike');
        if (!like.hasClass('liked')) {
            if ($(this).data('uid') !== 'None') {
                var url = $(location).attr('href');
                var data = {
                    'csrfmiddlewaretoken': $(this).data()['csrf'],
                    'like': 1
                };
                $.post(url, data, function (r) {
                    if (dislike.hasClass('disliked')) dislike.removeClass('disliked');
                    if (!like.hasClass('liked')) like.addClass('liked');
                    like.attr('data-csrf', r['csrf']);
                    dislike.attr('data-csrf', r['csrf']);
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
            if ($(this).data('uid') !== 'None') {
                var url = $(location).attr('href');
                var data = {
                    'csrfmiddlewaretoken': $(this).data('csrf'),
                    'like': 0
                };
                $.post(url, data, function (r) {
                    if (!dislike.hasClass('disliked')) dislike.addClass('disliked');
                    if (like.hasClass('liked')) like.removeClass('liked');
                    like.attr('data-csrf', r['csrf']);
                    dislike.attr('data-csrf', r['csrf']);
                    $('#likes').text(r['likes']);
                    $('#dislikes').text(r['dislikes']);
                });
            }
        }
    });
}).ajaxComplete(function () {
    // update DOM delete tag
    jQuery('.delete-tag').on('click', function () {
        updateTags(this);
    });
    jQuery('.bookmark-article').on('click', function () {
        bookmark(this);
    });
});