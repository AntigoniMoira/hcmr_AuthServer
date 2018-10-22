class AjaxError {
    constructor(error) {
        this.status = error.status;
        
        if (error.status >= 200 && error.status <= 206) {
            this.msg = 'Επιτυχής καταχώρηση';
        } else if (error.status === 400) {
            this.msg = 'Παρακαλούμε ελέγξτε ξανά τα εισαχθέντα στοιχεία';
        } else if (error.status === 401) {
            this.msg = 'Unauthorized';
        } else if (error.status === 404) {
            this.msg = 'Not Found.';
        } else if (error.status >= 500 && error.statusText <= 511) {
            this.msg = 'Server is down.';
        } 
        else {
            this.msg = 'Something went wrong. Please try again later.';
        }

    }

    //methods here
    printError() {
        console.error(this);
    }

} // end of class

export default AjaxError