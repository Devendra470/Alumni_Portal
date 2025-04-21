
document.addEventListener('DOMContentLoaded', function () {
    const profilePic = document.querySelector('.profile-pic')
    const dropdownMenu = document.querySelector('.dropdown-menu')

    // Toggle dropdown visibility on profile pic click
    profilePic.addEventListener('click', function (event) {
        event.stopPropagation() // Prevent the event from propagating to the document
        dropdownMenu.classList.toggle('show') // Toggle visibility
    })

    // Close dropdown if clicked outside the profile picture or dropdown menu
    document.addEventListener('click', function (event) {
        if (!profilePic.contains(event.target) && !dropdownMenu.contains(event.target)) {
            dropdownMenu.classList.remove('show')
        }
    })
})