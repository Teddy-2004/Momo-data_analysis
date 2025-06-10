function fetchAndRenderData(filters = {}) {
  let url = "/api/categories";

  fetch(url)
    .then(res => res.json())
    .then(categoriesData => {
      renderCards(categoriesData);
      renderChart(categoriesData);
    })
    .catch(err => console.error("Error fetching categories:", err));
}

function renderCards(categoriesData) {
  const tableRow = document.getElementById("tableRow");
  tableRow.innerHTML = "";

  categoriesData.forEach(tableContent => {
    const tableBody = document.querySelector("#category-table tbody");

    const row = document.createElement("tr");

    row.innerHTML = `
      <td>${tableContent.name}</td>
      <td>RWF ${tableContent.amount.toLocaleString()}</td>
      <td>${tableContent.transactions} transactions</td>
    `;

    tableBody.appendChild(row);


    row.addEventListener("click", () => {
      fetchFilteredTransactions({ category: tableContent.name });
    });

    tableRow.appendChild(row);
  });
}

function fetchFilteredTransactions(filters) {
  let url = "/api/transactions?";
  let params = [];

  if (filters.category) params.push(`category=${encodeURIComponent(filters.category)}`);
  if (filters.dateFrom) params.push(`dateFrom=${filters.dateFrom}`);
  if (filters.dateTo) params.push(`dateTo=${filters.dateTo}`);
  if (filters.minAmount) params.push(`minAmount=${filters.minAmount}`);
  if (filters.maxAmount) params.push(`maxAmount=${filters.maxAmount}`);
  if (filters.search) params.push(`search=${encodeURIComponent(filters.search)}`);

  url += params.join("&");

  fetch(url)
    .then(res => res.json())
    .then(txList => {
      openModal(`Filtered Transactions - ${filters.category || "All"}`, txList);
    })
    .catch(err => console.error(err));
}

function openModal(title, txList) {
  const modal = document.getElementById("detailsModal");
  const modalBody = document.getElementById("modalBody");
  modalBody.innerHTML = `<h3>${title}</h3>`;

  if (txList.length === 0) {
    modalBody.innerHTML += "<p>No transactions found.</p>";
  } else {
    txList.forEach(tx => {
      const div = document.createElement("div");
      div.className = "txItem";
      div.innerHTML = `
        <p><strong>ID:</strong> ${tx.transaction_id || "N/A"}</p>
        <p><strong>Date:</strong> ${tx.transaction_date || "N/A"}</p>
        <p><strong>Amount:</strong> RWF ${tx.amount || 0}</p>
        <p><strong>Body:</strong> ${tx.sms_body}</p>
        <hr/>
      `;
      modalBody.appendChild(div);
    });
  }

  modal.style.display = "block";
}

document.getElementById("closeModal").onclick = function () {
  document.getElementById("detailsModal").style.display = "none";
};

function renderChart(categoriesData) {
  const ctx = document.getElementById("momoChart").getContext("2d");

  if (window.momoChartInstance) {
    window.momoChartInstance.destroy();
  }

  const labels = categoriesData.map(c => c.name);
  const values = categoriesData.map(c => c.amount);

  window.momoChartInstance = new Chart(ctx, {
    type: "bar",
    data: {
      labels: labels,
      datasets: [
        {
          label: "Total Amount (RWF)",
          data: values,
          backgroundColor: "#3f3fe8",
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      layout: {
        padding: 20,
      },
      scales: {
        y: {
          type: "logarithmic",
          beginAtZero: true,
          ticks: {
            callback: function (value) {
              return Number(value).toLocaleString();
            },
          },
        },
      },
    },
  });

  document.getElementById("momoChart").parentNode.style.height = "500px";
}

document.getElementById("searchBar").addEventListener("keypress", function (event) {
  if (event.key === "Enter") {
    const searchText = this.value.trim();
    if (searchText !== "") {
      fetchFilteredTransactions({ search: searchText });
    }
  }
});

document.getElementById("filterBtn").addEventListener("click", function () {
  const filters = {
    category: document.getElementById("typeFilter").value,
    dateFrom: document.getElementById("dateFrom").value,
    dateTo: document.getElementById("dateTo").value,
    minAmount: document.getElementById("minAmount").value,
    maxAmount: document.getElementById("maxAmount").value,
  };

  fetchFilteredTransactions(filters);
});

document.querySelector(".navbar-brand h1").addEventListener("click", function () {
  document.getElementById("typeFilter").value = "";
  document.getElementById("dateFrom").value = "";
  document.getElementById("dateTo").value = "";
  document.getElementById("minAmount").value = "";
  document.getElementById("maxAmount").value = "";
  document.getElementById("searchBar").value = "";
  fetchAndRenderData();
});

window.onload = function () {
  fetchAndRenderData();
};