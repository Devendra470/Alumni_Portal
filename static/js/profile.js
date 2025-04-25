document.addEventListener('DOMContentLoaded', function () {
  const profilePic = document.querySelector('.profile-pic');
  const profilePlaceholder = document.querySelector('.profile-placeholder');
  const dropdownMenu = document.querySelector('.dropdown-menu');

  function toggleDropdown(event) {
      event.stopPropagation(); 
      dropdownMenu.classList.toggle('show');
  }

  if (profilePic) profilePic.addEventListener('click', toggleDropdown);
  if (profilePlaceholder) profilePlaceholder.addEventListener('click', toggleDropdown);

  document.addEventListener('click', function (event) {
      if (
          !profilePic?.contains(event.target) &&
          !profilePlaceholder?.contains(event.target) &&
          !dropdownMenu?.contains(event.target)
      ) {
          dropdownMenu?.classList.remove('show');
      }
  });
// File Upload Preview Logic
  const fileInput = document.getElementById('file-input');
  const imgTag = document.getElementById('profile-img');
  const placeholder = document.getElementById('profile-placeholder');

  if (fileInput && imgTag) {
      fileInput.addEventListener('change', function (event) {
          const file = event.target.files[0];
          if (file) {
              const reader = new FileReader();
              reader.onload = function (e) {
                  imgTag.src = e.target.result;
                  imgTag.style.display = 'block';
                  if (placeholder) placeholder.style.display = 'none';
              };
              reader.readAsDataURL(file);
          }
      });
  }
});

// Trigger the hidden file input when the custom button is clicked
document.getElementById('custom-button').addEventListener('click', function() {
    document.getElementById('file-input').click();  
  });  
