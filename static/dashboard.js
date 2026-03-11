//Obtaining the elements and declaring constants with them
const add_modal = document.querySelector(".add_modal");
const add_button = document.getElementById("add");
const close_button = document.querySelector(".close");


//Opens the add bill modal on the click of the add button
if (add_button && add_modal) {
    add_button.onclick = function() {
        add_modal.style.display = "block";
    }
}


//Closes the add bill modal on the click of the 'x' button
if (close_button && add_modal) {
    close_button.onclick = function() {
        add_modal.style.display = "none";
    }
}

//Waits for the whole page to load before running the following program
document.addEventListener("DOMContentLoaded", () => {
    //Declaring important constants and getting elements from the website pages
    const bill_modal = document.getElementById("bill_modal");
    const close_bill = document.querySelector(".close_bill");
    const modal_bill_name = document.getElementById("modal_bill_name");
    const modal_bill_amount = document.getElementById("modal_bill_amount")
    const bill_list = document.querySelectorAll(".bill_click")
    const modal_recipients = document.getElementById("modal_recipients")
    const modal_image = document.getElementById("modal_image")
    const hidden_delete_input = document.getElementById("hidden_delete_bill_id");
    const modal_date = document.getElementById("modal_date")
    const edit_modal = document.getElementById("edit_modal");
    const close_edit = document.querySelector(".close_edit");
    const edit_buttons = document.querySelectorAll(".edit_button");


    //Loops through every item in the bill list to make it clickable
    bill_list.forEach(item => {
        item.addEventListener("click", function() {
            //Declaring more constants by getting element ids
            const billId = this.getAttribute("data_bill_id");
            const paymentId = this.getAttribute("data_payment_id");

            const hidden_input = document.getElementById("hidden_payment_id");
            const paymentForm = document.getElementById("bill_payment");
            const bill_delete_form = document.getElementById("bill_delete")
            

            //Hides the delete button if someone is just paying a bill
            if (bill_delete_form) {
                if (paymentId) {
                    bill_delete_form.style.display = "none";
                }
            }
            
            //Shows the payment form if it is a bill for which they owe money
            if (paymentForm) {
                if (paymentId) {
                    paymentForm.style.display = "block";
                    if (hidden_input) hidden_input.value = paymentId;
                } else {
                    paymentForm.style.display = "none"; 
                }
            }

            //Sets the hidden input which will be used for deleting
            if (hidden_delete_input) {
                hidden_delete_input.value = billId;
            }   

            //Fecthes the data of the bill by using the flask python backend
            fetch(`/get_bill/${billId}`)
                .then(response => response.json())
                .then(data => {
                    if (data.error){
                        alert(data.error);
                        return;
                    }
                    
                    //Puts the data from the DB into the website
                    if (modal_date) modal_date.textContent = data.date;
                    if (modal_bill_name) modal_bill_name.textContent = data.name;
                    if (modal_bill_amount) modal_bill_amount.textContent = data.amount;
                    
                    //Chekcs if anyone has paid yet, this allows us to know if the bill can be deleted or not
                    if (bill_delete_form && !paymentId) {
                        let anyone_paid = false;
                        if (data.recipients) {
                            anyone_paid = data.recipients.some(person => person.paid === true);
                        }
                        
                        //Hides the delete button if atleast one person has paid the bill
                        if (anyone_paid) {
                            bill_delete_form.style.display = "none";
                        } else {
                            bill_delete_form.style.display = "block";
                        }
                    }
                    
                    //Creates a list of people who owe money for a bill and adds check marks or an X if they have already paid or not
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
                    
                    //Shows the recipient image if there is one available to show
                    if (modal_image) {
                        if (data.image) {
                            modal_image.src = "data:image/jpeg;base64," + data.image;
                            modal_image.style.display = "block";
                        } else {
                            modal_image.style.display = "none"; 
                            modal_image.src = ""; 
                        }
                    }

                    //Opens the modal whioch holds the details
                    if (bill_modal) bill_modal.style.display = "block"
                })
                //If an error occurs the following is outputted
                .catch(error => {
                    console.error("Error with data", error);
                });
        });
    });
    
    //Handles the edit buttons for each item in the list
    edit_buttons.forEach(button => {
        button.addEventListener("click", function(e) {
            e.stopPropagation(); //Stops the main modal from opening, only the edit modal will appear

            //Obtaining values
            const bill_Id = this.getAttribute("data_bill_id");
            const bill_name = this.getAttribute("data_bill_name");
            const bill_amount = this.getAttribute("data_bill_amount");

            //Adding these values to into the edit form
            document.getElementById("hidden_edit_bill_id").value = bill_Id;
            document.getElementById("edit_name").value = bill_name;
            document.getElementById("edit_amount").value = bill_amount;

            //Opens the edit modal
            edit_modal.style.display = "block";
        });
    });

    //Closes the main modal when the 'X' is clicked
    if(close_bill && bill_modal) {
        close_bill.addEventListener("click", () =>{
            bill_modal.style.display = "none";
        });
    }

    //Closes the edit modal when the 'X' is clikced
    if (close_edit) {
        close_edit.addEventListener("click", function() {
        edit_modal.style.display = "none";
    });
}
    
    //Closes an modal when the background is clicked
    window.addEventListener("click", (event) => {
        if (add_modal && event.target == add_modal) {
            add_modal.style.display = "none";
        }
        if (bill_modal && event.target == bill_modal){
            bill_modal.style.display = "none";
        }
        if (event.target == edit_modal) {
            edit_modal.style.display = "none";
        }
        })
    });

//Method to handle adding usernames to the add bill form
const recipientInput = document.getElementById("recipient");
if (recipientInput) {
    recipientInput.addEventListener("keydown", function(event) {
        const error = document.getElementById("recipient_error");
        if (error) error.style.display = "none";

        //When the enter key is pressed the following code is ran
        if (event.key === "Enter") {
            event.preventDefault(); 
            
            //Trim the name down to just the username
            let name = this.value.trim();
            let current_logged_input = document.getElementById("current_logged_user");
            let current_logged = current_logged_input ? current_logged_input.value.trim() : "";
            
            if (name !== "") {
                //Stops names which are two long
                if (name.length > 20) {
                    error.textContent = "Usernames cannot be longer than 20 characters.";
                    error.style.display = "block";
                    return;
                }
                
                //Stops name which matches the currently logged user
                if (name === current_logged) {
                    error.textContent = "You cannot address a bill to yourself.";
                    error.style.display = "block";
                    return;
                }

                //Checks if a username is already in the list of recipients
                let already_in = Array.from(document.querySelectorAll("input[name='recipientList']")).map(input => input.value)
                
                if (already_in.includes(name)) {
                    error.textContent = "This user is already in the list.";
                    error.style.display = "block";
                    return;
                }

                //Checks if the user actually exists in the DB
                const users = document.getElementById("user_data");
                if (users) {
                    const valid_users = JSON.parse(users.getAttribute("data-users"));
                    if (!valid_users.includes(name)) {
                        error.textContent = "User does not exist in the database.";
                        error.style.display = "block";
                        return;
                    }
                }
                
                //Adds the username to the webpage so it is visible with an 'X' next to it which once clicked will remove the name from the list
                let user = `<span>
                                ${name} 
                                <b style="cursor:pointer;" onclick="this.parentElement.remove()">×</b>
                                <input type="hidden" name="recipientList" value="${name}">
                            </span>`;
                const names_added = document.getElementById("names_added");
                //Adds the name to the HTML text
                if (names_added) names_added.innerHTML += user;

                this.value = "";
            }
        }
    });
}

//Stops the user from submitting a bill with no recipients
const billForm = document.querySelector("#bill");
if (billForm) {
    billForm.addEventListener('submit', function(event) {
        let hiddenData = document.getElementById("names_added");
        
        if (hiddenData && hiddenData.children.length === 0) {//Checks length of recipients list
            event.preventDefault(); 
            alert("Add at least one recipient");
        }
    });
}