document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll("tbody tr").forEach(row => {
        let dataCell = row.cells[2]; // Assume que a data está na terceira coluna (index 2)
        let dataTexto = dataCell.textContent.trim();

        if (dataTexto) {
            let dataObj = new Date(dataTexto);
            if (!isNaN(dataObj.getTime())) {
                let dia = String(dataObj.getDate()).padStart(2, '0');
                let mes = String(dataObj.getMonth() + 1).padStart(2, '0'); // Mês começa do zero
                let ano = dataObj.getFullYear();
                let horas = String(dataObj.getHours()).padStart(2, '0');
                let minutos = String(dataObj.getMinutes()).padStart(2, '0');

                dataCell.textContent = `${dia}/${mes}/${ano} ${horas}:${minutos}`;
            }
        }
    });
});