function validateForm() {
    // Fetching values from all input fields and textarea
    var fullName = document.getElementById("fullName").value;
    var email = document.getElementById("email").value;
    var phoneNumber = document.getElementById("phoneNumber").value;
    var city = document.getElementById("city").value;
    var membershipType = document.getElementById("membershipType").value;
    var comments = document.getElementById("comments").value;

    // Regular expression for basic email validation
    var emailRegEx = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;

    // Checking all input fields and textarea
    if (fullName.trim() == "" || email.trim() == "" || phoneNumber.trim() == "" || city.trim() == "" || membershipType.trim() == "") {
        alert("Please fill all required fields");
        return false;
    } else if (!emailRegEx.test(email)) {
        alert("Invalid email format. Please enter a valid email address.");
        return false;
    } else {
        // If all validations are successful, submit the form
        submitForm();
    }
}

function submitForm() {
    // You can perform further actions here, such as AJAX request to submit data
    alert("Form submitted successfully!");
    document.getElementById("registrationForm").reset(); // Reset form after submission
}