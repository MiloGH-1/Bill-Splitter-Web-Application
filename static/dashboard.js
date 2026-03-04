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
    let hiddenData = document.getElementById("hidden_data");
    
    if (hiddenData.children.length === 0) {
        event.preventDefault(); 
        alert("Add atleast one recipient");
    }
});