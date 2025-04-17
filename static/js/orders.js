document.addEventListener('DOMContentLoaded', function() {
    // 搜索功能
    const searchInput = document.getElementById('searchInput');
    const tableBody = document.getElementById('orderTableBody');
    const noResults = document.getElementById('noResults');
    const rows = tableBody.getElementsByTagName('tr');

    searchInput.addEventListener('input', function() {
        const searchText = this.value.toLowerCase();
        let hasResults = false;

        for (let row of rows) {
            const cells = row.getElementsByTagName('td');
            let found = false;

            for (let cell of cells) {
                if (cell.textContent.toLowerCase().includes(searchText)) {
                    found = true;
                    break;
                }
            }

            row.style.display = found ? '' : 'none';
            if (found) hasResults = true;
        }

        noResults.style.display = hasResults ? 'none' : 'block';
    });

    // 下載 CSV 功能
    const downloadBtn = document.querySelector('.download-btn');
    downloadBtn.addEventListener('click', function(e) {
        e.preventDefault();
        downloadCSV();
    });

    function downloadCSV() {
        const rows = [];
        const headers = Array.from(document.querySelectorAll('th')).map(th => th.textContent);
        rows.push(headers);

        const tableRows = document.querySelectorAll('tbody tr');
        tableRows.forEach(row => {
            if (row.style.display !== 'none') {
                const rowData = Array.from(row.querySelectorAll('td')).map(td => td.textContent);
                rows.push(rowData);
            }
        });

        let csvContent = "data:text/csv;charset=utf-8,";
        rows.forEach(row => {
            csvContent += row.join(',') + "\n";
        });

        const encodedUri = encodeURI(csvContent);
        const link = document.createElement("a");
        link.setAttribute("href", encodedUri);
        link.setAttribute("download", "訂單資料.csv");
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }

    // 表格排序功能
    const headers = document.querySelectorAll('th');
    headers.forEach(header => {
        header.addEventListener('click', function() {
            const index = Array.from(headers).indexOf(this);
            sortTable(index);
        });
    });

    function sortTable(columnIndex) {
        const table = document.querySelector('table');
        const tbody = table.querySelector('tbody');
        const rows = Array.from(tbody.querySelectorAll('tr'));
        
        rows.sort((a, b) => {
            const aValue = a.cells[columnIndex].textContent;
            const bValue = b.cells[columnIndex].textContent;
            
            if (!isNaN(aValue) && !isNaN(bValue)) {
                return aValue - bValue;
            }
            return aValue.localeCompare(bValue, 'zh-TW');
        });

        rows.forEach(row => tbody.appendChild(row));
    }
}); 