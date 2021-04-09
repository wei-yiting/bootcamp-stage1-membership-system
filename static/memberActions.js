// ==== initially show username on page ====
getName();

//========================================================
//============= get and show user name (AJAX) ============
//========================================================
async function getName(){
    fetch(`${window.origin}/api/user`)
    .then( res => res.json())
    .then( data => {
        const name = data.data.name;
        document.getElementById('name').innerText = name;
    })
}

//=========================================================== 
//============= member name search result (AJAX) ============
//===========================================================

const inquireForm = document.getElementById('inquireForm');
const inquireResult = document.getElementById('inquireResult');

// fetch api to and process JSON, show result on page
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


//=========================================================
//============= Update user's own name  (AJAX) ============
//=========================================================

const changeNameForm = document.getElementById('changeNameForm');

// When form submitted : fetch api and show result
changeNameForm.addEventListener('submit', evt => {
    evt.preventDefault();

    const nameToChange = document.getElementById('nameToChange');
    
    let newName = nameToChange.value;

    // show error if update name field is empty
    if(newName.trim() === ""){
    
        setErrorFor(nameToChange, "姓名不可空白");
        console.log("error!!!");

    }else{

        removeErrorFor(nameToChange);

        // fetch api using POST method with JSON in request body
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
            // show update result
            const updataResult = document.getElementById('updateResult');
            const updatedName = document.getElementById('name');
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

        // clear form field
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

// remove error message from form field
function removeErrorFor(inputfield){
    const formControl = inputfield.parentElement;
    const errorMessage = formControl.querySelector('small');

    errorMessage.innerText = "";
    formControl.classList.remove('error');
}