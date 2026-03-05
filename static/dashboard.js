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
        if (event.key === "Enter") {
            event.preventDefault(); 
            
            let name = this.value.trim();
            
            if (name !== "") {
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