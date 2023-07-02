document.addEventListener('DOMContentLoaded', () => {
    
    // ----------------------------------------------- DOM
    const bgEl = document.querySelector('#bgEl')
    const frontEl = document.querySelector('#frontEl')
    const bgPreview = document.querySelector('#bgPreview')
    const frontPreview = document.querySelector('#frontPreview')
    
    const nopeBtn = document.querySelector('#nopeBtn')
    const yepBtn = document.querySelector('#yepBtn')

    const choosenColor = document.querySelector('input#choosenColor')
    const predictBtn = document.querySelector('button#predictSingle')
    
    // ----------------------------------------------- Functions
    const changeColors = (bg = null, front =null) => {
        let randomColorBg = ''
        let randomColorFront = ''
        if (!bg & !front) {
            randomColorBg = '#' + Math.floor(Math.random()*16777215).toString(16);
            randomColorFront = '#' + Math.floor(Math.random()*16777215).toString(16);
        }
        else {
            randomColorBg = bg
            randomColorFront = front
        }
        

        bgEl.style.backgroundColor = randomColorBg;
        frontEl.style.color = randomColorFront;
        bgPreview.innerHTML = randomColorBg;
        frontPreview.innerHTML = randomColorFront;

        return {randomColorBg, randomColorFront}
    }

    const sendResults = async (bg_color, front_color, match) => {
        let data = await fetch('./api/send_result', {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ bg_color, front_color, match })
        })

        return data.json()
    }

    const handleYepNopeClick = async (match) => {
        const { randomColorBg, randomColorFront } = changeColors()
        const res = await sendResults(randomColorBg, randomColorFront, match)
        // Gestisci if (!res)
    }


    const predictSingleValue = async () => {
        const color = choosenColor.value
        const req_color = color.split('#')[1]
        console.log(color, req_color)
        const data = await fetch(`./api/predict_single/${req_color}`)
        const res = await data.json()
        const predictedColor = res.color
        changeColors(color, predictedColor)
    }


    // ------------------------------------------------ Init Calls
    changeColors()


    // ------------------------------------------------ Events
    nopeBtn.addEventListener('click', _=> handleYepNopeClick(0))
    yepBtn.addEventListener('click', _=> handleYepNopeClick(1))
    predictBtn.addEventListener('click', _=> predictSingleValue(1))
    
})