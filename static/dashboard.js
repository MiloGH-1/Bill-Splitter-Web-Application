const add_modal = document.querySelector(".add_modal");
const addButton = document.getElementById("add");
const closeButton = document.querySelector(".close");

if (addButton && add_modal) {
    addButton.onclick = function() {
        add_modal.style.display = "block";
    }
}

if (closeButton && add_modal) {
    closeButton.onclick = function() {
        add_modal.style.display = "none";
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
    const hidden_delete_input = document.getElementById("hidden_delete_bill_id");
    const modal_date = document.getElementById("modal_date")



    bill_list.forEach(item => {
        item.addEventListener("click", function() {
            const billId = this.getAttribute("data_bill_id");
            const paymentId = this.getAttribute("data_payment_id");

            const hidden_input = document.getElementById("hidden_payment_id");
            const paymentForm = document.getElementById("bill_payment");
            const bill_delete_form = document.getElementById("bill_delete")

           if (bill_delete_form) {
                if (paymentId) {
                    bill_delete_form.style.display = "none";
                }
            }

            if (paymentForm) {
                if (paymentId) {
                    paymentForm.style.display = "block";
                    if (hidden_input) hidden_input.value = paymentId;
                } else {
                    paymentForm.style.display = "none"; 
                }
            }

            if (hidden_delete_input) {
                hidden_delete_input.value = billId;
            }

            fetch(`/get_bill/${billId}`)
                .then(response => response.json())
                .then(data => {
                    if (data.error){
                        alert(data.error);
                        return;
                    }
                    
                    if (modal_date) modal_date.textContent = data.date;
                    if (modal_bill_name) modal_bill_name.textContent = data.name;
                    if (modal_bill_amount) modal_bill_amount.textContent = data.amount;

                    if (bill_delete_form && !paymentId) {
                        let anyone_paid = false;
                        if (data.recipients) {
                            anyone_paid = data.recipients.some(person => person.paid === true);
                        }
                        
                        if (anyone_paid) {
                            bill_delete_form.style.display = "none";
                        } else {
                            bill_delete_form.style.display = "block";
                        }
                    }
                    
                    if (modal_recipients) {
                        modal_recipients.innerHTML = ""; 
                        data.recipients.forEach(person => {
                            const row = document.createElement("div");
                            row.style.padding = "5px 0";
                            const icon = person.paid ? "✅" : "❌";
                            row.innerHTML = `<span>${icon} ${person.username}</span>`;
                            modal_recipients.appendChild(row);
                        });
                    }
                        
                    if (modal_image) {
                        if (data.image) {
                            modal_image.src = "data:image/jpeg;base64," + data.image;
                            modal_image.style.display = "block";
                        } else {
                            modal_image.style.display = "none"; 
                            modal_image.src = ""; 
                        }
                    }

                    if (bill_modal) bill_modal.style.display = "block"
                })
                .catch(error => {
                    console.error("Error with data", error);
                });
        });
    });

    if(close_bill && bill_modal) {
        close_bill.addEventListener("click", () =>{
            bill_modal.style.display = "none";
        });
    }

    window.addEventListener("click", (event) => {
        if (add_modal && event.target == add_modal) {
            add_modal.style.display = "none";
        }
        if (bill_modal && event.target == bill_modal){
            bill_modal.style.display = "none";
        }
    })
});

const recipientInput = document.getElementById("recipient");
if (recipientInput) {
    recipientInput.addEventListener("keydown", function(event) {
        const error = document.getElementById("recipient_error");
        if (error) error.style.display = "none";

        if (event.key === "Enter") {
            event.preventDefault(); 
            
            let name = this.value.trim();
            let current_logged_input = document.getElementById("current_logged_user");
            let current_logged = current_logged_input ? current_logged_input.value.trim() : "";
            
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
                if (users) {
                    const valid_users = JSON.parse(users.getAttribute("data-users"));
                    if (!valid_users.includes(name)) {
                        error.textContent = "User does not exist in the database.";
                        error.style.display = "block";
                        return;
                    }
                }

                let user = `<span>
                                ${name} 
                                <b style="cursor:pointer;" onclick="this.parentElement.remove()">×</b>
                                <input type="hidden" name="recipientList" value="${name}">
                            </span>`;
                const names_added = document.getElementById("names_added");
                if (names_added) names_added.innerHTML += user;

                this.value = "";
            }
        }
    });
}

const billForm = document.querySelector("#bill");
if (billForm) {
    billForm.addEventListener('submit', function(event) {
        let hiddenData = document.getElementById("names_added");
        
        if (hiddenData && hiddenData.children.length === 0) {
            event.preventDefault(); 
            alert("Add at least one recipient");
        }
    });
}