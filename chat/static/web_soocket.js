
    (function () {

        const senderId = window.SENDER_ID;
        const receiverId = window.RECEIVER_ID;

      const sortedIds = [senderId, receiverId].sort();
      const roomName = `chat_${sortedIds[0]}_${sortedIds[1]}`;
      const protocol = window.location.protocol === "https:" ? "wss" : "ws";

      // Create new WebSocket instance
      const socket = new WebSocket(
        `${protocol}://${window.location.host}/ws/${roomName}/`
      );

      window.chatSocket = socket;

      document.currentScript.parentElement.socket = socket;


      const messageInput = document.getElementById("message-input");
      const sendButton = document.getElementById("send-button");
      const messagesContainer = document.getElementById("messages-container");

      function updateSendButtonState() {
        const messageInput = document.getElementById("message-input");
        const messageText = messageInput.value.trim();
        const filePreviewElement = document.getElementById("file-preview");
        const hasFile = filePreviewElement.innerHTML.trim() !== "";

        // Enable button if either text or file is present
        document.getElementById("send-button").disabled = !messageText && !hasFile;
      }

      const fileObserver = new MutationObserver(updateSendButtonState);
  fileObserver.observe(document.getElementById("file-preview"), { childList: true, subtree: true });


  document.getElementById("message-input").addEventListener("input", updateSendButtonState);

//   messageInput.addEventListener("input", updateSendButtonState); 

      // WebSocket event handlers
      socket.onmessage = function (e) {
        const data = JSON.parse(e.data);
        console.log("Message received:", data);

        htmx.ajax("GET", window.RECENT_CHATS_URL, "#left-nav");

        // Create message container
        const messageContainer = document.createElement("div");
        messageContainer.classList.add("flex", "mb-4");
        if (data.sender_id == senderId) {
          messageContainer.classList.add("justify-end");
        }

        // Create message content
        const messageContent = document.createElement("div");
        messageContent.classList.add(
          data.sender_id == senderId ? "bg-whatsapp-light" : "bg-white",
          "rounded-lg",
          "p-3",
          "max-w-xs"
        );
        console.log(data.file_name);
        if (data.file_url) {
          let fileElement;
        
          // Check the file type based on the file URL extension
          if (data.file_url.toLowerCase().endsWith('.pdf')) {
            // Create a link for PDF files
            fileElement = document.createElement('a');
            fileElement.href = data.file_url;
            fileElement.textContent = 'Download PDF';
            fileElement.target = '_blank';  // Open in a new tab
          } else if (data.file_url.toLowerCase().endsWith('.doc') || data.file_url.toLowerCase().endsWith('.docx')) {
            // Create a link for Word documents
            fileElement = document.createElement('a');
            fileElement.href = data.file_url;
            fileElement.textContent = 'Download Word Document';
            fileElement.target = '_blank';  // Open in a new tab
          } else if (data.file_url.toLowerCase().endsWith('.png') || data.file_url.toLowerCase().endsWith('.jpg') || data.file_url.toLowerCase().endsWith('.jpeg') || data.file_url.toLowerCase().endsWith('.gif')) {
            // Create an image element for image files
            fileElement = document.createElement('img');
            fileElement.src = data.file_url;
            fileElement.alt = 'Uploaded Image';
            fileElement.style.maxWidth = '100%';
          } else {
            // Default behavior for other file types
            fileElement = document.createElement('a');
            fileElement.href = data.file_url;
            fileElement.textContent = 'Download File';
            fileElement.target = '_blank';  // Open in a new tab
          }
        
          // Append the file element to the message content
          messageContent.appendChild(fileElement);
        }
        // Also add any text message content
        if (data.message) {
          const messageText = document.createElement("p");
          messageText.classList.add("text-sm");
          messageText.innerText = data.message;
          messageContent.appendChild(messageText);
        }

        // Add timestamp
        const timestamp = document.createElement("span");
        timestamp.classList.add("text-xs", "text-gray-500", "mt-1", "block");
        timestamp.innerText = data.timestamp;

        // Append elements
        messageContent.appendChild(timestamp);
        messageContainer.appendChild(messageContent);

        // Add the message to the messages container
        messagesContainer.appendChild(messageContainer);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;


      };

      socket.onclose = function () {
        console.log("WebSocket connection closed");
      };

      document.body.addEventListener('htmx:afterSwap', function(event) {
        if (event.detail.target.id === 'file-preview') {
          // Enable the send button after a successful file upload
          updateSendButtonState();
        }
      });
      // Form submission handler
       // Chat form submission: include both text and the file reference from the preview.
      document.getElementById("chat-form").addEventListener("submit", function (e) {
    e.preventDefault();

    const messageInput = document.getElementById("message-input");
    const messageText = messageInput.value.trim();
    const fileInput = document.getElementById("file-input");

    const filePreviewElement = document.getElementById("file-preview");
    const fileUrlInput = filePreviewElement.querySelector("input[name='file_url']");
    const file_url = fileUrlInput ? fileUrlInput.value : "";

    if (messageText === "" && !file_url) {
      console.log("Message must contain either text or a file.");
      return;
    }

    window.chatSocket.send(JSON.stringify({
      message: messageText,
      sender_id: "{{ request.user.id }}",
      receiver_id: "{{ chat_user.id }}",
      file_url: file_url
    }));

    console.log("Sending message with file_url:", file_url);
    // Clear input fields after sending
    messageInput.value = "";
    filePreviewElement.innerHTML = "";
    fileInput.value = "";
    updateSendButtonState();
  });

  htmx.ajax("GET", window.RECENT_CHATS_URL, "#left-nav");


      // Initial scroll to bottom (if needed)
      if (messagesContainer) {
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
      }

      // Global error handler
      socket.onerror = function (error) {
        console.error("WebSocket Error:", error);
      };
    })();
