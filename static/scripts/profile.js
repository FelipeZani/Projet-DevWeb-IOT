function displayForm(button, index) {
    if (index < 0 || index > 1) {
        alert('Error: index out of range');
        return;
    }

    let formList = document.getElementsByClassName('change-info-form');
    let displayChanges = document.getElementsByClassName('display-changes');
    let formArray = Array.from(formList);

    if (!button || !displayChanges[index]) {
        console.error('Invalid button or display-changes element');
        return;
    }

    console.log(formList);

    button.classList.add('hide');
    displayChanges[index].classList.remove('hide');


    if (index === 1) {
        formArray.forEach(element => {
            element.classList.remove('hide-form')
        });
    } else {
        formArray.forEach(element =>{ 
            element.classList.add('hide-form')
            element.reset()
        });
    }
}
