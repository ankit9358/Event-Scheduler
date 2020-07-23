const token = getCookie('Token');

getEvents(token);

// --------------------------------------------READ-----------------------------------------------------
async function showModal(slug) {
    try {
        url = `http://127.0.0.1:8000/event/get_schedule/${slug}`
        params = {
            headers: {
                'Authorization': `Token  ${token}`
            }
        }
        const response = await fetch(url, params);
        const event = await response.json();
        document.getElementById('showTitle').innerHTML = event.title;
        document.getElementById('showEvent').innerHTML = event.event;
        document.getElementById('showDate').innerHTML = event.date;

    }
    catch (err) {

    }
}
// --------------------------------------------DELETE-----------------------------------------------------
async function deleteModal(slug) {
    try {
        url = `http://127.0.0.1:8000/event/del_schedule/${slug}`
        params = {
            method: 'DELETE',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Authorization': `Token  ${token}`
            },
        }
        let decission = confirm("Are you sure want to delete!");
        if (decission) {
            const response = await fetch(url, params);
            const event = await response.json();
            document.getElementById('delMsg').innerHTML = `<div class="alert alert-success alert-dismissible fade show" role="alert">
            <strong>Deleted!</strong> The Event has been deleted successfully
            <button type="button" class="close" data-dismiss="alert" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>`
            getEvents(token);
            return;
        }
        return;


    }
    catch (err) {

    }
}
// --------------------------------------------UPDATE-----------------------------------------------------
async function editModal(slug) {
    try {
        url = `http://127.0.0.1:8000/event/get_schedule/${slug}`
        params = {
            headers: {
                'Authorization': `Token  ${token}`
            }
        }
        const response = await fetch(url, params);
        const event = await response.json();
        document.getElementById('editTitle').value = event.title;
        document.getElementById('editEvent').value = event.event;
        document.getElementById('editDate').value = event.date;
        document.getElementById("saveChanges").addEventListener("click", async function good(event) {
            event.preventDefault()
            let title = (document.getElementById("editTitle").value);
            let eventDesc = (document.getElementById("editEvent").value);
            let date = (document.getElementById("editDate").value);
            if (title && eventDesc && date) {
                try {
                    console.log("2");
                    url = `http://127.0.0.1:8000/event/put_schedule/${slug}`
                    let data = { "title": title, "event": eventDesc, "date": date }

                    params = {
                        method: 'PUT',
                        headers: {
                            'Accept': 'application/json',
                            'Content-Type': 'application/json',
                            'Authorization': `Token  ${token}`
                        },
                        body: JSON.stringify(data)
                    }
                    console.log("2.5");
                    const response2 = await fetch(url, params);
                    console.log("3");
                    console.log(response);
                    const data2 = await response2.json();
                    console.log("4");
                    console.log(data2);
                    if (data2.success == "Update successfully") {
                        document.getElementById("saveChanges").removeEventListener("click", good);
                        document.getElementById("editTitle").value = "";
                        (document.getElementById("editEvent").value = "");
                        (document.getElementById("editDate").value = "");
                        alert("Updated Successfully");
                        getEvents(token);
                    }

                }
                catch (err) {
                    console.log(err);
                }

            }
            else {
                alert("Please Fill All Inputs");
            }

            getEvents(token);
            return;
        });


    }
    catch (err) {
        console.log(err)
    }
}
// --------------------------------------------CREATE-----------------------------------------------------
async function createModal() {
    document.getElementById("saveChanges").addEventListener("click", async function make(event) {
        event.preventDefault()
        let title = (document.getElementById("editTitle").value);
        let eventDesc = (document.getElementById("editEvent").value);
        let date = (document.getElementById("editDate").value);
        if (title && eventDesc && date) {
            try {
                console.log("2");
                url = `http://127.0.0.1:8000/event/post_schedule/`
                let data = { "title": title, "event": eventDesc, "date": date }

                params = {
                    method: 'POST',
                    headers: {
                        'Accept': 'application/json',
                        'Content-Type': 'application/json',
                        'Authorization': `Token  ${token}`
                    },
                    body: JSON.stringify(data)
                }
                console.log("2.5");
                const response2 = await fetch(url, params);
                console.log("3");
                console.log(response2);
                const data2 = await response2.json();
                console.log("4");
                console.log(data2);
                if (data2.success) {
                    document.getElementById("saveChanges").removeEventListener("click", make);
                    document.getElementById('delMsg').innerHTML = `<div class="alert alert-success alert-dismissible fade show" role="alert">
                                    <strong>Created!</strong> The Event has been created successfully
                                    <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                                    <span aria-hidden="true">&times;</span>
                                    </button>
                                </div>`
                    document.getElementById("editTitle").value = "";
                    (document.getElementById("editEvent").value = "");
                    (document.getElementById("editDate").value = "");
                    getEvents(token);
                    // return;
                }

            }
            catch (err) {
                console.log(err);
            }

        }
        else {
            alert("Please Fill All Inputs");
        }

        getEvents(token);
        return;
    });

}

// --------------------------------------------GET_ALL_EVENT--------------------------------------------------
async function getEvents(token) {
    try {
        url = 'http://127.0.0.1:8000/event/get_all_event/'
        params = {
            headers: {
                'Authorization': `Token  ${token}`
            }
        }
        const response = await fetch(url, params);
        const userData = await response.json();
        let welcome = document.getElementById("welcome");
        welcome.innerHTML = userData.user;
        let items = userData.events;
        let card = document.getElementById("allEvent");
        card.innerHTML = ""
        items.forEach(item => {
            let event = (item.event).substring(0, 30);
            card.innerHTML += `<div class="col-md-4">
                                <div class="card-content">
                                    <a href="#showModal" onClick="showModal('${item.slug}')" data-toggle="modal" data-focus="false">
                                        <div class="card-desc">
                                            <h3>${item.title}</h3>
                                            <p>${event}.....</p>
                                            <p>${item.date}</p>
                                    </a>
                                            <div>
                                            <button type="button" class="btn btn-secondary" data-toggle="modal"
                                                data-target="#editModal" onClick="editModal('${item.slug}')">Edit</button>
                                            <button type="button" onClick="deleteModal('${item.slug}')" class="btn btn-danger">Delete</button>
                                            </div>
                                        </div>
                                </div>
                                        
                            </div>`
        });
    }
    catch (err) {
        console.log(err);
    }
}
getEvents(token);

function logout(){
    deleteAllCookies();
    location.href = "/index.html";

}

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

function deleteAllCookies() {
    var cookies = document.cookie.split(";");

    for (var i = 0; i < cookies.length; i++) {
        var cookie = cookies[i];
        var eqPos = cookie.indexOf("=");
        var name = eqPos > -1 ? cookie.substr(0, eqPos) : cookie;
        document.cookie = name + "=;expires=Thu, 01 Jan 1970 00:00:00 GMT";
    }
}