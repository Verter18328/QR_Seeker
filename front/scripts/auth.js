function logIn(){
    const login = document.querySelector('#login').value;
    const password = document.querySelector('#haslo').value;

    console.log(login, password);

    fetch('/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            nickname: login,
            password: password
        })
    })
    .then(response => response.json())
    .then(data =>{
        if(data.status!=400){
            console.log('Zalogowano');
            userToken = data.token;
            localStorage.setItem('userToken', userToken);
        }
        else{
            console.log('Proba rejestracji');
            fetch('/register', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    nickname: login,
                    password: password
                })
            })
            .then(response => response.json())
            .then(data =>{
                if(data.status!=400){
                    console.log('Zarejestrowano');
                    userToken = data.token;
                    localStorage.setItem('userToken', userToken);
                }
                else{
                    console.log('Wystąpił błąd przy logowaniu!');
                }
        });
    }});
}