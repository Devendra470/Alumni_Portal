document.addEventListener('DOMContentLoaded', function () {
    const profilePic = document.querySelector('.profile-pic');
    const profilePlaceholder = document.querySelector('.profile-placeholder');
    const dropdownMenu = document.querySelector('.dropdown-menu');

    function toggleDropdown(event) {
        event.stopPropagation(); // Prevent the click from reaching the document
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
});
