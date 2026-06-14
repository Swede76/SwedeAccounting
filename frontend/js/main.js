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
    showModal('transactionModal');
}

// Form Submission Handlers
async function handleInvoiceSubmit(event) {
    event.preventDefault();
    
    const form = event.target;
    const invoiceNumber = form.querySelector('input[placeholder="Invoice Number"]').value;
    const customerId = form.querySelector('input[placeholder="Customer ID"]').value;
    const notes = form.querySelector('textarea').value;
    
    try {
        const response = await fetch(`${API_BASE_URL}/invoices`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                invoice_number: invoiceNumber,
                customer_id: customerId,
                notes: notes
            })
        });
        
        if (response.ok) {
            alert('Invoice created successfully!');
            form.reset();
            closeModal('invoiceModal');
            // Refresh invoice list
            loadInvoices();
        } else {
            alert('Error creating invoice');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error creating invoice: ' + error.message);
    }
}

async function handleAccountSubmit(event) {
    event.preventDefault();
    
    const form = event.target;
    const accountNumber = form.querySelector('input[placeholder="Account Number"]').value;
    const accountName = form.querySelector('input[placeholder="Account Name"]').value;
    const accountType = form.querySelector('select').value;
    
    try {
        const response = await fetch(`${API_BASE_URL}/bookkeeping/accounts`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                account_number: accountNumber,
                account_name: accountName,
                account_type: accountType
            })
        });
        
        if (response.ok) {
            alert('Account added successfully!');
            form.reset();
            closeModal('accountModal');
            // Refresh accounts list
            loadAccounts();
        } else {
            alert('Error adding account');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error adding account: ' + error.message);
    }
}

async function handleTransactionSubmit(event) {
    event.preventDefault();
    
    const form = event.target;
    const date = form.querySelector('input[type="date"]').value;
    const description = form.querySelector('input[placeholder="Description"]').value;
    const debit = form.querySelector('input[placeholder="Debit"]').value;
    const credit = form.querySelector('input[placeholder="Credit"]').value;
    
    try {
        const response = await fetch(`${API_BASE_URL}/bookkeeping/transactions`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                date: date,
                description: description,
                debit: debit,
                credit: credit
            })
        });
        
        if (response.ok) {
            alert('Transaction recorded successfully!');
            form.reset();
            closeModal('transactionModal');
            // Refresh transactions list
            loadTransactions();
        } else {
            alert('Error recording transaction');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error recording transaction: ' + error.message);
    }
}

// Load functions
async function loadInvoices() {
    try {
        const response = await fetch(`${API_BASE_URL}/invoices`);
        const data = await response.json();
        const tbody = document.getElementById('invoicesTable');
        
        if (data.invoices && data.invoices.length > 0) {
            tbody.innerHTML = data.invoices.map(invoice => `
                <tr>
                    <td>${invoice.invoice_number}</td>
                    <td>${invoice.customer_id}</td>
                    <td>$${invoice.amount || '0.00'}</td>
                    <td>${invoice.status || 'Pending'}</td>
                    <td>${invoice.date || 'N/A'}</td>
                    <td><button onclick="deleteInvoice(${invoice.id})">Delete</button></td>
                </tr>
            `).join('');
        }
    } catch (error) {
        console.error('Error loading invoices:', error);
    }
}

async function loadAccounts() {
    try {
        const response = await fetch(`${API_BASE_URL}/bookkeeping/accounts`);
        const data = await response.json();
        const tbody = document.getElementById('accountsTable');
        
        if (data.accounts && data.accounts.length > 0) {
            tbody.innerHTML = data.accounts.map(account => `
                <tr>
                    <td>${account.account_number}</td>
                    <td>${account.account_name}</td>
                    <td>${account.account_type}</td>
                    <td>$${account.balance || '0.00'}</td>
                </tr>
            `).join('');
        }
    } catch (error) {
        console.error('Error loading accounts:', error);
    }
}

async function loadTransactions() {
    try {
        const response = await fetch(`${API_BASE_URL}/bookkeeping/transactions`);
        const data = await response.json();
        const tbody = document.getElementById('transactionsTable');
        
        if (data.transactions && data.transactions.length > 0) {
            tbody.innerHTML = data.transactions.map(transaction => `
                <tr>
                    <td>${transaction.date}</td>
                    <td>${transaction.description}</td>
                    <td>${transaction.debit || '0.00'}</td>
                    <td>${transaction.credit || '0.00'}</td>
                </tr>
            `).join('');
        }
    } catch (error) {
        console.error('Error loading transactions:', error);
    }
}

// Navigation
function goToSection(sectionId) {
    const element = document.getElementById(sectionId);
    if (element) {
        element.scrollIntoView({ behavior: 'smooth' });
    }
}

// Close modal on outside click
window.onclick = function(event) {
    if (event.target.classList.contains('modal')) {
        event.target.classList.remove('show');
    }
}

// Navbar active link
function updateActiveNavLink() {
    const sections = document.querySelectorAll('section');
    const navLinks = document.querySelectorAll('.navbar-menu a');
    
    window.addEventListener('scroll', () => {
        let current = '';
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            if (pageYOffset >= sectionTop - 200) {
                current = section.getAttribute('id');
            }
        });
        
        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === `#${current}`) {
                link.classList.add('active');
            }
        });
    });
}

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    updateActiveNavLink();
    
    // Attach form submission handlers
    const invoiceForm = document.getElementById('invoiceForm');
    if (invoiceForm) {
        invoiceForm.addEventListener('submit', handleInvoiceSubmit);
    }
    
    const accountForm = document.getElementById('accountForm');
    if (accountForm) {
        accountForm.addEventListener('submit', handleAccountSubmit);
    }
    
    // Load data on startup
    loadInvoices();
    loadAccounts();
    loadTransactions();
});
