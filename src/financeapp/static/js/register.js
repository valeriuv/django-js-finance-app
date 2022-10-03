const usernameField=document.querySelector("#usernameField");
const feedBackArea=document.querySelector(".invalid_feedback");
const emailField=document.querySelector("#emailField");
const emailFeedBackArea=document.querySelector(".emailFeedBackArea");
const passwordField = document.querySelector("#passwordField");
const usernameSuccessOutput=document.querySelector(".usernameSuccessOutput");
const showPasswordToggle=document.querySelector(".showPasswordToggle");
const submitBtn = document.querySelector(".submit-btn");
const handleToggleInput = (e) => {
    if(showPasswordToggle.textContent === "SHOW"){

        showPasswordToggle.textContent = "HIDE";
        passwordField.setAttribute("type", "text");
        console.log("11111111 Password toggle hide");

    } else {
        showPasswordToggle.textContent = "SHOW";
        passwordField.setAttribute("type", "password");
        console.log("11111111 Password toggle show");
    }

}

usernameField.addEventListener("keyup", (e) => {

    const usernameVal = e.target.value;

    usernameSuccessOutput.style.display="block";

    usernameField.classList.remove("is-invalid");
    feedBackArea.style.display="none";
    

    if(usernameVal.length > 0) {

        usernameSuccessOutput.textContent=`Checking ${usernameVal}...`;

        fetch("/authentication/validate-username", {
            body: JSON.stringify({username: usernameVal}), 
            method: "POST",
        })
        .then((res) => res.json())
        .then((data) => {
            console.log("data", data)
            usernameSuccessOutput.style.display="none";
            if(data.username_error){
                submitBtn.disabled = true;
                usernameField.classList.add("is-invalid");
                feedBackArea.style.display="block";
                feedBackArea.innerHTML=`<div class="text-danger">${data.username_error}</div>`;
            } else {
                submitBtn.removeAttribute("disabled");
            }
        });

    } else {
        usernameSuccessOutput.style.display="none";
    }
})


emailField.addEventListener("keyup", (e)=>{

    const emailVal = e.target.value;

    emailField.classList.remove("is-invalid");
    emailFeedBackArea.style.display="none";
    

    if(emailVal.length > 0) {

        fetch("/authentication/validate-email", {
            body: JSON.stringify({email: emailVal}), 
            method: "POST",
        })
        .then((res) => res.json())
        .then((data) => {
            console.log("data", data)
            if(data.email_error){
                submitBtn.disabled = true;
                emailField.classList.add("is-invalid");
                emailFeedBackArea.style.display="block";
                emailFeedBackArea.innerHTML=`<div class="text-danger">${data.email_error}</div>`;
            } else {
                submitBtn.removeAttribute("disabled");
            }
        });

    }
})

showPasswordToggle.addEventListener("click", handleToggleInput);