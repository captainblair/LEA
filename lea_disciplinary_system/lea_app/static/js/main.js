// Initialize tooltips
document.addEventListener('DOMContentLoaded', function() {
    // Initialize all tooltips
    const tooltipTriggers = document.querySelectorAll('[data-tooltip]');
    
    tooltipTriggers.forEach(trigger => {
        trigger.addEventListener('mouseenter', showTooltip);
        trigger.addEventListener('mouseleave', hideTooltip);
    });
    
    // Center-specific styling
    const centerBadges = document.querySelectorAll('.center-badge');
    centerBadges.forEach(badge => {
        const center = badge.dataset.center;
        if (center === 'MSDP') {
            badge.classList.add('badge-msdp');
        } else if (center === 'Highway') {
            badge.classList.add('badge-highway');
        }
    });
    
    // Attendance form toggle
    const statusRadios = document.querySelectorAll('input[name="status"]');
    const reasonField = document.getElementById('reason-field');
    
    if (statusRadios && reasonField) {
        statusRadios.forEach(radio => {
            radio.addEventListener('change', function() {
                if (this.value === 'absent' && this.checked) {
                    reasonField.classList.remove('hidden');
                } else {
                    reasonField.classList.add('hidden');
                }
            });
        });
        
        // Check on page load
        const absentRadio = document.querySelector('input[name="status"][value="absent"]');
        if (absentRadio && absentRadio.checked) {
            reasonField.classList.remove('hidden');
        }
    }
    
    // Initialize all charts
    initializeCharts();
});

function showTooltip(e) {
    const tooltipText = this.getAttribute('data-tooltip');
    const tooltip = document.createElement('div');
    
    tooltip.className = 'absolute z-50 w-max max-w-xs px-2 py-1 text-xs text-white bg-gray-800 rounded shadow-lg';
    tooltip.textContent = tooltipText;
    tooltip.id = 'dynamic-tooltip';
    
    document.body.appendChild(tooltip);
    
    positionTooltip(this, tooltip);
}

function hideTooltip() {
    const tooltip = document.getElementById('dynamic-tooltip');
    if (tooltip) {
        tooltip.remove();
    }
}

function positionTooltip(element, tooltip) {
    const rect = element.getBoundingClientRect();
    const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
    
    tooltip.style.top = `${rect.top + scrollTop - tooltip.offsetHeight - 5}px`;
    tooltip.style.left = `${rect.left + rect.width / 2 - tooltip.offsetWidth / 2}px`;
}

function initializeCharts() {
    // Attendance Chart
    const attendanceCtx = document.getElementById('attendanceChart');
    if (attendanceCtx) {
        const attendanceChart = new Chart(attendanceCtx, {
            type: 'line',
            data: {
                labels: JSON.parse(attendanceCtx.dataset.labels),
                datasets: [{
                    label: 'Attendance Percentage',
                    data: JSON.parse(attendanceCtx.dataset.data),
                    backgroundColor: 'rgba(79, 70, 229, 0.1)',
                    borderColor: 'rgba(79, 70, 229, 1)',
                    borderWidth: 2,
                    tension: 0.3,
                    fill: true
                }]
            },
            options: getChartOptions('Attendance Percentage')
        });
    }
    
    // Compliance Chart
    const complianceCtx = document.getElementById('complianceChart');
    if (complianceCtx) {
        const complianceChart = new Chart(complianceCtx, {
            type: 'bar',
            data: {
                labels: JSON.parse(complianceCtx.dataset.labels),
                datasets: [
                    {
                        label: 'Physical',
                        data: JSON.parse(complianceCtx.dataset.physical),
                        backgroundColor: 'rgba(59, 130, 246, 0.7)',
                    },
                    {
                        label: 'Online',
                        data: JSON.parse(complianceCtx.dataset.online),
                        backgroundColor: 'rgba(139, 92, 246, 0.7)',
                    },
                    {
                        label: 'Meetups',
                        data: JSON.parse(complianceCtx.dataset.meetups),
                        backgroundColor: 'rgba(16, 185, 129, 0.7)',
                    }
                ]
            },
            options: getChartOptions('Session Types')
        });
    }
}

function getChartOptions(title) {
    return {
        responsive: true,
        plugins: {
            legend: {
                position: 'top',
                labels: {
                    color: getComputedStyle(document.documentElement).getPropertyValue('--text-color') || '#374151'
                }
            },
            title: {
                display: true,
                text: title,
                color: getComputedStyle(document.documentElement).getPropertyValue('--text-color') || '#374151'
            },
            tooltip: {
                mode: 'index',
                intersect: false
            }
        },
        scales: {
            y: {
                beginAtZero: true,
                max: 100,
                ticks: {
                    color: getComputedStyle(document.documentElement).getPropertyValue('--text-color') || '#374151',
                    callback: function(value) {
                        return value + '%';
                    }
                },
                grid: {
                    color: getComputedStyle(document.documentElement).getPropertyValue('--border-color') || 'rgba(0, 0, 0, 0.1)'
                }
            },
            x: {
                ticks: {
                    color: getComputedStyle(document.documentElement).getPropertyValue('--text-color') || '#374151'
                },
                grid: {
                    color: getComputedStyle(document.documentElement).getPropertyValue('--border-color') || 'rgba(0, 0, 0, 0.1)'
                }
            }
        }
    };
}