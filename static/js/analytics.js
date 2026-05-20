(function () {
   function loadWorkspaceRecommendations() {
      try {
         if (window.sessionStorage && sessionStorage.getItem("hideRecommendationsSpace") === "true") {
            console.log("Widget blocked via active session dismiss token.");
            return;
         }

         fetch("/api/recommendations")
            .then(response => {
               if (!response.ok) throw new Error("Backend connection offline.");
               return response.json();
            })
            .then(data => {
               const space = document.getElementById("recommendation-space");
               const container = document.getElementById("recommendation-space-links");
               const dismissBtn = document.getElementById("dismiss-rec-space");
               const statusOutput = document.getElementById("output");

               if (!space || !container) return;

               if (!data || data.length === 0) {
                  data = [{
                        "title": "Trending Support Portal",
                        "url": "/tickets",
                        "reason": "Manage active operational support streams."
                     },
                     {
                        "title": "Private Map Log",
                        "url": "/map-log",
                        "reason": "Log fishing spots to your personal database."
                     },
                     {
                        "title": "Community Map Log",
                        "url": "/community-map",
                        "reason": "Map fishing spots and engage with the community."
                     },
                     {
                        "title": "Hydrology Calculators",
                        "url": "/hydrology-calcs",
                        "reason": "Utilize the platform to it's fullest advantage and employ our hydrology calculators."
                     },
                     {
                        "title": "Personal Image Gallery",
                        "url": "/personal-gallery",
                        "reason": "Upload images of catches into your private image gallery."
                     },
                     {
                        "title": "Community Image Gallery",
                        "url": "/community-gallery",
                        "reason": "Upload images to the community image gallery and engage with others' catches."
                     },
                     {
                        "title": "Trending Support Portal",
                        "url": "/weather",
                        "reason": "Weather watch before you go fishing? Look at the current weather."
                     },
                     {
                        "title": "Historical Weather",
                        "url": "/historical-weather",
                        "reason": "Interested what weather was like in the past? Look at our historical weather page."
                     },
                     {
                        "title": "Weather Predictions",
                        "url": "/weather-predictions",
                        "reason": "Interested if your weather conditions are favorable? Find out here."
                     },
                     {
                        "title": "Messages",
                        "url": "/messages",
                        "reason": "Want to get in direct contact with a user? Do that here."
                     },
                     {
                        "title": "Main Platform Dashboard",
                        "url": "/",
                        "reason": "Return back to your primary workstation room."
                     }
                  ];
               }

               container.innerHTML = "";
               data.forEach(item => {
                  const card = document.createElement("a");
                  card.href = item.url;
                  card.style.cssText = "flex: 1; min-width: 220px; background: rgba(255, 255, 255, 0.04); padding: 12px; border-radius: 6px; text-decoration: none; color: white; border-left: 3px solid #ff7495; border-top: 1px solid rgba(255,255,255,0.01); transition: all 0.2s; box-sizing: border-box;";

                  card.innerHTML = `
                                    <strong style="display:block; font-size: 12px; color: #64b5f6; margin-bottom: 3px;">${item.title}</strong>
                                    <small style="display:block; font-size: 11px; color: #ccc; line-height: 1.3;">${item.reason}</small>
                                `;

                  card.addEventListener("mouseenter", () => {
                     card.style.background = "rgba(255, 255, 255, 0.08)";
                     card.style.transform = "translateY(-2px)";
                  });
                  card.style.addEventListener ? card.addEventListener("mouseleave", () => {
                     card.style.background = "rgba(255, 255, 255, 0.04)";
                     card.style.transform = "translateY(0px)";
                  }) : null;

                  container.appendChild(card);
               });

               space.style.setProperty("display", "block", "important");

               if (statusOutput) {
                  statusOutput.style.color = "#2ecc71";
                  statusOutput.style.fontWeight = "bold";
                  statusOutput.innerText = "● Active - Secure Session Established";
               }

               if (dismissBtn) {
                  dismissBtn.onclick = function () {
                     space.style.setProperty("display", "none", "important");
                     sessionStorage.setItem("hideRecommendationsSpace", "true");
                  };
               }
            })
            .catch(err => {
               console.log("Telemetry running inside backup local storage states: ", err);
            });
      } catch (e) {
         console.error("Critical tracking block isolation bypass active.", e);
      }
   }

   if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", loadWorkspaceRecommendations);
   } else {
      loadWorkspaceRecommendations();
   }
})();
