document
  .getElementById("create-form")
  .addEventListener("submit", function (event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const record = Object.fromEntries(formData.entries());

    fetch("/create", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(record),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("Registro criado:", data);
        alert("Registro criado com sucesso!");
      })
      .catch((error) => console.error("Erro ao criar registro:", error));
  });

document
  .getElementById("query-form")
  .addEventListener("submit", function (event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const name = formData.get("name");

    window.location.href = `record.html?name=${name}`;
  });
