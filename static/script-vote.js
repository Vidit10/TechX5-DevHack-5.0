function redirectToHome() {
  window.location.href = 'index.html';
}


function vote() {
  const username = document.getElementById('username').value;
  const selectedCandidate = document.querySelector('input[name="candidate"]:checked').value;

  const voteData = {
      'username': username,
      'candidate': selectedCandidate,
      'public_key': 'participant_public_key_here', // Replace with the participant's public key
      'signature': '', // Placeholder for signature, to be filled in by server
  };

  fetch('/submit_vote', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify(voteData)
  })
  .then(response => {
      if (response.ok) {
          return response.json();
      } else {
          throw new Error('Vote submission failed');
          
      }
  })
  .then(data => {
      console.log(data.message);
      // Handle success message
  })
  .catch(error => {
      console.error('Error:', error);
      // Handle error
  });
}

document.getElementById('voteForm').addEventListener('submit', function (event) {
    event.preventDefault(); // Prevent form submission

    // Redirect to thankyou.html after successful submission
    window.location.href = 'thankyou.html';
});