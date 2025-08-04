document.addEventListener('DOMContentLoaded', async function() {
    const user = JSON.parse(localStorage.getItem('user'));
    if (!user) {
        window.location.href = '/';
        return;
    }
    document.getElementById('intern-name').innerText = user.name;
    document.getElementById('referral-code').innerText = user.referral_code;
    document.getElementById('total-donations').innerText = user.total_donations;
    const rewardsList = document.getElementById('rewards-list');
    rewardsList.innerHTML = '';
    user.rewards.forEach(reward => {
        const li = document.createElement('li');
        li.innerHTML = `<strong>${reward.name}</strong>: ${reward.description} - <span style="color:${reward.unlocked ? 'green' : 'gray'}">${reward.unlocked ? 'Unlocked' : 'Locked'}</span>`;
        rewardsList.appendChild(li);
    });
});