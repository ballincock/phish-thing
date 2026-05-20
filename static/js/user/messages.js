let activeThreadId = null;
let cachedThreads = [];
let pollingInterval = null;
let typingTimeout = null;
let isCurrentlyTypingSignal = 0;

async function loadSidebarThreads() {
    const res = await fetch('/api/messages/sidebar');
    const data = await res.json();
    cachedThreads = data.threads || [];
    filterSidebarThreads();
}

function filterSidebarThreads() {
    const q = document.getElementById('sidebarSearchInput').value.toLowerCase();
    const container = document.getElementById('threadsContainer');
    container.innerHTML = '';
    
    const filtered = cachedThreads.filter(t => t.username.toLowerCase().includes(q) || t.preview.toLowerCase().includes(q));
    if (filtered.length === 0) {
        container.innerHTML = '<div style="color:#666; padding:20px; text-align:center; font-size:0.9rem;">No active threads found.</div>';
        return;
    }
    
    filtered.forEach(t => {
        const item = document.createElement('div');

        item.style = `padding:12px 15px; display:flex; align-items:center; gap:12px; cursor:pointer; border-bottom:1px solid #1e1e1e; background:${t.user_id === activeThreadId ? '#2d2d2d' : 'transparent'}`;
        item.onclick = () => selectActiveThread(t);
        item.innerHTML = `
            <div style="position:relative;">
                <img src="/static/${t.profile_picture}" style="width:42px; height:42px; border-radius:50%; object-fit:cover; border:1px solid #2d2d2d;">
                <div style="position:absolute; bottom:-2px; right:-2px; background:${t.online ? '#4cd137' : '#555'}; width:10px; height:10px; border-radius:50%; border:2px solid #121212;"></div>
                ${t.unread > 0 ? `<div style="position:absolute; top:-2px; right:-2px; background:var(--primary); width:10px; height:10px; border-radius:50%;"></div>` : ''}
            </div>
            <div style="flex:1; min-width:0;">
                <div style="display:flex; justify-content:space-between; align-items:baseline;">
                    <strong style="color:#fff; font-size:0.95rem; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">${t.display_name}</strong>
                    <span style="color:#666; font-size:0.7em;">${t.last_date.split(' ') || ''}</span>
                </div>
                <div style="color:${t.typing ? 'var(--primary)' : '#aaa'}; font-size:0.85rem; font-weight:${t.typing ? 'bold' : 'normal'}; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; margin-top:2px;">
                    ${t.typing ? 'is typing...' : (t.preview || 'No messages')}
                </div>
            </div>
        `;
        container.appendChild(item);
    });
}

async function selectActiveThread(thread) {
    activeThreadId = thread.user_id;
    document.getElementById('chatPlaceholderText').style.display = 'none';
    document.getElementById('chatHeader').style.display = 'flex';
    document.getElementById('messageInputForm').style.display = 'flex';
    document.getElementById('activeChatUser').innerText = thread.display_name;
    document.getElementById('activeChatAvatar').src = `/static/${thread.profile_picture}`;
    document.getElementById('blockUserBtn').innerText = thread.blocked ? "Unblock" : "Block";
    
    document.getElementById('messageBodyField').value = '';
    document.getElementById('charCounter').innerText = '0';
    
    if (window.innerWidth <= 768) { toggleSidebarView(false); }
    loadSidebarThreads();
    await fetchActiveMessages();
    
    clearInterval(pollingInterval);
    pollingInterval = setInterval(fetchActiveMessages, 3000);
}

async function fetchActiveMessages() {
    if (!activeThreadId) return;
    
    const res = await fetch(`/api/messages/thread/${activeThreadId}?typing=${isCurrentlyTypingSignal}`);
    const data = await res.json();
    
    document.getElementById('headerOnlineBadge').style.display = data.other_online ? 'block' : 'none';
    document.getElementById('headerTypingIndicator').style.display = data.other_typing ? 'block' : 'none';
    
    const feed = document.getElementById('messagesFeed');
    const wasAtBottom = feed.scrollHeight - feed.scrollTop <= feed.clientHeight + 100;
    
    feed.innerHTML = '';
    if (data.messages.length === 0) {
        feed.innerHTML = '<div style="margin:auto; color:#666;">No messages. Say hello!</div>';
        return;
    }
    
    data.messages.forEach(m => {
        const isMe = m.sender_id !== activeThreadId;
        const msgRow = document.createElement('div');
        msgRow.style = `display:flex; width:100%; justify-content:${isMe ? 'flex-end' : 'flex-start'};`;
        
        const bubble = document.createElement('div');
        bubble.title = `Sent at: ${m.time} - Click to copy text`;
        
        if (isMe) {
            bubble.style = "max-width:70%; padding:10px 14px; border-radius:12px; color:#ffffff; background:var(--primary); cursor:pointer;";
        } else {
            bubble.style = "max-width:70%; padding:10px 14px; border-radius:12px; color:#333333; background:#ffffff; cursor:pointer; border:1px solid #2d2d2d;";
        }
        
        bubble.innerHTML = `
            <div style="font-size:0.95rem; word-break:break-word;">${m.body}</div>
            <div style="display:flex; justify-content:space-between; align-items:center; font-size:0.65rem; color:${isMe ? '#ffd1e8' : '#777'}; margin-top:4px; gap:10px;">
                <span>${m.time}</span>
                ${m.deletable ? `<span onclick="deleteMessagePayload(${m.id}, event)" style="color:#f43f5e; font-weight:bold; margin-left:10px;">✕ Delete</span>` : ''}
            </div>
        `;
        bubble.onclick = () => { navigator.clipboard.writeText(m.body); alert("Text copied to clipboard!"); };
        
        msgRow.appendChild(bubble);
        feed.appendChild(msgRow);
    });
    
    if (wasAtBottom) { feed.scrollTop = feed.scrollHeight; }
}

function handleTypingNotification() {
    const field = document.getElementById('messageBodyField');
    document.getElementById('charCounter').innerText = field.value.length;
    
    if (isCurrentlyTypingSignal === 0) {
        isCurrentlyTypingSignal = 1;
    }
    
    clearTimeout(typingTimeout);
    typingTimeout = setTimeout(() => {
        isCurrentlyTypingSignal = 0;
    }, 3000);
}

async function sendMessagePayload(e) {
    e.preventDefault();
    const f = document.getElementById('messageBodyField');
    const body = f.value.trim();
    if (!body || !activeThreadId) return;
    
    isCurrentlyTypingSignal = 0;
    
    const res = await fetch('/api/messages/send', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ receiver_id: activeThreadId, body: body })
    });
    
    if (res.ok) {
        f.value = '';
        document.getElementById('charCounter').innerText = '0';
        await fetchActiveMessages();
        document.getElementById('messagesFeed').scrollTop = document.getElementById('messagesFeed').scrollHeight;
        loadSidebarThreads();
    } else {
        const data = await res.json();
        alert(data.error || "Failed to deliver message.");
    }
}

async function deleteMessagePayload(id, e) {
    e.stopPropagation();
    if (!confirm("Delete this message permanently?")) return;
    const res = await fetch(`/api/messages/delete/${id}`, { method: 'DELETE' });
    if (res.ok) { fetchActiveMessages(); loadSidebarThreads(); }
}

async function dispatchBlockToggle() {
    if (!activeThreadId) return;
    const res = await fetch(`/api/messages/block/${activeThreadId}`, { method: 'POST' });
    const data = await res.json();
    document.getElementById('blockUserBtn').innerText = data.status === "blocked" ? "Unblock" : "Block";
    loadSidebarThreads();
}

async function dispatchDeleteChat() {
    if (!activeThreadId || !confirm("Erase chat history? This cannot be undone.")) return;
    const res = await fetch(`/api/messages/delete-chat/${activeThreadId}`, { method: 'DELETE' });
    if (res.ok) { window.location.reload(); }
}

function openNewChatPrompt() { document.getElementById('newChatModal').style.display = 'flex'; }
function closeNewChatPrompt() { document.getElementById('newChatModal').style.display = 'none'; }

async function searchGlobalUsers(val) {
    const div = document.getElementById('globalSearchResults');
    div.innerHTML = '';
    if (val.trim().length === 0) return;
    
    const res = await fetch(`/api/messages/search-users?q=${encodeURIComponent(val)}`);
    const data = await res.json();
    
    data.users.forEach(u => {
        const row = document.createElement('div');
        row.style = "display:flex; align-items:center; gap:10px; padding:8px; background:#1e1e1e; border:1px solid #2d2d2d; border-radius:6px; cursor:pointer; color:#fff;";
        row.onclick = () => { selectActiveThread({ user_id: u.id, username: u.username, display_name: u.display_name, profile_picture: u.avatar, blocked: false, unread: 0, last_date: "", preview: "" }); closeNewChatPrompt(); };
        row.innerHTML = `<img src="/static/${u.avatar}" style="width:30px; height:30px; border-radius:50%; object-fit:cover;"><span>${u.display_name} (@${u.username})</span>`;
        div.appendChild(row);
    });
}

function toggleSidebarView(showSidebar) {
    const sidebar = document.getElementById('chatSidebar');
    const main = document.getElementById('chatMainDisplay');
    const toggleBtn = document.getElementById('sidebarToggleBtn');
    
    if (showSidebar) {
        sidebar.style.display = 'flex';
        main.style.display = 'none';
    } else {
        sidebar.style.display = 'none';
        main.style.display = 'flex';
        toggleBtn.style.display = 'block';
    }
}

window.addEventListener('resize', () => {
    if (window.innerWidth > 768) {
        document.getElementById('chatSidebar').style.display = 'flex';
        document.getElementById('chatMainDisplay').style.display = 'flex';
        document.getElementById('sidebarToggleBtn').style.display = 'none';
    }
});

document.addEventListener("DOMContentLoaded", () => {
    loadSidebarThreads();
    setInterval(loadSidebarThreads, 5000);
    if (window.innerWidth <= 768 && activeThreadId === null) { toggleSidebarView(true); }
});
