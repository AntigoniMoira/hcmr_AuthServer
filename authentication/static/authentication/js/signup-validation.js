import Ajax from './Ajax.js';
import Utils from './Utils.js';
import HomeRoutes from './routes.js';
import AjaxError from './ajax-errors.js';
const ajax = new Ajax($("[name=csrfmiddlewaretoken]").val());
const utils = new Utils();

const signupValidation = function () {

    //Phone validation
    $('#inputPhone').keypress(function (e) {
      utils.allowOnlyNumbers(e);
      //we can also use utils.allowCertainLength(e, $(this).val().length, 10); 
    });
    
    $(".form-signup").submit(function (e) {
        // catch the form's submit event
        e.preventDefault();
        utils.hidemsg('#signup-fail-message');
        utils.hidemsg('#signup-success-message');

        if (!(utils.validate_email($('#inputEmail').val()))) {
         utils.showmsg('#signup-fail-message', "This is not a valid email address.");
        }
        else {
          if ($("#inputPassword").val().length < 6){
            utils.showmsg('#signup-fail-message', "Password must be more than 5 characters.");
          }
          else{
            const signup_data = {
                firstname: $("#inputFirstName").val(),
                lastname: $("#inputLastName").val(),
                country: $("#inputCountry").val(),
                institution: $("#inputInstitution").val(),
                phone: $("#inputPhone").val(),
                email: $("#inputEmail").val(),
                password: $("#inputPassword").val(),
                password2: $("#inputConfirmPassword").val(),
                description: $("#inputDescription").val()
            };

            ajax.post(HomeRoutes.home.signup, signup_data).then((return_data) => {
              //edw na mpei loader
              if (return_data.success === true) {
                utils.hidemsg('#signup-fail-message');
                utils.showmsg('#signup-success-message', return_data.message);
              }else{
                utils.showmsg('#signup-fail-message', return_data.message);
              }
            }).catch((error) => {
              //edw na kryftei o loader
                const err = new AjaxError(error);
                utils.showmsg('#signup-fail-message', err.msg);
              });
          }//second else end
        }//first else end
    });//submit event end
}; //function END

export {signupValidation};