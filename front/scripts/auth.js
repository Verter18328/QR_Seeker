function logIn() {
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
    .then(response => {
        console.log(response.status)
        if (response.ok) {
            return response.json().then(data => {
                console.log('Zalogowano');
                userToken = data.token;
                localStorage.setItem('userToken', userToken);
            });
        } 
        else if (response.status == 430) {
            console.log('Proba rejestracji');
            return fetch('/register', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    nickname: login,
                    password: password
                })
            })
            .then(regResponse => {
                if (regResponse.ok) {
                    return regResponse.json().then(data => {
                        console.log('Zarejestrowano');
                        userToken = data.token;
                        localStorage.setItem('userToken', userToken);
                    });
                } else {
                    console.log('Wystąpił błąd przy logowaniu!');
                }
            });
        }
    })
    .catch(err => console.error("Błąd sieci:", err));
}