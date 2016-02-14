/**
 * Created by foutoucour on 2/13/16.
 */


$("#save-form").validate({
    rules: {
        //phone numbers
        phone: {
            remote: {
                url: "/directory/validations/phone",
                type: "post",
                data: {
                    country_id: function () {
                        return $("#country-select").find(":selected").val();
                    }
                }
            }
        },

        fax: {
            remote: {
                url: "/directory/validations/fax",
                type: "post",
                data: {
                    country_id: function () {
                        return $("#country-select").find(":selected").val();
                    }
                }
            }
        },
        mobile: {
            remote: {
                url: "/directory/validations/mobile",
                type: "post",
                data: {
                    country_id: function () {
                        return $("#country-select").find(":selected").val();
                    }
                }
            }
        },
        //Social networks
        linkedin: {
            remote: {url: "/directory/validations/linkedin", type: "post"}
        },
        twitter: {
            remote: {url: "/directory/validations/twitter", type: "post"}
        },
        vimeo: {
            remote: {url: "/directory/validations/vimeo", type: "post"}
        },
        youtube: {
            remote: {url: "/directory/validations/youtube", type: "post"}
        },
        facebook: {
            remote: {url: "/directory/validations/facebook", type: "post"}
        }
    }
});

//Little script to avoid an input to be validated while typing in it
$('#save-form').on('keyup keypress', function (e) {
    var keyCode = e.keyCode || e.which;
    if (keyCode === 13) {
        e.preventDefault();
        return false;
    }
});