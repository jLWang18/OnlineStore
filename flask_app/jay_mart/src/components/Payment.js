import { useState } from "react";
import { validateCardName, validateCardNumber, validateExpirationDate, validateVerificationCode } from '../logic/handle_inputs.js';
import useCheckout from "../hooks/useCheckout.js";
import { addPayment } from "../logic/add_payment.js";
import { useNavigate, useParams} from 'react-router-dom';
import useCustomer from "../hooks/useCustomer.js";

export default function Payment() {
    // for payment input fields
    const [cardNameInput, setCardNameInput] = useState("");
    const [cardNumberInput, setCardNumberInput] = useState("");
    const [cardTypeInput, setCardTypeInput] = useState("");
    const [expirationDateInput, setExpirationDateInput] = useState("");
    const [verificationCodeInput, setVerificationCodeInput] = useState("");

    // navigate to home page when payment is successfully added
    const navigate = useNavigate();

    // Handle errors initially empty
    const [formErrors, setFormErrors] = useState({});

    const {totalAmount} = useCheckout();

    const [isSubmitting, setIsSubmitting] = useState(false);

    const {orderId} = useParams();
    const {customerId} = useCustomer();


    const handleSubmit =  async (e) => {
        e.preventDefault();

        if (isSubmitting) return;

        const isValidPayment = validatePayment(cardNameInput, cardNumberInput, expirationDateInput, verificationCodeInput);

        if (isValidPayment === false) {
            alert("There is/are invalid input(s)");
            return;
        } else {
            setIsSubmitting(true);
            
            // extract the last 4 digits of credit card number
            let length = cardNumberInput.length
            let index = length - 4
            let last4 = cardNumberInput.slice(index)


            try {
                // add payment info a to the payment database 
                // and upon sucessful insertion, return order id
                const response = await addPayment(customerId, orderId, totalAmount, last4, cardTypeInput)

                if (response["message"] === "Payment info is added successfully") {
                    // direct user to the confirmation page
                    navigate(`/confirmation/${orderId}`)

                } else if (response["message"] === "An order already paid") {
                    // show the alert
                    alert('An order already paid')
                    // direct user to the confirmation page
                    navigate(`/confirmation/${orderId}`)
                }
                // after submission, clear all the fields
                setFormErrors("");
                setCardNameInput("");
                setCardNumberInput("");
                setCardTypeInput("");
                setExpirationDateInput("");
                setVerificationCodeInput("");
            
            } catch (err) {
                if (err.response?.status === 404) {
                    alert("Either customer id does not exist or order id does not exist");
                } else if (err.response?.status === 500) {
                    alert("There was an issue adding payment info")
                }
            }
        }
    }

    const validatePayment = (cardName, cardNumber, expirationDate, verificationCode) => {
        const errors = {};

        const validCardName = validateCardName(cardName);
        const validCardNumber = validateCardNumber(cardNumber);

        const validExpirationDate = validateExpirationDate(expirationDate);
        const validVerificationCode = validateVerificationCode(verificationCode);

        if (!validCardName) {
            errors.cardNameInput = 'Card name must contain alphabets only and at least between 6 and 200 characters';
        }

        if (!validCardNumber) {
            errors.cardNumberInput = 'Card number must contain at least between 13 and 16 digits';
        }

        if (!validExpirationDate) {
            errors.expirationDateInput = "Expiration Date must be in MM/YY (month/year) format";
        }

        if (!validVerificationCode) {
            errors.verificationCodeInput = "Verificaction code must contain at least between 3 and 4 digits";
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
                <div className="input-control">
                    <h3>Pay with</h3>
                    <div>
                        {formErrors.cardNameInput && <p className="error-message">{formErrors.cardNameInput}</p>}
                        <label htmlFor="card-name">Name on Card:</label>
                        <input type="text" id="card-name" autoComplete="off" onChange={(e) => setCardNameInput(e.target.value)} value={cardNameInput} required/>
                    </div>
                    <div>
                        {formErrors.cardNumberInput && <p className="error-message">{formErrors.cardNumberInput}</p>}
                        <label htmlFor="card-number">Credit Card Number:</label>
                        <input type="text" id="card-number" autoComplete="off" onChange={(e) => setCardNumberInput(e.target.value)} value={cardNumberInput} required/>
                    </div>
                    <div>
                       <label htmlFor="card-type">Card Type:</label>
                       <select name="card-type" id="card-type" onChange={(e) => setCardTypeInput(e.target.value)} value={cardTypeInput} required>
                        <option value="">Please Select</option>
                        <option value="Visa">Visa</option>
                        <option value="Mastercard">Mastercard</option>
                        <option value="American Express">American Express</option>
                        <option value="Discover">Discover</option>
                       </select>
                    </div>
                    <div>
                        {formErrors.expirationDateInput && <p className="error-message">{formErrors.expirationDateInput}</p>}
                        <label htmlFor="expiration-date">Expiration Date (MM/YY):</label>
                        <input type="text" id="expiration-date" autoComplete="off" onChange={(e) => setExpirationDateInput(e.target.value)} value={expirationDateInput} required/>
                    </div>
                    <div>
                        {formErrors.verificationCodeInput && <p className="error-message">{formErrors.verificationCodeInput}</p>}
                        <label htmlFor="verification-code">Verification Code:</label>
                        <input type="text" id="verification-code" autoComplete="off" onChange={(e) => setVerificationCodeInput(e.target.value)} value={verificationCodeInput} required/>
                    </div>
                    <div className = "payment-button">
                        <button className="button" type="submit">Confirm and pay</button>
                    </div>
                </div>
            </form>
        </div>
    )
}