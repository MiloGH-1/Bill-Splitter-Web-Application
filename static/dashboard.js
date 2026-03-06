const modal = document.querySelector(".add_modal");
const addButton = document.getElementById("add");
const closeButton = document.querySelector(".close");

addButton.onclick = function() {
    modal.style.display = "block";
}

closeButton.onclick = function() {
    modal.style.display = "none";
}

window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}

document.addEventListener("DOMContentLoaded", () => {
    const bill_modal = document.getElementById("bill_modal");
    const close_bill = document.querySelector(".close_bill");
    const modal_bill_name = document.getElementById("modal_bill_name");
    const modal_bill_amount = document.getElementById("modal_bill_amount")
    const bill_list = document.querySelectorAll(".bill_click")
    const modal_recipients = document.getElementById("modal_recipients")
    const modal_image = document.getElementById("modal_image")



    bill_list.forEach(item => {
        item.addEventListener("click", function() {
            const billId = this.getAttribute("data_bill_id");

            fetch(`/get_bill/${billId}`)
                .then(response => response.json())
                .then(data => {
                    if (data.error){
                        alert(data.error);
                        return;
                    }

                    modal_bill_name.textContent = data.name;
                    modal_bill_amount.textContent = data.amount;
                    modal_recipients.textContent = data.recipients
                    
                    if (data.image) {
                        modal_image.src = "data:image/jpeg;base64," + data.image;
                        modal_image.style.display = "block";

                    } else {
                        modal_image.style.display = "none"; 
                        modal_image.src = ""; 
                    }

                    bill_modal.style.display = "block"
                })
                .catch(error => {
                    console.error("Error with data", error);
                });
        });
    });

    if(close_bill){
        close_bill.addEventListener("click", () =>{
        bill_modal.style.display = "none";
    });
    }

    window.addEventListener("click", (event) => {
        if (event.target == bill_modal){
            bill_modal.style.display = "none";
        }
    })
});


document.getElementById("recipient").addEventListener("keydown", function(event) {
    const error = document.getElementById("recipient_error");
    error.style.display = "none";

    if (event.key === "Enter") {
        event.preventDefault(); 
        
        let name = this.value.trim();
        
        let current_logged = document.getElementById("current_logged_user").value.trim()
        
    
        if (name !== "") {
            if (name.length > 20) {
                error.textContent = "Usernames cannot be longer than 20 characters.";
                error.style.display = "block";
                return;
            }
        
            if (name === current_logged) {
                error.textContent = "You cannot address a bill to yourself.";
                error.style.display = "block";
                return;
            }

            let already_in = Array.from(document.querySelectorAll("input[name='recipientList']")).map(input => input.value)
            
            if (already_in.includes(name)) {
                error.textContent = "This user is already in the list.";
                error.style.display = "block";
                return;
            }

            const users = document.getElementById("user_data");
            const valid_users = JSON.parse(users.getAttribute("data-users"));
            if (!valid_users.includes(name)) {
                error.textContent = "User does not exist in the database.";
                error.style.display = "block";
                return;
            }

                let user = `<span>
                                ${name} 
                                <b onclick="this.parentElement.remove()">X</b>
                                <input type="hidden" name="recipientList" value="${name}">
                            </span>`;
                document.getElementById("names_added").innerHTML += user;

                this.value = "";
        }
    }
});

document.querySelector("#bill").addEventListener('submit', function(event) {
    let hiddenData = document.getElementById("names_added");
    
    if (hiddenData.children.length === 0) {
        event.preventDefault(); 
        alert("Add atleast one recipient");
    }
});