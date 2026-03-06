document.addEventListener("DOMContentLoaded", () => {
    const bill_modal = document.getElementById("bill_modal");
    const close_bill = document.querySelector(".close_bill");
    const modal_bill_name = document.getElementById("modal_bill_name");
    const modal_bill_amount = document.getElementById("modal_bill_amount");
    const bill_list = document.querySelectorAll(".bill_click");
    const modal_recipients = document.getElementById("modal_recipients");
    const modal_image = document.getElementById("modal_image"); 

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
                    
                    if (modal_bill_name) modal_bill_name.textContent = data.name;
                    if (modal_bill_amount) modal_bill_amount.textContent = data.amount;
                    
                    if (modal_recipients) {
                        modal_recipients.innerHTML = ""; 
                        data.recipients.forEach(person => {
                            const row = document.createElement("div");
                            row.style.padding = "5px 0";
                            const icon = person.paid ? "✅" : "❌❌";
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

                    if (bill_modal) bill_modal.style.display = "block";
                })
                .catch(error => {
                    console.error("Error with data", error);
                });
        });
    });

    if (close_bill && bill_modal) {
        close_bill.addEventListener("click", () => {
            bill_modal.style.display = "none";
        });
    }

    window.addEventListener("click", (event) => {
        if (event.target == bill_modal){
            bill_modal.style.display = "none";
        }
    });
});