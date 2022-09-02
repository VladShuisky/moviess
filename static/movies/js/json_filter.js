

// функция принимает url и params из формы, затем делает фетч запрос по url, вторым аргументом словарик с методом и headers
function ajaxSend(url, params) {
    fetch(`${url}?${params}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
    })
    .then(response => response.json())   //ожидаем ответ от сервера и обрабатываем его в json
    .then(json => render(json))          // функция берет json и вставляет в шаблон с помощью render
    .catch(error => console.error(error))  // если ответ не придет вылезет ошибка
}




// Выделение формы и добавление на нее события 'отправить ajax запрос' с параметрами из формы
const form = document.querySelector('form[name=filter]');   
form.addEventListener('submit', (event)=> {
    event.preventDefault();
    let url = form.action
    let params = new URLSearchParams(new FormData(form)).toString();
    ajaxSend(url, params)
})


function render(data) {
    let template = Hogan.compile(html) // хоган берет html тот что ниже и компилит в перемменную template
    let output = template.render(data) // data в которой json, вставляется в template встроенным методом render из библиотеки hogan
    const div = document.querySelector('.left-ads-display>.row')  // выбирается нужный кусок html
    div.innerHTML = output // innerHTml заменяется хогановским шаблоном
}







let html = '\
{{#movies}}\
        <div class="col-md-4 product-men">\
            <div class="product-shoe-info editContent text-center mt-lg-4" >\
                <div class="men-thumb-item">\
                    <img src="media/{{ poster }}" class="img-fluid" alt="" > \
                </div>\
                <div class="item-info-product">\
                    <h4 class="">\
                        <a href="{{ url }}" class="editContent" >{{title}}</a>\
                    </h4>\
                    <div class="product_price">\
                        <div class="grid-price">\
                            <span class="money editContent" >{{tagline}}\
                            </span>\
                        </div>\
                    </div>\
                </div>\
            </div>\
        </div>\
{{/movies}}'