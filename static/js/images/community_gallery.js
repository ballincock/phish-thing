    const posts = {{ posts|tojson }};

    function renderCurrentPost() {
    const post = posts[currentIndex];
    const stage = document.getElementById('post-stage');
    
    if (!post) {
        stage.innerHTML = '<p class="empty-msg">No posts to display.</p>';
        return;
    }

    stage.innerHTML = `
        <div class="social-card">
            <div class="card-header" onclick="window.location.href='/gallery-profile/${post.username}'">
                <img src="/static/${post.pfp}" class="avatar-sm">
                <span class="username">${post.display_name}</span>
            </div>
            
            <div class="image-box">
                <img src="/static/${post.image_path}" class="main-img">
            </div>

            <!-- Vote & Social Actions -->
            <div class="engagement-bar">
                <button onclick="handleVote(${post.id}, 1)" class="vote-btn">👍 <span id="likes-${post.id}">${post.likes}</span></button>
                <button onclick="handleVote(${post.id}, -1)" class="vote-btn">👎 <span id="dislikes-${post.id}">${post.dislikes}</span></button>
            </div>

            <!-- Metadata Tags -->
            <div class="post-details">
                <div class="tag-row">
                    <span class="tag">🐟 ${post.species}</span>
                    <span class="tag">🎣 ${post.lure_used}</span>
                    <span class="tag">🌡️ ${post.temp}°F</span>
                    <span class="tag">⏲️ ${post.time}</span>
                    <span class="tag">🌙 ${post.moon}</span>
                </div>
                <p class="post-notes">${post.notes}</p>
            </div>

            <!-- Comment Section -->
            <div class="comment-section">
            <div class="comment-input-group">
                <!-- IMPORTANT: The ID must have the -${post.id} suffix -->
                <input type="text" id="main-comment-input-${post.id}" placeholder="Write a comment...">
                <button class="btn-primary" onclick="sendComment(${post.id})">Post</button>
            </div>
            
            <!-- IMPORTANT: The ID must match what loadComments looks for -->
            <div id="comments-container-${post.id}" class="comments-list">
                Loading comments...
            </div>

        </div>
        </div>
    `;
    
    loadComments(post.id);

    window.requestAnimationFrame(() => {
        setTimeout(() => {
            loadComments(post.id);
        }, 50); 
    });

    setTimeout(() => {
        loadComments(post.id);
    }, 150); 
}

document.addEventListener('DOMContentLoaded', () => {
    console.log("Loaded posts:", posts);
    if (posts.length > 0) {
        renderCurrentPost();
    } else {
        document.getElementById('post-stage').innerHTML = '<p class="empty-msg">No community catches found yet.</p>';
    }
});
