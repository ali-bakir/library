import {getFormData} from "../utils/utils";

$(document).ready(function () {
    $('#id_comment_post').submit(function (event) {
        console.log("gürol çay içti")
        event.preventDefault();
        let form = $("form.js-book-comment");
        let book_comment_url = form.attr("book-comment-url");
        let book_id = form.attr("book-id");
        console.log(form)
        let form_data = getFormData(form)

        // form_data['book'] = book_id
        console.log(form_data)
        console.log(book_comment_url)
        //
        // $.post(
        //     book_comment_url,
        //     form_data,
        //     function (resp) {
        //         console.log(resp)
        //     }
        // )
    })
})