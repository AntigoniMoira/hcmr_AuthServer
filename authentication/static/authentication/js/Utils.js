class Utils {
    constructor() {}

    allowOnlyNumbers(event) {
        if (isNaN(parseInt(event.key)) && event.key !== '+'  && event.key !== '-' && event.key !== ' ' && event.key !== '.' && event.key !== ',' && event.key !== '(' && event.key !== ')' 
            && event.key !== 'Backspace' && event.key !== 'Delete' && event.key !== 'ArrowLeft' && event.key !== 'ArrowRight') {
            event.preventDefault();
        }
    }

    allowCertainLength(event, Curlen, AllLen) {
        if (Curlen === AllLen) {
            event.preventDefault();
        }
    }

    validate_email(email) {
        if (
            /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/.test(
                email
            )
        ) {
            return true;
        } else {
            return false;
        }
    }

    showmsg(id, error_message) {
        $(id).html("<h4>*" + error_message + "</h4>");
    }
  
    hidemsg(id) {
            $(id).html("");
    }
}
export default Utils