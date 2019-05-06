import Ajax from './Ajax.js';
import Utils from './Utils.js';
import HomeRoutes from './routes.js';
import AjaxError from './ajax-errors.js';
const ajax = new Ajax($('[name=csrfmiddlewaretoken]').val());
const utils = new Utils();


const loginValidation = function () {

    $('.form-signin').submit(function (e) {
        e.preventDefault();
        // catch the form's submit event
        $('#inputEmail').removeClass('is-invalid');
        $('#inputPassword').removeClass('is-invalid');
        utils.hidemsg('#login-fail-message');

        var login_data = {
            email: $('#inputEmail').val(),
            password: $('#inputPassword').val()
        };

        ajax.post(HomeRoutes.home.login, login_data).then((return_data) => {
            //edw na mpei loader
            if (return_data.success === true) {
                window.location.href = $("input[name='next']").val() + "&scope=" + return_data.scopes;
            } else if (return_data.success === false) {
                if (return_data.message.includes('email')){
                    $('#inputEmail').addClass('is-invalid');
                }
                else if(return_data.message.includes('password')){
                    $('#inputPassword').addClass('is-invalid');
                }
                utils.showmsg('#login-fail-message', return_data.message);
            }
        }).catch((error) => {
            //edw na kryftei o loader
            const err = new AjaxError(error);
            utils.showmsg('#login-fail-message', err.msg);
        });
    }); //submit event END

    $('.form-reset-psw').submit(function (e) {
        // catch the form's submit event
        e.preventDefault();
        $('#reser-psw-email').removeClass('is-invalid');
        utils.hidemsg('#reset-psw-success-message');
        utils.hidemsg('#reset-psw-fail-message');
        var data = {
            email: $('#reser-psw-email').val()
        };

        ajax.post(HomeRoutes.home.reset_password, data).then((return_data) => {
            //edw na mpei loader
            if (return_data.success === true) {
                utils.showmsg('#reset-psw-success-message', return_data.message);
            } else if (return_data.success === false) {
                $('#reser-psw-email').addClass('is-invalid');
                utils.showmsg('#reset-psw-fail-message', return_data.message);
            }
        }).catch((error) => {
            //edw na kryftei o loader
            const err = new AjaxError(error);
            utils.showmsg('#reset-psw-fail-message', err.msg);
        });
    }); //submit event END

}; //function END

export {
    loginValidation
};