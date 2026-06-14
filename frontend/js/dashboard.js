const API_BASE_URL = 'http://localhost:5000/api';

let incomeExpenseChart = null;
let accountBalanceChart = null;
let bankAccountsChart = null;
let financialSummaryChart = null;

async function updateDashboard() {
    const period = document.getElementById('dashboardPeriod').value;
    
    try {
        // Fetch dashboard data
        const summaryResponse = await fetch(`${API_BASE_URL}/reporting/dashboard?days=${period}`);
        const summaryData = await summaryResponse.json();
        
        // Update summary cards
        updateSummaryCards(summaryData.summary);
        
        // Fetch income/expense data
        const incomeExpenseResponse = await fetch(`${API_BASE_URL}/reporting/dashboard/income-expense?months=12`);
        const incomeExpenseData = await incomeExpenseResponse.json();
        updateIncomeExpenseChart(incomeExpenseData.data);
        
        // Fetch account balances
        const accountBalanceResponse = await fetch(`${API_BASE_URL}/reporting/dashboard/account-balances`);
        const accountBalanceData = await accountBalanceResponse.json();
        updateAccountBalanceChart(accountBalanceData);
        
        // Fetch bank accounts
        const bankAccountsResponse = await fetch(`${API_BASE_URL}/reporting/dashboard/bank-accounts`);
        const bankAccountsData = await bankAccountsResponse.json();
        updateBankAccountsChart(bankAccountsData);
        
        // Update financial summary
        updateFinancialSummaryChart(summaryData.summary);
        
    } catch (error) {
        console.error('Error updating dashboard:', error);
    }
}

function updateSummaryCards(summary) {
    document.getElementById('totalRevenue').textContent = `$${summary.total_revenue.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2})}`;
    document.getElementById('totalExpenses').textContent = `$${summary.total_expenses.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2})}`;
    document.getElementById('netIncome').textContent = `$${summary.net_income.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2})}`;
    document.getElementById('accountBalance').textContent = `$${summary.account_balance.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2})}`;
    document.getElementById('outstandingInvoices').textContent = `$${summary.outstanding_invoices.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2})}`;
    document.getElementById('pendingBills').textContent = `$${summary.pending_bills.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2})}`;
    document.getElementById('bankBalance').textContent = `$${summary.bank_balance.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2})}`;
    document.getElementById('payrollCosts').textContent = `$${summary.payroll_costs.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2})}`;
    
    // Update card colors based on values
    const netIncomeCard = document.getElementById('netIncome').closest('.stat-card');
    if (summary.net_income > 0) {
        netIncomeCard.classList.add('positive');
    } else {
        netIncomeCard.classList.add('negative');
    }
}

function updateIncomeExpenseChart(data) {
    const ctx = document.getElementById('incomeExpenseChart').getContext('2d');
    
    if (incomeExpenseChart) {
        incomeExpenseChart.destroy();
    }
    
    incomeExpenseChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.map(d => d.month_short),
            datasets: [
                {
                    label: 'Income',
                    data: data.map(d => d.income),
                    borderColor: '#28a745',
                    backgroundColor: 'rgba(40, 167, 69, 0.1)',
                    tension: 0.4,
                    fill: true,
                    pointRadius: 5,
                    pointBackgroundColor: '#28a745',
                    pointBorderColor: '#fff',
                    pointBorderWidth: 2
                },
                {
                    label: 'Expenses',
                    data: data.map(d => d.expenses),
                    borderColor: '#dc3545',
                    backgroundColor: 'rgba(220, 53, 69, 0.1)',
                    tension: 0.4,
                    fill: true,
                    pointRadius: 5,
                    pointBackgroundColor: '#dc3545',
                    pointBorderColor: '#fff',
                    pointBorderWidth: 2
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'top',
                    labels: {
                        usePointStyle: true,
                        padding: 15,
                        font: {
                            size: 12
                        }
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(0,0,0,0.8)',
                    padding: 12,
                    titleFont: {
                        size: 14
                    },
                    bodyFont: {
                        size: 13
                    },
                    callbacks: {
                        label: function(context) {
                            return context.dataset.label + ': $' + context.parsed.y.toFixed(2);
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            return '$' + value.toFixed(0);
                        }
                    }
                }
            }
        }
    });
}

function updateAccountBalanceChart(data) {
    const ctx = document.getElementById('accountBalanceChart').getContext('2d');
    
    if (accountBalanceChart) {
        accountBalanceChart.destroy();
    }
    
    const labels = Object.keys(data);
    const values = Object.values(data).map(d => d.total);
    const colors = ['#007bff', '#dc3545', '#ffc107'];
    
    accountBalanceChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: values,
                backgroundColor: colors,
                borderColor: '#fff',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 15,
                        font: {
                            size: 12
                        }
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return '$' + context.parsed.toFixed(2);
                        }
                    }
                }
            }
        }
    });
}

function updateBankAccountsChart(data) {
    const ctx = document.getElementById('bankAccountsChart').getContext('2d');
    
    if (bankAccountsChart) {
        bankAccountsChart.destroy();
    }
    
    bankAccountsChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.accounts.map(a => a.name),
            datasets: [{
                label: 'Balance',
                data: data.accounts.map(a => a.balance),
                backgroundColor: [
                    '#007bff',
                    '#28a745',
                    '#ffc107',
                    '#17a2b8'
                ],
                borderRadius: 5,
                borderSkipped: false
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: true,
                    labels: {
                        font: {
                            size: 12
                        }
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return 'Balance: $' + context.parsed.x.toFixed(2);
                        }
                    }
                }
            },
            scales: {
                x: {
                    ticks: {
                        callback: function(value) {
                            return '$' + value.toFixed(0);
                        }
                    }
                }
            }
        }
    });
}

function updateFinancialSummaryChart(summary) {
    const ctx = document.getElementById('financialSummaryChart').getContext('2d');
    
    if (financialSummaryChart) {
        financialSummaryChart.destroy();
    }
    
    const totalRevenue = summary.total_revenue;
    const totalExpenses = summary.total_expenses;
    const payrollCosts = summary.payroll_costs;
    const netIncome = summary.net_income;
    
    financialSummaryChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Revenue', 'Expenses', 'Payroll', 'Net Income'],
            datasets: [{
                label: 'Amount ($)',
                data: [totalRevenue, totalExpenses, payrollCosts, netIncome],
                backgroundColor: [
                    '#28a745',
                    '#dc3545',
                    '#ffc107',
                    netIncome >= 0 ? '#007bff' : '#dc3545'
                ],
                borderRadius: 5,
                borderSkipped: false
            }]
        },
        options: {
            indexAxis: 'x',
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: true,
                    labels: {
                        font: {
                            size: 12
                        }
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return '$' + context.parsed.y.toFixed(2);
                        }
                    }
                }
            },
            scales: {
                y: {
                    ticks: {
                        callback: function(value) {
                            return '$' + value.toFixed(0);
                        }
                    }
                }
            }
        }
    });
}

function goToSection(section) {
    document.getElementById(section).scrollIntoView({ behavior: 'smooth' });
}

// Initialize dashboard on page load
document.addEventListener('DOMContentLoaded', function() {
    updateDashboard();
    // Refresh dashboard every 5 minutes
    setInterval(updateDashboard, 5 * 60 * 1000);
});
