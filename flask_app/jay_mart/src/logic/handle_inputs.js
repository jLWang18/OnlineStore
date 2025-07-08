const isValidEmail = (email) => {
    const re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(String(email).toLowerCase());
}

const isAlphabetic = (input) => {
  var alphaPattern = /^[a-zA-Z]+$/;

 // if it contains alphabets, return true or else return false
  if (alphaPattern.test(input)) {
    return true;
  } else {
    return false;
  }
}

const isValidNumber = (input) => {
  var ch = input;
  var numberPattern = /[0-9]/;

  // if it contains digits, return true or else return false
  if(numberPattern.test(ch)){
    return true;
  } else {
    return false;
  }
}

const isValidExpDate = (input) => {
  var expDateFormat = /^(0[1-9]|1[0-2])\/\d{2}$/

  if (expDateFormat.test(input)) {
    return true;
  } else {
    return false;
  }
}


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

export const validatePassword = (password) => {
  var uppercase = /[A-Z]/;
  var lowercase = /[a-z]/;
  var number = /[0-9]/;
  var symbol = /[@_!#$%^&*()<>{~:]/


  // get password length
  var password_len = password.length

  if (password_len >= 8 && password.match(uppercase) && password.match(lowercase) 
    && password.match(number) && password.match(symbol)){
    return true;
    } else {
    return false;
  } 
}

export const validateFirstName  = (firstNameInput) => {
  if (isAlphabetic(firstNameInput) !== true) {
    return false;
  }else if (firstNameInput.length < 3 || firstNameInput.length > 50) {
    return false;
  }else {
    return true;
  }
}
    
export const validateLastName = (lastNameInput) => {
  if (lastNameInput === '') {
    return false;
  } else if (isAlphabetic(lastNameInput) !== true) {
    return false;
  } else if (lastNameInput.length < 3 || lastNameInput.length > 150) {
    return false;
  }
  else {
    return true;
  }
}

export const validatePhone = (phoneNumberInput) => {
  if(phoneNumberInput === '') {
    return false;
  } else if (phoneNumberInput.length !== 10) {
    return false;
  } else if (isValidNumber(phoneNumberInput) !== true) {
    return false;
  } else {
    return true;
  }
}

export const validateCardName = (cardNameInput) => {
  // remove any spaces in the input
  cardNameInput = cardNameInput.replace(/\s/g, '')

  if (isAlphabetic(cardNameInput) === false) {
    return false;
  }else if (cardNameInput.length < 6 || cardNameInput.length > 200) {
    return false;
  }else {
    return true;
  }
}

export const validateCardNumber = (cardNumberInput) => {
  if (cardNumberInput === '') {
    return false;
  } else if (cardNumberInput.length < 13 || cardNumberInput.length > 16) {
    return false;
  } else if (isValidNumber(cardNumberInput) === false) {
    return false;
  } else {
    return true;
  }
}

export const validateExpirationDate = (expirationDateInput) => {
  if (isValidExpDate(expirationDateInput) === false) {
    return false;
  } else if (expirationDateInput.length !== 5) {
    return false;
  } else {
    return true;
  }
}

export const validateVerificationCode = (verificationCodeInput) => {
  if (verificationCodeInput === '') {
    return false;
  } else if (verificationCodeInput.length < 3 || verificationCodeInput.length > 4) {
    return false;
  } else if (isValidNumber(verificationCodeInput) === false) {
    return false;
  } else {
    return true;
  }

}
    