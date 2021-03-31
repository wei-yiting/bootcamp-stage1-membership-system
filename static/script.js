
// ============= form validation and error message ============
const signUpForm = document.getElementById('sign-up-form');
const accountName = document.getElementById('name');
const signUpUsername = document.getElementById('sign-up-username');
const signUpPassword = document.getElementById('sign-up-password');


signUpForm.addEventListener('submit', (evt) => {
    
    const accountNameValue = accountName.value.trim();
    const signUpUsernameValue = signUpUsername.value.trim();
    const signUpPasswordValue = signUpPassword.value.trim();

    if(accountNameValue === ""){
        evt.preventDefault();
        setErrorFor(accountName, "姓名不可空白")
    }
    
    if(signUpUsernameValue === ""){
        evt.preventDefault();
        setErrorFor(signUpUsername, "帳號不可空白")
    }

    if(signUpPasswordValue === ""){
        evt.preventDefault();
        setErrorFor(signUpPassword, "密碼不可空白")
    }
    if(signUpPasswordValue.toLowerCase() === "password"){
        evt.preventDefault();
        setErrorFor(signUpPassword, "密碼不可為password")
    }
});


function setErrorFor(inputfield, message){
    const formControl = inputfield.parentElement;
    const errorMessage = formControl.querySelector('small');

    errorMessage.innerText = message;
    formControl.classList.add('error');
}


//============= Pop up Modal ================

const modalBtn = document.getElementById('signup-modal-btn');
const modal = document.getElementById('modal-bg');
const signInArea = document.getElementById('sign-in')

modalBtn.addEventListener('click', () => {
    modal.classList.add('show');
    signInArea.classList.add('hide')
});

const modalCloseBtn = document.getElementById('modal-close');
modalCloseBtn.addEventListener('click', ()=>{
    modal.classList.remove('show');
    signInArea.classList.remove('hide');
});