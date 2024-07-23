const mobbtn = document.querySelector('#mobbtn')
const mobmenu = document.querySelector('#mobile-menu')

window.randomcolors = ['#C084FC', '#9CFC84', '#FCA884', '#84E6FC', '#F4D842', '#8E84FC']

const usermenubtn = document.querySelector('#user-menu-button')
const usermenu = document.querySelector('#user-menu')

mobbtn.addEventListener('click', ()=>{
     mobmenu.classList.toggle('hidden')
})

usermenubtn.addEventListener('click', ()=>{
     usermenu.classList.toggle('hidden')
})

// Setting profile color
window.onload = () =>{
     let theme = sessionStorage.getItem('profiletheme')
     
     if (theme)
     {
          usermenubtn.style.background = theme
     }
     else
     {
          theme = randomcolors[Math.floor(Math.random() * 5)]
          usermenubtn.style.background = theme
          sessionStorage.setItem('profiletheme', theme)
     }
     window.theme = theme
}