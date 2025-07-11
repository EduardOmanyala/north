let lastUnreadCount = 0;
let lastUnreadCount2 = 0;
let lastSeenNotificationId = null;


function timeAgo(datetimeStr) {
  const now = new Date();
  const then = new Date(datetimeStr);
  const seconds = Math.floor((now - then) / 1000);

  const intervals = [
    { label: 'year', seconds: 31536000 },
    { label: 'month', seconds: 2592000 },
    { label: 'week', seconds: 604800 },
    { label: 'day', seconds: 86400 },
    { label: 'hour', seconds: 3600 },
    { label: 'minute', seconds: 60 },
    { label: 'second', seconds: 1 }
  ];

  for (const interval of intervals) {
    const count = Math.floor(seconds / interval.seconds);
    if (count >= 1) {
      return `${count} ${interval.label}${count !== 1 ? 's' : ''} ago`;
    }
  }
  return 'Just now';
}

// function fetchNotifications() {
//   fetch(fetchNotificationsUrl)
//     .then(response => response.json())
//     .then(data => {
//       const countSpan = document.getElementById("notification-count");

//       // 🔔 Play sound if new notifications arrived
//       if (data.unread_count > lastUnreadCount) {
//         const audio = document.getElementById("notification-sound");
//         if (audio) {
//           audio.volume = 0.9;
//           audio.play().catch(e => console.log("Autoplay blocked or failed:", e));
//         }
//       }

//       lastUnreadCount = data.unread_count;

//       if (data.unread_count > 0) {
//         countSpan.innerHTML = `<strong>${data.unread_count}</strong>`;
//         countSpan.style.display = "flex";
//       } else {
//         countSpan.style.display = "none";
//       }

//       const dropdown = document.getElementById("dropdownMenu");
//       let inner = "";

//       if (data.notifications.length > 0) {
//         data.notifications.forEach(n => {
//           if (n.task_id && n.task_slug) {
//             //const randomIndex = Math.floor(Math.random() * imgSrcs.length);
//             //const selectedImg = imgSrcs[randomIndex];
//             inner += `
//               <div>
//                 <a href="${taskBaseUrl}/${n.task_id}/${n.task_slug}/" style="display: flex; align-items: center; text-decoration: none;">
//                 <div style="flex: 0 0 20%; display: flex; justify-content: center;">
//                   <img src="${n.task_img}" style="width: 2.4rem; height: 2.4rem; border-radius: 50%; object-fit: cover;" alt="Cinque Terre">
//                 </div>
//                 <div style="flex: 1; padding-left: 0.5rem;">
//                   <p class="small">${n.message}</p>
//                   <small class="tasknot-title"><strong>${n.title.split(" ").slice(0, 6).join(" ")}</strong></small>
//                 </div>
//                 </a>
              
//               </div>`;
//           } else {
//             inner += `
//               <div>
//                 <a href="#">
//                   ${n.message}<br>
//                   <small style="color: gray;">No Task Linked</small>
//                 </a>
//               </div>`;
//           }
//         });
//       } else {
//         inner = `<div><a href="#">No new notifications</a></div>`;
//       }

//       inner += `<hr><div><a href="#">View All</a></div>`;
//       dropdown.innerHTML = inner;
//     });
// }

function fetchNotifications() {
  fetch(fetchNotificationsUrl)
    .then(response => response.json())
    .then(data => {
      const countSpan = document.getElementById("notification-count");

      // Find latest notification ID from the response
      const latestNotification = data.notifications[0];
      const latestNotificationId = latestNotification ? latestNotification.id : null;

      // 🔔 Play sound only if there's a new notification we haven't seen
      if (
        data.unread_count > 0 &&
        latestNotificationId &&
        latestNotificationId !== lastSeenNotificationId
      ) {
        const audio = document.getElementById("notification-sound");
        if (audio) {
          audio.volume = 0.9;
          audio.play().catch(e => console.log("Autoplay blocked or failed:", e));
        }
      }

      // Update the last seen ID and unread count
      lastSeenNotificationId = latestNotificationId;
      lastUnreadCount = data.unread_count;

      // UI updates (same as yours)
      if (data.unread_count > 0) {
        countSpan.innerHTML = `<strong>${data.unread_count}</strong>`;
        countSpan.style.display = "flex";
      } else {
        countSpan.style.display = "none";
      }

      const dropdown = document.getElementById("dropdownMenu");
      let inner = "";

      if (data.notifications.length > 0) {
        data.notifications.forEach(n => {
          if (n.task_id && n.task_slug) {
            inner += `
              <div>
                <a href="${taskBaseUrl}/${n.task_id}/${n.task_slug}/" style="display: flex; align-items: center; text-decoration: none;">
                <div style="flex: 0 0 20%; display: flex; justify-content: center;">
                  <img src="${n.task_img}" style="width: 2.4rem; height: 2.4rem; border-radius: 50%; object-fit: cover;" alt="Cinque Terre">
                </div>
                <div style="flex: 1; padding-left: 0.5rem;">
                  <p class="small">${n.message}</p>
                  <small class="tasknot-title"><strong>${n.title.split(" ").slice(0, 6).join(" ")}</strong></small>
                  <p class="small" style="color: gray;margin-top: 0.2rem; margin-bottom: 0;"">${timeAgo(n.created_at)}</p>
                </div>
                </a>
              </div>`;
          } else {
            inner += `
              <div>
                <a href="#">
                  ${n.message}<br>
                  <small style="color: gray;">No Task Linked</small>
                </a>
              </div>`;
          }
        });
      } else {
        inner = `<div><a href="#">No new notifications</a></div>`;
      }

      inner += `<hr><div><a href="#">View All</a></div>`;
      dropdown.innerHTML = inner;
    });
}


// function fetchMessageNotifications() {
//   fetch(fetchMessagesUrl)
//     .then(response => response.json())
//     .then(data => {
//       const countSpan = document.getElementById("message-count");

//       // Find latest notification ID from the response
//       const latestNotification = data.notifications[0];
//       const latestNotificationId = latestNotification ? latestNotification.id : null;

//       // 🔔 Play sound only if there's a new notification we haven't seen
//       if (
//         data.unread_count > 0 &&
//         latestNotificationId &&
//         latestNotificationId !== lastSeenNotificationId
//       ) {
//         const audio = document.getElementById("notification-sound");
//         if (audio) {
//           audio.volume = 0.9;
//           audio.play().catch(e => console.log("Autoplay blocked or failed:", e));
//         }
//       }

//       // Update the last seen ID and unread count
//       lastSeenNotificationId = latestNotificationId;
//       lastUnreadCount = data.unread_count;

//       // UI updates (same as yours)
//       if (data.unread_count > 0) {
//         countSpan.innerHTML = `<strong>${data.unread_count}</strong>`;
//         countSpan.style.display = "flex";
//       } else {
//         countSpan.style.display = "none";
//       }

//       const dropdown = document.getElementById("dropdownMenu");
//       let inner = "";

//       if (data.notifications.length > 0) {
//           data.notifications.forEach(n => {
//             if (n.user) {
//               inner += `
//                 <div>
//                   <a href="${messagesBaseUrl}/${n.user}/">
//                     <small class="tasknot-title"><strong>${n.message}</strong></small>
//                   </a>
//                 </div>`;
//             } else {
//               inner += `
//                 <div>
//                   <a href="#">
//                     ${n.message}<br>
//                     <small style="color: gray;">No Task Linked</small>
//                   </a>
//                 </div>`;
//             }
//           });
//         } else {
//           inner = `<div><a href="#">No new messages</a></div>`;
//         }
  
//         inner += `<hr><div><a href="#">View All</a></div>`;
//         dropdown.innerHTML = inner;
//     });
// }







// //get message notifications
function fetchMessageNotifications() {
    fetch(fetchMessagesUrl)
      .then(response => response.json())
      .then(data => {
        const countSpan = document.getElementById("message-count");
           //Find latest notification ID from the response
          const latestNotification = data.notifications[0];
           const latestNotificationId = latestNotification ? latestNotification.id : null;

           if (
        data.unread_count > 0 &&
        latestNotificationId &&
        latestNotificationId !== lastSeenNotificationId
      ) {
        const audio = document.getElementById("notification-sound");
        if (audio) {
          audio.volume = 0.9;
          audio.play().catch(e => console.log("Autoplay blocked or failed:", e));
        }
      }

      // Update the last seen ID and unread count
      lastSeenNotificationId = latestNotificationId;
      lastUnreadCount = data.unread_count;
  
//         // 🔔 Play sound if new notifications arrived
//         if (data.unread_count > lastUnreadCount) {
//           const audio = document.getElementById("notification-sound");
//           if (audio) {
//             audio.volume = 0.9;
//             audio.play().catch(e => console.log("Autoplay blocked or failed:", e));
//           }
//         }
  
//         lastUnreadCount = data.unread_count;
  
        if (data.unread_count > 0) {
          countSpan.innerHTML = `<strong>${data.unread_count}</strong>`;
          countSpan.style.display = "flex";
        } else {
          countSpan.style.display = "none";
        }
  
        const dropdown = document.getElementById("dropdownMenu3");
        let inner = "";
  
        if (data.notifications.length > 0) {
          data.notifications.forEach(n => {
            if (n.user) {
              inner += `<div>
                <a href="${messagesBaseUrl}/${n.user}/" style="display: flex; align-items: center; text-decoration: none;">
                <div style="flex: 0 0 20%; display: flex; justify-content: center;">
                  <img src="${imgMsg}" style="width: 2.4rem; height: 2.4rem; border-radius: 50%; object-fit: cover;" alt="Cinque Terre">
                </div>
                <div style="flex: 1; padding-left: 0.5rem;">
                  <p class="small">${n.message}</p>
                  <small class="tasknot-title"><strong>Please check and respond where necessary.</strong></small>
                  <p class="small" style="color: gray;margin-top: 0.2rem; margin-bottom: 0;"">${timeAgo(n.created_at)}</p>
                </div>
                </a>
              </div>`;
            } else {
              inner += `
                <div>
                  <a href="#">
                    ${n.message}<br>
                    <small style="color: gray;">No messages to show</small>
                  </a>
                </div>`;
            }
          });
        } else {
          inner = `<div><a href="#">No new messages</a></div>`;
        }
  
        inner += `<hr><div><a href="#">View All</a></div>`;
        dropdown.innerHTML = inner;
      });
  }

  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  const csrfToken = getCookie("csrftoken");



function toggleDropdown(id) {
  const allDropdowns = document.getElementsByClassName("dropdown-content");
  for (let i = 0; i < allDropdowns.length; i++) {
    if (allDropdowns[i].id !== id) {
      allDropdowns[i].classList.remove("show");
    }
  }

  const currentDropdown = document.getElementById(id);
  const willShow = !currentDropdown.classList.contains("show");
  currentDropdown.classList.toggle("show");

  if (id === "dropdownMenu" && willShow) {
    fetch(markNotificationsUrl, {
      method: "POST",
      headers: {
        "X-CSRFToken": csrfToken,
      },
    })
    .then(res => res.json())
    .then(() => {
      console.log("Notifications marked as read.");
      fetchNotifications();
    });
  }

    if (id === "dropdownMenu3" && willShow) {
    fetch(markMessagesUrl, {
      method: "POST",
      headers: {
        "X-CSRFToken": csrfToken,
      },
    })
    .then(res => res.json())
    .then(() => {
      console.log("Notifications marked as read.");
      fetchMessageNotifications();
    });
  }

}



window.onclick = function (event) {
  if (!event.target.closest('.dropbtn')) {
    const dropdowns = document.getElementsByClassName("dropdown-content");
    for (let i = 0; i < dropdowns.length; i++) {
      dropdowns[i].classList.remove("show");
    }
  }
};

window.onload = function () {
    fetchNotifications();
    fetchMessageNotifications();
  };
  
  setInterval(fetchNotifications, 20000);
  setInterval(fetchMessageNotifications, 20000);