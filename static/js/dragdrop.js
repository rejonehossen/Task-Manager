// Created by Rejone Hossen | Premium Task Manager | 2025

class Sortable {
    constructor(element, options = {}) {
        this.element = element;
        this.options = {
            animation: 150,
            ghostClass: 'sortable-ghost',
            onEnd: () => {},
            ...options
        };
        
        this.draggedItem = null;
        this.placeholder = null;
        this.init();
    }
    
    init() {
        this.element.querySelectorAll('.task-card').forEach(item => {
            item.setAttribute('draggable', 'true');
            
            item.addEventListener('dragstart', this.handleDragStart.bind(this));
            item.addEventListener('dragover', this.handleDragOver.bind(this));
            item.addEventListener('dragenter', this.handleDragEnter.bind(this));
            item.addEventListener('dragleave', this.handleDragLeave.bind(this));
            item.addEventListener('dragend', this.handleDragEnd.bind(this));
            item.addEventListener('drop', this.handleDrop.bind(this));
        });
    }
    
    handleDragStart(e) {
        this.draggedItem = e.target;
        e.dataTransfer.effectAllowed = 'move';
        e.dataTransfer.setData('text/html', e.target.innerHTML);
        
        // Add slight delay for better visual feedback
        setTimeout(() => {
            this.draggedItem.classList.add(this.options.ghostClass);
        }, 0);
    }
    
    handleDragOver(e) {
        e.preventDefault();
        e.dataTransfer.dropEffect = 'move';
        
        const afterElement = this.getDragAfterElement(e.clientY);
        if (afterElement == null) {
            this.element.appendChild(this.placeholder);
        } else {
            this.element.insertBefore(this.placeholder, afterElement);
        }
    }
    
    handleDragEnter(e) {
        e.preventDefault();
        if (!this.placeholder) {
            this.placeholder = document.createElement('div');
            this.placeholder.className = 'sortable-placeholder';
            this.placeholder.style.height = `${this.draggedItem.offsetHeight}px`;
        }
    }
    
    handleDragLeave(e) {
        e.preventDefault();
    }
    
    handleDragEnd(e) {
        e.preventDefault();
        this.draggedItem.classList.remove(this.options.ghostClass);
        if (this.placeholder && this.placeholder.parentNode) {
            this.placeholder.parentNode.removeChild(this.placeholder);
        }
        this.placeholder = null;
    }
    
    handleDrop(e) {
        e.preventDefault();
        if (e.target !== this.draggedItem && this.placeholder) {
            this.element.insertBefore(this.draggedItem, this.placeholder);
            this.element.removeChild(this.placeholder);
            this.placeholder = null;
            
            // Call the onEnd callback with the new order
            if (typeof this.options.onEnd === 'function') {
                const items = Array.from(this.element.children);
                this.options.onEnd({
                    oldIndex: items.indexOf(this.draggedItem),
                    newIndex: items.indexOf(this.draggedItem)
                });
            }
        }
    }
    
    getDragAfterElement(y) {
        const draggableElements = [...this.element.querySelectorAll('.task-card:not(.sortable-ghost)')];
        
        return draggableElements.reduce((closest, child) => {
            const box = child.getBoundingClientRect();
            const offset = y - box.top - box.height / 2;
            
            if (offset < 0 && offset > closest.offset) {
                return { offset: offset, element: child };
            } else {
                return closest;
            }
        }, { offset: Number.NEGATIVE_INFINITY }).element;
    }
}






