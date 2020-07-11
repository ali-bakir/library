$(document).ready(function () {
    $('#id_comment_post').click(function (event) {

            let form = $("form.js-book-comment");
            let book_comment_url = form.attr("book-comment-url");
            let book_id = form.attr("book-id");
            let form_data = getFormData(form)

            form_data['book'] = book_id

            $.post(
                book_comment_url,
                form_data,
                function (resp) {
                    console.log(resp)
                }
            )

            // $.ajax({
            //     url: book_comment_url,
            //     type: 'POST',
            //     data: form_data,
            //     dataType: 'json',
            //     success: function (resp) {
            //         console.log(resp);
            //     },
            //     error: function (err) {
            //         console.log(err);
            //     }
            // })

        }
    );
});

let getFormData = function (form) {
    let unindexed_array = form.serializeArray();
    let indexed_array = {};

    $.map(unindexed_array, function (n, i) {
        indexed_array[n['name']] = n['value'];
    });

    return indexed_array;
}


// let submitBookComment = function (book_id) {
//     var form = $(this).closest("form");
//     // let username = document.getElementById("id_comment_form_name").value;
//     // let comment = document.getElementById("id_comment_form_comment").value;
//     event.preventDefault();
//     console.log(book_id)
//     console.log(form.serialize())
//     console.log(form.attr("book-comment-url"))
//     // $.ajax({
//     //     url: form.attr("book-comment-url"),
//     //     data: form.serialize(),
//     //     dataType: 'json',
//     //     success: function (data) {
//     //       if (data.is_taken) {
//     //         alert(data.error_message);
//     //       }
//     //     }
//     //   });
// }