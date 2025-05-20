// Get references to the form, input fields,etc.
const form = document.getElementById('form');
const firstNameField = document.getElementById('fname');
const lastNameField = document.getElementById('lname');
const emailField = document.getElementById('email');
const phoneNumberField = document.getElementById('phone-number');


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

const isAlphabetic = (input) => {
  var alphaPattern = /^[a-zA-Z]+$/;

 // if it contains alphabets, return true or else return false
  if (alphaPattern.test(input)) {
    return true;
  } else {
    return false;
  }
}


const validateFirstName  = (firstNameField, firstNameInput) => {
  if (firstNameInput === '') {
    setError(firstNameField, 'First Name is required');
    return false;
  } else if (isAlphabetic(firstNameInput) !== true) {
    setError(firstNameField, 'Please provide a valid first name');
    return false;
  }else if (firstNameInput.length < 3 || firstNameInput.length > 50) {
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
  } else if (isAlphabetic(lastNameInput) !== true) {
    setError(lastNameField, 'Please provide a valid last name');
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
  } else if (phoneNumberInput.length < 10) {
    setError(phoneNumberField, 'Phone Number  must contain 10 digits');
    return false;
  } else if (isValidNumber(phoneNumberInput) !== true) {
    setError(phoneNumberField, 'Phone Number must contain digits only');
    return false;
  } else {
    setSuccess(phoneNumberField);
    return true;
  }

}



// Disable input event listeners initially
firstNameField.removeEventListener("input", firstNameInputListener);
lastNameField.removeEventListener("input", lastNameInputListener);
emailField.removeEventListener("input", emailInputListener);
phoneNumberField.removeEventListener("input", phoneNumberInputListener);


// function to add input event listener when the submit button is clicked
function addInputEventListeners() {
  firstNameField.addEventListener("input", firstNameInputListener);
  lastNameField.addEventListener("input", lastNameInputListener);
  emailField.addEventListener("input", emailInputListener);
  phoneNumberField.addEventListener("input", phoneNumberInputListener);
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


/*Specify what the submit button will do*/
form.addEventListener('submit', e => {
  /*prevent sumbission before validation */
  e.preventDefault();

  // // Enable input event listeners when the submit button is clicked
   addInputEventListeners();

  // Get Personal Input values: Trim to delete any leading and trailing whitespaces
  const firstNameInput = firstNameField.value.trim();
  const lastNameInput = lastNameField.value.trim();
  const emailInput = emailField.value.trim();
  const phoneNumberInput = phoneNumberField.value.trim();
  
  // validate the Personal Info section
  const isFirstNameValid = validateFirstName(firstNameField, firstNameInput);
  const isLastNameValid = validateLastName(lastNameField, lastNameInput);
  const isEmailValid = validateEmail(emailField, emailInput);
  const isPhoneNumberValid = validatePhoneNumber(phoneNumberField, phoneNumberInput);

  // Check if the form data is valid
  if (isFirstNameValid && isLastNameValid && isEmailValid 
    && isPhoneNumberValid) {
      // Create a new FormData object with the form data
      const formData = new FormData(form);

      //Send a POST request to the Flask route '/submit_customer'
      fetch('/submit_customer', {
        method: 'POST',
        body: formData // Include form data in the request body
      })
      .then(response => response.text()) // Parse response as text
      .then(htmlData => {
        // Replace the entire table HTML with the updated HTML received from the server
        document.querySelector('.content').innerHTML = htmlData;

      })
      .catch(error => {
        console.error('Error:', error);
      })

    }

});

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