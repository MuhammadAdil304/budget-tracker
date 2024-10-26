document.addEventListener('DOMContentLoaded', () => {
    const profileImg = document.querySelector('.profile-img');
    const dropdown = document.querySelector('.profile-dropdown');

    profileImg.addEventListener('mouseover', () => {
        dropdown.classList.add('show-dropdown');
    });

    profileImg.addEventListener('mouseleave', () => {
        setTimeout(() => { dropdown.classList.remove('show-dropdown'); }, 1500);
    });
});