function generateQuiz(questions){
    otworzQuizModal()

    let form = document.createElement('form')

    for(let question in questions){
        switch(question.type){
            case 'single': 
                form.innerHTML+=`
                <section>
                    <span>${question.question}</span>`

                for(answer in question.answers){
                    form.innerHTML+=`
                        <input type="radio" name="${question.question_id}" id="${question.question_id+answer[1]}">
                        <label for="${question.question_id+answer[1]}">${question.answers.keys[answer]}</label>
                    `
                }
                break;
            case 'multi':
                form.innerHTML+=
                break;
            case 'text':
                form.innerHTML+=
                break;
        }
    }

    
}