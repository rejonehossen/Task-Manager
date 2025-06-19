// Created by Rejone Hossen

document.addEventListener('DOMContentLoaded', function() {
  // Add ripple effect to all buttons
  const buttons = document.querySelectorAll('.btn-premium');
  buttons.forEach(button => {
    button.addEventListener('click', function(e) {
      // Remove any existing ripples
      const existingRipples = this.querySelectorAll('.ripple');
      existingRipples.forEach(ripple => ripple.remove());
      
      // Create new ripple
      const ripple = document.createElement('span');
      ripple.classList.add('ripple');
      
      // Position the ripple
      const rect = this.getBoundingClientRect();
      const size = Math.max(rect.width, rect.height);
      ripple.style.width = ripple.style.height = `${size}px`;
      ripple.style.left = `${e.clientX - rect.left - size/2}px`;
      ripple.style.top = `${e.clientY - rect.top - size/2}px`;
      
      this.appendChild(ripple);
      
      // Remove ripple after animation
      setTimeout(() => {
        ripple.remove();
      }, 600);
    });
  });
  
  // Form validation indicators
  const inputs = document.querySelectorAll('.premium-form input, .premium-form textarea, .premium-form select');
  inputs.forEach(input => {
    const formGroup = input.closest('.form-group');
    if (!formGroup) return;
    
    const validationIcon = document.createElement('div');
    validationIcon.classList.add('validation-icon');
    formGroup.appendChild(validationIcon);
    
    input.addEventListener('input', function() {
      if (this.checkValidity()) {
        validationIcon.innerHTML = '<i class="fas fa-check"></i>';
        validationIcon.style.color = '#4CAF50';
      } else if (this.value.length > 0) {
        validationIcon.innerHTML = '<i class="fas fa-times"></i>';
        validationIcon.style.color = '#F44336';
      } else {
        validationIcon.innerHTML = '';
      }
    });
  });
});