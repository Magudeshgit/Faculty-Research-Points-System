const authorsno = document.querySelector('.authorno')
const fieldswrap = document.querySelector('.authorwrap')

authorsno.addEventListener('input', (e)=>{
    fieldswrap.innerHTML = ''
    if (parseInt(e.target.value) <= 50)
    {
      makefields(parseInt(e.target.value))
    }
    else
    {
      e.target.value = ''
    }
})

function closingops (e){
  const successnotification = document.querySelector('.successnotification')
  successnotification.remove()
}

window.onload = () =>{
  if (authorsno.value != '')
  {
        makefields(parseInt(authorsno.value))
  }
}

function makefields(count)
{
  var who = 'Staff';
  if (window.location.pathname === '/fundingapplication/') 
  {
     who = 'CO-PI'
  }
  for (let index = 1; index < count+1; index++) {
        let pd = document.createElement('div')
        let lb = document.createElement('label')
        let int = document.createElement('input')
        pd.setAttribute('class', 'sm:col-span-3')
        lb.setAttribute('for', 'author')
        lb.setAttribute('class', 'block text-sm font-medium leading-6 text-gray-900')
        lb.innerText = `Employee ID of ${who} ${index}`
        int.setAttribute('id', 'author')
        int.setAttribute('name', `authorid${index}`)
        int.setAttribute('type', 'text')
        int.setAttribute('class', 'block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6')
        int.setAttribute('required', '')
        // REMOVE IN PRODUCTION
        // int.setAttribute('oninput', 'this.value = this.value.toUpperCase()')


        pd.append(lb,int)
        fieldswrap.append(pd)
    }
}

function addfundinginputs(e)
{
  console.log(e.target.value)
}