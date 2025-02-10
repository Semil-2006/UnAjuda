setTimeout(function() {
    const flashMessages = document.querySelectorAll('.alert');
    flashMessages.forEach(function(message) {
        message.remove();
    });
}, 3000);