function showLoading(buttonId) {
    var button = document.getElementById(buttonId);
    button.innerHTML = 'Loading...';
    button.disabled = true;
    button.style.backgroundColor = '#cccccc'; // Optional: change background color to indicate loading
    }