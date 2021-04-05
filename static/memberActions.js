// ============= member name search result ============
const inquireForm = document.getElementById('inquireForm');
const inquireResult = document.getElementById('inquireResult');

inquireForm.addEventListener('submit', evt => {
    evt.preventDefault();
    const inquireUsername = document.getElementById('inquireUsername');
    let username = inquireUsername.value;

    fetch(`${window.origin}/api/users?username=${username}`)
    .then( res => res.json())
    .then( data => {
        if(!data.data){
            inquireResult.innerText = "查詢不到資料";
        }
        else{
            let result = `${data.data.name} ( ${data.data.username} )`
            inquireResult.innerText = result;
        }
    })
    .catch( err =>{
        console.log(`Fetch error: ${err}`)
    })

    inquireUsername.value = '';
})

// ============= change name ================

const changeNameForm = document.getElementById('changeNameForm');

changeNameForm.addEventListener('submit', evt => {
    evt.preventDefault();

    const nameToChange = document.getElementById('nameToChange');
    
    let newName = nameToChange.value;

    if(newName.trim() === ""){
    
        setErrorFor(nameToChange, "姓名不可空白");
        console.log("error!!!");

    }else{

        removeErrorFor(nameToChange);

        let requestData = {name: newName};

        fetch(`${window.origin}/api/user`,{
            method:'POST',
            headers:new Headers({
                "Content-Type":"application/json"
            }),
            body:JSON.stringify(requestData)
        })
        .then( response => response.json())
        .then( data => {
            const updataResult = document.getElementById('updateResult');
            const updatedName = document.getElementById('updatedName');
            if (data.ok){
                updataResult.innerText = "更新成功";
                updatedName.innerText = newName;
            }
            else if(data.error){
                updataResult.innerText = "更新失敗";
            }
        })
        .catch( err => {
            console.log(`Fetch error: ${err}`);
        })

        nameToChange.value = '';
    }
})


// show error message from form field
function setErrorFor(inputfield, message){
    const formControl = inputfield.parentElement;
    const errorMessage = formControl.querySelector('small');

    errorMessage.innerText = message;
    formControl.classList.add('error');
}

// show error message from form field
function removeErrorFor(inputfield){
    const formControl = inputfield.parentElement;
    const errorMessage = formControl.querySelector('small');

    errorMessage.innerText = "";
    formControl.classList.remove('error');
}