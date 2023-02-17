let state = false;

function toggle(event) {
    let button = document.querySelector('#selectButton');
    let checkboxes = document.querySelectorAll('.checkbox');
    state = !state;
    button.innerText = state ? 'Unselect all' : 'Select all';
    for (let checkbox of checkboxes) {
        checkbox.checked = state;
    }
}
