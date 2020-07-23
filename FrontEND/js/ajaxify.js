const csrftoken = getCookie('csrftoken');

document.getElementById("loginBtn").addEventListener("click", async function (event) {
    event.preventDefault()
    console.log("1");
    let email = String(document.getElementById("email").value);
    let password = String(document.getElementById("password").value);
    if(email && password){
        try {
            console.log("2");
            url = 'http://127.0.0.1:8000/webapp/login/'
            let data = {"email":email,"password":password}
            
            params = {
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            }
            console.log("2.5");
            const response = await fetch(url,params);
            console.log("3");
            console.log(response);
            const data2 = await response.json();
            console.log("4");
            console.log(data2);
            if(data2.failed=="Invalid login credentials"){
                alert("Invalid login credentials");
                document.getElementById("loginForm").reset();
            }
            else if(data2.token!=null){
                setCookie("Token",data2.token);
                window.location.href ="/dashboard.html";
                console.log('still here')
            }
        }
        catch(err){
            console.log(err);
        }
    }
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function setCookie(cname, cvalue) {
  document.cookie = cname + "=" + cvalue + ";"
}