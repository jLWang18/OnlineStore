const isValidEmail = (email) => {
    const re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(String(email).toLowerCase());
  };

  export const validateEmail = (emailInput) => {
  
    if (emailInput === '') {
      return false;
    } else if (!isValidEmail(emailInput)) {
      return false;
    }else if(emailInput.length < 13 || emailInput.length > 31) {
      return false;
    } else {
      return true;
    }

  }
  export const validatePassword = (passwordInput) => {
      if(passwordInput === '') {
        return false;
      } else if(passwordInput.length < 8) {
        return false;
      } else {
        return true;
      }
    }
