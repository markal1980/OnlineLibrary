var updateBtns = document.getElementsByClassName('update-cart')

for (var i=0; i < updateBtns.length; i++ ){
    updateBtns[i].addEventListener('click', function (){
        var book_id = this.dataset.product
        var action = this.dataset.action
        // var user1 = this.dataset.user
        console.log('BookId:', book_id, 'Action: ', action)

        // console.log('User:', user)
        if(user === 'AnonymousUser'){
            console.log('User is not logged in')
        }else{
            updateUserOrder(book_id, action)
        }
    })
}


function updateUserOrder(book_id, action){
    console.log('Sending data...')

    var url = '/update_item/'

    fetch(url, {
        method: 'POST',
        headers:{
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body:JSON.stringify({'book_id': book_id, 'action': action})
    })
        .then((response) =>{
            return response.json()
        })
        .then((data) =>{
            console.log('data: ', data)
            location.reload()
        })
}