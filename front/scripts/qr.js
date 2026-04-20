function createQrScaner(){
    const html5QrCode = new Html5Qrcode("reader");

    const qrCodeSuccessCallback = (decodedText, decodedResult) => {
        console.log(`Zeskanowano: ${decodedText}`);
        document.getElementById('result-info').innerText = "Przetwarzanie...";

        const userToken = localStorage.getItem('userToken');

        fetch(`/qr-scan/${decodedText}`,{
            method: 'GET',
            headers: { 
				'Content-Type': 'application/json',
				'Authorization': userToken
			}
        })
        .then(response => {
			if(response.ok){
                document.getElementById('result-info').innerText = "Pomyślnie zeskanowano kod qr!";
				return response.json().then(data => {
                    document.getElementById('result-info').innerText = data.message;
                    if(data.questions){
                        document.querySelector('#quiz_button').style = 'display: block;';
                        document.querySelector('#quiz_button').onclick = ()=>{
                            
                        }
                    }
				})
			}
            else{

            }
		})
    }

    const config = { fps: 10, qrbox: { width: 550, height: 550 } };

    html5QrCode.start(
        { facingMode: "environment" },
        config, 
        qrCodeSuccessCallback
    ).catch((err) => {
        console.error("Nie udało się odpalić kamery, próbuję trybu domyślnego...");
        html5QrCode.start({ facingMode: "user" }, config, qrCodeSuccessCallback);
    });
}
