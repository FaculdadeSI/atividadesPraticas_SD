document.addEventListener("DOMContentLoaded", () => {
  const urlParams = new URLSearchParams(window.location.search);
  const name = urlParams.get("name");

  fetch(`/query?name=${name}`)
    .then((response) => response.json())
    .then((data) => {
      if (data.error) {
        alert(data.error);
        window.location.href = "/";
      } else {
        document.getElementById(
          "record-details"
        ).innerText = `Nome: ${data.name}, Email: ${data.email}, CPF: ${data.CPF}`;
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
        alert("Registro atualizado com sucesso!");
        location.reload();
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
        alert("Registro modificado com sucesso!");
        location.reload();
      })
      .catch((error) => console.error("Erro ao modificar registro:", error));
  });

document.getElementById("delete-btn").addEventListener("click", function () {
  const name = new URLSearchParams(window.location.search).get("name");

  fetch("/delete", {
    method: "DELETE",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ name }),
  })
    .then((response) => response.json())
    .then((data) => {
      alert("Registro excluído com sucesso!");
      window.location.href = "/";
    })
    .catch((error) => console.error("Erro ao excluir registro:", error));
});
