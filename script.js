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

    fetch(`/query?name=${name}`)
      .then((response) => response.json())
      .then((data) => {
        if (data.error) {
          alert(data.error);
        } else {
          alert(`Registro encontrado: ${JSON.stringify(data)}`);
        }
      })
      .catch((error) => console.error("Erro ao buscar registro:", error));
  });

document
  .getElementById("update-form")
  .addEventListener("submit", function (event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const record = Object.fromEntries(formData.entries());

    fetch("/update", {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(record),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("Registro atualizado:", data);
        alert("Registro atualizado com sucesso!");
      })
      .catch((error) => console.error("Erro ao atualizar registro:", error));
  });

document
  .getElementById("patch-form")
  .addEventListener("submit", function (event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const record = Object.fromEntries(formData.entries());

    fetch("/modify", {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(record),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("Registro modificado:", data);
        alert("Registro modificado com sucesso!");
      })
      .catch((error) => console.error("Erro ao modificar registro:", error));
  });

document
  .getElementById("delete-form")
  .addEventListener("submit", function (event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const record = Object.fromEntries(formData.entries());

    fetch("/delete", {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(record),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("Registro excluído:", data);
        alert("Registro excluído com sucesso!");
      })
      .catch((error) => console.error("Erro ao excluir registro:", error));
  });
