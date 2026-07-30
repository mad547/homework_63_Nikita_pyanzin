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

function getToken() {
    return getCookie('api_token');
}

document.addEventListener('DOMContentLoaded', () => {
    const likeButtons = document.querySelectorAll('.like-btn');

    likeButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const postId = btn.dataset.postId;
            const icon = btn.querySelector('.like-icon');
            const countEl = btn.closest('.p-3').querySelector('.likes-count');
            const token = getToken();

            if (!token) {
                window.location.href = '/accounts/login/';
                return;
            }

            fetch(`/api/posts/${postId}/like/`, {
                method: 'POST',
                headers: {
                    'Authorization': `Token ${token}`,
                    'Content-Type': 'application/json',
                }
            })
            .then(response => response.json())
            .then(data => {
                countEl.textContent = `${data.likes_count} отметок «Нравится»`;
                if (data.liked) {
                    icon.textContent = '❤️';
                } else {
                    icon.textContent = '🤍';
                }
            });
        });
    });
});