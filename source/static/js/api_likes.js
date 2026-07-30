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
    return getCookie('apiToken');
}

document.addEventListener('DOMContentLoaded',  () => {
    const likeButtons = document.querySelectorAll('.like-btn');

    likeButtons.forEach(likeButton => {
        btn.addEventListener('click', () => {
            const postId = btn.dataset.postId;
            const countSpan = btn.querySelector('.likes-count');
            const icon = btn.querySelector('.like-icon');
            const token = getToken();

            if (!token) {
                window.location.href = 'accounts/login/';
            }

            fetch(`/api/posts/${postId}/like/`, {
                method: 'POST',
                headers: {
                    'autorization': `Token ${token}`,
                    'content-type': 'application/json',
                }
            })
            .then(response => response.json())
            .then(data => {
                countSpan.textContent = data.likes_count;
                if (data.liked) {
                    icon.textContent = '❤️';
                } else {
                    icon.textContent = '🤍';
                }
            });
        });
    });
});