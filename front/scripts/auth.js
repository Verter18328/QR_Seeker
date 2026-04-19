document.querySelector('#formularzLogowania').onsubmit = ()=>{
    const login = document.querySelector('#login').value;
    const password = document.querySelector('#haslo').value;

    fetch('https://qr-seeker.onrender.com/login', {
        method: 'POST',
        body: {
            "nickname": login,
            "password": password
        }
    })
    .then(response => response.json())
    .then(data =>{
        if(data.status!=400){
            userToken = data.token;
            localStorage.setItem('userToken', userToken);
        }
        else{
            fetch('https://qr-seeker.onrender.com/register', {
                method: 'POST',
                body: {
                    "nickname": login,
                    "password": password
                }
            })
            .then(response => response.json())
            .then(data =>{
                if(data.status!=400){
                    userToken = data.token;
                    localStorage.setItem('userToken', userToken);
                }
                else{
                    console.log('Wystąpił błąd przy logowaniu!');
                }
        });
    }});
}