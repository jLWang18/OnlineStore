import { useState } from "react";
import { validateCardName, validateCardNumber, validateExpirationDate, validateVerificationCode } from '../logic/handle_inputs.js';

export default function Payment() {
    // for payment input fields
    const [cardName, setCardName] = useState("");
    const [cardNumber, setCardNumber] = useState("");

    const [cardType, setCardType] = useState("");

    const [expirationDate, setExpirationDate] = useState("");
    const [verificationCode, setVerificationCode] = useState("");

    // for shipping input fields
    // const {streetAddressOne, setStreetAddressOne} = useState("");
    // const {streetAddressTwo, setStreetAddressTwo} = useState("");
    // const {city, setCity} = useState("");
    // const {state, setState} = useState("");
    // const {zip, setZip} = useState("");

    // Handle errors initially empty
    const [formErrors, setFormErrors] = useState({});

    const handleSubmit = (e) => {
        e.preventDefault();

        const isValidPayment = validatePayment(cardName, cardNumber, expirationDate, verificationCode);
        // const isValidShipping = validateShipping(streetAddressOne, streetAddressTwo, city, state, zip)

        if (isValidPayment === false) {
            alert("There is/are invalid input(s)");
            return;
        } else {
            alert("Congratz!! input successful :)");

            // after submission, clear all the fields
            setFormErrors("");
            setCardName("");
            setCardNumber("");
            setCardType("");
            setExpirationDate("");
            setVerificationCode("");

            return;
        }
    }

    const validatePayment = (cardName, cardNumber, expirationDate, verificationCode) => {
        const errors = {};

        const validCardName = validateCardName(cardName);
        const validCardNumber = validateCardNumber(cardNumber);
        
        // const validCardType = validateCardType(cardType);

        const validExpirationDate = validateExpirationDate(expirationDate);
        const validVerificationCode = validateVerificationCode(verificationCode);

        if (!validCardName) {
            errors.cardName = 'Card name must contain alphabets only and at least between 6 and 200 characters';
        }

        if (!validCardNumber) {
            errors.cardNumber = 'Card number must contain at least between 13 and 16 digits';
        }

        if (!validExpirationDate) {
            errors.expirationDate = "Expiration Date must be in MM/YY (month/year) format";
        }

        if (!validVerificationCode) {
            errors.verificationCode = "Verificaction code must contain at least between 3 and 4 digits";
        }

        // if there is/are invalid inputs, return false
        if (Object.keys(errors).length > 0) {
            setFormErrors(errors);
            return false;
        }

        return true;
    }


    return (
        <div>
            <form onSubmit={handleSubmit}>
                <div class="input-control">
                    <h3>Pay with</h3>
                    <div>
                        {formErrors.cardName && <p className="error-message">{formErrors.cardName}</p>}
                        <label htmlFor="card-name">Name on Card:</label>
                        <input type="text" id="card-name" autoComplete="off" onChange={(e) => setCardName(e.target.value)} value={cardName} required/>
                    </div>
                    <div>
                        {formErrors.cardNumber && <p className="error-message">{formErrors.cardNumber}</p>}
                        <label htmlFor="card-number">Credit Card Number:</label>
                        <input type="text" id="card-number" autoComplete="off" onChange={(e) => setCardNumber(e.target.value)} value={cardNumber} required/>
                    </div>
                    <div>
                       <label htmlFor="card-type">Card Type:</label>
                       <select name="card-type" id="card-type" onChange={(e) => setCardType(e.target.value)} value={cardType} required>
                        <option value="">Please Select</option>
                        <option value="Visa">Visa</option>
                        <option value="Mastercard">Mastercard</option>
                        <option value="American Express">American Express</option>
                        <option value="Discover">Discover</option>
                       </select>
                    </div>
                    <div>
                        {formErrors.expirationDate && <p className="error-message">{formErrors.expirationDate}</p>}
                        <label htmlFor="expiration-date">Expiration Date (MM/YY):</label>
                        <input type="text" id="expiration-date" autoComplete="off" onChange={(e) => setExpirationDate(e.target.value)} value={expirationDate} required/>
                    </div>
                    <div>
                        {formErrors.verificationCode && <p className="error-message">{formErrors.verificationCode}</p>}
                        <label htmlFor="verification-code">Verification Code:</label>
                        <input type="text" id="verification-code" autoComplete="off" onChange={(e) => setVerificationCode(e.target.value)} value={verificationCode} required/>
                    </div>
                </div>
                {/* <div class="input-control">
                    <h3>Ship to</h3>
                    <div>
                        <label htmlFor="street-address-one">Street Address 1:</label>
                        <input type="text" id="street-address-one" autoComplete="off" onChange={(e) => setStreetAddressOne(e.target.value)} value={streetAddressOne} required/>
                    </div>
                    <div>
                        <label htmlFor="street-address-two">Street Address 2:</label>
                        <input type="text" id="street-address-two" autoComplete="off" onChange={(e) => setStreetAddressTwo(e.target.value)} value={streetAddressTwo}/>
                    </div>
                    <div>
                        <label htmlFor="city">City:</label>
                        <input type="text" id="city" autoComplete="off" onChange={(e) => setCity(e.target.value)} value={city} required/>
                    </div>
                    <div>
                        <label htmlFor="state">State:</label>
                        <input type="text" id="state" autoComplete="off" onChange={(e) => setState(e.target.value)} value={state} required/>
                    </div>
                    <div>
                        <label htmlFor="zip">Zip:</label>
                        <input type="text" id="zip" autoComplete="off" onChange={(e) => setZip(e.target.value)} value={zip} required/>
                    </div>
                </div> */}
                <button class="button" type="submit">Confirm and pay</button>
            </form>
        </div>
    )
}