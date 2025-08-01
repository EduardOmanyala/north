
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




function fetchNotifications() {
  fetch(fetchNotificationsUrl)
    .then(response => response.json())
    .then(data => {
      const countSpan = document.getElementById("notification-count"); 

      // UI updates (same as yours)
      if (data.unread_count > 0) {
        countSpan.innerHTML = `<strong>${data.unread_count}</strong>`;
        countSpan.style.background = "red";
    
      } else {
        countSpan.style.display = "none";
      }

      const dropdown = document.getElementById("notify-list");
      let inner = "";

      if (data.notifications.length > 0) {
        data.notifications.forEach(n => {
          if (n.task_id && n.task_slug) {
            inner += `<a href="${taskBaseUrl}/${n.task_id}/${n.task_slug}/" class="notify-item">
            <div class="notify-thumb"><img src="${n.task_img}" style="width: 2.4rem; height: 2.4rem; border-radius: 50%; object-fit: cover;" alt="Cinque Terre"></div>
            <div class="notify-text">
            <p>${n.message}</p>
            <p>${n.title.split(" ").slice(0, 6).join(" ")}</p>
            <span>${timeAgo(n.created_at)}</span>
            </div>
            </a>`;
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




function fetchMessageNotifications() {
  fetch(fetchMessagesUrl)
    .then(response => response.json())
    .then(data => {
      const countSpan = document.getElementById("notification-count2"); 

      // UI updates (same as yours)
      if (data.unread_count > 0) {
        countSpan.innerHTML = `<strong>${data.unread_count}</strong>`;
        countSpan.style.background = "red";
    
      } else {
        countSpan.style.display = "none";
      }

      const dropdown = document.getElementById("notify-list2");
      let inner = "";

      if (data.notifications.length > 0) {
        data.notifications.forEach(n => {
          if (n.user) {
            inner += `<a href="${messagesBaseUrl}/${n.user}/" class="notify-item">
            <div class="notify-thumb"><img src="${imgMsg}" style="width: 2.4rem; height: 2.4rem; border-radius: 50%; object-fit: cover;" alt="Cinque Terre"></div>
            <div class="notify-text">
            <p>${n.message}</p>
            <span>${timeAgo(n.created_at)}</span>
            </div>
            </a>`;
          } else {
            inner += `
              <div>
                <a href="#">
                  ${n.message}<br>
                  <small style="color: gray;">No Messages Yet</small>
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




document.addEventListener('DOMContentLoaded', function () {
  const bellIcon = document.getElementById('notification-bell');

  if (bellIcon) {
    bellIcon.addEventListener('click', function () {
      console.log('Bell icon clicked. Showing dropdown...');

      // Send POST request to mark notifications as read
      fetch(markNotificationsUrl, {
        method: 'POST',
        headers: {
          'X-CSRFToken': csrfToken,
        },
      })
      .then(res => res.json())
      .then(() => {
        console.log('Notifications marked as read.');
        fetchNotifications(); // Refresh the list
      });
    });
  } else {
    console.warn('Bell icon not found in DOM.');
  }
});




document.addEventListener('DOMContentLoaded', function () {
  const envIcon = document.getElementById('notification-envelope');

  if (envIcon) {
    envIcon.addEventListener('click', function () {
      console.log('Bell icon clicked. Showing dropdown...');

      // Send POST request to mark notifications as read
      fetch(markMessagesUrl, {
        method: 'POST',
        headers: {
          'X-CSRFToken': csrfToken,
        },
      })
      .then(res => res.json())
      .then(() => {
        console.log('Messages marked as read.');
        fetchNotifications(); // Refresh the list
      });
    });
  } else {
    console.warn('Bell icon not found in DOM.');
  }
});














window.onload = function () {
    fetchNotifications();
    fetchMessageNotifications();
  };
  
  setInterval(fetchNotifications, 20000);
  setInterval(fetchMessageNotifications, 20000);
