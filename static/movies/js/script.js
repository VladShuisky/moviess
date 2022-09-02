document.addEventListener('DOMContentLoaded', ()=>{
    let coma = document.querySelector('.del_comma');
    if(coma) {coma.lastChild.remove()} ;
})

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


const rating = document.querySelector('form[name=rating]')
console.log(rating)
rating.addEventListener('change', function(event) {
    let data = new FormData(this) //берет номер звезды высланный из формы
    console.log(event.target)
    let url = `${this.action}`    // url из action формы
    fetch(url, {method: 'POST', body: data})   // отправляет звезду по url на сервер
    .then(response => alert('Рейтинг установлен'))   // ждет ответ      
    .catch(error => alert('Ошибка'))
})

