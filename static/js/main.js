function openModal1(id) {
   const modal = document.getElementById(id);
   if (modal) modal.style.display = 'flex';
}

function closeModal1(id) {
   const modal = document.getElementById(id);
   if (modal) modal.style.display = 'none';
}

window.onclick = function (event) {
   if (event.target.classList.contains('modal-overlay')) {
      event.target.style.display = 'none';
   }
};

async function submitGalleryImage() {
   const form = document.getElementById('galleryForm');
   const formData = new FormData(form);

   try {
      const response = await fetch('/gallery/upload', {
         method: 'POST',
         body: formData
      });

      const result = await response.json();

      if (result.success) {
         alert("Catch logged successfully!");
         window.location.reload();
      } else {
         alert("Error: " + (result.error || "Upload failed"));
      }
   } catch (err) {
      console.error("Gallery Upload Error:", err);
      alert("Server connection failed.");
   }
}

async function viewDetails(imgId) {
   try {
      const response = await fetch(`/gallery/details/${imgId}`);
      const data = await response.json();

      if (data.error) {
         alert(data.error);
         return;
      }

      const detailContent = document.getElementById('detailContent');

      detailContent.innerHTML = `
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                <div class="detail-img-container">
                    <img src="/static/${data.image_path}" style="width: 100%; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);">
                </div>
                <div class="detail-meta-container">
                    <h2 style="margin-top: 0; color: #1e293b;">${data.species || 'Unknown Catch'}</h2>
                    <hr style="border: 0; border-top: 1px solid #e2e8f0; margin: 15px 0;">
                    
                    <p><strong>Lure / Bait:</strong> ${data.lure_used || 'N/A'}</p>
                    <p><strong>Conditions:</strong> ${data.temperature || '?' }°F | ${data.cloud_cover || 'N/A'}</p>
                    <p><strong>Barometer:</strong> ${data.pressure || 'N/A'} inHg</p>
                    <p><strong>Lunar Phase:</strong> ${data.moon_cycle || 'N/A'}</p>
                    
                    <div style="background: #f8fafc; padding: 15px; border-radius: 8px; border: 1px solid #e2e8f0; margin-top: 20px;">
                        <strong style="display: block; margin-bottom: 5px;">Field Notes:</strong>
                        <p style="margin: 0; font-size: 0.9rem; color: #475569;">${data.notes || 'No extra notes provided.'}</p>
                    </div>
                </div>
            </div>
        `;

      openModal1('detailsModal');
   } catch (err) {
      console.error("Fetch Detail Error:", err);
      alert("Could not load catch details.");
   }
}
async function submitProfileUpdate() {
   const form = document.getElementById('editProfileForm');
   const formData = new FormData(form);

   const response = await fetch('/profile/update', {
      method: 'POST',
      body: formData
   });

   const result = await response.json();
   if (result.success) {
      window.location.reload();
   } else {
      alert("Failed to update profile.");
   }
}

async function handleLogin() {
   const userEl = document.getElementById('login-username');
   const passEl = document.getElementById('login-password');

   if (!userEl || !passEl) return alert("Fields missing");

   const data = {
      username: userEl.value,
      password: passEl.value
   };

   const response = await fetch('/login', {
      method: 'POST',
      headers: {
         'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
   });

   const result = await response.json();
   if (result.success) {
      window.location.reload();
   } else {
      alert(result.error || "Login failed");
   }
}

function toggleAuth(view) {
   const loginForm = document.getElementById('login-form');
   const regForm = document.getElementById('register-form');
   const loginBtn = document.getElementById('btn-login-view');
   const regBtn = document.getElementById('btn-reg-view');

   if (view === 'login') {
      loginForm.style.display = 'block';
      regForm.style.display = 'none';
      loginBtn.classList.add('active');
      regBtn.classList.remove('active');
   } else {
      loginForm.style.display = 'none';
      regForm.style.display = 'block';
      loginBtn.classList.remove('active');
      regBtn.classList.add('active');
   }
}
async function handleRegister() {
   const fields = {
      username: 'reg-username',
      email: 'reg-email',
      password: 'reg-password',
      confirm: 'reg-confirm',
      question: 'reg-question',
      answer: 'reg-answer',
      backup_email: 'reg-backup'
   };

   const data = {};

   for (const [key, id] of Object.entries(fields)) {
      const el = document.getElementById(id);
      if (!el) {
         console.error(`Error: Element with ID "${id}" missing from the page.`);
         return;
      }
      data[key] = el.value.trim();
   }

   if (!data.username || !data.email || !data.password || !data.answer) {
      alert("Please fill in all required fields (Username, Email, Password, and Security Answer).");
      return;
   }

   if (data.password !== data.confirm) {
      alert("Passwords do not match!");
      return;
   }

   try {
      const response = await fetch('/register', {
         method: 'POST',
         headers: {
            'Content-Type': 'application/json'
         },
         body: JSON.stringify(data)
      });

      const result = await response.json();

      if (response.ok && result.mnemonic) {
         const modal = document.getElementById('mnemonicModal');
         const textDisplay = document.getElementById('mnemonicText');

         if (modal && textDisplay) {
            textDisplay.innerText = result.mnemonic;
            modal.style.display = 'flex';
         } else {
            alert("Account created! Your mnemonic is: " + result.mnemonic);
         }
      } else {
         alert(result.error || "Registration failed. Please try again.");
      }
   } catch (err) {
      console.error("Fetch Error:", err);
      alert("Could not connect to the server. Check your internet or CSP settings.");
   }
}
let activeType = null;

function triggerUpdate(type) {
   activeType = type;
   openModal1('verifyModal');
   document.getElementById('confirmBtn').onclick = processSecurityUpdate;
}

async function processSecurityUpdate() {
   const mnemonic = document.getElementById('verify_key').value;
   let payload = {
      type: activeType,
      mnemonic: mnemonic
   };

   if (activeType === 'password') {
      payload.val = document.getElementById('new_pass').value;
      payload.confirm = document.getElementById('conf_pass').value;
   } else if (activeType === 'email') {
      payload.email = document.getElementById('set_email').value;
      payload.backup = document.getElementById('set_backup').value;
   } else if (activeType === 'qa') {
      payload.question = document.getElementById('set_question').value;
      payload.answer = document.getElementById('set_answer').value;
   }

   const response = await fetch('/settings/update-field', {
      method: 'POST',
      headers: {
         'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload)
   });

   const result = await response.json();
   alert(result.message || result.error);
   if (result.success) window.location.reload();
}

async function hardDelete() {
   const payload = {
      confirm_user: document.getElementById('del_user').value,
      mnemonic: document.getElementById('del_key').value
   };

   const response = await fetch('/settings/delete-account', {
      method: 'POST',
      headers: {
         'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload)
   });

   const result = await response.json();
   if (result.success) window.location.href = '/register';
   else alert(result.error);
}
let currentPosts = [];
let currentIndex = 0;

function cycle(dir) {
   if (posts.length <= 1) return; 

   currentIndex = (currentIndex + dir + posts.length) % posts.length;
   renderCurrentPost();

   const currentPostId = posts[currentIndex].id;
   loadComments(currentPostId);
}

async function handleVote(postId, val) {
   const res = await fetch('/community/vote', {
      method: 'POST',
      headers: {
         'Content-Type': 'application/json'
      },
      body: JSON.stringify({
         post_id: postId,
         vote: val
      })
   });
   const data = await res.json();
   currentPosts[currentIndex].likes = data.likes;
   currentPosts[currentIndex].dislikes = data.dislikes;
   renderCurrentPost();
}

async function postComment(postId) {
   const input = document.getElementById(`comment-input-${postId}`);
   const res = await fetch('/community/comment', {
      method: 'POST',
      headers: {
         'Content-Type': 'application/json'
      },
      body: JSON.stringify({
         post_id: postId,
         text: input.value
      })
   });
   if (res.ok) {
      input.value = '';
   }
}
async function submitPublicPost() {
   const form = document.getElementById('publicUploadForm');
   if (!form) return console.error("Upload form not found!");

   const formData = new FormData(form);

   try {
      const res = await fetch('/community/upload', {
         method: 'POST',
         body: formData
      });

      const result = await res.json();

      if (res.ok && result.success) {
         alert("Catch shared with the community!");
         window.location.reload();
      } else {
         alert("Upload failed: " + (result.error || "Check your image and fields."));
      }
   } catch (err) {
      console.error("Upload Error:", err);
      alert("Server connection failed.");
   }
}


async function handleVote(postId, val) {
   const res = await fetch('/community/vote', {
      method: 'POST',
      headers: {
         'Content-Type': 'application/json'
      },
      body: JSON.stringify({
         post_id: postId,
         vote: val
      })
   });
   const data = await res.json();

   const activePost = posts.find(p => p.id === postId);
   if (activePost) {
      activePost.likes = data.likes;
      activePost.dislikes = data.dislikes;
      renderCurrentPost();
   }
}
async function sendComment(postId, parentId = null) {
   const inputId = parentId ? `input-${parentId}` : `main-comment-input-${postId}`;
   const inputEl = document.getElementById(inputId);

   if (!inputEl) {
      console.error(`Could not find input element: ${inputId}`);
      return;
   }

   const text = inputEl.value.trim();
   if (!text) return;

   const res = await fetch('/community/comment', {
      method: 'POST',
      headers: {
         'Content-Type': 'application/json'
      },
      body: JSON.stringify({
         post_id: postId,
         parent_id: parentId,
         text: text
      })
   });

   if (res.ok) {
      inputEl.value = '';
      loadComments(postId);
   }
}


function showReplyInput(commentId) {
   const box = document.getElementById(`reply-box-${commentId}`);
   box.style.display = box.style.display === 'none' ? 'block' : 'none';
}

async function loadComments(postId) {
   const container = document.getElementById(`comments-container-${postId}`);

   if (!container) return;

   try {
      const res = await fetch(`/community/get-comments/${postId}`);
      const html = await res.text();
      container.innerHTML = html;
   } catch (err) {
      console.error("Failed to load comments:", err);
   }
}

function toggleReply(id) {
   const box = document.getElementById(`reply-to-${id}`);
   box.style.display = box.style.display === 'none' ? 'block' : 'none';
}
// In static/js/main.js
async function sendComment(postId, parentId = null) {
   const inputId = parentId ? `input-${parentId}` : `main-comment-input-${postId}`;
   const inputEl = document.getElementById(inputId);

   if (!inputEl) {
      console.error("Input not found for ID:", inputId);
      return;
   }

   const text = inputEl.value.trim();
   if (!text) return;

   const res = await fetch('/community/comment', {
      method: 'POST',
      headers: {
         'Content-Type': 'application/json'
      },
      body: JSON.stringify({
         post_id: postId,
         parent_id: parentId,
         text: text
      })
   });

   if (res.ok) {
      inputEl.value = '';
      loadComments(postId); 
   }
}

async function loadComments(postId) {
   const id = `comments-container-${postId}`;
   const container = document.getElementById(id);

   if (!container) {
      console.warn(`Target ID not found: ${id}. Retrying...`);
      return;
   }

   try {
      const res = await fetch(`/community/get-comments/${postId}`);
      if (!res.ok) throw new Error("Comments fetch failed");
      const html = await res.text();
      container.innerHTML = html;
   } catch (err) {
      container.innerHTML = '<p style="color:red; font-size:0.8rem;">Could not load comments.</p>';
   }
}

async function addFriend(targetId) {
   const res = await fetch(`/friend/add/${targetId}`, {
      method: 'POST',
      headers: {
         'Content-Type': 'application/json'
      }
   });
   const data = await res.json();
   if (data.success) {
      alert(data.message);
   } else {
      alert(data.error);
   }
}
