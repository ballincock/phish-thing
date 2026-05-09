function openModal(id) {
   const modal = document.getElementById(id);
   if (modal) modal.style.display = 'flex';
}

function closeModal(id) {
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

      openModal('detailsModal');
   } catch (err) {
      console.error("Fetch Detail Error:", err);
      alert("Could not load catch details.");
   }
}
