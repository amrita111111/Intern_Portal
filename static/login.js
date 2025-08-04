document.getElementById('login-form').addEventListener('submit', async function(e) {
    e.preventDefault();
    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;
    const user_id = parseInt(document.getElementById('user-select').value);
    
    if (!user_id) {
        document.getElementById('message').innerText = 'Please select a user to login as';
        return;
    }
    
    const res = await fetch('/api/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password, user_id })
    });
    const data = await res.json();
    if (data.success) {
        localStorage.setItem('user', JSON.stringify(data.user));
        window.location.href = '/dashboard';
    } else {
        document.getElementById('message').innerText = data.message;
    }
});