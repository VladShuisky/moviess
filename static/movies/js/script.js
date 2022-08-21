console.log('hahahah')
let money_fields = document.querySelectorAll('.m')

function moneyFormat(el) {
    let reverseStacks = el.innerHTML.split('').reverse()
    reverseStacks.splice(3, 0, ' ');
    reverseStacks.splice(7, 0, ' ');
    reverseStacks.splice(11, 0, ' '); 
    el.innerHTML = `${reverseStacks.reverse().join('').trim()}`
    return 0
}

money_fields.forEach(field => moneyFormat(field))