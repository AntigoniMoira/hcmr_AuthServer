import {loginValidation} from "./login-validation.js";
import {signupValidation} from "./signup-validation.js";

$(document).ready(function() {
    if($.trim($('.alert').html())==''){
        $(".alert").hide();
    }
    loginValidation();
    signupValidation();    
});