const searchField = document.querySelector('#searchField');
const tableOutput = document.querySelector(".table-output");
const appTable = document.querySelector(".app-table");
const paginationContainer = document.querySelector(".pagination-container");
const tbody = document.querySelector(".table-body");
tableOutput.style.display = "none";

searchField.addEventListener("keyup", (e) => {
    const searchValue = e.target.value;

    if (searchValue.trim().length > 0) {
        console.log('searchValue is: ', searchValue);
        paginationContainer.style.display = "none";
        tbody.innerHTML = "";

        fetch("/income/income-search", {
            body: JSON.stringify({ searchText: searchValue}), 
            method: "POST",
        })
        .then((res) => res.json())
        .then((data) => {
            console.log("data", data);

        appTable.style.display = "none";

        tableOutput.style.display = "block";

        if(data.length===0){
            tableOutput.innerHTML="No results found.";
        } else {
            data.forEach((item)=>{
                tbody.innerHTML+=`
                <tr class="align-middle">
                    <td>${item.amount}</td>
                    <td>${item.source}</td>
                    <td>${item.description}</td>
                    <td>${item.date}</td>
                </tr>`;
            })
        }
        
        });
    } else {
        appTable.style.display = "block";
        paginationContainer.style.display = "";
        tableOutput.style.display = "none";
    }
});