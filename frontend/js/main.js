const API_BASE_URL = 'http://localhost:5000/api';

// Modal Functions
function showModal(modalId) {
    document.getElementById(modalId).classList.add('show');
}

function closeModal(modalId) {
    document.getElementById(modalId).classList.remove('show');
}

function showInvoiceForm() {
    showModal('invoiceModal');
}

function showAccountForm() {
    showModal('accountModal');
}

function showTransactionForm() {
    alert('Transaction form - to be implemented');
}

// API Functions
async function fetchInvoices() {
    try {
        const response = await fetch(`${API_BASE_URL}/invoices/`);
        const invoices = await response.json();
        displayInvoices(invoices);
    } catch (error) {
        console.error('Error fetching invoices:', error);
    }
}

async function fetchAccounts() {
    try {
        const response = await fetch(`${API_BASE_URL}/bookkeeping/accounts`);
        const accounts = await response.json();
        displayAccounts(accounts);
    } catch (error) {
        console.error('Error fetching accounts:', error);
    }
}

async function generateBalanceSheet() {
    try {
        const response = await fetch(`${API_BASE_URL}/reporting/balance-sheet`);
        const data = await response.json();
        displayBalanceSheet(data);
    } catch (error) {
        console.error('Error generating balance sheet:', error);
    }
}

async function generateIncomeStatement() {
    try {
        const response = await fetch(`${API_BASE_URL}/reporting/income-statement`);
        const data = await response.json();
        displayIncomeStatement(data);
    } catch (error) {
        console.error('Error generating income statement:', error);
    }
}

// Display Functions
function displayInvoices(invoices) {
    const table = document.getElementById('invoicesTable');
    if (invoices.length === 0) {
        table.innerHTML = '<tr><td colspan="6">No invoices yet.</td></tr>';
        return;
    }
    table.innerHTML = invoices.map(inv => `
        <tr>
            <td>${inv.invoice_number}</td>
            <td>Customer #${inv.customer_id}</td>
            <td>$${inv.total_amount.toFixed(2)}</td>
            <td><span class="status ${inv.status}">${inv.status}</span></td>
            <td>${new Date(inv.invoice_date).toLocaleDateString()}</td>
            <td><a href="#">View</a></td>
        </tr>
    `).join('');
}

function displayAccounts(accounts) {
    const table = document.getElementById('accountsTable');
    if (accounts.length === 0) {
        table.innerHTML = '<tr><td colspan="4">No accounts yet.</td></tr>';
        return;
    }
    table.innerHTML = accounts.map(acc => `
        <tr>
            <td>${acc.account_number}</td>
            <td>${acc.account_name}</td>
            <td>${acc.account_type}</td>
            <td>$${acc.balance.toFixed(2)}</td>
        </tr>
    `).join('');
}

function displayBalanceSheet(data) {
    const output = document.getElementById('reportOutput');
    let html = '<h3>Balance Sheet</h3>';
    html += '<h4>Assets</h4><ul>';
    data.assets.forEach(asset => {
        html += `<li>${asset.account_name}: $${asset.balance.toFixed(2)}</li>`;
    });
    html += `</ul><strong>Total Assets: $${data.totals.total_assets.toFixed(2)}</strong>`;
    html += '<h4>Liabilities</h4><ul>';
    data.liabilities.forEach(liability => {
        html += `<li>${liability.account_name}: $${liability.balance.toFixed(2)}</li>`;
    });
    html += `</ul><strong>Total Liabilities: $${data.totals.total_liabilities.toFixed(2)}</strong>`;
    html += '<h4>Equity</h4><ul>';
    data.equity.forEach(eq => {
        html += `<li>${eq.account_name}: $${eq.balance.toFixed(2)}</li>`;
    });
    html += `</ul><strong>Total Equity: $${data.totals.total_equity.toFixed(2)}</strong>`;
    output.innerHTML = html;
}

function displayIncomeStatement(data) {
    const output = document.getElementById('reportOutput');
    let html = '<h3>Income Statement</h3>';
    html += '<h4>Revenues</h4><ul>';
    data.revenues.forEach(rev => {
        html += `<li>${rev.account_name}: $${rev.balance.toFixed(2)}</li>`;
    });
    html += `</ul><strong>Total Revenue: $${data.totals.total_revenue.toFixed(2)}</strong>`;
    html += '<h4>Expenses</h4><ul>';
    data.expenses.forEach(exp => {
        html += `<li>${exp.account_name}: $${exp.balance.toFixed(2)}</li>`;
    });
    html += `</ul><strong>Total Expenses: $${data.totals.total_expenses.toFixed(2)}</strong>`;
    html += `<h4>Net Income: $${data.totals.net_income.toFixed(2)}</h4>`;
    output.innerHTML = html;
}

// Close modal on outside click
window.onclick = function(event) {
    if (event.target.classList.contains('modal')) {
        event.target.classList.remove('show');
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    fetchInvoices();
    fetchAccounts();
});
