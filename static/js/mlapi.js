const vbtn = document.querySelector('.verify')
const input = document.querySelector('.coursename')
const coursewrap = document.querySelector('.coursewrap')

const rc = document.querySelector('.rc')
const nrc = document.querySelector('.nrc')

vbtn.addEventListener('click', (e)=>{
    e.preventDefault()
    if (input.value === '') return null
    let response = fetch(
        `${document.location['origin']}/api/verifycourse/${input.value}/`, {method: "POST"}
    )
    response.then(e=>e.json().then(f=>{
        rc.style.display = 'none'
        nrc.style.display = 'none'
        if (f.prediction)
        {
            rc.style.display = 'block'
        }
        else
        {
            nrc.style.display = 'block'
        }
    }))
})
