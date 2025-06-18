// Created by Rejone Hossen | Premium Task Manager | 2025

document.addEventListener('DOMContentLoaded', function() {
    // Dark mode toggle
    const darkModeToggle = document.getElementById('darkModeToggle');
    if (darkModeToggle) {
        darkModeToggle.addEventListener('change', function() {
            document.documentElement.classList.toggle('dark', this.checked);
            document.cookie = `darkMode=${this.checked}; path=/; max-age=31536000`;
        });
    }

    // Toggle task completion
    document.querySelectorAll('.toggle-complete').forEach(button => {
        button.addEventListener('click', function() {
            const taskId = this.dataset.taskId;
            const icon = this.querySelector('i');
            
            fetch(`/toggle-complete/${taskId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.completed) {
                    icon.classList.remove('fa-circle', 'text-gray-300');
                    icon.classList.add('fa-check-circle', 'text-green-500');
                    
                    // Get the task card and animate completion
                    const taskCard = this.closest('.task-card');
                    taskCard.classList.add('completed');
                    
                    // Show toast notification
                    showToast('Task marked as complete!', 'success');
                } else {
                    icon.classList.remove('fa-check-circle', 'text-green-500');
                    icon.classList.add('fa-circle', 'text-gray-300');
                    
                    // Show toast notification
                    showToast('Task marked as incomplete', 'info');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showToast('Error updating task', 'error');
            });
        });
    });

    // Initialize date pickers
    const dateInputs = document.querySelectorAll('input[type="datetime-local"]');
    dateInputs.forEach(input => {
        // Format the date value for display if it exists
        if (input.value) {
            const date = new Date(input.value);
            input.value = date.toISOString().slice(0, 16);
        }
    });

    // Check for overdue tasks and apply animation
    document.querySelectorAll('.task-card').forEach(card => {
        if (card.querySelector('.text-red-500')) {
            card.classList.add('overdue');
        }
    });
});

// Helper function to get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Toast notification function
function showToast(message, type) {
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.textContent = message;
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.classList.add('show');
    }, 100);
    
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => {
            toast.remove();
        }, 300);
    }, 3000);
}

// Initialize tooltips
function initTooltips() {
    const tooltipElements = document.querySelectorAll('[data-tooltip]');
    tooltipElements.forEach(el => {
        const tooltip = document.createElement('div');
        tooltip.className = 'tooltip';
        tooltip.textContent = el.dataset.tooltip;
        document.body.appendChild(tooltip);
        
        el.addEventListener('mouseenter', () => {
            const rect = el.getBoundingClientRect();
            tooltip.style.left = `${rect.left + rect.width / 2 - tooltip.offsetWidth / 2}px`;
            tooltip.style.top = `${rect.top - tooltip.offsetHeight - 5}px`;
            tooltip.style.opacity = '1';
        });
        
        el.addEventListener('mouseleave', () => {
            tooltip.style.opacity = '0';
        });
    });
}