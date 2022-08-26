finergy.ready(function() {
    // bind events here
    $(".page-header-actions-block .btn-primary, .page-header-actions-block .btn-default").addClass('hidden');
    $(".text-right .btn-primary").addClass('hidden');

    if (finergy.utils.get_url_arg('name')) {
        $('.page-content .btn-form-submit').addClass('hidden');
    } else {
        user_name = finergy.full_name
        user_email_id = finergy.session.user
        $('[data-fieldname="currency"]').val("INR");
        $('[data-fieldname="name_of_applicant"]').val(user_name);
        $('[data-fieldname="email"]').val(user_email_id);
        $('[data-fieldname="amount"]').val(20000);
    }
})
