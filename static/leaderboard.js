document.addEventListener('DOMContentLoaded', async function() {
    const res = await fetch('/api/leaderboard');
    const leaderboard = await res.json();
    const tbody = document.getElementById('leaderboard-body');
    tbody.innerHTML = '';
    leaderboard.forEach((user, idx) => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${idx + 1}</td>
            <td>${user.name}</td>
            <td>${user.referral_code}</td>
            <td>$${user.total_donations}</td>
        `;
        tbody.appendChild(tr);
    });
});