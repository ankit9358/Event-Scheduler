let signForm = document.createElement('form');
signForm.id = "signForm";
signForm.innerHTML = `<div class="form-group">
<label class="lead" for="exampleInputEmail1">First Name</label>
<input type="text" class="form-control" aria-describedby="emailHelp"
    name="fname" placeholder="First Name">
    <label class="lead" for="exampleInputEmail1">Last Name</label>
<input type="Last Name" class="form-control" aria-describedby="emailHelp"
    name="lname" placeholder="Last Name">
<label class="lead" for="exampleInputEmail1">Email address</label>
<input type="email" class="form-control" aria-describedby="emailHelp"
    name="email" placeholder="Enter email">
<label class="lead" for="exampleInputPassword1">Password</label>
<input type="password" class="form-control" id="exampleInputPassword1" name="password"
    placeholder="Set Password">
</div>
<div class="d-flex justify-content-between">
<button type="submit" class="btn btn-success">Signup</button>
<!-- <br>
<br> -->
<a onclick="formLogin()" href="#" style="color:#0000FF">Login</a>
</div>`;

let loginForm = document.createElement('form');
loginForm.id = "loginForm";
loginForm.innerHTML = `<div class="form-group">
<label class="lead" for="exampleInputEmail1">Email address</label>
<input type="email" class="form-control" id="exampleInputEmail1" aria-describedby="emailHelp"
    name="email" placeholder="Enter email">
<label class="lead" for="exampleInputPassword1">Password</label>
<input type="password" class="form-control" id="exampleInputPassword1" name="password"
    placeholder="Password">
</div>
<div class="d-flex justify-content-between">
<button class="btn btn-success">Login</button>
<!-- <br>
<br> -->
<a onclick="formSignup()" href="#" style="color:#0000FF">Sign up</a>

</div>`

function formSignup() {
    let loginForm = document.getElementById('loginForm');
    let ex = document.querySelector('.mainCard');
    ex.style.top = "calc(50% - 250px)";
    ex.children[0].children[1].children[0].innerHTML = "Sign up"
    loginForm.replaceWith(signForm);
}

function formLogin(){
    let signForm = document.getElementById('signForm');
    let ex = document.querySelector('.mainCard');
    ex.style.top = "calc(50% - 150px)";
    ex.children[0].children[1].children[0].innerHTML = "Sign in"
    signForm.replaceWith(loginForm);
}
