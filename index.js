// Get references to the form, input fields,etc.
const form = document.getElementById('form');
const firstNameField = document.getElementById('fname');
const lastNameField = document.getElementById('lname');
const emailField = document.getElementById('email');
const phoneNumberField = document.getElementById('phone-number');
const passwordField1 = document.getElementById('password1');
const passwordField2 = document.getElementById('password2')


const addressField1 = document.getElementById('address1');
const addressField2 = document.getElementById('address2');
const cityField = document.getElementById("city");
const stateField = document.getElementById("state");
const zipField = document.getElementById('zip');

/*Display an error*/
const setError = (element, message) => {
  const inputControl = element.parentElement;
  const errorDisplay = inputControl.querySelector('.error');

  errorDisplay.innerText = message;
  inputControl.classList.add('error');
  inputControl.classList.remove('success');
};

/*remove the error display*/
const setSuccess = (element) => {
  const inputControl = element.parentElement;
  const errorDisplay = inputControl.querySelector('.error');

  errorDisplay.innerText = '';
  inputControl.classList.add('sucesss');
  inputControl.classList.remove('error');

};

const isValidEmail = (email) => {
  const re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
  return re.test(String(email).toLowerCase());
};

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


const validateFirstName  = (firstNameField, firstNameInput) => {
  if (firstNameInput === '') {
    setError(firstNameField, 'First Name is required');
    return false;
  } else if (firstNameInput.length < 3 || firstNameInput.length > 50) {
    setError(firstNameField, 'First Name must be at least between 3 and 50 characters');
    return false;
  }else {
    setSuccess(firstNameField);
    return true;
  }
}

const validateLastName = (lastNameField, lastNameInput) => {
  if (lastNameInput === '') {
    setError(lastNameField, 'Last Name is required');
    return false;
  } else if (lastNameInput.length < 3 || lastNameInput.length > 150) {
    setError(lastNameField, 'Last Name must be at least between 3 and 150 characters');
    return false;
  }
  else {
    setSuccess(lastNameField);
    return true;
  }
}

const validateEmail = (emailField, emailInput) => {
  
  if (emailInput === '') {
    setError(emailField, 'Email is required');
    return false;
  } else if (!isValidEmail(emailInput)) {
    setError(emailField, "Please provide valid email");
    return false;
  }else if(emailInput.length < 13 || emailInput.length > 31) {
    setError(emailField, 'Email must be at least between 13 and 31 characters');
    return false;
  }  else {
    setSuccess(emailField);
    return true;
  }
}

const validatePhoneNumber = (phoneNumberField, phoneNumberInput) => {
  if(phoneNumberInput === '') {
    setError(phoneNumberField, 'Phone Number is required');
    return false;
  } else if (phoneNumberInput.length < 13) {
    setError(phoneNumberField, 'Phone Number  must contain 9 digits');
    return false;
  } else if (isValidNumber(phoneNumberInput) !== true) {
    setError(phoneNumberField, 'Phone Number must contain digits only');
    return false;
  } else {
    setSuccess(phoneNumberField);
    return true;
  }

}

const validatePassword1 = (passwordField1, passwordInput1) => {
  if(passwordInput1 == '') {
    setError(passwordField1, 'Password is required');
    return false;
  } else if(passwordInput1.length < 8) {
    setError(passwordField1, 'Password must be at least 8 characters');
    return false;
  } else {
    setSuccess(password1);
    return true;
  }
}

const validatePassword2 = (passwordField2, passwordInput1, passwordInput2) => {
  if(passwordInput1 == '') {
    setError(passwordField2, 'Password field is required');
    return false;
  } else if(passwordInput2 == '') {
    setError(passwordField2, 'Confirm Password is required');
    return false;
  } else if(passwordInput1.length < 8) {
    setError(passwordField2, 'Password must be at least 8 characters');
    return false;
  }else if(passwordInput2 !== passwordInput1) {
    setError(passwordField2, "Passwords does not match");
    return false;
  } else {
    setSuccess(passwordField2);
    return true;
  }
}

const validateAddress1 = (addressField1, addressInput1) => {
  if(addressInput1 === '') {
    setError(addressField1, 'Address is required');
    return false;
  } else if (addressInput1.length < 4 || addressInput1.length > 150) {
    setError(addressField1, 'Address must be at least between 4 and 150 characters');
    return false;
  } else {
    setSuccess(addressField1);
    return true;
  }
}

const validateAddress2 = (addressField2, addressInput2) => {
  // if address2 is not null, check if it is within the range
  if ((addressInput2 !== '') && (addressInput2.length < 4 || addressInput2.length > 150)) {
    setError(addressField2, 'Address must be at least between 4 and 150 characters');
    return false;
  } else {
    setSuccess(addressField2);
    return true;
  }
}

const validateCity = (cityField, cityInput) => {
  if(cityInput === '') {
    setError(cityField, 'City is required');
    return false;
  } else if (cityInput.length < 3 || cityInput.length > 75) {
    setError(cityField, 'City must be at least between 3 and 75 characters');
    return false;
  } else {
    setSuccess(cityField);
    return true;
  }

}

const validateState = (stateField, stateInput) => {
  if(stateInput === '') {
    setError(stateField, 'State is required');
    return false;
  } else if (stateInput.length < 2 || stateInput.length > 2) {
    setError(stateField, 'State must be 2 characters (e.g., WA, OK, NY, TX, etc.');
    return false;
  } else {
    setSuccess(stateField);
    return true;
  }
}

const validateZip = (zipField, zipInput) => {
  if(zipInput === '') {
    setError(zipField, 'Zip is required');
    return false;
  } else if(isValidNumber(zipInput) !== true) {
    setError(zipField, 'zip must be contain digits only');
    return false;
  } else if (zipInput.length < 5 || zipInput.length > 5) {
    setError(zipField, 'Zip must be 5 digits');
    return false;
  } else {
    setSuccess(zipField);
    return true;
  }
}


// Disable input event listeners initially
firstNameField.removeEventListener("input", firstNameInputListener);
lastNameField.removeEventListener("input", lastNameInputListener);
emailField.removeEventListener("input", emailInputListener);
phoneNumberField.removeEventListener("input", phoneNumberInputListener);
passwordField1.removeEventListener("input", passwordInputListener1);
passwordField2.removeEventListener("input", passwordInputListener2);
addressField1.removeEventListener("input", addressInputListener1);
addressField2.removeEventListener("input", addressInputListener2);
cityField.removeEventListener("input", cityInputListener);
stateField.removeEventListener("input", stateInputListener);
zipField.removeEventListener("input", zipInputListener);


// function to add input event listener when the submit button is clicked
function addInputEventListeners() {
  firstNameField.addEventListener("input", firstNameInputListener);
  lastNameField.addEventListener("input", lastNameInputListener);
  emailField.addEventListener("input", emailInputListener);
  phoneNumberField.addEventListener("input", phoneNumberInputListener);
  passwordField1.addEventListener("input", passwordInputListener1);
  passwordField2.addEventListener("input", passwordInputListener2);
  addressField1.addEventListener("input", addressInputListener1);
  addressField2.addEventListener("input", addressInputListener2);
  cityField.addEventListener("input", cityInputListener);
  stateField.addEventListener("input", stateInputListener);
  zipField.addEventListener("input", zipInputListener);

}

function firstNameInputListener (e) {
  const firstNameInput = e.target.value;
  validateFirstName(firstNameField, firstNameInput);
}

function lastNameInputListener (e) {
  const lastNameInput = e.target.value;
  validateLastName(lastNameField, lastNameInput);
}

function emailInputListener (e) {
  const emailInput = e.target.value;
  validateEmail(emailField, emailInput);
}

function phoneNumberInputListener (e) {
  const phoneNumberInput = e.target.value;
  validatePhoneNumber(phoneNumberField, phoneNumberInput);
}

function passwordInputListener1 (e) {
  const passwordInput1 = e.target.value;
  validatePassword1(passwordField1, passwordInput1);
}

function passwordInputListener2 (e) {
  const passwordInput1 = e.target.value;
  const passwordInput2 = e.target.value;
  validatePassword2(passwordField2, passwordInput1, passwordInput2);
}

function addressInputListener1 (e) {
  const addressInput1 = e.target.value;
  validateAddress1(addressField1, addressInput1);
}

function addressInputListener2 (e) {
  const addressInput2 = e.target.value;
  validateAddress2(addressField2, addressInput2);
}

function cityInputListener (e) {
  const cityInput = e.target.value;
  validateCity(cityField, cityInput);
}

function stateInputListener (e) {
  const stateInput = e.target.value;
  validateState(stateField, stateInput);
}

function zipInputListener (e) {
  const zipInput = e.target.value;
  validateZip(zipField, zipInput);
}


/*Specify what the submit button will do*/
form.addEventListener('submit', e => {
  /*prevent sumbission before validation */
  e.preventDefault();

  // Enable input event listeners when the submit button is clicked
  addInputEventListeners();

  // Get Personal Input values: Trim to delete any leading and trailing whitespaces
  const firstNameInput = firstNameField.value.trim();
  const lastNameInput = lastNameField.value.trim();
  const emailInput = emailField.value.trim();
  const phoneNumberInput = phoneNumberField.value.trim();
  const passwordInput1 = passwordField1.value.trim();
  const passwordInput2 = passwordField2.value.trim();

  // Get Shipping Address Input values: Trim to delete any leading and trailing whitespaces
  const addressInput1 = addressField1.value.trim();
  const addressInput2 = addressField2.value.trim();
  const cityInput = cityField.value.trim();
  const stateInput = stateField.value.trim();
  const zipInput = zipField.value.trim();

  // validate the Personal Info section
  const isFirstNameValid = validateFirstName(firstNameField, firstNameInput);
  const isLastNameValid = validateLastName(lastNameField, lastNameInput);
  const isEmailValid = validateEmail(emailField, emailInput);
  const isPhoneNumberValid = validatePhoneNumber(phoneNumberField, phoneNumberInput);
  const isPasswordValid1 = validatePassword1(passwordField1, passwordInput1);
  const isPasswordValid2 = validatePassword2(passwordField2, passwordInput1, passwordInput2);

  // validate the Shipping Address Section
  const isAddressValid1 = validateAddress1(addressField1, addressInput1);
  const isAddressValid2 = validateAddress2(addressField2, addressInput2);
  const isCityValid = validateCity(cityField, cityInput);
  const isStateValid = validateState(stateField, stateInput);
  const isZipValid = validateZip(zipField, zipInput); 
  


  if (isFirstNameValid && isLastNameValid && isEmailValid 
    && isPhoneNumberValid && isPasswordValid1 && isPasswordValid2
    && isAddressValid1 && isAddressValid2 && isCityValid
    && isStateValid && isZipValid) {
    alert("Form submitted successfully!");
  } else {
    alert("Please fill out the required fields before submitting.")
  }

});


/*const validateShippingAddress = () => {







};*/



/*Checkbox validation*/
function validate() {
    var valid = false;

    if (document.getElementById("cd1").checked) {
      valid = true;
    } else if (document.getElementById("cd2").checked) {
      valid = true;
    } else if (document.getElementById("dvd1").checked) {
      valid = true;
    } else if (document.getElementById("dvd2").checked) {
      valid = true;
    }

    if (valid) {
      alert("Are you sure you want these products?");
    } else {
      alert("Please select at least one product.");
    }
  }

  /*format the phone number*/
  function formatPhoneNumber(value) {
    /*if the value is blank, then it's an error*/
    if (!value) return value;
    /*replaCe any non-digit number with '' */
    const phoneNumber = value.replace(/[^\d]/g, "");
    const phoneNumberLength = phoneNumber.length;

    /*format the phone number based on the phone length*/
    if (phoneNumberLength < 4) return phoneNumber; 
    if (phoneNumberLength < 7) {
      return `(${phoneNumber.slice(0, 3)}) ${phoneNumber.slice(3)}`;
    }
    return `(${phoneNumber.slice(0, 3)}) ${phoneNumber.slice(
      3,
      6
    )}-${phoneNumber.slice(6, 9)}`;
  }

  /*phone number validation*/
  function phoneNumberFormatter() {
    /*get user input*/
    const inputField = document.getElementById("phone-number");
    /*calling the formatPhoneNumber method*/
    const formattedInputValue = formatPhoneNumber(inputField.value);
    /*set it back to the input field*/
    inputField.value = formattedInputValue;
  }