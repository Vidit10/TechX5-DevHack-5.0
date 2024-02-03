function redirectToHome() {
  window.location.href = 'index.html';
}

function login() {
  const username = document.getElementById('username').value;
  const password = document.getElementById('password').value;

  fetch('login.csv')
    .then(response => response.text())
    .then(csv => {
      const rows = csv.split('\n');
      for (let i = 1; i < rows.length; i++) { // Start from 1 to skip header
        const columns = rows[i].split(',');
        const csvUsername = columns[0].trim();
        const csvPassword = columns[1].trim();
        if (csvUsername === username && csvPassword === password) {
          alert('Login successful!');
          return;
        }
      }
      alert('Invalid username or password. Please try again.');
    })
    .catch(error => console.error('Error:', error));
}

// Attach the click event listener directly to the button
document.getElementById('loginButton').addEventListener('click', function(event) {
  event.preventDefault(); // Prevent form submission
  login(); // Call login function
});
